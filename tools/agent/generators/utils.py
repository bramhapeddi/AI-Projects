"""
Utility functions for test generators
"""

from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import re

def jenv(base: Path):
    """Get Jinja2 environment for templates"""
    return Environment(
        loader=FileSystemLoader(str(base)),
        trim_blocks=True,
        lstrip_blocks=True
    )

def slug(s: str):
    """Convert string to slug format for filenames"""
    return re.sub(r"[^a-z0-9_]+", "_", s.lower()).strip("_")

def write(path: Path, content: str):
    """Write content to file, creating directories as needed"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

def sanitize_filename(s: str):
    """Sanitize string for use as filename"""
    return re.sub(r"[^\w\-_\.]", "_", s)

def extract_test_type(labels: list) -> str:
    """Extract test type from labels"""
    test_types = ['smoke', 'regression', 'functional', 'e2e']
    for label in labels:
        if label.lower() in test_types:
            return label.lower()
    return 'functional'

def extract_layer(labels: list) -> str:
    """Extract test layer from labels"""
    layers = ['ui', 'api', 'backend', 'integration']
    for label in labels:
        if label.lower() in layers:
            return label.lower()
    return 'ui'
