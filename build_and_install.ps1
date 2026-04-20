param([switch]$Elevated)

# Check for Administrator privileges
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    if ($Elevated) {
        Write-Error "Impossibile ottenere i privilegi di Amministratore."
        exit 1
    }
    
    Write-Host "Richiesta privilegi di Amministratore in corso..."
    Start-Process -FilePath PowerShell.exe -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`" -Elevated" -Verb RunAs
    exit
}

# --- Everything below this line runs as Administrator ---

$SourceDir = "C:\Users\turni\Documents\Progetti 2\JXRConverter"
$InstallDir = "C:\Program Files\JXRConverter"

Set-Location $SourceDir

Write-Host "`n>> Fermo il processo se e' in esecuzione..."
Stop-Process -Name "JXRConverter" -ErrorAction SilentlyContinue
Stop-Process -Name "main" -ErrorAction SilentlyContinue

Write-Host "`n>> Compilazione via PyInstaller..."
# Remove old dist
if (Test-Path "$SourceDir\dist\JXRConverter") { Remove-Item "$SourceDir\dist\JXRConverter" -Recurse -Force }

# Run Pyinstaller using the absolute path since the Scripts dir might not be in PATH
$PyInstallerExe = "$env:APPDATA\Python\Python314\Scripts\pyinstaller.exe"
if (-not (Test-Path $PyInstallerExe)) {
    # Try global pyinstaller
    $PyInstallerExe = "pyinstaller"
}

Invoke-Expression "& `"$PyInstallerExe`" --noconfirm --windowed --name JXRConverter main.py"

Write-Host "`n>> Copia tools originali nel pacchetto distributivo..."

$HdrfixPath = "$SourceDir\hdrfix.exe"
$DistHdrfixPath = "$SourceDir\dist\JXRConverter\hdrfix.exe"
if (Test-Path $HdrfixPath) {
    Copy-Item $HdrfixPath -Destination $DistHdrfixPath -Force
} else {
    Write-Warning "hdrfix.exe non trovato in $HdrfixPath!"
}

$JxrPath = "C:\Users\turni\Videos\jxr_to_png.exe"
$DistJxrPath = "$SourceDir\dist\JXRConverter\jxr_to_png.exe"
if (Test-Path $JxrPath) {
    Copy-Item $JxrPath -Destination $DistJxrPath -Force
} else {
    Write-Warning "jxr_to_png.exe non trovato in $JxrPath!"
}

Write-Host "`n>> Spostamento in C:\Program Files..."
if (Test-Path $InstallDir) {
    Remove-Item $InstallDir -Recurse -Force
}
Copy-Item "$SourceDir\dist\JXRConverter" -Destination $InstallDir -Recurse -Force

Write-Host "`n>> Creazione scorciatoia sul Desktop..."
$WshShell = New-Object -comObject WScript.Shell
$DesktopPath = [Environment]::GetFolderPath("Desktop")
$Shortcut = $WshShell.CreateShortcut("$DesktopPath\JXR to PNG Converter.lnk")
$Shortcut.TargetPath = "$InstallDir\JXRConverter.exe"
$Shortcut.WorkingDirectory = "$InstallDir"
$Shortcut.Description = "JXR to PNG Auto-Converter"
$Shortcut.Save()

Write-Host "`n>> Completato con successo!"
Write-Host "Lanciando l'app..."
Start-Process -FilePath "$InstallDir\JXRConverter.exe"
start-sleep -Seconds 3
