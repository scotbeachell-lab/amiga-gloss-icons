<#
.SYNOPSIS
  Apply (or remove) AmigaGloss icons on Windows for the current user.

.DESCRIPTION
  Uses only per-user, reversible settings:
    - desktop.ini IconResource for your user folders (Documents, Downloads, ...)
    - HKCU registry overrides for drive icons and the Recycle Bin
  System files (imageres.dll, shell32.dll) and HKLM are never touched.
  The icons are copied to %USERPROFILE%\.amigagloss (a hidden folder) and
  everything changed is backed up there first; -Uninstall puts it all back.
  (Not %LOCALAPPDATA%: Explorer's folder windows won't load folder icons from there.)

  Build the icons first:  cd gen; python build_windows.py

.EXAMPLE
  .\install-windows.ps1 -DryRun     # show what would change
  .\install-windows.ps1             # apply
  .\install-windows.ps1 -Uninstall  # restore the originals
#>
[CmdletBinding()]
param(
    [switch]$Uninstall,
    [switch]$DryRun
)
$ErrorActionPreference = 'Stop'

$Src     = Join-Path $PSScriptRoot 'windows\ico'
$Home_   = Join-Path $env:USERPROFILE '.amigagloss'
$IcoDir  = Join-Path $Home_ 'ico'
$Backup  = Join-Path $Home_ 'backup'
$RegBak  = Join-Path $Backup 'registry.json'

function Shell-Folder($name, $guid) {
    $k = 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders'
    $v = (Get-ItemProperty $k -ErrorAction SilentlyContinue).$name
    if (-not $v -and $guid) { $v = (Get-ItemProperty $k -ErrorAction SilentlyContinue).$guid }
    if ($v) { [Environment]::ExpandEnvironmentVariables($v) }
}

# folder -> icon
$Folders = [ordered]@{
    (Shell-Folder 'Personal')                                    = 'places\folder-documents'
    (Shell-Folder '{374DE290-123F-4565-9164-39C4925E467B}')      = 'places\folder-download'
    (Shell-Folder 'My Music')                                    = 'places\folder-music'
    (Shell-Folder 'My Pictures')                                 = 'places\folder-pictures'
    (Shell-Folder 'My Video')                                    = 'places\folder-videos'
    (Join-Path $env:USERPROFILE 'GitHub')                        = 'places\folder-development'
}

# Windows 10/11 "known folders" take their icon from a machine-wide registration that
# overrides desktop.ini, so they also need a per-user override of their shell CLSID.
$KnownFolderClsid = [ordered]@{
    '{d3162b92-9365-467a-956b-92703aca08af}' = 'places\folder-documents'
    '{088e3905-0323-4b02-9826-5d99428e115f}' = 'places\folder-download'
    '{3dfdf296-dbec-4fb4-81d1-6a3438bcf4de}' = 'places\folder-music'
    '{24ad3ad4-a569-4530-98e1-ab02f9417aa8}' = 'places\folder-pictures'
    '{f86fa3ab-70d2-4fc7-9c99-fcbf05467f3a}' = 'places\folder-videos'
}
$ClsidRoot = 'HKCU:\Software\Classes\CLSID'

$RecycleKey ='HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\CLSID\{645FF040-5081-101B-9F08-00AA002F954E}\DefaultIcon'
$DriveRoot  = 'HKCU:\Software\Classes\Applications\Explorer.exe\Drives'

function Say($msg) { if ($DryRun) { Write-Host "[dry run] $msg" } else { Write-Host $msg } }
function Ico($rel) { Join-Path $IcoDir ($rel + '.ico') }
function Safe-Name($path) { ($path -replace '[:\\/]', '_') }

function Remove-RegValue($key, $name) {
    # Remove-ItemProperty can't delete a key's default value by the name '(default)'
    if (-not (Test-Path $key)) { return }
    $sub = (Convert-Path $key) -replace '^HKEY_CURRENT_USER\\', ''
    $rk = [Microsoft.Win32.Registry]::CurrentUser.OpenSubKey($sub, $true)
    if ($rk) {
        $rk.DeleteValue($(if ($name -eq '(default)') { '' } else { $name }), $false)
        $rk.Close()
    }
}

function Drive-Icon($letter, $type) {
    if ($type -eq 'Fixed') {
        try {
            $disk = Get-Partition -DriveLetter $letter -ErrorAction Stop | Get-Disk -ErrorAction Stop
            if ($disk.BusType -eq 'USB') { return 'devices\drive-harddisk-usb' }
            $media = (Get-PhysicalDisk -ErrorAction Stop | Where-Object { $_.DeviceId -eq "$($disk.Number)" }).MediaType
            if ($disk.BusType -eq 'NVMe' -or $media -eq 'SSD') { return 'devices\drive-harddisk-solidstate' }
        } catch { }
        return 'devices\drive-harddisk'
    }
    switch ($type) {
        'Removable' { 'devices\drive-harddisk-usb' }
        'CDRom'     { 'devices\drive-optical' }
        'Network'   { 'places\folder-remote' }
        default     { $null }
    }
}

function Refresh-Icons {
    if ($DryRun) { return }
    $exe = Join-Path $env:SystemRoot 'System32\ie4uinit.exe'
    if (Test-Path $exe) { & $exe -show }
}

# ---------------------------------------------------------------- uninstall
if ($Uninstall) {
    if (-not (Test-Path $Backup)) { Write-Host 'Nothing to undo: no AmigaGloss backup found.'; exit 0 }
    foreach ($dir in $Folders.Keys) {
        if (-not $dir -or -not (Test-Path $dir)) { continue }
        $ini = Join-Path $dir 'desktop.ini'
        $bak = Join-Path $Backup ((Safe-Name $dir) + '.desktop.ini')
        $none = $bak + '.none'
        if (Test-Path $bak) {
            Say "restore  $ini"
            if (-not $DryRun) {
                if (Test-Path $ini) { attrib -h -s -r $ini }
                Copy-Item $bak $ini -Force
                attrib +h +s $ini
            }
        } elseif (Test-Path $none) {
            Say "remove   $ini (did not exist before)"
            if (-not $DryRun -and (Test-Path $ini)) { attrib -h -s -r $ini; Remove-Item $ini -Force }
        }
    }
    if (Test-Path $RegBak) {
        $saved = Get-Content $RegBak -Raw | ConvertFrom-Json
        foreach ($e in $saved) {
            if ($e.existed) {
                Say "restore  $($e.key) [$($e.name)]"
                if (-not $DryRun) {
                    if (-not (Test-Path $e.key)) { New-Item $e.key -Force | Out-Null }
                    Set-ItemProperty -Path $e.key -Name $e.name -Value $e.value
                }
            } else {
                Say "remove   $($e.key) [$($e.name)]"
                if (-not $DryRun) { Remove-RegValue $e.key $e.name }
            }
        }
        # drop override keys we created if they are now empty; an empty per-user
        # DefaultIcon key would hide the system icon and leave a blank one
        if (-not $DryRun) {
            $parents = @()
            if (Test-Path $DriveRoot) { $parents += Get-ChildItem $DriveRoot | ForEach-Object { $_.PSPath } }
            $parents += $KnownFolderClsid.Keys | ForEach-Object { Join-Path $ClsidRoot $_ } | Where-Object { Test-Path $_ }
            foreach ($p in $parents) {
                $di = Join-Path $p 'DefaultIcon'
                if ((Test-Path $di) -and -not (Get-Item $di).Property -and -not (Get-ChildItem $di)) { Remove-Item $di -Force }
                if (-not (Get-Item $p).Property -and -not (Get-ChildItem $p)) { Remove-Item $p -Force }
            }
        }
    }
    Say "remove   $Home_"
    if (-not $DryRun) { Remove-Item $Home_ -Recurse -Force }
    Refresh-Icons
    Write-Host 'AmigaGloss removed. If an icon is still showing, sign out and back in (or restart Explorer).'
    exit 0
}

# ---------------------------------------------------------------- install
if (-not (Test-Path $Src)) {
    throw "No built icons at $Src. Run:  cd gen; python build_windows.py"
}
if (Test-Path $RegBak) {
    throw "AmigaGloss already looks installed (backup at $Backup). Run with -Uninstall first."
}

Say "copy     $Src -> $IcoDir"
if (-not $DryRun) {
    New-Item $Backup -ItemType Directory -Force | Out-Null
    if (Test-Path $IcoDir) { Remove-Item $IcoDir -Recurse -Force }
    Copy-Item $Src $IcoDir -Recurse
    (Get-Item $Home_ -Force).Attributes = 'Directory, Hidden'
}

# --- folders
foreach ($dir in $Folders.Keys) {
    if (-not $dir -or -not (Test-Path $dir)) { continue }
    $icon = Ico $Folders[$dir]
    $ini  = Join-Path $dir 'desktop.ini'
    $bak  = Join-Path $Backup ((Safe-Name $dir) + '.desktop.ini')
    Say "folder   $dir  ->  $(Split-Path $icon -Leaf)"
    if ($DryRun) { continue }

    if (Test-Path $ini) {
        Copy-Item $ini $bak -Force
        $lines = @(Get-Content $ini -Force)
    } else {
        New-Item ($bak + '.none') -ItemType File -Force | Out-Null
        $lines = @()
    }
    # keep everything else (e.g. the localized folder name); swap the icon lines
    $lines = @($lines | Where-Object { $_ -notmatch '^\s*(IconResource|IconFile|IconIndex)\s*=' })
    $i = [Array]::FindIndex([string[]]$lines, [Predicate[string]]{ param($l) $l -match '^\s*\[\.ShellClassInfo\]' })
    if ($i -lt 0) { $lines += '[.ShellClassInfo]'; $i = $lines.Count - 1 }
    $new = @()
    if ($i -ge 0) { $new += $lines[0..$i] }
    $new += "IconResource=$icon,0"
    if ($i + 1 -lt $lines.Count) { $new += $lines[($i + 1)..($lines.Count - 1)] }

    if (Test-Path $ini) { attrib -h -s -r $ini }
    Set-Content -Path $ini -Value $new -Encoding Unicode
    attrib +h +s $ini
    attrib +r $dir    # Explorer only reads desktop.ini on read-only/system folders
}

# --- registry (backed up value by value)
$regBackup = @()
function Set-Reg($key, $name, $value) {
    $existed = $false; $old = $null
    if (Test-Path $key) {
        $p = Get-ItemProperty $key -ErrorAction SilentlyContinue
        if ($p -and ($p.PSObject.Properties.Name -contains $name)) { $existed = $true; $old = $p.$name }
    }
    $script:regBackup += [pscustomobject]@{ key = $key; name = $name; existed = $existed; value = $old }
    Say "registry $key [$name] = $value"
    if (-not $DryRun) {
        if (-not (Test-Path $key)) { New-Item $key -Force | Out-Null }
        Set-ItemProperty -Path $key -Name $name -Value $value
    }
}

$empty = Ico 'places\user-trash'
$full  = Ico 'places\user-trash-full'
# (default) is the icon shown right now; Explorer swaps it as the bin fills/empties,
# so start it on whichever state the bin is in.
$cur = Get-ItemProperty $RecycleKey -ErrorAction SilentlyContinue
$isFull = $cur -and $cur.'(default)' -and ($cur.'(default)' -eq $cur.full)
Set-Reg $RecycleKey '(default)' $(if ($isFull) { "$full,0" } else { "$empty,0" })
Set-Reg $RecycleKey 'empty'     "$empty,0"
Set-Reg $RecycleKey 'full'      "$full,0"

foreach ($c in $KnownFolderClsid.Keys) {
    Set-Reg (Join-Path $ClsidRoot ($c + '\DefaultIcon')) '(default)' ((Ico $KnownFolderClsid[$c]) + ',0')
}

foreach ($d in Get-PSDrive -PSProvider FileSystem) {
    if ($d.Root -notmatch '^[A-Z]:\\$') { continue }
    $rel = Drive-Icon $d.Name ([IO.DriveInfo]$d.Root).DriveType
    if (-not $rel -or -not (Test-Path (Join-Path $Src ($rel + '.ico')))) { continue }
    Set-Reg (Join-Path $DriveRoot ($d.Name + '\DefaultIcon')) '(default)' (Ico $rel)
}

if (-not $DryRun) { $regBackup | ConvertTo-Json | Set-Content $RegBak -Encoding UTF8 }
Refresh-Icons
if ($DryRun) { Write-Host 'Dry run only: nothing was changed.' }
else { Write-Host 'AmigaGloss applied. If some icons have not changed yet, sign out and back in (or restart Explorer).' }
