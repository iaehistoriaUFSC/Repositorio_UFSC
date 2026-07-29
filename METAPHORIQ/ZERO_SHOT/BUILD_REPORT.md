# Build report

Release: `0.1.1`

Built: `2026-07-28`

Installer:
`METAPHORIQ_ZeroShot_Setup_v0.1.1_Windows_2026-07-28.exe`

Size: `184709782` bytes (`176.15 MiB`)

SHA-256:
`0F7E4FFC21C24B29F588C0B875F96C083F4A7CF7536A0C929BF745D2565A7FB5`

## Verification

- Automated suite: `11 passed`.
- Final installer: silent install, bundled-data health check, and uninstall passed.
- GUI: installed Tk/Matplotlib window opened with the expected title.
- GUI workflow: setup strip and permanent Run action were visible at
  `1080x720`; the built-in example completed with three detections.
- Bundled dataset: 44 assignable taxonomy classes and 4 model definitions.
- Official MelBERT VUA-18 checkpoint: download and packaged inference passed.
- XLM-R VUAMC checkpoint: download and packaged inference passed.
- Test sentence: both detectors marked `attacked`, `planted`, and `seeds`.
- Chronology/taxonomy integration: 1820 mapped to period `B`; detections
  received provisional Javier taxonomy candidates.

MelBERT and XLM-R downloads remain in
`%LOCALAPPDATA%\MetaphoriqZeroShot\models`. Third-party weights are not
redistributed inside the installer.
