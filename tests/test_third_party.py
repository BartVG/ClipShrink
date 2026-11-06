"""The bundled builds stay pinned, and their licences and source stay accounted for."""
import json, sys, tarfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import fetch_sources, fetch_vendor


def lock():
    return json.loads((ROOT / "tools" / "vendor.lock.json").read_text(encoding="utf-8"))


@pytest.mark.parametrize("name", ["ffmpeg", "mpv"])
def test_builds_are_pinned_to_one_file_and_checksum(name):
    item = lock()[name]
    assert len(item["sha256"]) == 64
    assert "latest" not in item["url"]
    assert item["url"].endswith(item["file"])


def test_a_download_with_the_wrong_checksum_is_refused(tmp_path, monkeypatch):
    def fake_download(url, dest):
        Path(dest).write_bytes(b"not the real file")
    monkeypatch.setattr(fetch_vendor.urllib.request, "urlretrieve", fake_download)
    item = {"file": "x.zip", "url": "https://example.invalid/x.zip", "sha256": "0" * 64}
    with pytest.raises(SystemExit) as stopped:
        fetch_vendor.download_verified(item, "https://example.invalid/mirror/", tmp_path / "x.zip")
    assert "checksum" in str(stopped.value)


def test_our_own_copy_is_used_when_upstream_has_deleted_a_build(tmp_path, monkeypatch):
    good = b"the real file"
    item = {"file": "x.zip", "url": "https://example.invalid/x.zip", "sha256": __import__("hashlib").sha256(good).hexdigest()}
    def fake_download(url, dest):
        if "mirror" not in url:
            raise fetch_vendor.urllib.error.URLError("404")
        Path(dest).write_bytes(good)
    monkeypatch.setattr(fetch_vendor.urllib.request, "urlretrieve", fake_download)
    fetch_vendor.download_verified(item, "https://example.invalid/mirror/", tmp_path / "x.zip")
    assert (tmp_path / "x.zip").read_bytes() == good


def test_a_build_with_a_different_checksum_is_replaced(tmp_path):
    item = {"check": "a.exe", "sha256": "1" * 64}
    (tmp_path / "a.exe").write_text("x")
    assert not fetch_vendor.is_current(item, tmp_path)
    (tmp_path / fetch_vendor.MARKER).write_text("2" * 64)
    assert not fetch_vendor.is_current(item, tmp_path)
    (tmp_path / fetch_vendor.MARKER).write_text("1" * 64)
    assert fetch_vendor.is_current(item, tmp_path)


def test_reads_every_repository_from_a_build_script():
    text = 'SCRIPT_REPO="https://a/x.git"\nSCRIPT_COMMIT="abc"\nSCRIPT_REPO2="https://a/y.git"\nSCRIPT_COMMIT2="def"\nSCRIPT_REPO3="https://a/z"\nSCRIPT_REV="7"\n'
    assert fetch_sources.parse_btbn_script(text) == [("https://a/x.git", "abc"), ("https://a/y.git", "def")]


def test_mpv_recipe_walk_only_includes_what_mpv_uses(tmp_path):
    packages = tmp_path / "packages"
    packages.mkdir()
    (packages / "mpv.cmake").write_text("ExternalProject_Add(mpv\n    DEPENDS\n        ffmpeg\n    GIT_REPOSITORY https://a/mpv.git\n)\n")
    (packages / "ffmpeg.cmake").write_text("ExternalProject_Add(ffmpeg\n    DEPENDS\n        ${ffmpeg_x265}\n    GIT_REPOSITORY https://a/ffmpeg.git\n)\n")
    (packages / "x265.cmake").write_text("ExternalProject_Add(x265\n    GIT_REPOSITORY https://a/x265.git\n    GIT_TAG main\n)\n")
    (packages / "unused.cmake").write_text("ExternalProject_Add(unused\n    GIT_REPOSITORY https://a/unused.git\n)\n")
    found = fetch_sources.mpv_components(tmp_path, "2026-01-01", {"mpv": "abc1234"})
    assert sorted(c["name"] for c in found) == ["ffmpeg", "mpv", "x265"]
    assert next(c for c in found if c["name"] == "mpv")["commit"] == "abc1234"


def test_only_submodules_the_build_uses_are_fetched(tmp_path):
    packages = tmp_path / "packages"
    packages.mkdir()
    (packages / "mpv.cmake").write_text(
        "ExternalProject_Add(mpv\n    DEPENDS\n        a\n        b\n        c\n    GIT_REPOSITORY https://x/mpv\n)\n"
        'ExternalProject_Add(a\n    GIT_REPOSITORY https://x/a\n    GIT_SUBMODULES ""\n)\n'
        "ExternalProject_Add(b\n    GIT_REPOSITORY https://x/b\n    GIT_SUBMODULES lib/one\n)\n"
        "ExternalProject_Add(c\n    GIT_REPOSITORY https://x/c\n)\n")
    found = {c["name"]: c["submodules"] for c in fetch_sources.mpv_components(tmp_path, "2026-01-01", {})}
    assert found == {"mpv": "all", "a": [], "b": ["lib/one"], "c": "all"}


def test_git_can_never_ask_for_a_login(monkeypatch):
    seen = {}
    def fake_run(cmd, **kwargs):
        seen.update(cmd=cmd, env=kwargs["env"], stdin=kwargs["stdin"])
        return fetch_sources.subprocess.CompletedProcess(cmd, 0, stdout="")
    monkeypatch.setattr(fetch_sources.subprocess, "run", fake_run)
    fetch_sources.git("status")
    assert "credential.helper=" in seen["cmd"]
    assert seen["env"]["GCM_INTERACTIVE"] == "never" and seen["env"]["GIT_TERMINAL_PROMPT"] == "0"
    assert seen["stdin"] == fetch_sources.subprocess.DEVNULL


def test_finds_licence_files_only_where_they_belong(tmp_path):
    archive = tmp_path / "a.tar"
    with tarfile.open(archive, "w") as tar:
        for name in ("p/COPYING.LGPL", "p/LICENSES/MIT.txt", "p/src/LICENSE", "p/readme.md"):
            file = tmp_path / "f"
            file.write_text("text")
            tar.add(file, arcname=name)
    assert sorted(name for name, _ in fetch_sources.license_members(archive)) == ["COPYING.LGPL", "MIT.txt"]


def test_a_licence_kept_in_a_header_comment_is_found(tmp_path):
    source = tmp_path / "nvEncodeAPI.h"
    source.write_text("/* Permission is hereby granted */\nint code;\n")
    archive = tmp_path / "a.tar"
    with tarfile.open(archive, "w") as tar:
        tar.add(source, arcname="p/include/ffnvcodec/nvEncodeAPI.h")
    assert fetch_sources.license_members(archive) == [("LICENSE-from-nvEncodeAPI.h", b"/* Permission is hereby granted */")]


def test_sourceforge_projects_keep_separate_names():
    assert fetch_sources.component_name("https://git.code.sf.net/p/soxr/code") == "soxr"
    assert fetch_sources.component_name("https://git.code.sf.net/p/opencore-amr/code") == "opencore-amr"
    assert fetch_sources.component_name("https://github.com/Netflix/vmaf.git") == "vmaf"


def test_reads_submodules_in_either_line_order():
    text = '[submodule "a"]\n\tpath = third_party/a\n\turl = ../a.git\n[submodule "b"]\n\turl = https://x/b\n\tpath = b\n'
    assert fetch_sources.parse_gitmodules(text) == [("third_party/a", "../a.git"), ("b", "https://x/b")]


def test_installer_includes_the_licence_folder():
    assert '"licenses;licenses"' in (ROOT / "build.bat").read_text(encoding="utf-8")


def test_licence_texts_the_installer_must_carry_are_present():
    licenses = ROOT / "licenses"
    assert (licenses / "COMPONENTS.md").exists()
    assert list(licenses.glob("qt/pyside-setup-*/LGPL-3.0-only*"))
    assert (licenses / "python" / "python" / "LICENSE.txt").exists()
    assert (licenses / "python" / "openpyxl").is_dir()
    for name in ("x265", "SVT-AV1", "vmaf", "x264"):
        assert any(licenses.glob(f"ffmpeg/{name}/*")), name
    assert any(licenses.glob("mpv/mpv/*"))


def test_notices_say_where_the_exact_source_is():
    text = (ROOT / "THIRD_PARTY_NOTICES.md").read_text(encoding="utf-8")
    assert "releases/tag/third-party-1.5.1" in text
    assert lock()["ffmpeg"]["version"] in text and lock()["mpv"]["version"] in text
