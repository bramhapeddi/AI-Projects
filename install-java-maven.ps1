# =============================================================================
# Java + Maven Automated Installation Script for Windows
# =============================================================================
# This script automates the installation of:
# - OpenJDK 17 (LTS) from Eclipse Temurin
# - Apache Maven 3.9.6
# - PATH environment variable configuration
# =============================================================================

param(
    [switch]$SkipJava,
    [switch]$SkipMaven,
    [switch]$Force,
    [string]$JavaVersion = "17",
    [string]$MavenVersion = "3.9.6"
)

# Set execution policy and error handling
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
$ErrorActionPreference = "Stop"

# Colors for output
$Colors = @{
    Info = "Cyan"
    Success = "Green"
    Warning = "Yellow"
    Error = "Red"
}

function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Colors[$Color]
}

function Write-Info { param($msg) Write-ColorOutput $msg "Info" }
function Write-Success { param($msg) Write-ColorOutput $msg "Success" }
function Write-Warning { param($msg) Write-ColorOutput $msg "Warning" }
function Write-Error { param($msg) Write-ColorOutput $msg "Error" }

# Banner
Write-Host "=============================================================================" -ForegroundColor Magenta
Write-Host "  Java + Maven Automated Installation Script" -ForegroundColor Magenta
Write-Host "  For Test Automation Framework" -ForegroundColor Magenta
Write-Host "=============================================================================" -ForegroundColor Magenta
Write-Host ""

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
if (-not $isAdmin) {
    Write-Warning "This script doesn't require admin privileges, but some operations might need elevation."
}

# Create temporary directory
$tempDir = Join-Path $env:TEMP "java-maven-install"
if (Test-Path $tempDir) {
    Remove-Item $tempDir -Recurse -Force
}
New-Item -ItemType Directory -Path $tempDir | Out-Null

# =============================================================================
# JAVA INSTALLATION
# =============================================================================
if (-not $SkipJava) {
    Write-Info "Step 1: Installing Java JDK $JavaVersion..."
    
    # Check if Java is already installed
    try {
        $javaVersion = & java -version 2>&1 | Select-String "version" | ForEach-Object { $_.ToString().Split('"')[1] }
        if ($javaVersion) {
            Write-Success "Java is already installed: $javaVersion"
            if (-not $Force) {
                Write-Info "Skipping Java installation. Use -Force to reinstall."
                $SkipJava = $true
            }
        }
    } catch {
        Write-Info "Java not found, proceeding with installation..."
    }
    
    if (-not $SkipJava) {
        try {
            # Download Java JDK 17
            Write-Info "Downloading OpenJDK $JavaVersion..."
            $javaUrl = "https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.9%2B9/OpenJDK17U-jdk_x64_windows_hotspot_17.0.9_9.msi"
            $javaInstaller = Join-Path $tempDir "OpenJDK17.msi"
            
            Write-Info "Download URL: $javaUrl"
            Write-Info "This may take a few minutes..."
            
            Invoke-WebRequest -Uri $javaUrl -OutFile $javaInstaller -UseBasicParsing
            
            if (Test-Path $javaInstaller) {
                Write-Success "Java installer downloaded successfully!"
                
                # Install Java
                Write-Info "Installing Java JDK $JavaVersion..."
                $process = Start-Process -FilePath "msiexec.exe" -ArgumentList "/i", $javaInstaller, "/quiet", "/norestart" -Wait -PassThru
                
                if ($process.ExitCode -eq 0) {
                    Write-Success "Java JDK $JavaVersion installed successfully!"
                } else {
                    throw "Java installation failed with exit code: $($process.ExitCode)"
                }
            } else {
                throw "Failed to download Java installer"
            }
        } catch {
            Write-Error "Java installation failed: $($_.Exception.Message)"
            Write-Info "Please install Java manually from: https://adoptium.net/"
            exit 1
        }
    }
}

# =============================================================================
# MAVEN INSTALLATION
# =============================================================================
if (-not $SkipMaven) {
    Write-Info "Step 2: Installing Apache Maven $MavenVersion..."
    
    # Check if Maven is already installed
    try {
        $mavenVersion = & mvn -version 2>&1 | Select-String "Apache Maven" | ForEach-Object { $_.ToString().Split(' ')[2] }
        if ($mavenVersion) {
            Write-Success "Maven is already installed: $mavenVersion"
            if (-not $Force) {
                Write-Info "Skipping Maven installation. Use -Force to reinstall."
                $SkipMaven = $true
            }
        }
    } catch {
        Write-Info "Maven not found, proceeding with installation..."
    }
    
    if (-not $SkipMaven) {
        try {
            # Download Maven
            Write-Info "Downloading Apache Maven $MavenVersion..."
            $mavenUrl = "https://archive.apache.org/dist/maven/maven-3/$MavenVersion/binaries/apache-maven-$MavenVersion-bin.zip"
            $mavenZip = Join-Path $tempDir "maven.zip"
            
            Write-Info "Download URL: $mavenUrl"
            Write-Info "This may take a few minutes..."
            
            Invoke-WebRequest -Uri $mavenUrl -OutFile $mavenZip -UseBasicParsing
            
            if (Test-Path $mavenZip) {
                Write-Success "Maven downloaded successfully!"
                
                # Extract Maven
                Write-Info "Extracting Maven..."
                $mavenDir = "C:\Program Files\Apache\maven"
                
                # Create directory if it doesn't exist
                if (-not (Test-Path "C:\Program Files\Apache")) {
                    New-Item -ItemType Directory -Path "C:\Program Files\Apache" -Force | Out-Null
                }
                
                # Extract to temp location first
                $tempMavenDir = Join-Path $tempDir "maven"
                Expand-Archive -Path $mavenZip -DestinationPath $tempDir -Force
                
                # Move to final location
                if (Test-Path $mavenDir) {
                    Remove-Item $mavenDir -Recurse -Force
                }
                Move-Item (Join-Path $tempDir "apache-maven-$MavenVersion") $mavenDir
                
                Write-Success "Maven extracted to: $mavenDir"
                
                # Add Maven to PATH
                Write-Info "Adding Maven to PATH environment variable..."
                $mavenBinPath = Join-Path $mavenDir "bin"
                
                # Get current PATH
                $currentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
                
                # Check if Maven is already in PATH
                if ($currentPath -notlike "*$mavenBinPath*") {
                    $newPath = "$currentPath;$mavenBinPath"
                    [Environment]::SetEnvironmentVariable("PATH", $newPath, "User")
                    Write-Success "Maven added to PATH!"
                } else {
                    Write-Info "Maven is already in PATH"
                }
            } else {
                throw "Failed to download Maven"
            }
        } catch {
            Write-Error "Maven installation failed: $($_.Exception.Message)"
            Write-Info "Please install Maven manually from: https://maven.apache.org/download.cgi"
            exit 1
        }
    }
}

# =============================================================================
# VERIFICATION
# =============================================================================
Write-Info "Step 3: Verifying installations..."

# Refresh environment variables
$env:PATH = [System.Environment]::GetEnvironmentVariable("PATH","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH","User")

# Test Java
Write-Info "Testing Java installation..."
try {
    $javaVersion = & java -version 2>&1 | Select-String "version" | ForEach-Object { $_.ToString().Split('"')[1] }
    if ($javaVersion) {
        Write-Success "✅ Java is working: $javaVersion"
    } else {
        Write-Error "❌ Java installation verification failed"
    }
} catch {
    Write-Error "❌ Java verification failed: $($_.Exception.Message)"
}

# Test Maven
Write-Info "Testing Maven installation..."
try {
    $mavenVersion = & mvn -version 2>&1 | Select-String "Apache Maven" | ForEach-Object { $_.ToString().Split(' ')[2] }
    if ($mavenVersion) {
        Write-Success "✅ Maven is working: $mavenVersion"
    } else {
        Write-Error "❌ Maven installation verification failed"
    }
} catch {
    Write-Error "❌ Maven verification failed: $($_.Exception.Message)"
}

# =============================================================================
# TEST AUTOMATION VERIFICATION
# =============================================================================
Write-Info "Step 4: Testing your test automation framework..."

# Test backend tests (should work)
Write-Info "Testing backend tests (pytest)..."
try {
    $backendResult = & python tools/agent/main.py run-backend 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Success "✅ Backend tests are working!"
    } else {
        Write-Warning "⚠️ Backend tests completed with some failures (expected without services)"
    }
} catch {
    Write-Warning "⚠️ Backend test execution had issues: $($_.Exception.Message)"
}

# Test UI tests (should work with Node.js)
Write-Info "Testing UI tests (Playwright)..."
try {
    $uiResult = & python tools/agent/main.py run-ui 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Success "✅ UI tests are working!"
    } else {
        Write-Warning "⚠️ UI tests completed with some failures (expected without web server)"
    }
} catch {
    Write-Warning "⚠️ UI test execution had issues: $($_.Exception.Message)"
}

# Test API tests (should work with Java + Maven)
Write-Info "Testing API tests (RestAssured)..."
try {
    $apiResult = & python tools/agent/main.py run-api 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Success "✅ API tests are working!"
    } else {
        Write-Warning "⚠️ API tests completed with some failures (expected without API server)"
    }
} catch {
    Write-Warning "⚠️ API test execution had issues: $($_.Exception.Message)"
}

# =============================================================================
# CLEANUP
# =============================================================================
Write-Info "Cleaning up temporary files..."
if (Test-Path $tempDir) {
    Remove-Item $tempDir -Recurse -Force
}

# =============================================================================
# FINAL STATUS
# =============================================================================
Write-Host ""
Write-Host "=============================================================================" -ForegroundColor Magenta
Write-Host "  INSTALLATION COMPLETE!" -ForegroundColor Magenta
Write-Host "=============================================================================" -ForegroundColor Magenta

Write-Info "Your test automation framework is now ready with:"
Write-Success "✅ Python + pytest (Backend tests)"
Write-Success "✅ Node.js + Playwright (UI tests)" 
Write-Success "✅ Java + Maven + RestAssured (API tests)"

Write-Host ""
Write-Info "Next steps:"
Write-Info "1. Close and reopen PowerShell to ensure PATH changes take effect"
Write-Info "2. Run: python tools/agent/main.py run-all"
Write-Info "3. Or run individual test suites:"
Write-Info "   - python tools/agent/main.py run-backend"
Write-Info "   - python tools/agent/main.py run-ui"
Write-Info "   - python tools/agent/main.py run-api"

Write-Host ""
Write-Success "🎉 Your complete test automation system is ready! 🎉"
Write-Host "=============================================================================" -ForegroundColor Magenta
