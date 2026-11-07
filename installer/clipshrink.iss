; Per-user install: no administrator password, no separate downloads.
[Setup]
AppName=ClipShrink
AppVersion=1.7
AppPublisher=ClipShrink
DefaultDirName={localappdata}\Programs\ClipShrink
DefaultGroupName=ClipShrink
DisableProgramGroupPage=yes
DisableDirPage=yes
DisableReadyPage=yes
PrivilegesRequired=lowest
OutputDir=..\dist
OutputBaseFilename=ClipShrink-Setup
Compression=lzma2
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64compatible
ArchitecturesAllowed=x64compatible
UninstallDisplayIcon={app}\ClipShrink.exe
WizardStyle=modern
SetupIconFile=..\assets\clipshrink.ico
; The installer offers the app's seven languages, English first and preselected.
ShowLanguageDialog=yes
LanguageDetectionMethod=none

[Languages]
Name: "en"; MessagesFile: "compiler:Default.isl"
Name: "fr"; MessagesFile: "compiler:Languages\French.isl"
Name: "nl"; MessagesFile: "compiler:Languages\Dutch.isl"
Name: "de"; MessagesFile: "compiler:Languages\German.isl"
Name: "es"; MessagesFile: "compiler:Languages\Spanish.isl"
Name: "it"; MessagesFile: "compiler:Languages\Italian.isl"
Name: "pt"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[CustomMessages]
en.OpenNow=Open ClipShrink now
fr.OpenNow=Ouvrir ClipShrink maintenant
nl.OpenNow=ClipShrink nu openen
de.OpenNow=ClipShrink jetzt öffnen
es.OpenNow=Abrir ClipShrink ahora
it.OpenNow=Apri ClipShrink ora
pt.OpenNow=Abrir o ClipShrink agora

[Files]
Source: "..\dist\ClipShrink\*"; DestDir: "{app}"; Flags: recursesubdirs ignoreversion

[Icons]
Name: "{userprograms}\ClipShrink"; Filename: "{app}\ClipShrink.exe"
Name: "{userdesktop}\ClipShrink"; Filename: "{app}\ClipShrink.exe"

[Run]
Filename: "{app}\ClipShrink.exe"; Description: "{cm:OpenNow}"; Flags: nowait postinstall skipifsilent
