#!/usr/bin/env python3
"""
Test Automation Agent - Main Orchestrator
Builds, scaffolds, and runs complete test automation solutions
"""

import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional

import typer
from pydantic import BaseModel
from ruamel.yaml import YAML
from jinja2 import Environment, FileSystemLoader

app = typer.Typer()
yaml = YAML()

# Agent Registry
AGENTS = {
    "planner": "main.py:plan",
    "scaffolder": "main.py:scaffold",
    "req2test_ui": "generators/story_to_tests.py:generate_from_stories",
    "req2test_api": "generators/openapi_to_tests.py:generate_from_openapi",
    "ci_writer": "main.py:scaffold (CI section)",
    "runner_ui": "main.py:run_ui",
    "runner_api": "main.py:run_api",
    "runner_backend": "main.py:run_backend",
}

class Solution(BaseModel):
    solution: dict

ROOT = Path(__file__).resolve().parents[2]

def write(path: Path, content: str):
    """Write content to file, creating directories as needed"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

def get_template_env():
    """Get Jinja2 template environment"""
    template_dir = Path(__file__).parent / "templates"
    return Environment(
        loader=FileSystemLoader(str(template_dir)),
        trim_blocks=True,
        lstrip_blocks=True
    )

@app.command()
def list_agents():
    """Print registered agents and their entrypoints."""
    typer.echo("Available Agents:")
    typer.echo("=" * 50)
    for key, val in AGENTS.items():
        typer.echo(f"{key:14} -> {val}")

@app.command()
def plan(spec: str = "solution.yaml"):
    """Display the resolved plan from solution.yaml"""
    spec_path = ROOT / spec
    if not spec_path.exists():
        typer.echo(f"Error: {spec} not found", err=True)
        raise typer.Exit(1)
    
    data = yaml.load(spec_path.read_text())
    s = Solution(**data)
    typer.echo(json.dumps({"plan": s.solution}, indent=2))

@app.command()
def scaffold(spec: str = "solution.yaml"):
    """Scaffold the complete test automation solution"""
    spec_path = ROOT / spec
    if not spec_path.exists():
        typer.echo(f"Error: {spec} not found", err=True)
        raise typer.Exit(1)
    
    data = yaml.load(spec_path.read_text())
    s = Solution(**data)
    tpl = get_template_env()
    
    typer.echo("Scaffolding test automation solution...")
    
    # UI Framework
    if s.solution['ui']['framework'] == 'playwright':
        typer.echo("Scaffolding Playwright UI tests...")
        ui_dir = ROOT / "ui" / "playwright"
        
        # Core Playwright files
        files_to_create = [
            ("package.json", "playwright/package.json.j2"),
            ("playwright.config.ts", "playwright/playwright.config.ts.j2"),
            ("src/pages/LoginPage.ts", "playwright/LoginPage.ts.j2"),
            ("src/pages/DashboardPage.ts", "playwright/DashboardPage.ts.j2"),
            ("tests/login.spec.ts", "playwright/login.spec.ts.j2"),
            ("tests/smoke.spec.ts", "playwright/smoke.spec.ts.j2"),
            ("tests/utils/data.ts", "playwright/data.ts.j2"),
            ("tsconfig.json", "playwright/tsconfig.json.j2"),
        ]
        
        for file_path, template_name in files_to_create:
            try:
                template = tpl.get_template(template_name)
                content = template.render(sol=s.solution)
                write(ui_dir / file_path, content)
            except Exception as e:
                typer.echo(f"Warning: Could not create {file_path}: {e}")
    
    # API Framework
    if s.solution['api']['framework'] == 'restassured':
        typer.echo("Scaffolding RestAssured API tests...")
        api_dir = ROOT / "api" / "restassured"
        
        files_to_create = [
            ("pom.xml", "restassured/pom.xml.j2"),
            ("src/test/java/base/ApiTest.java", "restassured/ApiTest.java.j2"),
            ("src/test/java/specs/GeneratedTests.java", "restassured/GeneratedTests.java.j2"),
            ("src/test/resources/application.properties", "restassured/application.properties.j2"),
        ]
        
        for file_path, template_name in files_to_create:
            try:
                template = tpl.get_template(template_name)
                content = template.render(sol=s.solution)
                write(api_dir / file_path, content)
            except Exception as e:
                typer.echo(f"Warning: Could not create {file_path}: {e}")
    
    # Backend Framework
    if s.solution['backend']['framework'] == 'pytest':
        typer.echo("Scaffolding pytest backend tests...")
        backend_dir = ROOT / "backend" / "pytest"
        
        files_to_create = [
            ("pyproject.toml", "pytest/pyproject.toml.j2"),
            ("conftest.py", "pytest/conftest.py.j2"),
            ("tests/test_health.py", "pytest/test_health.py.j2"),
            ("tests/test_database.py", "pytest/test_database.py.j2"),
            ("requirements.txt", "pytest/requirements.txt.j2"),
        ]
        
        for file_path, template_name in files_to_create:
            try:
                template = tpl.get_template(template_name)
                content = template.render(sol=s.solution)
                write(backend_dir / file_path, content)
            except Exception as e:
                typer.echo(f"Warning: Could not create {file_path}: {e}")
    
    # CI/CD Files
    typer.echo("Scaffolding CI/CD pipelines...")
    ci_dir = ROOT / "ci"
    
    cicd_files = [
        ("Jenkinsfile", "ci/Jenkinsfile.j2"),
        ("azure-pipelines.yaml", "ci/azure-pipelines.yaml.j2"),
        ("aws/buildspec.yml", "ci/aws/buildspec.yml.j2"),
        ("gcp/cloudbuild.yaml", "ci/gcp/cloudbuild.yaml.j2"),
    ]
    
    for file_path, template_name in cicd_files:
        try:
            template = tpl.get_template(template_name)
            content = template.render(sol=s.solution)
            write(ci_dir / file_path, content)
        except Exception as e:
            typer.echo(f"Warning: Could not create {file_path}: {e}")
    
    # Environment configs
    typer.echo("Scaffolding environment configurations...")
    env_dir = ROOT / "env"
    
    for env in s.solution.get('environments', ['dev', 'qa', 'stage']):
        config_file = f"config.{env}.yaml"
        try:
            template = tpl.get_template("env/config.yaml.j2")
            content = template.render(sol=s.solution, environment=env)
            write(env_dir / config_file, content)
        except Exception as e:
            typer.echo(f"Warning: Could not create {config_file}: {e}")
    
    # Documentation
    typer.echo("Scaffolding documentation...")
    docs_dir = ROOT / "docs"
    
    try:
        template = tpl.get_template("docs/README.md.j2")
        content = template.render(sol=s.solution)
        write(docs_dir / "README.md", content)
    except Exception as e:
        typer.echo(f"Warning: Could not create README.md: {e}")
    
    typer.echo("Scaffold complete!")

@app.command()
def generate_tests(
    spec: str = "solution.yaml",
    stories: str = "docs/stories.md",
    features: str = "docs/features",
    openapi: str = "specs/api.yaml",
):
    """Generate tests from requirements (stories/Gherkin/OpenAPI)"""
    try:
        from generators.story_to_tests import generate_from_stories
        from generators.openapi_to_tests import generate_from_openapi
        
        spec_path = ROOT / spec
        if not spec_path.exists():
            typer.echo(f"Error: {spec} not found", err=True)
            raise typer.Exit(1)
        
        data = yaml.load(spec_path.read_text())
        s = Solution(**data)
        
        typer.echo("Generating tests from requirements...")
        
        # Generate UI tests from stories
        stories_path = ROOT / stories
        features_dir = ROOT / features
        if stories_path.exists() or features_dir.exists():
            generate_from_stories(
                root=ROOT,
                sol=s.solution,
                stories_path=stories_path,
                features_dir=features_dir
            )
        
        # Generate API tests from OpenAPI
        openapi_path = ROOT / openapi
        if openapi_path.exists():
            generate_from_openapi(
                root=ROOT,
                sol=s.solution,
                openapi_path=openapi_path
            )
        
        typer.echo("Test generation complete!")
        
    except ImportError as e:
        typer.echo(f"Error: Could not import generators: {e}", err=True)
        typer.echo("Make sure to run 'scaffold' first to create the generator modules.")
        raise typer.Exit(1)

@app.command()
def run_ui(headed: bool = False, spec: str = "solution.yaml"):
    """Run UI tests"""
    spec_path = ROOT / spec
    if not spec_path.exists():
        typer.echo(f"Error: {spec} not found", err=True)
        raise typer.Exit(1)
    
    data = yaml.load(spec_path.read_text())
    s = Solution(**data)
    
    ui_dir = ROOT / "ui" / s.solution['ui']['framework']
    if not ui_dir.exists():
        typer.echo(f"Error: UI directory {ui_dir} not found. Run 'scaffold' first.", err=True)
        raise typer.Exit(1)
    
    typer.echo("Running UI tests...")
    
    try:
        # Install dependencies
        subprocess.check_call(["npm", "install"], cwd=ui_dir)
        subprocess.check_call(["npx", "playwright", "install", "--with-deps"], cwd=ui_dir)
        
        # Run tests
        cmd = ["npx", "playwright", "test"]
        if headed:
            cmd.append("--headed")
        
        subprocess.check_call(cmd, cwd=ui_dir)
        typer.echo("UI tests completed successfully!")
        
    except subprocess.CalledProcessError as e:
        typer.echo(f"UI tests failed: {e}", err=True)
        raise typer.Exit(1)

@app.command()
def run_api(spec: str = "solution.yaml"):
    """Run API tests"""
    spec_path = ROOT / spec
    if not spec_path.exists():
        typer.echo(f"Error: {spec} not found", err=True)
        raise typer.Exit(1)
    
    data = yaml.load(spec_path.read_text())
    s = Solution(**data)
    
    api_dir = ROOT / "api" / s.solution['api']['framework']
    if not api_dir.exists():
        typer.echo(f"Error: API directory {api_dir} not found. Run 'scaffold' first.", err=True)
        raise typer.Exit(1)
    
    typer.echo("Running API tests...")
    
    try:
        subprocess.check_call(["mvn", "-B", "test"], cwd=api_dir)
        typer.echo("API tests completed successfully!")
        
    except subprocess.CalledProcessError as e:
        typer.echo(f"API tests failed: {e}", err=True)
        raise typer.Exit(1)

@app.command()
def run_backend(spec: str = "solution.yaml"):
    """Run backend tests"""
    spec_path = ROOT / spec
    if not spec_path.exists():
        typer.echo(f"Error: {spec} not found", err=True)
        raise typer.Exit(1)
    
    data = yaml.load(spec_path.read_text())
    s = Solution(**data)
    
    backend_dir = ROOT / "backend" / s.solution['backend']['framework']
    if not backend_dir.exists():
        typer.echo(f"Error: Backend directory {backend_dir} not found. Run 'scaffold' first.", err=True)
        raise typer.Exit(1)
    
    typer.echo("Running backend tests...")
    
    try:
        subprocess.check_call(["pip", "install", "-r", "requirements.txt"], cwd=backend_dir)
        subprocess.check_call(["python", "-m", "pytest", "-v"], cwd=backend_dir)
        typer.echo("Backend tests completed successfully!")
        
    except subprocess.CalledProcessError as e:
        typer.echo(f"Backend tests failed: {e}", err=True)
        raise typer.Exit(1)

@app.command()
def run_all(spec: str = "solution.yaml"):
    """Run all test suites"""
    typer.echo("Running all test suites...")
    
    try:
        run_ui(spec=spec)
        run_api(spec=spec)
        run_backend(spec=spec)
        typer.echo("All test suites completed successfully!")
        
    except typer.Exit:
        typer.echo("Some test suites failed. Check the output above.", err=True)
        raise

if __name__ == "__main__":
    app()
