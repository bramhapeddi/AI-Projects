# 🚀 AI-Powered Test Automation Framework

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Node.js](https://img.shields.io/badge/Node.js-18+-green.svg)](https://nodejs.org)
[![Java](https://img.shields.io/badge/Java-17+-orange.svg)](https://adoptium.net)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)](https://github.com/yourusername/test-automation-framework)

> **An intelligent, agentic system that automatically plans, scaffolds, and runs complete test automation solutions for Web UI, API, and backend services.**

## 🌟 Features

- **🤖 Multi-Agent Architecture** - 8 specialized agents for different aspects of test automation
- **🔧 Multi-Language Support** - Python, TypeScript, and Java
- **🎯 Framework Agnostic** - Playwright, RestAssured, pytest, and more
- **📊 Comprehensive Reporting** - Allure, HTML, XML, and custom reports
- **🚀 CI/CD Ready** - Jenkins, Azure DevOps, AWS CodeBuild, Google Cloud Build
- **🌍 Cross-Platform** - Windows, Linux, macOS support
- **📱 Multi-Browser** - Chromium, Firefox, WebKit support
- **🔐 Environment Management** - Dev, QA, Stage, Production configurations
- **📈 Data-Driven Testing** - CSV, JSON, and custom data sources

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│   Requirements  │    │  Tech-Stack      │    │   Scaffolder     │
│   Ingestion     │───▶│  Planner         │───▶│  (Jinja2 +       │
│   Agent         │    │  (Rule Engine)   │    │   Generators)    │
└─────────────────┘    └──────────────────┘    └──────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│ Test Generator  │    │ CI/CD Writer     │    │ Runner &         │
│ (Gherkin/API)   │    │ (Jenkins/Azure)  │    │ Orchestrator     │
└─────────────────┘    └──────────────────┘    └──────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│ Data & Secrets  │    │ Env Config      │    │ Reporting        │
│ Manager         │    │ Manager          │    │ Adapter          │
└─────────────────┘    └──────────────────┘    └──────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** with pip
- **Node.js 18+** with npm
- **Java 17+** (OpenJDK recommended)
- **Git**

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/test-automation-framework.git
cd test-automation-framework
```

### 2. Install Dependencies

```bash
# Install Python dependencies
pip install -r tools/agent/requirements.txt

# Install Node.js dependencies (for UI tests)
cd ui/playwright
npm install
cd ../..

# Install Java dependencies (for API tests)
cd api/restassured
mvn dependency:resolve
cd ../..
```

### 3. Run the Framework

```bash
# List available agents
python tools/agent/main.py list-agents

# Scaffold the complete project
python tools/agent/main.py scaffold

# Generate tests from requirements
python tools/agent/main.py generate-tests

# Run all test suites
python tools/agent/main.py run-all
```

## 🎯 What You Get

After running the framework, you'll have:

```
test-automation-framework/
├── 📁 ui/playwright/          # TypeScript + Playwright UI tests
├── 📁 api/restassured/        # Java + RestAssured API tests  
├── 📁 backend/pytest/         # Python + pytest backend tests
├── 📁 ci/                     # CI/CD pipeline configurations
├── 📁 env/                    # Environment configurations
├── 📁 data/                   # Test data and fixtures
├── 📁 docs/                   # Documentation and examples
├── 📁 reports/                # Test execution reports
├── 📁 tools/agent/            # Core automation framework
└── 📁 specs/                  # API specifications
```

## 🤖 Available Agents

| Agent | Purpose | Command |
|-------|---------|---------|
| **planner** | Shows solution configuration | `python tools/agent/main.py plan` |
| **scaffolder** | Creates project structure | `python tools/agent/main.py scaffold` |
| **req2test_ui** | Generates UI tests from stories | `python tools/agent/main.py generate-tests` |
| **req2test_api** | Generates API tests from OpenAPI | `python tools/agent/main.py generate-tests` |
| **ci_writer** | Creates CI/CD pipelines | `python tools/agent/main.py scaffold` |
| **runner_ui** | Executes UI test automation | `python tools/agent/main.py run-ui` |
| **runner_api** | Runs API test automation | `python tools/agent/main.py run-api` |
| **runner_backend** | Executes backend tests | `python tools/agent/main.py run-backend` |

## ⚙️ Configuration

### Solution Configuration (`solution.yaml`)

```yaml
solution:
  name: my-test-automation
  description: Complete test automation solution
  languages:
    ui: typescript
    api: java
    backend: python
  ui:
    framework: playwright
    pattern: POM
    browsers: [chromium, firefox, webkit]
  api:
    framework: restassured
    inputs:
      openapi: specs/api.yaml
  backend:
    framework: pytest
    services: [db, queue]
  environments: [dev, qa, stage]
  cicd:
    providers: [jenkins, azure, aws, gcp]
  reporting:
    providers: [allure, playwright_html]
```

### Environment Configuration

```yaml
# env/config.dev.yaml
base_url: https://dev.example.com
api:
  base_url: https://dev-api.example.com
backend:
  db:
    uri: postgresql://user:pass@localhost:5432/dev_db
```

## 🧪 Test Types

### UI Tests (Playwright)
- **Page Object Model (POM)** implementation
- **Cross-browser testing** (Chromium, Firefox, WebKit)
- **Visual regression testing** support
- **Mobile responsive testing**

### API Tests (RestAssured)
- **OpenAPI specification** driven
- **Request/response validation**
- **Authentication flows**
- **Performance testing** integration

### Backend Tests (pytest)
- **Database integration** testing
- **Message queue** testing
- **Service health** checks
- **Integration testing** support

## 📊 Reporting & Analytics

- **Allure Reports** - Rich HTML reports with trends
- **Playwright HTML** - Interactive test results
- **JUnit XML** - CI/CD integration
- **Custom dashboards** - Metrics and KPIs

## 🔄 CI/CD Integration

### Jenkins Pipeline
```groovy
pipeline {
    agent any
    stages {
        stage('UI Tests') {
            steps {
                dir('ui/playwright') {
                    sh 'npm ci && npx playwright test'
                }
            }
        }
        stage('API Tests') {
            steps {
                dir('api/restassured') {
                    sh 'mvn test'
                }
            }
        }
        stage('Backend Tests') {
            steps {
                dir('backend/pytest') {
                    sh 'pytest --junitxml=report.xml'
                }
            }
        }
    }
}
```

### Azure DevOps
```yaml
trigger: [ main ]
pool: { vmImage: 'ubuntu-latest' }
stages:
- stage: Test
  jobs:
  - job: UI
    steps:
    - script: |
        cd ui/playwright
        npm ci
        npx playwright test
```

## 🚀 Advanced Features

### Test Data Management
- **CSV/JSON** data sources
- **Database** fixtures
- **API** mock data
- **Dynamic** test data generation

### Parallel Execution
- **Multi-threaded** test execution
- **Browser parallelization**
- **Test sharding** support
- **Resource optimization**

### Security & Compliance
- **Secret management** (Vault, AWS Secrets Manager)
- **Environment isolation**
- **Audit logging**
- **Compliance reporting**

## 📚 Documentation

- [Installation Guide](INSTALLATION-README.md)
- [API Reference](docs/api-reference.md)
- [Best Practices](docs/best-practices.md)
- [Troubleshooting](docs/troubleshooting.md)
- [Examples](docs/examples/)

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/test-automation-framework.git

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r tools/agent/requirements.txt
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Playwright** team for the excellent UI testing framework
- **RestAssured** community for Java API testing
- **pytest** team for Python testing framework
- **Allure** team for beautiful test reporting

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/test-automation-framework/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/test-automation-framework/discussions)
- **Wiki**: [Project Wiki](https://github.com/yourusername/test-automation-framework/wiki)

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/test-automation-framework&type=Date)](https://star-history.com/#yourusername/test-automation-framework&Date)

---

**Made with ❤️ by the Test Automation Community**

[![GitHub stars](https://img.shields.io/github/stars/yourusername/test-automation-framework?style=social)](https://github.com/yourusername/test-automation-framework)
[![GitHub forks](https://img.shields.io/github/forks/yourusername/test-automation-framework?style=social)](https://github.com/yourusername/test-automation-framework)
[![GitHub issues](https://img.shields.io/github/issues/yourusername/test-automation-framework)](https://github.com/yourusername/test-automation-framework)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/yourusername/test-automation-framework)](https://github.com/yourusername/test-automation-framework)
