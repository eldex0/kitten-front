$ErrorActionPreference = "Stop"
Set-Location -LiteralPath $PSScriptRoot

$bundledPython = Join-Path $env:USERPROFILE ".cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
$pythonCommand = $null
if (Test-Path -LiteralPath $bundledPython) {
    $pythonCommand = $bundledPython
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    $pythonCommand = "py"
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonCommand = "python"
} else {
    throw "Python 3 est introuvable. Installez Python puis relancez ce script."
}

$pythonArgs = @()
if ($pythonCommand -eq "py") { $pythonArgs = @("-3") }
& $pythonCommand @pythonArgs -m pip install -r requirements-dev.txt
& $pythonCommand @pythonArgs -m PyInstaller --noconfirm --clean --onefile --windowed --paths ".deps" --add-data "assets;assets" --icon "assets\kitten-front.ico" --name "KITTEN FRONT" main.py
Write-Host "Executable cree : $PSScriptRoot\dist\KITTEN FRONT.exe"
