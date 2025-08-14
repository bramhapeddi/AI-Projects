# acme-banking-qa Test Automation

Web + API + backend automation for Acme Banking

## 🚀 Overview

This repository contains a comprehensive test automation solution for acme-banking-qa, covering:

- **UI Testing**: Playwright with POM pattern
- **API Testing**: Restassured 
- **Backend Testing**: Pytest
- **CI/CD Integration**: jenkins, azure, aws, gcp
- **Reporting**: allure, playwright_html

## 🏗️ Architecture

```
acme-banking-qa/
├── ui/playwright/          # UI test automation
├── api/restassured/        # API test automation  
├── backend/pytest/ # Backend test automation
├── ci/                                 # CI/CD pipeline definitions
├── env/                                # Environment configurations
├── data/                               # Test data files
├── reports/                            # Test execution reports
├── tools/agent/                        # Test automation orchestrator
└── docs/                               # Documentation
```

## 🛠️ Technology Stack

| Layer | Technology | Version |
|-------|------------|---------|
| **UI** | Playwright | Latest |
| **API** | Restassured | Latest |
| **Backend** | Pytest | Latest |
| **Orchestrator** | Python + Typer | 3.8+ |
| **CI/CD** | jenkins, azure, aws, gcp | - |
| **Reporting** | allure, playwright_html | - |

## 📋 Prerequisites

### System Requirements
- **Node.js**: 18.0.0+
- **Java**: 11+
- **Python**: 3.8+
- **Git**: 2.0+

### Tools
- **npm/yarn**: For UI dependencies
- **Maven**: For API dependencies  
- **pip**: For Python dependencies
- **Docker**: Optional, for containerized execution

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone <repository-url>
cd acme-banking-qa
```

### 2. Install Dependencies

```bash
# Install Python orchestrator dependencies
pip install -r tools/agent/requirements.txt

# Or install the orchestrator package
pip install -e tools/agent/
```

### 3. Scaffold the Solution

```bash
# Generate the complete test automation solution
python tools/agent/main.py scaffold

# Or use the package
acme-banking-qa-test scaffold
```

### 4. Configure Environment

```bash
# Copy and customize environment configuration
cp env/config.dev.yaml env/config.local.yaml
# Edit env/config.local.yaml with your settings
```

### 5. Run Tests

```bash
# Run all test suites
python tools/agent/main.py run-all

# Run specific test suites
python tools/agent/main.py run-ui
python tools/agent/main.py run-api  
python tools/agent/main.py run-backend

# Run with custom configuration
python tools/agent/main.py run-ui --spec custom-solution.yaml
```

## 📚 Available Commands

```bash
# List all available agents
python tools/agent/main.py list-agents

# View the resolved plan
python tools/agent/main.py plan

# Scaffold the solution
python tools/agent/main.py scaffold

# Generate tests from requirements
python tools/agent/main.py generate-tests

# Run test suites
python tools/agent/main.py run-ui [--headed]
python tools/agent/main.py run-api
python tools/agent/main.py run-backend
python tools/agent/main.py run-all
```

## 🔧 Configuration

### Solution Configuration (`solution.yaml`)

The main configuration file that defines:
- Framework choices (Playwright, RestAssured, pytest)
- Language preferences (TypeScript, Java, Python)
- Test types and data strategies
- CI/CD providers and reporting options
- Quality settings (retries, parallelism)

### Environment Configuration

Environment-specific settings in `env/config.{env}.yaml`:
- Base URLs and endpoints
- Database and service connections
- Test data file paths
- Browser and platform configurations

### Environment Variables

Key environment variables:
```bash
# Base configuration
BASE_URL=https://your-app.com
TEST_ENV=qa

# Authentication
API_TOKEN=your-api-token
TEST_USERNAME=testuser
TEST_PASSWORD=testpass

# Database
DB_URI=postgresql://user:pass@host:port/db
REDIS_URI=redis://host:port

# Test execution
PARALLEL=true
WORKERS=4
HEADLESS=true
```

## 🧪 Test Structure

### UI Tests (Playwright)

```
ui/playwright/
├── src/pages/           # Page Object Models
├── tests/               # Test specifications
├── tests/utils/         # Test utilities and helpers
├── playwright.config.ts # Playwright configuration
└── package.json         # Dependencies
```

**Running UI Tests:**
```bash
cd ui/playwright
npm install
npx playwright install --with-deps
npx playwright test
```

### API Tests (Restassured)

```
api/restassured/
├── src/test/java/
│   ├── base/            # Base test classes
│   └── specs/           # Test specifications
├── pom.xml              # Maven configuration
└── src/test/resources/  # Test resources
```

**Running API Tests:**
```bash
cd api/restassured
mvn test
```

### Backend Tests (Pytest)

```
backend/pytest/
├── tests/               # Test modules
├── conftest.py          # Pytest configuration
├── pyproject.toml       # Project configuration
└── requirements.txt     # Dependencies
```

**Running Backend Tests:**
```bash
cd backend/pytest
pip install -r requirements.txt
python -m pytest
```

## 🔄 CI/CD Integration

### Jenkins

The `ci/Jenkinsfile` provides a comprehensive pipeline with:
- Parallel test execution
- Multiple browser support
- Artifact archiving
- HTML and Allure reporting
- Configurable parameters

### Azure Pipelines

The `ci/azure-pipelines.yaml` includes:
- Multi-stage pipeline
- Browser matrix testing
- Test result publishing
- Artifact management
- Deployment stages

### Other CI Providers

Templates are also available for:
- AWS CodeBuild (`ci/aws/buildspec.yml`)
- Google Cloud Build (`ci/gcp/cloudbuild.yaml`)

## 📊 Reporting

### Allure Reports

Comprehensive test reporting with:
- Test execution history
- Failure analysis
- Screenshots and videos
- Performance metrics
- Environment information

### HTML Reports

Quick-view reports for:
- Playwright test results
- pytest execution summary
- Test coverage information

### JUnit XML

Standard test results for:
- CI/CD integration
- Test result aggregation
- Build status reporting

## 🎯 Test Generation

### From User Stories

```bash
# Generate tests from markdown stories
python tools/agent/main.py generate-tests --stories docs/stories.md

# Generate tests from Gherkin features
python tools/agent/main.py generate-tests --features docs/features/
```

### From OpenAPI Specifications

```bash
# Generate API tests from OpenAPI spec
python tools/agent/main.py generate-tests --openapi specs/api.yaml
```

## 🚀 Advanced Usage

### Custom Test Data

```bash
# Add test data files
echo "username,password,role" > data/users.csv
echo "testuser,password,user" >> data/users.csv
echo "admin,admin123,admin" >> data/users.csv
```

### Parallel Execution

```bash
# Run tests with custom parallelism
python tools/agent/main.py run-ui --parallel --workers 8
```

### Environment-Specific Execution

```bash
# Run against specific environment
TEST_ENV=stage python tools/agent/main.py run-all
```

### Custom Configuration

```bash
# Use custom solution configuration
python tools/agent/main.py scaffold --spec custom-solution.yaml
```

## 🐛 Troubleshooting

### Common Issues

1. **Dependencies not found**
   ```bash
   # Reinstall dependencies
   python tools/agent/main.py scaffold
   ```

2. **Browser installation issues**
   ```bash
   cd ui/playwright
   npx playwright install --with-deps
   ```

3. **Database connection failures**
   - Check environment configuration
   - Verify database service is running
   - Check credentials and network access

4. **Test failures**
   - Review test logs and screenshots
   - Check application state
   - Verify test data availability

### Debug Mode

```bash
# Run with debug output
DEBUG=true python tools/agent/main.py run-ui

# Run specific test with debug
npx playwright test --debug
```

## 🤝 Contributing

### Development Setup

```bash
# Install development dependencies
pip install -r tools/agent/requirements-dev.txt

# Run linting
black tools/agent/
flake8 tools/agent/
mypy tools/agent/

# Run tests
python -m pytest tools/agent/tests/
```

### Adding New Frameworks

1. Create templates in `tools/agent/templates/`
2. Update the main orchestrator
3. Add framework-specific logic
4. Update documentation

### Adding New CI Providers

1. Create pipeline template
2. Update scaffold function
3. Test with sample configuration
4. Update documentation

## 📖 Documentation

- [User Stories](docs/stories.md) - Test requirements and scenarios
- [API Specifications](specs/) - OpenAPI definitions
- [Test Data](data/) - Sample test data files
- [CI/CD Guides](ci/) - Pipeline configuration details

## 📄 License

[Add your license information here]

## 🆘 Support

For questions and support:
- Create an issue in the repository
- Contact the QA team
- Check the troubleshooting guide above

---

**Happy Testing! 🧪✨**