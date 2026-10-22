# SMCH v0.4 — Phase A inventory

Date: 2026-10-22 · Session: Claude Code on the web (cloud container), repository `iaehistoriaufsc/repositorio_ufsc`, branch `claude/awesome-ramanujan-9r66f1`.
Prompt followed: `CLAUDE_CODE_PROMPT_SMCH_v0_4.md` (uploaded to the session, SHA-256 `85e83bef7e97b6f905bcb9dc3df1514426144ed0000fea0625cd8f2893381ab1`).

Reporting convention: **FATO** (verified in this container) · **LACUNA** (required but absent) · **OPINIÃO** (my proposal or estimate).

---

## 0. Headline

**FATO.** The working directory the prompt names (`…\VISUAL_ENGINE\SMCH_4`) is a Windows path. This session runs inside a Linux container holding only the Git repository `Repositorio_UFSC`. The repository contains **none** of the SMCH_4 files the prompt expects:

| Expected item | Status |
|---|---|
| `SMCH_4/CLAUDE.md` (standing rules) | **LACUNA** — not in repo, not uploaded |
| `SMCH_4/.claude/settings.json` (telemetry/feedback off) | **LACUNA** — no `.claude/` directory anywhere in the repo |
| `_context/SMCH_REFERENCE.md` | **LACUNA** |
| `_context/build_smch_v0_1_original.py` (v0.1 curve definitions) | **LACUNA** — baseline reproduction (step 3) impossible |
| `_context/metaphoriq_annotation_dataset_v3.csv` | **LACUNA** |
| `_context/smch_documentation_v0_2_to_v0_3alpha.pdf` | **LACUNA** |
| `_context/javier_taxonomy.csv` | **LACUNA** as CSV; a JSON cousin exists (see §1.2) |
| `_context/metaphoriq-taxonomy.txt` | **FATO present** at `METAPHORIQ/ZERO_SHOT/data/reference/metaphoriq-taxonomy.txt` (38,434 B). Classified `context-candidate`, never a source. |
| `sources/` (44 source items) | **LACUNA** — zero source texts: no PDF, no DOCX, no scholarly MD/TXT anywhere in the repo |
| `smch_anchors_v0_2.csv` (A01–A29) | **LACUNA** |
| K-anchor table (K001–K061) | **LACUNA** |
| 244 corpus occurrences | **LACUNA** (nearest relatives: 163 annotations / 214 examples, see §4) |
| v0.3 meta / previews | **LACUNA** |

Consequence: Phase A steps 1–2 (source inventory), 3 (baseline hash) and 4 (prior artefacts) cannot be completed against real inputs. Everything that does not depend on the missing files (schemas, mining plan, data-use line, integrity design) is done below. **Mining has not started and will not start** until the files are in the container and the user approves schema, plan and file moves.

**OPINIÃO — what the user needs to do.** Put the SMCH_4 material where this session can read it, either (a) commit it to the repository under `METAPHORIQ/SMCH_4/` (`_context/`, `sources/`, prior CSVs — see the `.gitignore` warning in §7), or (b) upload the files to the session, or (c) run the prompt locally on the Windows machine with Claude Code pointed at `SMCH_4`. Option (a) is preferable because the build must be reproducible and hashed; the repository already uses Git LFS for large binaries (`.gitattributes`), so PDFs can go through LFS.

---

## 1. File inventory (step 1)

**FATO.** 323 tracked files in the repository plus 1 uploaded prompt = 324 files, 125,588,321 bytes. Full table with size, SHA-256 and class: `inventory_files_v0_4.tsv` (same folder). Classification used the prompt's classes, with `-candidate` suffixes where a file resembles an expected item but is not the item itself.

| class | files | note |
|---|---|---|
| `source` | **0** | user expects 44 |
| `context` (under `_context/`) | 0 | no `_context/` exists |
| `context-candidate` | 4 | `metaphoriq-taxonomy.txt`, `javier_taxonomy_updated_44_classes.json`, `taxonomy_nodes.jsonl`, `families.jsonl` (all in `METAPHORIQ/ZERO_SHOT/data/reference/`) |
| `prior-artefact` | 0 | |
| `prior-artefact-candidate` | 3 | `annotations.jsonl` (163 rows), `examples.jsonl` (214 rows), `dataset-profile.json` |
| `prompt/config` | 3 | the uploaded prompt, `data/MANIFEST.json`, `data/models.json` |
| `other` | 314 | WOKE word-embedding project, OAI-PMH extraction, Zero-Shot app code, notebooks, 130 `.joblib` models, 3 Git-LFS pointer `.exe` files |

Duplicates by hash: one group only, two identical CSS files (`Etapa_3/…/style.css` = `SKINNER/src/style_skinner.css`); irrelevant to SMCH. No book split into chapter files, because no books are present.

Integrity of the candidate files: `data/MANIFEST.json` lists SHA-256 for the eight reference files; **FATO** all eight recomputed hashes match the manifest (checked in this session).

### 1.2 The context-candidates, described

- `metaphoriq-taxonomy.txt` — Markdown-like taxonomy of metaphors of history (6 families, 44–45 classes) with quoted examples and "Fonte:" lines, hosted by Fernández Sebastián 2024 ("Key metaphors", per `container_publication_id`). It is the taxonomy, i.e. the reference the prompt calls `metaphoriq-taxonomy.txt`. **It is not a source of concept anchors.**
- `families.jsonl` — the 6 families (1 Metaphors for History · 2 Time and Memory · 3 Pasts, Presents, Futures · 4 Sources, Events, Processes · 5 Revolution, Crisis, Modernity · 6 Progress, Decline, Transition) with colours and descriptions. Matches the 1–6 `related_family` codes of the M-schema.
- `taxonomy_nodes.jsonl` / `javier_taxonomy_updated_44_classes.json` — 45 class nodes, 44 assignable (5.3 is a grouping node; 5.3.6.1 assignable). Usable as the `node_id` vocabulary for AM-anchors (§3.2 of the prompt).

---

## 2. Per-source description (step 2)

**LACUNA.** No source present → no language, format, length, extractability or full-text/abstract classification can be given. The procedure is ready (below) and will be run the moment `sources/` exists.

Procedure (OPINIÃO, for approval): for every file in `sources/`: SHA-256; format by magic bytes; PDF → `pypdf` page count + extracted-character count per page (page with < 50 chars → "image-only page"; ≥ 50 % image-only pages → flag "scanned, OCR needed; not done unless the user agrees"); DOCX → `python-docx`-free unzip of `word/document.xml`; MD/TXT → word count; language by stop-word profile (de/en/pt/es/fr), German read in German; full text vs abstract by length (< 600 words and titled "abstract"/"Zusammenfassung" → abstract-only) and by the user's own list.

Tooling check **FATO**: `uv 0.11.32`, Python 3.13.16, `pypdf 6.17.0` available. `numpy`, `pandas`, `matplotlib`, `scipy` are not installed system-wide and will be pulled by `uv run --with …` as the prompt specifies (network via proxy is on; the first `uv run` will download wheels — this is a tool install, not a bibliographic lookup, and is not logged in `web_lookups.md`).

---

## 3. Baseline check (step 3)

**LACUNA.** `_context/build_smch_v0_1_original.py` is absent, so the 43×6 series cannot be reproduced and nothing can be compared with the documented fragments `52F79369…53FDB`. The hash procedure is specified here so it is unambiguous when the file arrives:

1. Copy the curve definitions verbatim into `build_smch_v0_4.py::structural_v0_1()`.
2. Evaluate on the 43 decade points the script defines; clip to [0.02, 1.0]; round to 4 decimals.
3. Hash A = SHA-256 of the CSV bytes (UTF-8, `\n` line endings, header + rows, column order exactly as the original script writes them).
4. Hash B = SHA-256 of `json.dumps(series, separators=(',',':'), ensure_ascii=False)` of the `series` values only.
5. Compare prefix `52F79369` / suffix `53FDB` against both, case-insensitive. Report FATO match / FATO mismatch / LACUNA. On mismatch: do not block; carry the object as `structural_v0_1_reproduced`; the user decides whether it counts as v0.2.

Open question for the user (needed to avoid a false mismatch): are the documented fragments from the CSV bytes or the JSON `series` values, and were the CSV line endings `\r\n` (Windows) when the original hash was taken?

---

## 4. Prior artefacts and the annotation dataset (step 4)

**LACUNA** for all four prior artefacts (`smch_anchors_v0_2.csv`, K001–K061, 244 occurrences, v0.3 meta). Consequence: the "existing anchor files byte-identical" self-test is N/A; `concept_series_K` is omitted with LACUNA; the secondary pass (3.2) uses the fallback AM-schema because the v0.2 A-header cannot be copied.

**LACUNA** for `_context/metaphoriq_annotation_dataset_v3.csv`. In its place the repository holds two JSONL files that look like earlier or sibling exports of the same annotation work. **FATO** about them (do not assume they are the v3 CSV; they are not 244 rows):

| | `annotations.jsonl` | `examples.jsonl` |
|---|---|---|
| rows | 163 | 214 |
| what a row is | one annotated TXT line from `metaphoriq-taxonomy.txt` ("july_27_annotation_text"), reconciled to an example | one curated example of a metaphor of history (123 curated + 91 gold-standard) |
| family encoding | `family_id` string "1"–"6" | same |
| class encoding | `class_id` dotted ("1.1" … "6.3", 44 distinct) | same (43 distinct) |
| date encoding | `representative_year`, `interval_start`, `interval_end` (ints or null), `temporal_precision` ∈ {year, century_midpoint, unknown}, `date_basis` (earliest_cited_source / primary_metaphor_occurrence / original_publication_year / container_publication_fallback / …), `date_resolved`, `chronology_eligible` | same fields |
| resolved rows | 109 (54 unresolved, 25 of them dated only by the 2024 host publication) | 188 (26 unresolved) |
| date range (resolved) | −500 … 2024 | −500 … 2024 |
| rows per family (all / resolved) | 1: 46/22 · 2: 49/35 · 3: 24/22 · 4: 10/8 · 5: 29/18 · 6: 5/4 | 1: 44/38 · 2: 62/48 · 3: 35/33 · 4: 14/13 · 5: 45/43 · 6: 14/13 |
| resolved rows ≥ 1600, by half-century | 1600s 5 · 1650s 1 · 1700s 1 · 1750s 2 · 1800s 12 · 1850s 18 · 1900s 13 · 1950s 22 · 2000s 32 | 8 · 3 · 1 · 10 · 23 · 27 · 27 · 39 · 47 |
| period field | `period_id` ∈ {basement, early-modern, sattelzeit, industrial-modern, crisis-decades, great-acceleration, contemporary} — a 7-period scheme **different** from the Zero-Shot app's A/B/C/transition/D scheme | same |
| host | all rows cite Fernández Sebastián 2024 as container (`host_publication_year` = 2024 for all 214 examples) | |

Is this the 244-row v0.3-alpha blend set? **FATO: no** — 163 ≠ 244 and 214 ≠ 244, and neither file is a CSV. **OPINIÃO:** the 244 set is probably a later, larger export of the same annotation lineage (`dataset-profile.json` records this export as `metaphoriq-temporal-graph-prototype3-v1`, created 2026-07-28, 163 annotations / 214 examples). I cannot confirm that without the v3 CSV.

**Proposal for Phase C feed (needs confirmation, do not act yet):**
- If the user supplies `metaphoriq_annotation_dataset_v3.csv`: it is the corpus density for §4.7 (lambda blend) and §4.9 (`corpus_vs_concepts`); the row count and file hash go into `smch_v0_4.json` meta, as the prompt demands.
- If the user does not supply it: use `examples.jsonl`, rows with `chronology_eligible = true` (188), year = `representative_year`, weight 1.0 for `temporal_precision = year`, 0.4 for `century_midpoint`; exclude `date_basis = container_publication_fallback` rows (they are dated by the 2024 host, which is exactly the publication-year error the prompt forbids). Meta records `corpus_source = examples.jsonl (188 eligible of 214), hash 12d79dd1…`. `annotations.jsonl` is not used as a density (it is a reconciliation layer over the same text, and would double-count).
- In either case the corpus density is CORPUS tier, read-only, never an anchor source, and never shares an axis with the family layer.

---

## 5. Proposed v0.4 schemas (step 5)

### 5.1 `smch_manchors_v0_4.csv` (M-anchors)

| column | type / domain | rule | flag |
|---|---|---|---|
| `anchor_id` | `M001…` | zero-padded 3 digits, 4 if > 999 | |
| `class` | const `mined_concept` | | |
| `concept_term` | str, original language | as in source | |
| `concept_lemma_en` | str | link key across rows | **ADD rule:** controlled lower-case singular; convergence is counted on this key |
| `language` | ISO 639-1 (de/en/pt/es/fr/it…) | of `concept_term` | |
| `year` | int | dated concept-state (never publication unless coinage) | |
| `year_precision` | exact / decade / approx / span | | |
| `year_start`, `year_end` | int or blank | required when `span`; else blank | |
| `year_published` | int | of the source | |
| `author`, `work` | str | | |
| `source_file` | str | exact filename in `sources/` | |
| `locator` | str | page / section / paragraph | |
| `dating_basis` | str | mandatory free text; must say "coinage" if year = year_published | |
| `c1_indispensable` … `c4_horizon` | yes / no / unclear + locator in `notes` or in-cell `yes@p.12` | at least one `yes` | **OPINIÃO:** encode as `yes@<locator>` in-cell so each criterion carries its own locator without 4 extra columns |
| `temporalization`, `politicization`, `ideologization`, `democratization` | yes / no / unclear (`@locator`) | | same encoding |
| `movement_concept` | yes / no / unclear | | |
| `late_modernity_claim` | str, one short paraphrase | only for `year ≥ 1968`; else blank | |
| `semantic_fields` | `;`-separated | | |
| `related_family` | 1–6 or blank | only when the source itself ties the concept to a time-metaphor family | |
| `tier` | ANCHORED / LICENSED / EXCLUDED | | |
| `quote` | < 15 words, original language, never Portuguese | optional, max one per source | |
| `paraphrase_en` | str | | |
| `curation_source` | const `claude-code` | | |
| `curation_status` | const `pending` (user later: accepted / rejected) | | |
| `notes` | str | disputes recorded, never resolved | |
| **proposed ADD** `source_id` | short key (e.g. `S07`) | joins to a `sources_v0_4.tsv` manifest with hash, language, pages | **ADD** — keeps `source_file` human-readable and the join stable if a file is renamed |
| **proposed ADD** `dating_type` | primary / secondary | whether the dated state is the source's own historical claim about an earlier state (primary) or the source's own coinage (secondary) — mirrors the AM-schema and makes the "no publication-year dating unless coinage" self-test mechanical | **ADD** |
| **proposed ADD** `dispute` | yes / no | flags rows whose `notes` record a dispute between sources, so the gap report can list them | **ADD** (optional) |

Nothing proposed for dropping.

### 5.2 `smch_amanchors_v0_4.csv` (AM-anchors)

Fallback schema (v0.2 header unavailable, LACUNA): `anchor_id (AM001…), class="mined_metaphor", family_id (1–6), node_id (taxonomy leaf from taxonomy_nodes.jsonl, else family), metaphor_term, year, year_precision, year_published, author, work, source_file, locator, dating_type (primary|secondary), uso_ou_mencao (uso|mencao), e_citacao, fonte_citada, tier, quote, paraphrase_en, claim_ordinal (dominant|present|marginal), curation_source, curation_status, notes`. **Proposed ADD:** `year_start`, `year_end` for span dates, same semantics as the M-table. If `smch_anchors_v0_2.csv` arrives, its header is copied instead and this fallback is dropped.

### 5.3 Review and manifest files

`manchors_needing_review_v0_4.md` (rows failing minimum), `suggested_sources.md` (expected-but-absent anchors), `mining_log/<source_file>.md`, `MANIFEST_v0_4.sha256`, `CHANGELOG.md` — as specified; no changes proposed.

---

## 6. Mining plan (step 6)

**LACUNA** on the source list, so order, per-source estimates and token cost are given as a method plus a formula, to be instantiated when `sources/` exists.

Order (OPINIÃO): 1) full texts before abstracts, without exception; 2) German *Forum Interdisziplinäre Begriffsgeschichte* volumes early, because they carry the contested 1968– segment and the late-modernity claims; 3) Koselleck's own methodological texts (the four processes are defined there, so the yes/no/unclear coding is calibrated on them before the rest); 4) monographs and edited volumes in descending length; 5) articles; 6) abstracts last, and only for sources with no text present.

Chunking so nothing is skipped: each PDF is extracted page by page; chunks of ~8–10 pages (≈ 4–6 k words) with a 1-page overlap; every chunk is logged in `mining_log/<source_file>.md` as "pages a–b: n anchors / none / skipped because <reason>". A chunk is never skipped for length. Image-only pages are listed under "pages skipped" with "scanned — OCR not authorised". Front matter, bibliographies and indexes are read but logged as "no anchors expected". Long German volumes are read in German; terms are recorded in German with an English lemma.

Estimates: anchors per source ≈ 2–6 for an article, 8–25 for a monograph chapter sequence, 0–2 for an abstract. Token cost per source ≈ (extracted words × 1.4) input tokens plus ~1.5 k output tokens per chunk for the anchor rows and log; a 300-page German volume ≈ 150 k words ≈ 210 k input tokens. Total for 44 items cannot be estimated without their sizes; it will be put in the instantiated plan.

What I cannot read: scanned PDFs without OCR; DRM-protected PDFs; any file not in the container.

---

## 7. Data-use and session line (step 7)

**FATO.** This session is Claude Code on the web (claude.ai cloud container), started from the claude.ai account `bonaldo2024@gmail.com` with GitHub access scoped to `iaehistoriaufsc/repositorio_ufsc` only. The container is ephemeral; anything not committed and pushed is lost when it is reclaimed. Outbound HTTPS goes through an agent proxy and is on. The session does not expose its data-retention terms to me; whatever applies is the claude.ai consumer agreement attached to that login — I cannot verify it from inside the container, so this is reported as what the session exposes, not as a legal statement.

**LACUNA.** No `.claude/settings.json` exists in the repository or in the container's `~/.claude/`, so the claim that `/feedback`, `/bug`, `/share` are disabled is **not** in force here. If the user wants it, the file must be added to the repo (proposal: `METAPHORIQ/SMCH_4/.claude/settings.json`) — I have not created it because the prompt treats it as user-provided configuration.

**FATO.** No web lookups were made in Phase A (`web_lookups.md`).

**FATO — a repository hazard the prompt does not anticipate.** The root `.gitignore` ignores `*.csv` and `*.log`. The v0.4 deliverables `smch_manchors_v0_4.csv`, `smch_amanchors_v0_4.csv`, `smch_v0_4.csv`, `selftest_v0_4.log` and any prior CSVs the user commits would be silently excluded from Git. **OPINIÃO:** add to `.gitignore` the lines `!METAPHORIQ/SMCH_4/**/*.csv` and `!METAPHORIQ/SMCH_4/**/*.log` (or a local `METAPHORIQ/SMCH_4/.gitignore` with `!*.csv` / `!*.log`) before any data is committed. Not done pending approval, since it changes repository policy outside `SMCH_4`.

---

## 8. Stop

Phase A is complete to the extent the inputs allow. **Mining has not started.** Waiting on the user for:

1. The SMCH_4 material in the container (`_context/`, `sources/` with the 44 items, any prior CSVs, `CLAUDE.md`, `.claude/settings.json`) — or a decision to run locally on Windows.
2. Confirmation of the file layout `METAPHORIQ/SMCH_4/…` inside the repository (this report already lives there) and of the `.gitignore` exceptions.
3. Approval or amendment of the schemas in §5 (the three proposed ADD columns).
4. Approval of the mining order and chunking in §6.
5. Decision on the Phase C corpus feed in §4 (v3 CSV, or `examples.jsonl` eligible rows as fallback).
6. The baseline-hash question in §3 (CSV bytes vs JSON values; line endings).
