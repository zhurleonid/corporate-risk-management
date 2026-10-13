# MF 731 Corporate Risk Management

Coursework for MF 731 (Boston University MSMFT). One folder per assignment,
each self-contained: code, write-up, data, and the PDF that gets submitted.

Leonid Zhuravlev

## Assignments

| | Topic | Code | Write-up |
| --- | --- | --- | --- |
| [Homework 1](homework_1/) | Volatility of SPY: MA(100), EWMA(0.94), GARCH(1,1) fit and forecast | [hw1_code.ipynb](homework_1/hw1_code.ipynb) | [hw1_written.ipynb](homework_1/hw1_written.ipynb) |
| [Homework 2](homework_2/) | Full, linearized and second order loss operators for a delta-hedged short put, Monte Carlo loss distribution | [hw2_code.ipynb](homework_2/hw2_code.ipynb) | [hw2_written.ipynb](homework_2/hw2_written.ipynb) |
| [Homework 3](homework_3/) | Three sheets, one sub-folder each: [Part 1](homework_3/part1_var_estimation/) VaR of a market-cap-weighted MSFT/AAPL/GOOGL portfolio (historical and normal-EWMA); [Part 2](homework_3/part2_var_backtest/) backtesting one-day VaR on the S&P 500; [Part 3](homework_3/part3_var_10day/) 10-day VaR of a delta-hedged short put vs the square-root-of-time rule | [part1](homework_3/part1_var_estimation/hw3_part1_code.ipynb), [part2](homework_3/part2_var_backtest/hw3_part2_code.ipynb), [part3](homework_3/part3_var_10day/hw3_part3_code.ipynb) | [part1](homework_3/part1_var_estimation/hw3_part1_written.ipynb), [part2](homework_3/part2_var_backtest/hw3_part2_written.ipynb), [part3](homework_3/part3_var_10day/hw3_part3_written.ipynb) |
| [Homework 4](homework_4/) | Expected shortfall: normal, discrete and loan-portfolio examples, VaR monotonicity, exponential and Pareto losses. No code: the whole sheet is pencil-and-paper, so the submission is handwritten | - | - |

## How a homework is put together

Each assignment is split into two source notebooks and one generated from them:

```
hw1_code.ipynb        code and comments, nothing else
hw1_written.ipynb     the written work: pseudocode, derivations, figures, results
        |
        +--> hw1_submission.ipynb --> hw1_submission.pdf    (what gets submitted)
```

The split exists because the two halves change for different reasons. Code gets
re-run when the data or the model changes; prose gets edited when the argument
changes. Keeping them apart means neither rebuild disturbs the other, and the
code notebook stays readable as code rather than as a document.

`make_submission.py` joins them — the written work first, then the code cells
appended under an appendix heading. That single file satisfies the course rule
that everything arrives as one PDF carrying both the pseudocode and the source.

**`hwN_submission.ipynb` is generated. Never edit it.** Edit a source notebook
and rebuild, or the change is lost on the next build.

### Figures

`hw1_written.ipynb` embeds its figures as base64 attachments pulled from the
executed code notebook, so it renders on its own anywhere — GitHub, a fresh
clone, an email attachment — with no image folder to carry along or to fall out
of sync.

### Data

Price data lives in a csv next to the notebook that uses it. Runs are therefore
offline and reproducible: re-downloading from the vendor can shift results if
they revise their history. Simulations are seeded, so repeated runs give
identical output.

## Running it

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd homework_1 && jupyter notebook
```

Python 3.12. [how_to_run.md](how_to_run.md) has the full runbook: rebuilding a
submission, the three PDF export routes and their separate dependencies, and the
two export traps worth knowing about before you hit them.

## Repository layout

```
README.md                 this file
how_to_run.md             commands: setup, running, rebuilding, exporting
requirements.txt          shared environment for every assignment
make_submission.py        merges the written + code notebooks
submission_criteria.md    the course's submission rules
.vscode/settings.json     points VS Code at .venv (its PDF export needs this)
homework_N/               one folder per assignment
homework_N/partK_*/       when an assignment comes as several sheets, one
                          self-contained sub-folder per sheet (Homework 3)
```

`.venv/` is gitignored — build your own from `requirements.txt`.

## Note on results

Numbers quoted in the write-ups come from the committed data and the executed
notebooks, not from memory. If you re-run and see something different, the data
changed; the GARCH fit for Homework 1 should give
$\alpha_0 = 6.7425\times10^{-6}$, $\alpha_1 = 0.0581$, $\beta_1 = 0.8236$.
