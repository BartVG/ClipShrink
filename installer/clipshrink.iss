; Per-user install: no administrator password, no separate downloads.
[Setup]
AppName=ClipShrink
AppVersion=1.2
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

[Files]
Source: "..\dist\ClipShrink\*"; DestDir: "{app}"; Flags: recursesubdirs ignoreversion

[Icons]
Name: "{userprograms}\ClipShrink"; Filename: "{app}\ClipShrink.exe"
Name: "{userdesktop}\ClipShrink"; Filename: "{app}\ClipShrink.exe"

[Run]
Filename: "{app}\ClipShrink.exe"; Description: "Open ClipShrink now"; Flags: nowait postinstall skipifsilent
