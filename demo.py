#!/usr/bin/env python3
"""
Demo script for the Acme Banking QA Test Automation System

This script demonstrates how to use the orchestrator to:
1. Scaffold the project structure
2. Generate tests from user stories and OpenAPI specs
3. Run the generated tests

Usage:
    python demo.py
"""

import subprocess
import sys
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run a command and return the result"""
    try:
        result = subprocess.run(
            cmd, 
            cwd=cwd, 
            shell=True, 
            capture_output=True, 
            text=True, 
            check=True
        )
        print(f"✅ Command successful: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
        if result.stdout:
            print(result.stdout)
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
        print(f"Error: {e.stderr}")
        return None

def main():
    """Main demo function"""
    print("🚀 Acme Banking QA Test Automation Demo")
    print("=" * 50)
    
    # Get the project root directory
    root = Path(__file__).parent
    agent_dir = root / "tools" / "agent"
    
    if not agent_dir.exists():
        print("❌ Agent directory not found. Please run this from the project root.")
        sys.exit(1)
    
    print(f"📁 Project root: {root}")
    print(f"🔧 Agent directory: {agent_dir}")
    
    # Step 1: List available agents
    print("\n1️⃣ Listing available agents...")
    run_command("python main.py list-agents", cwd=agent_dir)
    
    # Step 2: Plan the solution
    print("\n2️⃣ Planning the solution...")
    run_command("python main.py plan", cwd=agent_dir)
    
    # Step 3: Scaffold the project
    print("\n3️⃣ Scaffolding the project structure...")
    result = run_command("python main.py scaffold", cwd=agent_dir)
    if result is None:
        print("❌ Scaffolding failed. Exiting.")
        sys.exit(1)
    
    # Step 4: Generate tests from requirements
    print("\n4️⃣ Generating tests from user stories and OpenAPI specs...")
    result = run_command("python main.py generate-tests", cwd=agent_dir)
    if result is None:
        print("❌ Test generation failed. Exiting.")
        sys.exit(1)
    
    # Step 5: Show what was generated
    print("\n5️⃣ Generated project structure:")
    show_project_structure(root)
    
    print("\n🎉 Demo completed successfully!")
    print("\nNext steps:")
    print("1. Review the generated code in ui/, api/, and backend/ directories")
    print("2. Install dependencies: npm install (ui), mvn install (api), pip install -r requirements.txt (backend)")
    print("3. Run tests: python tools/agent/main.py run-ui")
    print("4. Check generated reports in the reports/ directory")

def show_project_structure(root, max_depth=3, current_depth=0):
    """Recursively show the project structure"""
    if current_depth > max_depth:
        return
    
    indent = "  " * current_depth
    
    for item in sorted(root.iterdir()):
        if item.name.startswith('.') or item.name in ['__pycache__', 'node_modules', 'target']:
            continue
            
        if item.is_dir():
            print(f"{indent}📁 {item.name}/")
            show_project_structure(item, max_depth, current_depth + 1)
        else:
            print(f"{indent}📄 {item.name}")

if __name__ == "__main__":
    main()
