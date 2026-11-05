"""Stage 4: side by side playback. One mpv process decodes both files into a
single picture, so left and right can never drift apart."""
import json, os, subprocess, threading, time, uuid
from . import tools


class PlayerError(RuntimeError):
    pass


class SideBySidePlayer:
    def __init__(self, original, converted, wid=None, mute=False, width=None, height=None):
        self.original, self.converted = str(original), str(converted)
        self.wid, self.mute = wid, mute
        self.pipe = rf"\\.\pipe\clipshrink_{uuid.uuid4().hex}"
        self.proc = None
        self._f = None
        self._lock = threading.Lock()
        self._req = 0
        self.detail = False
        self.src_width, self.src_height = width, height

    def _graph(self):
        w, h = self.src_width, self.src_height
        if self.detail and w and h:
            # 1:1 pixels, a window from the centre of each picture
            cw, ch = min(w, 960), min(h, 1080)
            f = f"crop={cw}:{ch}:{(w - cw) // 2}:{(h - ch) // 2}"
        elif w and w > 1920:
            f = "scale=1920:-2"
        else:
            f = "null"
        return f"[vid1]{f}[a];[vid2]{f}[b];[a][b]hstack[vo]"

    def start(self):
        if self.src_width is None:
            from .scan import probe_file
            info = probe_file(self.original)
            self.src_width, self.src_height = info.width, info.height
        cmd = [tools.mpv(), self.original, f"--external-file={self.converted}", "--no-config", "--pause",
               "--keep-open=always", "--hr-seek=yes", "--osc=no", "--input-default-bindings=no", "--input-vo-keyboard=no",
               "--osd-level=0", "--force-window=yes", "--hwdec=auto-copy-safe", "--title=ClipShrink side by side",
               f"--input-ipc-server={self.pipe}", f"--lavfi-complex={self._graph()}", "--aid=1", "--msg-level=all=error"]
        if self.mute:
            cmd.append("--mute=yes")
        if self.wid is not None:
            cmd.append(f"--wid={int(self.wid)}")
        self.proc = subprocess.Popen(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                     creationflags=tools.NOWIN)
        tools.bind_to_us(self.proc)
        end = time.time() + 20
        while True:
            try:
                self._f = open(self.pipe, "r+b", buffering=0)
                break
            except OSError:
                if time.time() > end or self.proc.poll() is not None:
                    raise PlayerError("the video player did not start")
                time.sleep(0.05)
        while self.duration() is None:
            if time.time() > end or self.proc.poll() is not None:
                raise PlayerError("the video player could not open these files")
            time.sleep(0.05)
        self._settle()

    def _cmd(self, *args):
        with self._lock:
            if self._f is None:
                raise PlayerError("the video player is closed")
            self._req += 1
            rid = self._req
            self._f.write((json.dumps({"command": list(args), "request_id": rid}) + "\n").encode())
            buf = b""
            while True:
                c = self._f.read(4096)
                if not c:
                    raise PlayerError("the video player stopped")
                buf += c
                while b"\n" in buf:
                    line, buf = buf.split(b"\n", 1)
                    try:
                        m = json.loads(line)
                    except ValueError:
                        continue
                    if m.get("request_id") == rid:
                        return m

    def _get(self, prop):
        m = self._cmd("get_property", prop)
        return m.get("data") if m.get("error") == "success" else None

    def _settle(self, seconds=8):
        end = time.time() + seconds
        while time.time() < end:
            if self._get("seeking") is False and self._get("playback-time") is not None:
                return
            time.sleep(0.02)

    def duration(self):
        return self._get("duration")

    def position(self):
        return self._get("playback-time")

    def is_paused(self):
        return bool(self._get("pause"))

    def seek(self, t):
        self._cmd("seek", float(t), "absolute+exact")
        self._settle()

    def play(self):
        self._cmd("set_property", "pause", False)

    def pause(self):
        self._cmd("set_property", "pause", True)
        self._settle()

    def step(self, forward=True):
        self._cmd("frame-step" if forward else "frame-back-step")
        self._settle()

    def set_detail(self, on):
        self.detail = bool(on)
        at = self.position() or 0
        paused = self.is_paused()
        m = self._cmd("set_property", "lavfi-complex", self._graph())
        if m.get("error") != "success":
            raise PlayerError(f"could not switch view: {m.get('error')}")
        self.seek(at)
        if paused:
            self.pause()

    def screenshot(self, path):
        """Saves the combined picture, full resolution, without scaling."""
        path = str(path)
        m = self._cmd("screenshot-to-file", path, "video")
        if m.get("error") != "success":
            raise PlayerError(f"screenshot failed: {m.get('error')}")
        end = time.time() + 10
        while not (os.path.exists(path) and os.path.getsize(path) > 0):
            if time.time() > end:
                raise PlayerError("screenshot was not written")
            time.sleep(0.05)

    def close(self):
        if self._f:
            try:
                self._cmd("quit")
            except (PlayerError, OSError):
                pass
            try:
                self._f.close()
            except OSError:
                pass
            self._f = None
        if self.proc:
            try:
                self.proc.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.proc.kill()
            self.proc = None
