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
        self.zoom = None            # None for the whole picture, or 1, 2 or 4 times
        self.centre = (0.5, 0.5)    # the middle of the zoomed view, as a fraction of the picture
        self.src_width, self.src_height = width, height
        self.conv_width, self.conv_height = None, None

    def _graph(self):
        w, h = self.conv_width or self.src_width, self.conv_height or self.src_height
        if self.zoom and w and h:
            # The same window from each picture. 100% is 1:1 pixels; 200% and 400% enlarge
            # each pixel into a block, so the detail shows instead of a blur.
            cw, ch, x, y = self.window(w, h)
            f = f"crop={cw}:{ch}:{x}:{y}"
            if self.zoom > 1:
                f += f",scale={cw * self.zoom}:{ch * self.zoom}:flags=neighbor"
        elif w and w > 1920:
            f = "scale=1920:-2"
        else:
            f = "null"
        # A shrunk conversion: bring the original to the same size so they can sit side by side.
        match = f"scale={w}:{h}:flags=lanczos," if self.conv_width and self.conv_width != self.src_width else ""
        return f"[vid1]{match}{f}[a];[vid2]{f}[b];[a][b]hstack[vo]"

    def window(self, w=None, h=None):
        """Size and top-left corner of the zoomed window, kept inside the picture."""
        w = w or self.conv_width or self.src_width
        h = h or self.conv_height or self.src_height
        z = self.zoom or 1
        cw = max(2, min(w, 960) // z // 2 * 2)
        ch = max(2, min(h, 1080) // z // 2 * 2)
        x = min(max(0, round(self.centre[0] * w - cw / 2)), w - cw)
        y = min(max(0, round(self.centre[1] * h - ch / 2)), h - ch)
        return cw, ch, x, y

    def clamp_centre(self, cx, cy):
        """The nearest centre whose window stays inside the picture."""
        w, h = self.conv_width or self.src_width, self.conv_height or self.src_height
        if not (w and h):
            return cx, cy
        z = self.zoom or 1
        hw, hh = min(w, 960) // z / 2 / w, min(h, 1080) // z / 2 / h
        return min(max(cx, hw), 1 - hw), min(max(cy, hh), 1 - hh)

    def start(self):
        if self.src_width is None:
            from .scan import probe_file
            info = probe_file(self.original)
            self.src_width, self.src_height = info.width, info.height
            conv = probe_file(self.converted)
            self.conv_width, self.conv_height = conv.width, conv.height
        cmd = [tools.mpv(), self.original, f"--external-file={self.converted}", "--no-config", "--pause",
               "--keep-open=always", "--hr-seek=yes", "--osc=no", "--input-default-bindings=no", "--input-vo-keyboard=no",
               "--osd-level=0", "--cursor-autohide=no", "--force-window=yes", "--hwdec=auto-copy-safe", "--title=ClipShrink side by side",
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
            buf = b""
            try:
                self._f.write((json.dumps({"command": list(args), "request_id": rid}) + "\n").encode())
            except OSError:
                raise PlayerError("the video player stopped") from None
            while True:
                try:
                    c = self._f.read(4096)
                except OSError:
                    raise PlayerError("the video player stopped") from None
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
        self.set_view(1 if on else None)

    def set_view(self, zoom, centre=None):
        """zoom None shows the whole picture; 1, 2 or 4 shows a window at that size."""
        self.zoom = zoom
        if centre is not None:
            self.centre = self.clamp_centre(*centre)
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
