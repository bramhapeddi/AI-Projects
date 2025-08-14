@echo off
echo =============================================================================
echo   Java + Maven Automated Installation
echo   For Test Automation Framework
echo =============================================================================
echo.
echo This script will install Java JDK 17 and Apache Maven 3.9.6
echo.
echo Press any key to continue or Ctrl+C to cancel...
pause >nul

echo.
echo Starting installation...
echo.

powershell -ExecutionPolicy Bypass -File "%~dp0install-java-maven.ps1"

echo.
echo Installation script completed!
echo Please close and reopen PowerShell for PATH changes to take effect.
echo.
pause
