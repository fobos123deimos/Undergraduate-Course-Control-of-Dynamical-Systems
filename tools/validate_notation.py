"""Check Markdown math delimiters, notebook structure and diagram assets.

This structural check complements (and does not replace) PDF/browser inspection.
Run from any directory; --record writes the local audit record.
"""
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]


def math_blocks(text, label):
    text = re.sub(r"\x60{3}.*?\x60{3}", "", text, flags=re.S)
    text = re.sub(r"\x60[^\x60\n]*\x60", "", text)
    assert "\ufffd" not in text, f"Replacement character in {label}"
    assert not re.search(r"[A-Za-z][˙¨]", text), f"Untypeset derivative in {label}"
    tokens = list(re.finditer(r"(?<!\\)\${1,2}", text))
    blocks = []
    opening = None
    for token in tokens:
        if opening is None:
            opening = token
        else:
            assert token.group() == opening.group(), f"Mixed math delimiters in {label}"
            expression = text[opening.end():token.start()]
            assert expression.strip(), f"Empty math expression in {label}"
            stack = []
            for env in re.finditer(r"\\(begin|end)\{([^}]+)\}", expression):
                if env[1] == "begin":
                    stack.append(env[2])
                else:
                    assert stack and stack.pop() == env[2], f"Math environment mismatch in {label}"
            assert not stack, f"Unclosed math environment in {label}"
            assert len(re.findall(r"\\left\b", expression)) == len(re.findall(r"\\right\b", expression)), label
            blocks.append((len(opening.group()) == 2, expression, label))
            opening = None
    assert opening is None, f"Unclosed math delimiter in {label}"
    return blocks


def audit():
    blocks = []
    markdown_files = list(ROOT.rglob("*.md"))
    for file in markdown_files:
        blocks.extend(math_blocks(file.read_text(encoding="utf-8"), file.relative_to(ROOT).as_posix()))
    notebooks = list(ROOT.glob("laboratories/*/notebook.ipynb"))
    for file in notebooks:
        nb = json.loads(file.read_text(encoding="utf-8"))
        assert nb["nbformat"] == 4
        diagrams = [c for c in nb["cells"] if c.get("id") == "system-diagram"]
        assert len(diagrams) == 1, file
        assert len([c for c in nb["cells"] if c.get("id")=="physical-system"])==1, file
        for index, cell in enumerate(nb["cells"]):
            if cell["cell_type"] == "markdown":
                blocks.extend(math_blocks("".join(cell["source"]), file.parent.name + f"/cell-{index}"))
    diagrams = list(ROOT.glob("laboratories/*/figures/system-diagram.tikz"))
    diagrams += list(ROOT.glob("laboratories/*/figures/physical-system.tikz"))
    diagrams += list(ROOT.glob("problem-sets/*/figures/*.tikz"))
    assert len(diagrams) == 25, len(diagrams)
    for source in diagrams:
        assert source.with_suffix(".png").is_file(), source
        text = source.read_text(encoding="utf-8")
        assert text.count(r"\begin{tikzpicture}") == text.count(r"\end{tikzpicture}") == 1, source
    record = {
        "markdown_files": len(markdown_files), "notebooks": len(notebooks),
        "math_expressions": len(blocks), "tikz_diagrams": len(diagrams),
        "delimiter_and_asset_checks": "passed",
        "scope": "Structural checks; PDF compilation and visual review are documented separately."
    }
    return record, blocks


if __name__ == "__main__":
    record, _ = audit()
    if "--record" in sys.argv:
        (ROOT / "docs/notation-validation.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(record, indent=2))
