# How to run

Coursework for MF 731 Corporate Risk Management. One folder per assignment.

## Layout

```
requirements.txt          shared environment for every homework
make_submission.py        merges the written + code notebooks into one
submission_criteria.md    the course submission rules
.gitignore                keeps .venv and build leftovers out of git
homework_N/
    hwN_code.ipynb        code and comments only
    hwN_written.ipynb     written work: pseudocode, math, figures, results
    hwN_submission.ipynb  generated - written work with the code appended
    hwN_submission.pdf    generated - what gets submitted
    hwN_theory.pdf        the assignment handout
    *.csv                 any data the notebook needs, saved so it runs offline
```

Two source notebooks, one generated. `hwN_code.ipynb` holds only code and
comments. `hwN_written.ipynb` holds everything written - pseudocode,
derivations, figures and results - with the figures embedded so it stands on its
own. `hwN_submission.ipynb` is built from the two and should never be edited by
hand; edit a source notebook and rebuild.

## Setup (once)

From the repo root:

```
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m playwright install chromium    # only needed for PDF export
```

`.venv/` is gitignored, so each machine builds its own from
`requirements.txt`.

Needs Python 3.12. Reactivate with `source .venv/bin/activate` in new shells.

## Running a homework

```
cd homework_N
jupyter notebook            # then open the .ipynb and Run All
```

Headless:

```
jupyter nbconvert --to notebook --execute --inplace <notebook>.ipynb
```

Run it from inside the homework folder — the notebooks read their data files
from the working directory.

### Data

Price data is saved to csv next to each notebook so runs are reproducible and
work offline. Re-downloading may shift results slightly if the vendor revises
its history. Simulations are seeded, so repeated runs give identical output.

## Building the submission notebook

From inside the homework folder, after running the code notebook:

```
python ../make_submission.py        # -> hwN_submission.ipynb
```

`make_submission.py` finds the one `*_written.ipynb` and the one `*_code.ipynb`
in the folder, or takes them as arguments. It copies both as they are and does
not execute anything, so run the code notebook first if you want its outputs in
the result.

To get the submission PDF, export the merged notebook:

```
jupyter nbconvert --to webpdf hw1_submission.ipynb
```

`--to webpdf` needs `pip install nbconvert[webpdf]` plus
`python -m playwright install chromium` the first time. Exporting via `--to
html` and printing to PDF from the browser also works and needs nothing extra.

VS Code's "Export to PDF" button uses a different route: nbconvert's LaTeX
exporter, which needs **pandoc** and a TeX install (`brew install pandoc`).
Without pandoc it fails with `PandocMissing`.

One gotcha with that route: markdown pipe tables break it. Pandoc 3.x turns them
into `longtable`, which nbconvert's LaTeX template cannot handle, and the export
dies with `No counter 'none' defined`. Write tables as `$$\begin{array}{...}$$`
instead - those survive both the LaTeX and the browser routes.

## Submitting

Per `submission_criteria.md`: submit one PDF only. No `.ipynb`, `.py` or `.zip`
attachments. The PDF must carry the pseudocode, and either a working link to
this repo or the full source in an appendix — the write-ups here do both.

Before submitting, check that the work is actually pushed, or the link in the
PDF will 404 for the grader.
