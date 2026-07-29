# Architecture

## Pipeline

```text
input text + document year
  -> sentence and word segmentation
  -> one or more token-level metaphor detectors
  -> explicit ensemble rule
  -> detected span + sentence context
  -> Javier taxonomy prototype classifier
  -> conceptual-history period lookup
  -> result manifest, JSONL/CSV, Matplotlib views
```

Detection, taxonomy classification, and chronology are separate stages. Every
row records the selected model IDs, ensemble rule, thresholds, taxonomy method,
dataset snapshot hash, and period rule.

## Runtime

The desktop application is packaged with PyInstaller. Model files live under
`%LOCALAPPDATA%\MetaphoriqZeroShot\models` and are never written into the
installation directory. Download records and model revisions are persisted in
`state.json`.

Hugging Face models run through one generic token-classification adapter.
MelBERT and FrameBERT use isolated repository adapters because their official
implementations predate the current Transformers API.

## Taxonomy stage

The built-in classifier uses deterministic word/character TF-IDF prototypes
constructed from accepted annotated examples, class descriptions, and
indicative terms. XLM-R or CreativeLang RoBERTa encoder prototypes can be
selected when those models are installed. Similarity and top-two margin are
reported; neither is called a probability.

## Chronology

Period assignment comes only from a user-supplied document year or imported
metadata. `1946-1949` remains an explicit transition gap because the requested
periods stop at 1945 and resume at 1950.

