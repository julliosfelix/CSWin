; Script do Instalador CSWin - Versão 1.2 (Final - Correção de Menu Iniciar)
; Este script força a criação da pasta InnovFly no caminho correto do Windows.

[Setup]
; --- Identidade do App ---
AppName=CSWin
AppVersion=1.0
AppPublisher=InnovFly
AppCopyright=© 2026 InnovFly - Jullios Felix
AppPublisherURL=https://github.com/julliosfelix/CSWin

; --- ARQUITETURA 64 BITS ---
; Garante instalação em C:\Program Files
ArchitecturesInstallIn64BitMode=x64

; --- Onde Instalar Arquivos ---
DefaultDirName={autopf}\InnovFly\CSWin
DisableDirPage=no

; --- PRIVILÉGIOS (Essencial para acessar pastas de sistema) ---
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=commandline

; --- Saída do Instalador ---
OutputDir=D:\Dev\julliosfelix\CSWin
OutputBaseFilename=Instalador_CSWin_v1_x64
Compression=lzma2/ultra64
SolidCompression=yes

; --- Visual ---
SetupIconFile=D:\Dev\julliosfelix\CSWin\assets\CSWin.ico
UninstallDisplayIcon={app}\CSWin.exe
WizardStyle=modern

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Copia os arquivos para C:\Program Files\InnovFly\CSWin
Source: "D:\Dev\julliosfelix\CSWin\Montagem_CSWin\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
; CORREÇÃO DO MENU INICIAR:
; Força a criação da pasta InnovFly dentro da hierarquia correta de programas do Windows
Name: "{commonprograms}\InnovFly\CSWin"; Filename: "{app}\CSWin.exe"; IconFilename: "{app}\CSWin.exe"
Name: "{commonprograms}\InnovFly\Desinstalar CSWin"; Filename: "{uninstallexe}"

; Atalho na Área de Trabalho
Name: "{autodesktop}\CSWin"; Filename: "{app}\CSWin.exe"; Tasks: desktopicon

[Run]
; Inicia o app após fechar o instalador
Filename: "{app}\CSWin.exe"; Description: "Iniciar CSWin agora"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Limpa a pasta de configurações em AppData se ela existir
Type: filesandordirs; Name: "{userappdata}\InnovFly\CSWin"