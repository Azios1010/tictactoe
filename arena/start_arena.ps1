$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$rootDir = Resolve-Path (Join-Path $scriptDir "..")
$backendDir = Join-Path $scriptDir "..\\backend"
$pythonExe = Join-Path $backendDir "venv\\Scripts\\python.exe"
$envFile = Join-Path $backendDir ".env"

if (Test-Path $envFile) {
  Get-Content $envFile | ForEach-Object {
    $line = $_.Trim()
    if (-not $line -or $line.StartsWith("#") -or -not $line.Contains("=")) {
      return
    }
    $parts = $line.Split("=", 2)
    $name = $parts[0].Trim()
    $value = $parts[1].Trim().Trim('"').Trim("'")
    if ($name) {
      [Environment]::SetEnvironmentVariable($name, $value, "Process")
    }
  }
}

if (-not (Test-Path $pythonExe)) {
  Write-Host "Khong tim thay Python trong backend\\venv. Hay chay .\\backend\\start_backend.ps1 truoc."
  exit 1
}

Write-Host "Starting Gomoku Arena API on http://127.0.0.1:8100"
Push-Location $rootDir
try {
  & $pythonExe -m uvicorn arena.service:app --app-dir $rootDir --host 127.0.0.1 --port 8100 --reload --reload-dir (Join-Path $rootDir "arena")
} finally {
  Pop-Location
}
