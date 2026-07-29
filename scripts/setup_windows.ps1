param(
    [Parameter(Mandatory = $true)][string]$AppDir,
    [ValidateSet("none", "defaults", "all")][string]$Models = "none",
    [string]$RuntimeDir = "venv",
    [switch]$SkipRuntime
)

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"
$logDir = Join-Path $env:LOCALAPPDATA "Woke\logs"
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$log = Join-Path $logDir "install.log"
Start-Transcript -Path $log -Append

try {
    $uv = Join-Path $AppDir "tools\uv.exe"
    $venv = Join-Path $AppDir $RuntimeDir
    $python = Join-Path $venv "Scripts\python.exe"
    $readyMarker = Join-Path $AppDir ".runtime-ready"
    $streamlitStatic = Join-Path $venv "Lib\site-packages\streamlit\static\index.html"
    if (-not $SkipRuntime) {
        $runtimeReady = (Test-Path -LiteralPath $readyMarker) -and
                        (Test-Path -LiteralPath $python) -and
                        (Test-Path -LiteralPath $streamlitStatic)
        if ($runtimeReady) {
            Write-Host "Runtime WOKE já verificado: $RuntimeDir"
        }
        else {
            Remove-Item -LiteralPath $readyMarker -Force -ErrorAction SilentlyContinue
            Write-Host "WOKE - preparando Python 3.12. Por favor, aguarde."
            if (-not (Test-Path -LiteralPath $uv)) { throw "uv.exe não foi encontrado no instalador." }
            $env:UV_PYTHON_INSTALL_DIR = Join-Path $env:LOCALAPPDATA "Woke\python"
            & $uv python install 3.12
            if ($LASTEXITCODE -ne 0) { throw "Não foi possível instalar o Python 3.12." }
            & $uv venv $venv --python 3.12 --clear
            if ($LASTEXITCODE -ne 0) { throw "Não foi possível criar o ambiente Python em $RuntimeDir." }
            Write-Host "Instalando as bibliotecas científicas..."
            & $uv pip install --python $python -r (Join-Path $AppDir "requirements-windows.txt")
            if ($LASTEXITCODE -ne 0) { throw "Não foi possível instalar as dependências." }
            & $python -c "from pathlib import Path; import gensim, streamlit, plotly, sklearn, webview; static = Path(streamlit.__file__).parent / 'static' / 'index.html'; assert static.is_file(), static; print('Dependencias WOKE: OK')"
            if ($LASTEXITCODE -ne 0) { throw "A verificação das dependências falhou." }
            Set-Content -LiteralPath $readyMarker -Value "runtime=$RuntimeDir" -Encoding ASCII
        }
    }
    elseif (-not (Test-Path -LiteralPath $readyMarker)) {
        throw "O runtime do WOKE não foi concluído; o download de modelos foi interrompido."
    }

    if ($Models -ne "none") {
        Write-Host "Baixando modelos: $Models. Esta etapa pode levar muitos minutos."
        & $python (Join-Path $AppDir "woke_setup.py") --models $Models
        if ($LASTEXITCODE -ne 0) { throw "O download dos modelos não foi concluído." }
    }
}
finally {
    Stop-Transcript
}
