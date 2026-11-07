"""Every English text the app translates, found in the code: tr("..."), N_("...") and ntr("...", "...", n)."""
import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def keys():
    """(messages, plurals): sets of English texts, and of (singular, plural) pairs."""
    messages, plurals = set(), set()
    for path in sorted((ROOT / "clipshrink").glob("*.py")):
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            if not isinstance(node, ast.Call):
                continue
            name = node.func.id if isinstance(node.func, ast.Name) else getattr(node.func, "attr", None)
            args = [a.value if isinstance(a, ast.Constant) and isinstance(a.value, str) else None for a in node.args]
            if name in ("tr", "N_", "words") and args and args[0]:
                messages.add(args[0])
            elif name == "ntr" and len(args) >= 2 and args[0] and args[1]:
                plurals.add((args[0], args[1]))
    # Built from variables, so not visible above
    import sys
    sys.path.insert(0, str(ROOT))
    from clipshrink import config, i18n, reports
    messages |= set(i18n.REASONS) | set(reports.COLUMNS) | {config.QUALITY_EXPLANATION}
    return messages, plurals


if __name__ == "__main__":
    m, p = keys()
    for k in sorted(m):
        print(repr(k))
    print("--- plurals")
    for k in sorted(p):
        print(repr(k))
    print(len(m), "messages,", len(p), "plurals")
