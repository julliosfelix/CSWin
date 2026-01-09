; Script do Instalador CSWin - Versão 64-bit Nativa
; Caminho ajustado para D:\Dev\julliosfelix\CSWin\Montagem_CSWin

[Setup]
; --- Identidade do App ---
AppName=CSWin
AppVersion=1.0
AppPublisher=InnovFly
AppCopyright=© 2026 InnovFly - Jullios Felix

; --- ARQUITETURA 64 BITS (A Linha Mágica) ---
; Isso remove o (x86) e manda para C:\Program Files
ArchitecturesInstallIn64BitMode=x64

; --- Onde Instalar ---
DefaultDirName={autopf}\InnovFly\CSWin
DefaultGroupName=InnovFly
DisableDirPage=no

; --- Saída ---
OutputDir=D:\Dev\julliosfelix\CSWin
OutputBaseFilename=Instalador_CSWin_v1_x64
Compression=lzma2/ultra64
SolidCompression=yes

; --- Visual ---
SetupIconFile=D:\Dev\julliosfelix\CSWin\assets\CSWin.ico
UninstallDisplayIcon={app}\CSWin.exe

; --- Privilégios ---
PrivilegesRequired=admin

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "D:\Dev\julliosfelix\CSWin\Montagem_CSWin\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\CSWin"; Filename: "{app}\CSWin.exe"
Name: "{group}\Desinstalar CSWin"; Filename: "{uninstallexe}"
Name: "{autodesktop}\CSWin"; Filename: "{app}\CSWin.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\CSWin.exe"; Description: "Iniciar CSWin agora"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{userappdata}\InnovFly\CSWin"