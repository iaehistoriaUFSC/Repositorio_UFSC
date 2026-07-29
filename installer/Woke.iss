#define MyAppName "WOKE"
#define MyAppVersion "0.1.3-demo"
#define MyAppPublisher "Equipe IA & História — UFSC"
#define MyAppExeName "woke_launcher.py"
#define MyRuntimeDir "venv-0.1.3"

[Setup]
AppId={{773A661C-A549-47F3-9BC6-2BA07887F180}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={localappdata}\Programs\WOKE
DefaultGroupName=WOKE
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
OutputDir=..
OutputBaseFilename=Woke_Setup_v0.1.3-demo_Runtime-fix_Windows_2026-07-23
SetupIconFile=..\assets\woke.ico
UninstallDisplayIcon={app}\assets\woke.ico
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
WizardSizePercent=110
SetupLogging=yes
CloseApplications=yes
RestartApplications=no

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "Criar um atalho na Área de Trabalho"; GroupDescription: "Atalhos:"; Flags: checkedonce
Name: "models\defaults"; Description: "Baixar História (HST) Temporal e Incremental — Modelo 1, série 2003–2024 (recomendado; aproximadamente 63 MB)"; GroupDescription: "Modelos locais:"; Flags: exclusive checkedonce
Name: "models\none"; Description: "Não baixar modelos agora (poderei baixar pela interface)"; GroupDescription: "Modelos locais:"; Flags: exclusive unchecked
Name: "models\all"; Description: "Baixar todos os 28 pacotes (pode ocupar dezenas de GB)"; GroupDescription: "Modelos locais:"; Flags: exclusive unchecked

[Files]
Source: "..\woke_app.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\woke_analysis.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\woke_catalog.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\woke_models.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\woke_launcher.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\woke_setup.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\requirements-windows.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\assets\woke.ico"; DestDir: "{app}\assets"; Flags: ignoreversion
Source: "..\assets\woke.png"; DestDir: "{app}\assets"; Flags: ignoreversion
Source: "uv.exe"; DestDir: "{app}\tools"; Flags: ignoreversion
Source: "..\scripts\setup_windows.ps1"; DestDir: "{app}\scripts"; Flags: ignoreversion

[Icons]
Name: "{group}\WOKE"; Filename: "{app}\{#MyRuntimeDir}\Scripts\pythonw.exe"; Parameters: """{app}\{#MyAppExeName}"""; WorkingDir: "{app}"; IconFilename: "{app}\assets\woke.ico"
Name: "{autodesktop}\WOKE"; Filename: "{app}\{#MyRuntimeDir}\Scripts\pythonw.exe"; Parameters: """{app}\{#MyAppExeName}"""; WorkingDir: "{app}"; IconFilename: "{app}\assets\woke.ico"; Tasks: desktopicon

[Run]
Filename: "{sys}\WindowsPowerShell\v1.0\powershell.exe"; Parameters: "-NoProfile -ExecutionPolicy Bypass -File ""{app}\scripts\setup_windows.ps1"" -AppDir ""{app}"" -Models none -RuntimeDir ""{#MyRuntimeDir}"""; StatusMsg: "Instalando Python e bibliotecas científicas. Isso pode levar alguns minutos..."; Flags: waituntilterminated runhidden
Filename: "{sys}\WindowsPowerShell\v1.0\powershell.exe"; Parameters: "-NoProfile -ExecutionPolicy Bypass -File ""{app}\scripts\setup_windows.ps1"" -AppDir ""{app}"" -Models defaults -RuntimeDir ""{#MyRuntimeDir}"" -SkipRuntime"; StatusMsg: "Baixando a série completa de História, 2003–2024 (aproximadamente 63 MB). Por favor, aguarde..."; Flags: waituntilterminated runhidden; Tasks: models\defaults
Filename: "{sys}\WindowsPowerShell\v1.0\powershell.exe"; Parameters: "-NoProfile -ExecutionPolicy Bypass -File ""{app}\scripts\setup_windows.ps1"" -AppDir ""{app}"" -Models all -RuntimeDir ""{#MyRuntimeDir}"" -SkipRuntime"; StatusMsg: "Baixando todos os 28 pacotes WOKE. Esta etapa pode ser muito demorada..."; Flags: waituntilterminated runhidden; Tasks: models\all
Filename: "{app}\{#MyRuntimeDir}\Scripts\pythonw.exe"; Parameters: """{app}\{#MyAppExeName}"""; Description: "Abrir o WOKE"; Flags: nowait postinstall skipifsilent; Check: RuntimeReady

[UninstallDelete]
Type: filesandordirs; Name: "{app}\venv"
Type: filesandordirs; Name: "{app}\venv-*"
Type: filesandordirs; Name: "{app}\__pycache__"
Type: files; Name: "{app}\.runtime-ready"
Type: filesandordirs; Name: "{localappdata}\Woke\python"
Type: filesandordirs; Name: "{localappdata}\Woke\logs"

[Code]
var
  RemoveModelData: Boolean;

function RuntimeReady(): Boolean;
begin
  Result := FileExists(ExpandConstant('{app}\.runtime-ready'));
end;

function InitializeUninstall(): Boolean;
begin
  Result := True;
  RemoveModelData := False;
  if not UninstallSilent then
    RemoveModelData := MsgBox(
      'Deseja excluir também todos os modelos WOKE baixados? Eles podem ocupar muitos gigabytes. Se escolher Não, poderão ser reutilizados numa futura instalação.',
      mbConfirmation, MB_YESNO) = IDYES;
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  if (CurUninstallStep = usPostUninstall) and RemoveModelData then
    DelTree(ExpandConstant('{localappdata}\Woke\modelos'), True, True, True);
end;
