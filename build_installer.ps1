$ErrorActionPreference = "Stop"
Set-Location -LiteralPath $PSScriptRoot

& (Join-Path $PSScriptRoot "build_exe.ps1")

$candidates = @(
    (Join-Path ${env:ProgramFiles(x86)} "Inno Setup 6\ISCC.exe"),
    (Join-Path $env:ProgramFiles "Inno Setup 6\ISCC.exe")
)
$compiler = $candidates | Where-Object { $_ -and (Test-Path -LiteralPath $_) } | Select-Object -First 1
if (-not $compiler) {
    throw "Inno Setup 6 est introuvable. Installez-le puis relancez build_installer.ps1."
}

& $compiler (Join-Path $PSScriptRoot "packaging\installer.iss")
Write-Host "Installateur cree : $PSScriptRoot\dist\KITTEN-FRONT-Setup.exe"
