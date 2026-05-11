$ErrorActionPreference = 'Stop'

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$venvDir = Join-Path $scriptDir 'venv'
$pythonExe = Join-Path $venvDir 'Scripts\python.exe'
$requirementsFile = Join-Path $scriptDir 'requirements.txt'

if (-not (Test-Path $pythonExe)) {
    Write-Host 'Creating virtual environment...'
    python -m venv $venvDir
}

Write-Host 'Checking backend dependencies...'
$dependencyCheck = & $pythonExe -c "import importlib.util; import sys; modules = ('fastapi', 'uvicorn', 'pydantic'); missing = [name for name in modules if importlib.util.find_spec(name) is None]; print(','.join(missing)); sys.exit(1 if missing else 0)" 2>$null
if ($LASTEXITCODE -ne 0) {
    if ($dependencyCheck) {
        Write-Host ('Missing modules: ' + $dependencyCheck)
    }
    Write-Host 'Installing missing dependencies from requirements.txt...'
    & $pythonExe -m pip install --upgrade pip
    & $pythonExe -m pip install -r $requirementsFile
    if ($LASTEXITCODE -ne 0) {
        throw 'Dependency installation failed. Backend server was not started.'
    }
}

Write-Host 'Starting FastAPI server at http://127.0.0.1:8000'
Push-Location $scriptDir
try {
    & $pythonExe -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
}
finally {
    Pop-Location
}
