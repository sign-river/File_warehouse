# HDA-DeepSC IEEE Conference Revision

This directory contains an IEEE conference-style revision of the HDA-DeepSC imperfect-CSI manuscript and an editable Word-source draft.

## Files

- `main.tex`: English IEEEtran conference manuscript.
- `references.bib`: corrected BibTeX database.
- `paper_word.md`: editable source used to generate the Word draft.
- `generate_figures.py`: reproduces the architecture diagram and the aggregate controlled-NMSE result figure from the values reported in the manuscript.
- `figures/`: generated PDF/PNG graphics.
- `SUBMISSION_CHECKLIST.md`: remaining author and camera-ready checks.

## Build the figures

```bash
python -m pip install matplotlib numpy
python generate_figures.py
```

## Build the LaTeX paper

A standard TeX Live installation with the IEEEtran class is required.

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

A manual build sequence is also possible:

```bash
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

## Build the editable Word draft

Pandoc and an IEEE CSL style are required:

```bash
curl -L \
  https://raw.githubusercontent.com/citation-style-language/styles/master/ieee.csl \
  -o ieee.csl

pandoc paper_word.md \
  --from markdown+tex_math_dollars+pipe_tables \
  --citeproc \
  --bibliography=references.bib \
  --csl=ieee.csl \
  --resource-path=. \
  -o HDA_DeepSC_IEEE_Draft.docx
```

The Word file is intended for editing and supervisor review. It is single-column and does not attempt to reproduce every detail of IEEE's two-column conference layout.

## Required author edits before submission

Replace the placeholder author names, affiliation, city/country, and email addresses in `main.tex` and `paper_word.md`. Add funding acknowledgments only when they apply. Verify the conference-specific page limit, copyright notice, submission identifier, anonymization requirement, and final PDF eXpress instructions.

## Scope of the generated figures

`controlled_nmse_results.pdf/png` visualizes only the four aggregate values already reported in the manuscript. It does not fabricate per-SNR samples or confidence intervals. The architecture diagram is explanatory rather than an experimental result.

## Important result boundary

The revised manuscript claims receiver gains only for the controlled imperfect-CSI study, primarily in the 16-QAM region. Packet-error-rate, frame-error-rate, artificial semantic erasure, and mask-conditioned recovery are described as implemented diagnostics or future experiments; no unmeasured recovery gain is claimed.
