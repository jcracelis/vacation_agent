# ============================================================
#  Vacation Agent - Quick Start (PowerShell)
#  Installs Ollama, pulls llama3, starts server, opens VS Code
# ============================================================

$ErrorActionPreference = "Continue"

$AGENT_DIR = "C:\Users\racel\github\vacation_agent\.github\agents"
$VSCODE_DIR = Join-Path $AGENT_DIR "vscode-extension"
$PYTHON_PATH = "C:\Program Files\Python314\python.exe"

Write-Host ""
Write-Host " ============================================================" -ForegroundColor Cyan
Write-Host "  Vacation Agent - Windows Setup (PowerShell)" -ForegroundColor Cyan
Write-Host " ============================================================" -ForegroundColor Cyan
Write-Host ""

# --- 1. Check Python ---
Write-Host "[1/5] Checking Python..." -ForegroundColor Yellow
if (Test-Path $PYTHON_PATH) {
    Write-Host "  Found: $PYTHON_PATH" -ForegroundColor Green
} else {
    # Try to find Python via py launcher
    $pyPath = (where.exe py 2>$null)
    if ($pyPath) {
        $PYTHON_PATH = "py"
        Write-Host "  Found Python via 'py' launcher" -ForegroundColor Green
    } else {
        Write-Host "  ERROR: Python not found. Install from https://python.org" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

# --- 2. Install Python dependencies ---
Write-Host "[2/5] Installing Python dependencies..." -ForegroundColor Yellow
$reqFile = Join-Path $AGENT_DIR "requirements.txt"
if (Test-Path $reqFile) {
    & $PYTHON_PATH -m pip install -r $reqFile --quiet --user 2>&1 | Out-Null
    Write-Host "  Dependencies installed." -ForegroundColor Green
} else {
    Write-Host "  WARNING: requirements.txt not found at $reqFile" -ForegroundColor Yellow
}

# --- 3. Install Ollama ---
Write-Host "[3/5] Checking for Ollama..." -ForegroundColor Yellow
$ollamaCmd = Get-Command ollama -ErrorAction SilentlyContinue
if ($ollamaCmd) {
    Write-Host "  Ollama is already installed." -ForegroundColor Green
} else {
    Write-Host "  Downloading Ollama..." -ForegroundColor Yellow
    $installerPath = "$env:TEMP\OllamaSetup.exe"
    try {
        Invoke-WebRequest -Uri "https://ollama.com/download/OllamaSetup.exe" -OutFile $installerPath -UseBasicParsing
        Write-Host "  Running installer (silent)..." -ForegroundColor Yellow
        Start-Process -FilePath $installerPath -ArgumentList "/SILENT" -Wait -NoNewWindow
        Remove-Item $installerPath -Force -ErrorAction SilentlyContinue
        
        # Refresh PATH in current session
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
        
        $ollamaCmd = Get-Command ollama -ErrorAction SilentlyContinue
        if ($ollamaCmd) {
            Write-Host "  Ollama installed successfully." -ForegroundColor Green
        } else {
            Write-Host "  WARNING: Ollama may need a restart. Please install manually from https://ollama.com" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "  ERROR: Could not download Ollama. Install from https://ollama.com" -ForegroundColor Red
    }
}

# --- 4. Pull model and start Ollama ---
Write-Host "[4/5] Setting up Ollama model..." -ForegroundColor Yellow
$ollamaCmd = Get-Command ollama -ErrorAction SilentlyContinue
if ($ollamaCmd) {
    Write-Host "  Starting Ollama server in background..." -ForegroundColor Yellow
    Start-Process -FilePath "ollama" -ArgumentList "serve" -WindowStyle Hidden
    
    Write-Host "  Waiting for server to start..." -ForegroundColor Yellow
    Start-Sleep -Seconds 5
    
    Write-Host "  Pulling llama3 model (this may take a few minutes)..." -ForegroundColor Yellow
    & ollama pull llama3 2>&1 | ForEach-Object { Write-Host "    $_" -ForegroundColor Gray }
    
    Write-Host "  Ollama is running and llama3 is ready." -ForegroundColor Green
} else {
    Write-Host "  WARNING: Ollama not available." -ForegroundColor Yellow
    Write-Host "  Install from https://ollama.com, then run:" -ForegroundColor Yellow
    Write-Host "    ollama pull llama3" -ForegroundColor Gray
    Write-Host "    ollama serve" -ForegroundColor Gray
}

# --- 5. Open VS Code ---
Write-Host "[5/5] Opening VS Code..." -ForegroundColor Yellow
if (Test-Path $VSCODE_DIR) {
    $codeCmd = Get-Command code -ErrorAction SilentlyContinue
    if ($codeCmd) {
        Set-Location $VSCODE_DIR
        Write-Host "  Launching VS Code..." -ForegroundColor Green
        Start-Process -FilePath "code" -ArgumentList "." -WindowStyle Normal
        
        Write-Host ""
        Write-Host " ============================================================" -ForegroundColor Cyan
        Write-Host "  VS Code is opening..." -ForegroundColor Green
        Write-Host ""
        Write-Host "  Next steps:" -ForegroundColor White
        Write-Host "   1. Press F5 to launch Extension Development Host" -ForegroundColor White
        Write-Host "   2. Click the 🌴 Vacation Agent icon in the sidebar" -ForegroundColor White
        Write-Host "   3. Start chatting!" -ForegroundColor White
        Write-Host " ============================================================" -ForegroundColor Cyan
        Write-Host ""
    } else {
        Write-Host "  ERROR: 'code' command not found in PATH." -ForegroundColor Red
        Write-Host "  Open VS Code manually and open: $VSCODE_DIR" -ForegroundColor Yellow
        Write-Host "  Then press F5." -ForegroundColor Yellow
    }
} else {
    Write-Host "  ERROR: Extension directory not found: $VSCODE_DIR" -ForegroundColor Red
}

Read-Host "Press Enter to exit"
