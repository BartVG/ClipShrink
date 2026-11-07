"""The app's languages. English is written in the code. Each other language is a module in
locales/ that maps the English text to its translation. Anything missing shows in English."""
import contextlib, re, threading

LANGUAGES = {"en": "English", "fr": "Français", "nl": "Nederlands", "de": "Deutsch", "es": "Español",
             "it": "Italiano", "pt": "Português"}
QT_NAMES = {"fr": "fr", "nl": "nl", "de": "de", "es": "es", "it": "it", "pt": "pt_BR"}   # Qt's own buttons
ONE_INCLUDES_ZERO = {"fr", "pt"}    # "0 fichier", "0 arquivo"

_ENGLISH = {"code": "en", "messages": {}, "plurals": {}}
_state = dict(_ENGLISH)
_local = threading.local()      # in_english() on one thread leaves the others alone


def _now():
    return _ENGLISH if getattr(_local, "english", 0) else _state


def N_(text):
    """Marks English text that is translated where it is shown."""
    return text


def catalogue(code):
    """(messages, plurals) of a language. English has none: the code is the English."""
    from .locales import de, es, fr, it, nl, pt
    mod = {"fr": fr, "nl": nl, "de": de, "es": es, "it": it, "pt": pt}.get(code)
    return (mod.MESSAGES, mod.PLURALS) if mod else ({}, {})


def set_language(code):
    code = code if code in LANGUAGES else "en"
    messages, plurals = catalogue(code)
    _state.update(code=code, messages=messages, plurals=plurals)
    return code


def language():
    return _now()["code"]


def tr(text):
    if not text:
        return text
    return _now()["messages"].get(text, text)


def plural_index(n, code=None):
    code = code or _now()["code"]
    if code in ONE_INCLUDES_ZERO:
        return 0 if abs(n) < 2 else 1
    return 0 if n == 1 else 1


def ntr(one, many, n):
    """The singular or plural English text, translated. Use {n} in both and .format(n=n)."""
    forms = _now()["plurals"].get(one)
    if forms:
        return forms[plural_index(n)]
    return one if n == 1 else many


def comma(text):
    """English writes 95.5; the other languages here write 95,5."""
    return text if _now()["code"] == "en" else text.replace(".", ",")


def num(x, digits=1):
    return comma(f"{x:.{digits}f}")


def g(x):
    return comma(f"{x:g}")


@contextlib.contextmanager
def english():
    _local.english = getattr(_local, "english", 0) + 1
    try:
        yield
    finally:
        _local.english -= 1


def in_english(fn):
    with english():
        return fn()


# --- Reasons. The engine stores them in English, in the batch's memory and its report,
# and they are translated when shown. A placeholder's value is translated in turn, so
# "Could not convert, original kept: the encoder stopped: ..." works at both levels.
REASONS = [N_(t) for t in (
    "Could not convert, original kept: {error}",
    "This is {codec}, not H.264, so it was left alone.",
    "the encoder stopped: {detail}",
    "the encoder failed: {detail}",
    "could not write the file: {detail}",
    "could not read a sample from the file: {detail}",
    "the VMAF comparison could not run: {detail}",
    "the VMAF comparison returned no frames",
    "the original changed while it was being converted",
    "Conversion is not smaller ({out} vs {src} bytes), original kept.",
    "Conversion did not match the original, original kept: {problems}",
    "video is {codec}",
    "resolution differs",
    "pixel format differs ({out} vs {src})",
    "colour range differs",
    "audio tracks differ",
    "duration differs ({out}s vs {src}s)",
    "frame count differs ({out} vs {src})",
    "audio or telemetry tracks changed",
    "camera info changed",
    "VMAF compared {frames} frames out of {total}, original kept.",
    "VMAF short of what the search aims for.",
    "VMAF below your minimum: average {mean} (minimum {min_mean}), worst 1% {p1} (minimum {min_p1}). "
    "Nothing was kept, and your original is untouched.",
    "VMAF below the target: average {mean} (target {warn_mean}), worst 1% {p1} (target {warn_p1}). "
    "Compare it before removing the original.",
    "this file was never converted by this tool",
    "its original has not been sent to the Recycle Bin",
    "the converted file is missing",
    "it already has the original's name",
    "the converted file has changed since it was verified",
    "another file already has that name",
    "renaming was not confirmed",
    "Windows refused the rename: {error}",
    "it is not an LRV file",
    "its full video is not beside it",
    "Windows did not move it to the Recycle Bin, so it was left in place",
    "its conversion is not verified (status: {status})",
    "the original has changed since it was verified",
    "the converted file's content does not match what was verified",
    "the converted file cannot be read: {error}",
    "the converted file is not H.265 or AV1",
    "deletion was not confirmed",
    "its conversion is below the default quality target, and that was not confirmed",
    "its conversion has a lower resolution, and that was not confirmed",
)]


def _pattern(template):
    parts = re.split(r"\{(\w+)\}", template)
    rx = "".join(re.escape(p) if i % 2 == 0 else f"(?P<{p}>.*?)" for i, p in enumerate(parts))
    return re.compile(rx, re.S)


_PATTERNS = [(t, _pattern(t)) for t in REASONS]
_NUMBER = re.compile(r"-?\d+(\.\d+)?")


def reason(text):
    """A stored English reason, in the current language. Unknown text, such as an FFmpeg
    error, stays as it is."""
    if not text or _now()["code"] == "en":
        return text
    for template, rx in _PATTERNS:
        m = rx.fullmatch(text)
        if not m:
            continue
        values = {}
        for name, value in m.groupdict().items():
            if name == "problems":
                values[name] = "; ".join(reason(p) for p in value.split("; "))
            elif _NUMBER.fullmatch(value):
                values[name] = comma(value)
            else:
                values[name] = reason(value)
        return tr(template).format(**values)
    return text
