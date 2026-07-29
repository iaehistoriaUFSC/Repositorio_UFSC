$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $Root ".venv\Scripts\python.exe"
$Iscc = "C:\Users\Rodrigo\AppData\Local\Programs\Inno Setup 6\ISCC.exe"

if (-not (Test-Path -LiteralPath $Python)) {
    throw "Build environment missing: $Python"
}

Push-Location $Root
try {
    & $Python -B scripts\make_data_manifest.py
    if ($LASTEXITCODE -ne 0) { throw "Data manifest generation failed" }
    & $Python -B -m pytest tests -q -p no:cacheprovider
    if ($LASTEXITCODE -ne 0) { throw "Tests failed" }
    if (Test-Path -LiteralPath "dist\METAPHORIQ-ZeroShot") {
        Remove-Item -LiteralPath "dist\METAPHORIQ-ZeroShot" -Recurse -Force
    }
    & $Python -B -m PyInstaller `
        --noconfirm `
        --clean `
        --windowed `
        --onedir `
        --name "METAPHORIQ-ZeroShot" `
        --add-data "data;data" `
        --collect-all matplotlib `
        --collect-all transformers `
        --collect-all huggingface_hub `
        --collect-all gdown `
        --hidden-import matplotlib.backends.backend_tkagg `
        --hidden-import app.workers.hf_worker `
        --hidden-import app.workers.melbert_worker `
        --hidden-import app.workers.framebert_worker `
        app\main.py
    if ($LASTEXITCODE -ne 0) { throw "PyInstaller build failed" }

    # PyTorch 2.13 includes deeply nested copies of vendor licenses that exceed
    # Inno Setup's staging-path limit. Keep PyTorch's own LICENSE and metadata.
    $DistRoot = (Resolve-Path -LiteralPath "dist\METAPHORIQ-ZeroShot").Path
    Get-ChildItem -LiteralPath (Join-Path $DistRoot "_internal") -Directory -Filter "torch-*.dist-info" |
        ForEach-Object {
            $ThirdPartyLicenses = Join-Path $_.FullName "licenses\third_party"
            if (Test-Path -LiteralPath $ThirdPartyLicenses) {
                $ResolvedLicenses = (Resolve-Path -LiteralPath $ThirdPartyLicenses).Path
                if (-not $ResolvedLicenses.StartsWith($DistRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
                    throw "Refusing to clean a path outside the runtime: $ResolvedLicenses"
                }
                Remove-Item -LiteralPath $ResolvedLicenses -Recurse -Force
            }
        }

    & $Iscc "installer\METAPHORIQ-ZeroShot.iss"
    if ($LASTEXITCODE -ne 0) { throw "Inno Setup build failed" }
}
finally {
    Pop-Location
}
