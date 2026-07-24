# Script para generar DataCleaner.exe con dependencias mínimas
$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$VenvPath = Join-Path $ProjectRoot ".venv-build"

Set-Location $ProjectRoot

Write-Host "==> Creando entorno virtual limpio..." -ForegroundColor Cyan
if (-not (Test-Path $VenvPath)) {
    python -m venv $VenvPath
}

$Python = Join-Path $VenvPath "Scripts\python.exe"
$Pip = Join-Path $VenvPath "Scripts\pip.exe"

Write-Host "==> Instalando dependencias..." -ForegroundColor Cyan
& $Python -m pip install --upgrade pip
& $Pip install -r requirements.txt
& $Pip install -r requirements-dev.txt

Write-Host "==> Compilando ejecutable..." -ForegroundColor Cyan
& $Python -m PyInstaller DataCleaner.spec --noconfirm --clean

$ExePath = Join-Path $ProjectRoot "dist\DataCleaner.exe"
if (Test-Path $ExePath) {
    $SizeMB = [math]::Round((Get-Item $ExePath).Length / 1MB, 1)
    Write-Host ""
    Write-Host "Listo: dist\DataCleaner.exe ($SizeMB MB)" -ForegroundColor Green
    Write-Host ""
    Write-Host "Para ejecutar:" -ForegroundColor Yellow
    Write-Host "  .\dist\DataCleaner.exe"
    Write-Host ""
    Write-Host "Los CSV procesados se guardan en:" -ForegroundColor Yellow
    Write-Host "  .\dist\output\   (junto al .exe si lo mueves)"
} else {
    Write-Host "Error: no se genero el ejecutable." -ForegroundColor Red
    exit 1
}
