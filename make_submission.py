"""Build the submission notebook: written work, then the code appended.

Reads hw<N>_written.ipynb and hw<N>_code.ipynb from the current folder and
writes hw<N>_submission.ipynb. Nothing is executed - both inputs are copied as
they are, so run the code notebook first if you want its outputs included.

Usage, from inside a homework folder:

    python ../make_submission.py                 # finds the *_written / *_code pair
    python ../make_submission.py hw1_written.ipynb hw1_code.ipynb hw1_submission.ipynb
"""

import copy
import glob
import json
import re
import sys

SEPARATOR = "# Appendix: source code\n\nThe code below produces every figure and number above."


def load(path):
    with open(path) as f:
        return json.load(f)


def find_pair(argv):
    """Either take the paths off the command line, or work them out."""
    if len(argv) >= 3:
        written, code = argv[1], argv[2]
        out = argv[3] if len(argv) > 3 else derive_output(written)
        return written, code, out

    written = [f for f in glob.glob("*_written.ipynb")]
    code = [f for f in glob.glob("*_code.ipynb")]
    if len(written) != 1 or len(code) != 1:
        raise SystemExit(
            "expected exactly one *_written.ipynb and one *_code.ipynb here; "
            f"found {len(written)} and {len(code)}. Name them explicitly instead."
        )
    return written[0], code[0], derive_output(written[0])


def derive_output(written_path):
    return re.sub(r"_written\.ipynb$", "_submission.ipynb", written_path)


def main():
    written_path, code_path, out_path = find_pair(sys.argv)

    written = load(written_path)
    code = load(code_path)

    cells = copy.deepcopy(written["cells"])
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": SEPARATOR.split("\n"),
    })

    # Keep the code cells and anything they printed. Drop the code notebook's
    # own headings, since the written half already has its own structure.
    appended = 0
    for cell in code["cells"]:
        if cell["cell_type"] != "code":
            continue
        cells.append(copy.deepcopy(cell))
        appended += 1

    out = copy.deepcopy(written)
    out["cells"] = cells
    # carry the code notebook's kernel so the result is runnable
    if "kernelspec" in code.get("metadata", {}):
        out.setdefault("metadata", {})["kernelspec"] = code["metadata"]["kernelspec"]
    if "language_info" in code.get("metadata", {}):
        out.setdefault("metadata", {})["language_info"] = code["metadata"]["language_info"]

    # give every cell an id - nbformat 4.5+ requires it, and some exporters
    # (VS Code's among them) are stricter about it than the command line
    for i, cell in enumerate(out["cells"]):
        cell.setdefault("id", f"cell-{i:03d}")
    out["nbformat"] = 4
    out["nbformat_minor"] = max(out.get("nbformat_minor", 5), 5)

    with open(out_path, "w") as f:
        json.dump(out, f, indent=1)

    print(f"{out_path}: {len(written['cells'])} written cells + {appended} code cells "
          f"= {len(cells)} total")


if __name__ == "__main__":
    main()
