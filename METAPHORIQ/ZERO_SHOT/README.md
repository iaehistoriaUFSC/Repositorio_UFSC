# METAPHORIQ Zero-Shot Workbench

Windows desktop prototype for:

1. token-level metaphor detection;
2. ensemble comparison between detector models;
3. provisional classification against Javier Fernandez Sebastian's taxonomy;
4. conceptual-history period assignment from document metadata; and
5. reproducible tables, JSONL/CSV exports, and Matplotlib figures.

The installer contains the application, taxonomy snapshot, lexical prototype
classifier, and scientific plotting runtime. Third-party model weights are
downloaded on demand from their original hosts because they are large and have
different licenses.

## Run an analysis

1. Select `Load runnable example`, or paste/open a source text.
2. Select `Set up recommended pipeline` if the readiness strip reports missing
   detectors. The same download can be started automatically by Run.
3. Enter the document year when chronology is required.
4. Select `RUN ANALYSIS` in the permanent bottom action bar, or press
   `Ctrl+Enter`.

## Scientific boundaries

- MelBERT, XLM-R, CreativeLang RoBERTa, and FrameBERT are metaphor detectors.
  Their binary/token labels do not contain Javier taxonomy classes.
- Taxonomy assignment is a separate nearest-prototype stage built from the
  project's annotated samples. It is provisional until independently evaluated.
- A model score is not presented as a calibrated probability.
- Document year is metadata. The software does not infer a historical date from
  linguistic style.
- The requested periods are represented without hidden overlap:
  `A=1600-1749`, `B=1750-1849`, `C=1850-1945`,
  `transition=1946-1949`, `D=1950+`.

## Development

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-build.txt
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m app.main
```

Build the Windows package with `scripts/build.ps1`.

The current installer checksum and executed release checks are recorded in
`BUILD_REPORT.md`.
