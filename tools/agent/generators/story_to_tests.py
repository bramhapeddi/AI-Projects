"""
Story to Test Generator
Converts user stories and Gherkin scenarios into executable tests
"""

from pathlib import Path
import re
import typer
from .utils import jenv, slug, write, extract_test_type, extract_layer

GHERKIN_RE = re.compile(r"^(Feature:|Scenario:|Given |When |Then |And )", re.I)

def parse_stories_md(md: str):
    """Parse markdown stories file into structured blocks"""
    blocks, cur, mode = [], {"title": "", "gherkin": "", "labels": []}, None
    
    for line in md.splitlines():
        if line.startswith("### ") and "Story:" in line:
            if cur["gherkin"]:
                blocks.append(cur)
                cur = {"title": "", "gherkin": "", "labels": []}
            cur["title"] = line.split("Story:", 1)[1].strip()
        elif line.strip().lower().startswith("labels:"):
            cur["labels"] = [t.strip().lstrip("@") for t in line.split(":", 1)[1].split(",")]
        elif line.strip().lower().startswith("gherkin:"):
            mode = "gh"
            cur["gherkin"] = ""
            continue
        elif line.strip().startswith("```") and mode == "gh":
            mode = None
            continue
        elif mode == "gh":
            cur["gherkin"] += line + "\n"
    
    if cur["gherkin"]:
        blocks.append(cur)
    
    return blocks

def gherkin_to_playwright_steps(gherkin: str):
    """Convert Gherkin steps to Playwright code"""
    steps = []
    
    for raw in [l.strip() for l in gherkin.splitlines() if GHERKIN_RE.search(l)]:
        # Given I am on the login page
        if re.search(r"^Given I am on the login page$", raw, flags=re.I):
            steps.append("await page.goto(baseUrl + '/login');")
            continue
        
        # When I login as 'user'/'pass'
        m = re.match(r"^When I login as '(.+)'/'(.+)'$", raw, flags=re.I)
        if m:
            u, p = m.group(1), m.group(2)
            steps.append(f"await page.fill('#username', '{u}');")
            steps.append(f"await page.fill('#password', '{p}');")
            steps.append("await page.click('button[type=submit]');")
            continue
        
        # Then I should see the dashboard
        if re.search(r"^Then I should see the dashboard$", raw, flags=re.I):
            steps.append("await expect(page.getByText(/dashboard/i)).toBeVisible();")
            continue
        
        # Given I am logged in as 'user'
        m = re.match(r"^Given I am logged in as '(.+)'$", raw, flags=re.I)
        if m:
            user = m.group(1)
            steps.append(f"// Login as {user}")
            steps.append("await page.goto(baseUrl + '/login');")
            steps.append(f"await page.fill('#username', '{user}');")
            steps.append("await page.fill('#password', 'password');")
            steps.append("await page.click('button[type=submit]');")
            steps.append("await expect(page.getByText(/dashboard/i)).toBeVisible();")
            continue
        
        # When I click on 'element'
        m = re.match(r"^When I click on '(.+)'$", raw, flags=re.I)
        if m:
            element = m.group(1)
            steps.append(f"await page.click('text={element}');")
            continue
        
        # Then I should see 'text'
        m = re.match(r"^Then I should see '(.+)'$", raw, flags=re.I)
        if m:
            text = m.group(1)
            steps.append(f"await expect(page.getByText('{text}')).toBeVisible();")
            continue
        
        # When I fill 'field' with 'value'
        m = re.match(r"^When I fill '(.+)' with '(.+)'$", raw, flags=re.I)
        if m:
            field, value = m.group(1), m.group(2)
            steps.append(f"await page.fill('text={field}', '{value}');")
            continue
        
        # Default: add as comment for manual implementation
        steps.append(f"// TODO: Implement step: {raw}")
    
    return steps

def generate_from_stories(root: Path, sol: dict, stories_path: Path, features_dir: Path):
    """Generate tests from stories and features"""
    tpl = jenv(root / "tools" / "agent" / "templates")
    ui_out = root / "ui" / sol['ui']['framework'] / "tests"
    
    # 1) Markdown stories
    if stories_path.exists():
        typer.echo(f"Parsing stories from {stories_path}")
        blocks = parse_stories_md(stories_path.read_text(encoding="utf-8"))
        
        for b in blocks:
            if sol['ui']['framework'] == "playwright":
                steps = gherkin_to_playwright_steps(b["gherkin"])
                name = slug(b["title"]) or "story"
                
                spec = tpl.get_template("playwright/spec.spec.ts.j2").render(
                    name=name,
                    labels=b["labels"],
                    steps=steps,
                    base_url_var="process.env.BASE_URL",
                    test_type=extract_test_type(b["labels"]),
                    layer=extract_layer(b["labels"])
                )
                
                write(ui_out / f"{name}.spec.ts", spec)
                typer.echo(f"  Generated {name}.spec.ts")
    
    # 2) Raw .feature files
    if features_dir.exists():
        typer.echo(f"Parsing Gherkin features from {features_dir}")
        
        for feat in features_dir.glob("*.feature"):
            g = feat.read_text(encoding="utf-8")
            title = re.search(r"Feature:\s*(.+)", g)
            name = slug(title.group(1) if title else feat.stem)
            
            if sol['ui']['framework'] == "playwright":
                steps = gherkin_to_playwright_steps(g)
                
                spec = tpl.get_template("playwright/spec.spec.ts.j2").render(
                    name=name,
                    labels=["ui", "regression"],
                    steps=steps,
                    base_url_var="process.env.BASE_URL",
                    test_type="regression",
                    layer="ui"
                )
                
                write(ui_out / f"{name}.spec.ts", spec)
                typer.echo(f"  Generated {name}.spec.ts from {feat.name}")

if __name__ == "__main__":
    # For testing
    import typer
    typer.echo("Story to Test Generator")
