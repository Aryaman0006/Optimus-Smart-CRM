[Setup]
AppName=Optimus Smart CRM
AppVersion=1.0
SetupIconFile=C:\Users\Aryaman\OneDrive\Desktop\Smart-CRM\backend\icon.ico

DefaultDirName={pf}\Optimus Smart CRM
DefaultGroupName=Optimus Smart CRM

OutputDir=output
OutputBaseFilename=OptimusSmartCRMSetup

Compression=lzma
SolidCompression=yes


[Files]

Source: "C:\Users\Aryaman\OneDrive\Desktop\Smart-CRM\backend\dist\OptimusSmartCRM.exe"; DestDir: "{app}"; Flags: ignoreversion

Source: "C:\Users\Aryaman\OneDrive\Desktop\Smart-CRM\backend\data\*"; DestDir: "{app}\data"; Flags: ignoreversion recursesubdirs createallsubdirs

Source: "C:\Users\Aryaman\OneDrive\Desktop\Smart-CRM\backend\templates\*"; DestDir: "{app}\templates"; Flags: ignoreversion recursesubdirs createallsubdirs

Source: "C:\Users\Aryaman\OneDrive\Desktop\Smart-CRM\backend\static\*"; DestDir: "{app}\static"; Flags: ignoreversion recursesubdirs createallsubdirs


[Dirs]

Name: "{userdocs}\OptimusExports"


[Icons]

Name: "{group}\Optimus Smart CRM"; Filename: "{app}\OptimusSmartCRM.exe"

Name: "{commondesktop}\Optimus Smart CRM"; Filename: "{app}\OptimusSmartCRM.exe"


[Run]

Filename: "{app}\OptimusSmartCRM.exe"; Description: "Launch Optimus Smart CRM"; Flags: nowait postinstall skipifsilent