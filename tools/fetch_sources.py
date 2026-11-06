"""Gathers what the GPL and LGPL ask for when ClipShrink ships FFmpeg, mpv and Qt:
the source code behind those binaries, and the licence texts of everything inside them.

Writes:
  dist/third-party-source/  one archive per component, to attach to a release
  licenses/                 licence texts and COMPONENTS.md, committed and installed with the app

Run it again after changing tools/vendor.lock.json. Finished downloads are kept, so it
can be re-run after a failure. Archives are only read, never executed."""
import io, json, os, re, shutil, subprocess, sys, tarfile, tempfile, threading, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCK = Path(__file__).with_name("vendor.lock.json")
OUT = ROOT / "dist" / "third-party-source"
LICENSES = ROOT / "licenses"
LICENSE_LOCK = threading.Lock()
LICENSE_NAME = re.compile(r"^(licen[cs]e|copying|copyright|notice|unlicense|patents?)([._-].*)?$", re.I)
LICENSE_DIRS = {"licenses", "licences", "license", "licence"}
# Script folders for things this FFmpeg build turns off (--disable-libfdk-aac, --disable-whisper,
# --disable-libpulse, --disable-libxcb, --disable-xlib), so they are not in the binary.
FFMPEG_NOT_IN_BUILD = ("fdk-aac", "whisper", "pulseaudio", "45-x11")
PYTHON_PACKAGES_IN_APP = {"pyinstaller", "pyside6_essentials", "shiboken6"}
# Projects that keep their licence somewhere other than the usual place.
LICENSE_ELSEWHERE = {"distrib/docs/english/source/avisynthdoc/license.rst", "include/ffnvcodec/nvEncodeAPI.h"}
SVN_ROOTS = ("https://svn.code.sf.net/p/lame/svn", "https://svn.xvid.org")
FULL_COMMIT = re.compile(r"^[0-9a-f]{40}$")
HEX = re.compile(r"^[0-9a-f]{6,39}$")


def git(*args, cwd=None):
    # Never ask anyone to sign in: a server that wants a login counts as a failure, and is reported.
    # The empty credential.helper and GCM_INTERACTIVE stop Git Credential Manager opening a window.
    result = subprocess.run(["git", "-c", "core.longpaths=true", "-c", "credential.helper=", *args],
                            cwd=cwd, check=True, capture_output=True, text=True, encoding="utf-8", errors="replace",
                            stdin=subprocess.DEVNULL, timeout=3600,
                            env={**os.environ, "GIT_TERMINAL_PROMPT": "0", "GCM_INTERACTIVE": "never"})
    return result.stdout.strip()


def parse_btbn_script(text):
    """Returns (repo, commit) pairs from one of BtbN's build scripts."""
    values = dict(re.findall(r'^SCRIPT_([A-Z0-9_]+)="?([^"\n]*)"?$', text, re.M))
    pairs = []
    for suffix in ("", "2", "3"):
        repo = values.get(f"REPO{suffix}")
        commit = values.get(f"COMMIT{suffix}") or values.get(f"REV{suffix}")
        if repo and commit:
            pairs.append((repo, commit))
    return pairs


def component_name(repo):
    """The last part of the address, except SourceForge's, which are all called "code"."""
    parts = re.sub(r"(\.git)?/?$", "", repo).split("/")
    return parts[-2] if parts[-1] == "code" else parts[-1]


def btbn_components(folder):
    found = {}
    scripts = folder / "scripts.d"
    for script in sorted(scripts.rglob("*.sh")):
        relative = script.relative_to(scripts).as_posix()
        if any(skip in relative for skip in FFMPEG_NOT_IN_BUILD):
            continue
        text = script.read_text(encoding="utf-8", errors="replace")
        submodules = "all" if "git submodule update" in text else []
        for repo, commit in parse_btbn_script(text):
            name = component_name(repo)
            found[(name, commit)] = {"name": name, "group": "ffmpeg", "repo": repo, "commit": commit, "submodules": submodules}
    return list(found.values())


def recipe_submodules(body):
    """What a CMake recipe builds from: no setting means every submodule, "" means none."""
    match = re.search(r"^\s*GIT_SUBMODULES\s+(.*)$", body, re.M)
    if not match:
        return "all"
    return [part for part in match.group(1).replace('"', " ").split()]


def parse_cmake_packages(folder):
    """Reads ExternalProject_Add blocks: target -> {repo, tag, url, depends}."""
    targets = {}
    for file in sorted(folder.glob("*.cmake")):
        text = file.read_text(encoding="utf-8", errors="replace")
        for match in re.finditer(r"ExternalProject_Add\(\s*(\S+)(.*?)^\)", text, re.S | re.M):
            target, body = match.groups()
            depends = re.search(r"DEPENDS\s+(.*?)(?=^\s*[A-Z_]{3,}\s)", body, re.S | re.M)
            repo = re.search(r"^\s*GIT_REPOSITORY\s+(\S+)", body, re.M)
            tag = re.search(r"^\s*GIT_TAG\s+(\S+)", body, re.M)
            url = re.search(r"^\s*URL\s+(\S+)", body, re.M)
            targets[target] = {
                "repo": repo.group(1) if repo else None, "tag": tag.group(1) if tag else None,
                "url": url.group(1).strip('"') if url else None,
                "submodules": recipe_submodules(body),
                "depends": [d for d in depends.group(1).split() if not d.startswith("#")] if depends else [],
            }
    return targets


def resolve_target_name(dep):
    return "x265" if dep.startswith("${ffmpeg_x265") else dep


def mpv_components(folder, built_at, exact):
    """Everything mpv depends on, walked from the mpv target itself. These recipes follow each
    project's newest code, so the commit is the newest one when the build started."""
    targets = parse_cmake_packages(folder / "packages")
    found, queue, seen = [], ["mpv"], set()
    while queue:
        target = resolve_target_name(queue.pop())
        if target in seen or target not in targets:
            continue
        seen.add(target)
        info = targets[target]
        queue.extend(info["depends"])
        item = {"name": target, "group": "mpv", "built_at": built_at}
        if info["repo"]:
            found.append({**item, "repo": info["repo"], "tag": info["tag"], "commit": exact.get(target),
                          "submodules": info["submodules"]})
        elif info["url"]:
            found.append({**item, "url": info["url"]})
    return found


def resolve_commit(component):
    """Turns a full commit, short commit, tag or build date into a full commit."""
    wanted = component.get("commit")
    if wanted and FULL_COMMIT.match(wanted):
        return wanted
    with tempfile.TemporaryDirectory() as tmp:
        git("init", "-q", "--bare", tmp)
        repo = component["repo"]
        if wanted and not HEX.match(wanted):
            git("fetch", "-q", "--depth", "1", repo, f"refs/tags/{wanted}", cwd=tmp)
            return git("rev-parse", "FETCH_HEAD^{commit}", cwd=tmp)
        git("fetch", "-q", "--filter=tree:0", repo, component.get("tag") or "HEAD", cwd=tmp)
        if wanted:
            return git("rev-parse", wanted + "^{commit}", cwd=tmp)
        return git("rev-list", "-1", f"--before={component['built_at']}", "FETCH_HEAD", cwd=tmp)


def archive_svn(component, dest):
    """Exports one revision over HTTP, because these projects are not in git and svn may not be installed."""
    root = next(r for r in SVN_ROOTS if component["repo"].startswith(r))
    path = component["repo"][len(root):].strip("/")
    base = f"{root}/!svn/bc/{component['commit']}/{path}/"
    with tarfile.open(dest, "w:gz") as tar:
        def walk(url, relative):
            # Xvid asks for its public "anonymous" login with no password, as its build recipe does.
            headers = {"Authorization": "Basic YW5vbnltb3VzOg=="} if "svn.xvid.org" in url else {}
            with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=120) as response:
                body = response.read()
            if not url.endswith("/"):
                info = tarfile.TarInfo(f"{component['name']}/{relative}")
                info.size = len(body)
                tar.addfile(info, io.BytesIO(body))
                return
            for href in re.findall(r'href="([^"?#/][^"?#]*)"', body.decode("utf-8", "replace")):
                if "://" not in href and href != "../":
                    walk(url + href, relative + urllib.parse.unquote(href))
        walk(base, "")
    return component["commit"], []


def archive_git(component, dest):
    """Writes dest. Returns the commit used and the git submodules that commit points to."""
    repo = component["repo"]
    commit = resolve_commit(component)
    with tempfile.TemporaryDirectory() as tmp:
        git("init", "-q", "--bare", tmp)
        try:
            git("fetch", "-q", "--depth", "1", repo, commit, cwd=tmp)
        except subprocess.CalledProcessError:      # some servers won't hand out a single commit
            git("fetch", "-q", repo, "+refs/heads/*:refs/heads/*", cwd=tmp)
        prefix = f"{component['name']}/"
        git("archive", "--format=tar.gz", f"--prefix={prefix}", "-o", str(dest), commit, cwd=tmp)
        modules = []
        try:
            gitmodules = git("show", f"{commit}:.gitmodules", cwd=tmp)
        except subprocess.CalledProcessError:
            gitmodules = ""
        wanted = component.get("submodules", [])
        for path, url in parse_gitmodules(gitmodules):
            if wanted != "all" and path not in wanted:      # the build doesn't use it, so it isn't in the binary
                continue
            tree = git("ls-tree", commit, path, cwd=tmp).split()
            if len(tree) >= 3 and tree[1] == "commit":
                modules.append({"repo": urllib.parse.urljoin(repo.rstrip("/") + "/", url), "commit": tree[2], "path": path})
        return commit, modules


def parse_gitmodules(text):
    """Returns (path, url) for each section, whichever order its lines are in."""
    pairs = []
    for section in re.split(r"^\s*\[submodule", text, flags=re.M)[1:]:
        path = re.search(r"^\s*path\s*=\s*(\S+)", section, re.M)
        url = re.search(r"^\s*url\s*=\s*(\S+)", section, re.M)
        if path and url:
            pairs.append((path.group(1), url.group(1)))
    return pairs


def license_members(archive):
    """Licence files at the top of an archive or in its LICENSES folder, as (name, bytes)."""
    found = []
    with tarfile.open(archive) as tar:
        for member in tar:
            if not member.isfile():
                continue
            parts = member.name.split("/")[1:]
            top_level = len(parts) == 1 and LICENSE_NAME.match(parts[0])
            in_folder = len(parts) == 2 and parts[0].lower() in LICENSE_DIRS
            if (top_level or in_folder) and member.size < 2_000_000:
                found.append((parts[-1], tar.extractfile(member).read()))
            elif "/".join(parts) in LICENSE_ELSEWHERE:
                data = tar.extractfile(member).read()
                if parts[-1].endswith(".h"):                # the notice is the comment at the top of the header
                    data = data[:data.index(b"*/") + 2]
                found.append((f"LICENSE-from-{parts[-1]}", data))
    return found


def save_licenses(component, archive):
    with LICENSE_LOCK:      # one at a time: several builds of one project share a folder
        members = license_members(archive)
        folder = LICENSES / component["group"] / component["name"]
        shutil.rmtree(folder, ignore_errors=True)
        if members:
            folder.mkdir(parents=True)
            for name, data in members:
                (folder / re.sub(r"[^\w.+-]", "_", name)).write_bytes(data)
        return [name for name, _ in members]


def download(url, dest):
    request = urllib.request.Request(url, headers={"User-Agent": "clipshrink-source-fetch"})
    partial = dest.with_name(dest.name + ".part")
    with urllib.request.urlopen(request, timeout=600) as response, open(partial, "wb") as f:
        shutil.copyfileobj(response, f)
    partial.replace(dest)


def row_for(component, dest, source, commit):
    readable = tarfile.is_tarfile(dest)
    return {"name": component["name"], "group": component["group"], "source": source, "commit": commit,
            "file": dest.relative_to(OUT).as_posix(), "bytes": dest.stat().st_size,
            "licenses": save_licenses(component, dest) if readable else []}


def gather(component):
    """Fetches one component. Returns result rows, or a row with an error."""
    group_dir = OUT / component["group"]
    group_dir.mkdir(parents=True, exist_ok=True)
    label = component["name"]
    try:
        if component.get("url"):
            suffix = "".join(Path(urllib.parse.urlparse(component["url"]).path).suffixes[-2:])
            dest = group_dir / f"{label}{suffix}"
            if not dest.exists():
                download(component["url"], dest)
            return [row_for(component, dest, component["url"], None)]
        short = (component.get("commit") or "dated")[:12]
        dest = group_dir / f"{label}-{short}.tar.gz"
        is_svn = any(component["repo"].startswith(root) for root in SVN_ROOTS)
        commit, modules = (archive_svn if is_svn else archive_git)(component, dest)
        rows = [row_for(component, dest, component["repo"], commit)]
        for module in modules:
            sub = {"name": f"{label}--{module['path'].replace('/', '-')}", "group": component["group"],
                   "repo": module["repo"], "commit": module["commit"], "submodules": "all"}
            rows.extend(gather(sub))
        return rows
    except Exception as e:  # one failing project must not hide the others in the report
        detail = getattr(e, "stderr", "") or str(e)
        return [{"name": label, "group": component["group"], "error": str(detail).strip()[:400],
                 "source": component.get("repo") or component.get("url")}]


def recipe(repo, commit, tmp):
    dest = Path(tmp) / repo.replace("/", "_")
    archive = dest.with_suffix(".tar.gz")
    download(f"https://codeload.github.com/{repo}/tar.gz/{commit}", archive)
    with tarfile.open(archive) as tar:
        tar.extractall(dest, filter="data")
    return next(dest.iterdir()), archive


def pypi_source(spec):
    name, version = spec.split("==")
    with urllib.request.urlopen(f"https://pypi.org/pypi/{name}/{version}/json", timeout=60) as r:
        data = json.load(r)
    url = next(u["url"] for u in data["urls"] if u["packagetype"] == "sdist")
    return {"name": f"{name}-{version}", "group": "python", "url": url}


def copy_python_licenses():
    """Licence texts for the Python parts of the app, from the packages it was built with."""
    site = Path(sys.prefix) / "Lib" / "site-packages"
    target = LICENSES / "python"
    shutil.rmtree(target, ignore_errors=True)
    for info in sorted(site.glob("*.dist-info")):
        name = info.name.split("-")[0].lower()
        if name not in PYTHON_PACKAGES_IN_APP:
            continue
        for file in sorted(p for p in info.rglob("*") if p.is_file() and LICENSE_NAME.match(p.name)):
            dest = target / name / file.name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(file, dest)
    python_license = Path(sys.base_prefix) / "LICENSE.txt"
    (target / "python").mkdir(parents=True, exist_ok=True)
    shutil.copy(python_license, target / "python" / "LICENSE.txt")


def write_components(rows, lock):
    lines = ["# Components inside ClipShrink's bundled programs", "",
             "Generated by `tools/fetch_sources.py`. Licence texts are in the folders next to this file.", "",
             f"FFmpeg `{lock['ffmpeg']['version']}` and mpv `{lock['mpv']['version']}`. mpv's commits, other than "
             f"mpv, FFmpeg and libplacebo, are the newest at the time its build started ({lock['mpv']['built_at']}), "
             "because its build follows each project's newest code.", "",
             "| Part of | Component | Commit | Source | Licence files |", "|---|---|---|---|---|"]
    for row in sorted(rows, key=lambda r: (r["group"], r["name"].lower())):
        commit = (row.get("commit") or "release archive")[:12]
        lines.append(f"| {row['group']} | {row['name']} | `{commit}` | {row['source']} | {', '.join(row.get('licenses', [])) or 'none found'} |")
    (LICENSES / "COMPONENTS.md").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def main():
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    OUT.mkdir(parents=True, exist_ok=True)
    LICENSES.mkdir(exist_ok=True)
    copy_python_licenses()
    with tempfile.TemporaryDirectory() as tmp:
        ff, mp = lock["ffmpeg"], lock["mpv"]
        ff_folder, ff_recipe = recipe(ff["recipe_repo"], ff["recipe_commit"], tmp)
        mp_folder, mp_recipe = recipe(mp["recipe_repo"], mp["recipe_commit"], tmp)
        shutil.copy(ff_recipe, OUT / "FFmpeg-Builds-recipe.tar.gz")
        shutil.copy(mp_recipe, OUT / "mpv-winbuild-cmake-recipe.tar.gz")
        components = [{"name": "FFmpeg", "group": "ffmpeg", "repo": ff["repo"], "commit": ff["commit"], "tag": "release/8.1"}]
        components += btbn_components(ff_folder)
        components += mpv_components(mp_folder, mp["built_at"], mp["exact_commits"])
    components += lock["extra_sources"]
    components += [pypi_source(spec) for spec in lock["pypi_sources"]]
    print(f"Gathering {len(components)} components", flush=True)
    with ThreadPoolExecutor(6) as pool:
        rows = [row for result in pool.map(gather, components) for row in result]
    good = [r for r in rows if "error" not in r]
    failed = [r for r in rows if "error" in r]
    write_components(good, lock)
    (OUT / "SOURCES.json").write_text(json.dumps(rows, indent=1), encoding="utf-8")
    print(f"{len(good)} archived, {sum(r['bytes'] for r in good) / 1e9:.1f} GB")
    no_licence = [r["name"] for r in good if not r.get("licenses")]
    if no_licence:
        print("No licence file found, check by hand: " + ", ".join(no_licence))
    if failed:
        print("FAILED:")
        for row in failed:
            print(f"  {row['group']}/{row['name']} ({row['source']}): {row['error']}")
        sys.exit(1)


if __name__ == "__main__":
    main()
