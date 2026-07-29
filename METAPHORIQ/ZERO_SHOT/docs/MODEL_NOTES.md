# Model notes

## MelBERT

MelBERT is a target-word binary metaphor detector from NAACL 2021. The paper
reported strong results on VUA-18, VUA-20, MOH-X, and TroFi. This supports using
it as the recommended first detector, but not the claim that it remained the
overall best model in 2025. The official repository declares Python 3.7,
PyTorch 1.6, and Transformers 4.2.2, so compatibility is managed by an adapter.

## XLM-R

`lwachowiak/Metaphor-Detection-XLMR` is a token classifier fine-tuned on the
English VU Amsterdam Metaphor Corpus. Its multilingual encoder enables
cross-lingual zero-shot experiments, but Portuguese and Spanish performance
must be evaluated locally rather than assumed from the English benchmark.

## CreativeLang RoBERTa

`CreativeLang/metaphor_detection_roberta_seq` is an English RoBERTa-base token
classifier fine-tuned on VUA-20. It is useful as a second English detector and
as an experimental taxonomy feature encoder.

## FrameBERT

FrameBERT combines RoBERTa with FrameNet embeddings and emits metaphor and
frame labels. Its official inference path requires the project repository and
additional frame resources. The application therefore labels it experimental.

## Redistribution

The installer does not redistribute third-party weights or repositories.
Downloads occur only after the user selects a model. The registry displays the
declared license or `not declared` when the upstream artifact has no clear
license file.

