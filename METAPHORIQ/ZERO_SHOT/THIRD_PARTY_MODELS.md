# Third-party models

The installer contains no third-party model weights or external research
repositories. The in-app model manager downloads selected artifacts directly.

| ID | Upstream | Declared license | Installed role |
|---|---|---|---|
| `melbert` | `jin530/MelBERT` + official Google Drive checkpoint | Not declared upstream | Binary target-word detection |
| `xlmr` | `lwachowiak/Metaphor-Detection-XLMR` | CC-BY-NC-SA-3.0 | Token detection, optional prototype encoder |
| `cl_roberta` | `CreativeLang/metaphor_detection_roberta_seq` | CC-BY-2.0 | Token detection, optional prototype encoder |
| `framebert` | `liyucheng09/MetaphorFrame` | Not declared upstream | Experimental token/frame detection |

Users are responsible for confirming that their intended use complies with the
upstream licenses and dataset terms.

