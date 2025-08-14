# Java + Maven Installation Guide

This guide will help you install Java JDK 17 and Apache Maven 3.9.6 to run all test types in your test automation framework.

## 🚀 Quick Installation

### Option 1: Double-Click Installation (Easiest)
1. **Double-click** `install-java-maven.bat`
2. **Press any key** when prompted
3. **Wait** for the installation to complete
4. **Close and reopen** PowerShell

### Option 2: PowerShell Script
1. **Right-click** `install-java-maven.ps1`
2. **Select** "Run with PowerShell"
3. **Wait** for the installation to complete
4. **Close and reopen** PowerShell

### Option 3: Manual PowerShell
```powershell
# Run the script directly
.\install-java-maven.ps1

# Or with specific options
.\install-java-maven.ps1 -Force  # Force reinstall
.\install-java-maven.ps1 -SkipJava  # Skip Java installation
.\install-java-maven.ps1 -SkipMaven  # Skip Maven installation
```

## 📋 What the Script Does

### 1. **Java JDK 17 Installation**
- Downloads OpenJDK 17 (LTS) from Eclipse Temurin
- Installs silently using MSI installer
- Automatically adds to PATH

### 2. **Apache Maven 3.9.6 Installation**
- Downloads Maven 3.9.6 from Apache archives
- Extracts to `C:\Program Files\Apache\maven`
- Adds Maven bin directory to PATH

### 3. **Verification & Testing**
- Tests Java installation
- Tests Maven installation
- Tests your test automation framework
- Runs sample tests to verify everything works

## 🔧 Script Options

| Parameter | Description | Example |
|-----------|-------------|---------|
| `-SkipJava` | Skip Java installation | `.\install-java-maven.ps1 -SkipJava` |
| `-SkipMaven` | Skip Maven installation | `.\install-java-maven.ps1 -SkipMaven` |
| `-Force` | Force reinstall existing tools | `.\install-java-maven.ps1 -Force` |
| `-JavaVersion` | Specify Java version | `.\install-java-maven.ps1 -JavaVersion "17"` |
| `-MavenVersion` | Specify Maven version | `.\install-java-maven.ps1 -MavenVersion "3.9.6"` |

## 📁 Installation Locations

- **Java**: `C:\Program Files\Eclipse Adoptium\jdk-17.x.x.x-hotspot`
- **Maven**: `C:\Program Files\Apache\maven`
- **Temporary files**: `%TEMP%\java-maven-install`

## ✅ Verification Commands

After installation, verify everything works:

```powershell
# Check Java
java --version

# Check Maven
mvn --version

# Test your framework
python tools/agent/main.py list-agents
python tools/agent/main.py run-backend
python tools/agent/main.py run-ui
python tools/agent/main.py run-api
```

## 🚨 Troubleshooting

### **Java Issues**
- **"java not recognized"**: Restart PowerShell after installation
- **Installation fails**: Check if you have admin privileges
- **PATH issues**: Manually add Java to PATH environment variable

### **Maven Issues**
- **"mvn not recognized"**: Restart PowerShell after installation
- **Download fails**: Check internet connection, try manual download
- **Extraction fails**: Ensure you have write permissions to `C:\Program Files\Apache`

### **General Issues**
- **Execution policy error**: Run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
- **Permission denied**: Run PowerShell as Administrator
- **Download timeout**: Check firewall/antivirus settings

## 🔄 Manual Installation (If Script Fails)

### **Java Manual Installation**
1. Download from [adoptium.net](https://adoptium.net/)
2. Run installer as Administrator
3. Add to PATH: `C:\Program Files\Eclipse Adoptium\jdk-17.x.x.x-hotspot\bin`

### **Maven Manual Installation**
1. Download from [maven.apache.org](https://maven.apache.org/download.cgi)
2. Extract to `C:\Program Files\Apache\maven`
3. Add to PATH: `C:\Program Files\Apache\maven\bin`

## 🎯 Expected Results

After successful installation:

✅ **Java JDK 17** working  
✅ **Apache Maven 3.9.6** working  
✅ **Backend tests** (pytest) working  
✅ **UI tests** (Playwright) working  
✅ **API tests** (RestAssured) working  

## 🚀 Next Steps

1. **Run all tests**: `python tools/agent/main.py run-all`
2. **Explore agents**: `python tools/agent/main.py list-agents`
3. **Generate tests**: `python tools/agent/main.py generate-tests`
4. **Customize configuration**: Edit `solution.yaml`

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify your system meets requirements (Windows 10/11, PowerShell 5.1+)
3. Check Windows Event Viewer for installation errors
4. Try running the script as Administrator

---

**🎉 Congratulations!** Once Java and Maven are installed, you'll have a complete, professional-grade test automation framework running on your machine!
