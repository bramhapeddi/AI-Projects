"""
OpenAPI to Test Generator
Converts OpenAPI specifications into executable API tests
"""

from pathlib import Path
import yaml
from .utils import jenv, write, slug

DEFAULT_STATUS_CODES = {
    "get": 200,
    "post": 201,
    "put": 200,
    "patch": 200,
    "delete": 204,
    "head": 200,
    "options": 200
}

def generate_from_openapi(root: Path, sol: dict, openapi_path: Path):
    """Generate API tests from OpenAPI specification"""
    try:
        spec = yaml.safe_load(openapi_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"Error loading OpenAPI spec: {e}")
        return
    
    tpl = jenv(root / "tools" / "agent" / "templates")
    
    if sol["api"]["framework"] == "restassured":
        out = root / "api" / sol["api"]["framework"] / "src" / "test" / "java" / "specs"
        
        # Generate tests for each path and operation
        paths = spec.get("paths", {})
        for path, operations in paths.items():
            for method, operation in operations.items():
                if method.lower() in DEFAULT_STATUS_CODES:
                    op_id = operation.get("operationId") or f"{method}_{slug(path)}"
                    responses = operation.get("responses", {})
                    
                    # Get expected status code
                    status = next(iter(responses.keys()), str(DEFAULT_STATUS_CODES.get(method.lower(), 200)))
                    
                    # Get request body if POST/PUT/PATCH
                    has_body = method.lower() in ["post", "put", "patch"]
                    body_schema = None
                    if has_body and "requestBody" in operation:
                        body_schema = operation["requestBody"].get("content", {}).get("application/json", {}).get("schema")
                    
                    # Get parameters
                    parameters = operation.get("parameters", [])
                    query_params = [p for p in parameters if p.get("in") == "query"]
                    path_params = [p for p in parameters if p.get("in") == "path"]
                    
                    # Generate test class
                    java = tpl.get_template("restassured/OperationTest.java.j2").render(
                        sol=sol,
                        class_name=f"{slug(op_id).title().replace('_', '')}Test",
                        method=method.upper(),
                        path=path,
                        expected_status=str(status),
                        operation_id=op_id,
                        summary=operation.get("summary", ""),
                        has_body=has_body,
                        body_schema=body_schema,
                        query_params=query_params,
                        path_params=path_params,
                        tags=operation.get("tags", [])
                    )
                    
                    filename = f"{slug(op_id).title().replace('_', '')}Test.java"
                    write(out / filename, java)
                    print(f"  Generated {filename}")
    
    elif sol["api"]["framework"] == "playwright_api":
        out = root / "api" / sol["api"]["framework"] / "tests"
        
        # Generate Playwright API tests
        paths = spec.get("paths", {})
        for path, operations in paths.items():
            for method, operation in operations.items():
                if method.lower() in DEFAULT_STATUS_CODES:
                    op_id = operation.get("operationId") or f"{method}_{slug(path)}"
                    responses = operation.get("responses", {})
                    status = next(iter(responses.keys()), str(DEFAULT_STATUS_CODES.get(method.lower(), 200)))
                    
                    ts_test = tpl.get_template("playwright_api/api.spec.ts.j2").render(
                        test_name=slug(op_id),
                        method=method.upper(),
                        path=path,
                        expected_status=int(status),
                        operation_id=op_id,
                        summary=operation.get("summary", "")
                    )
                    
                    filename = f"{slug(op_id)}.spec.ts"
                    write(out / filename, ts_test)
                    print(f"  Generated {filename}")

def generate_test_data_from_schemas(root: Path, sol: dict, openapi_path: Path):
    """Generate test data from OpenAPI schemas"""
    try:
        spec = yaml.safe_load(openapi_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"Error loading OpenAPI spec: {e}")
        return
    
    schemas = spec.get("components", {}).get("schemas", {})
    if not schemas:
        return
    
    # Generate test data files
    data_dir = root / "data"
    data_dir.mkdir(exist_ok=True)
    
    for schema_name, schema in schemas.items():
        if schema.get("type") == "object":
            properties = schema.get("properties", {})
            test_data = {}
            
            for prop_name, prop_schema in properties.items():
                prop_type = prop_schema.get("type", "string")
                
                # Generate sample data based on type
                if prop_type == "string":
                    if "email" in prop_name.lower():
                        test_data[prop_name] = "test@example.com"
                    elif "password" in prop_name.lower():
                        test_data[prop_name] = "password123"
                    elif "name" in prop_name.lower():
                        test_data[prop_name] = "Test User"
                    else:
                        test_data[prop_name] = f"test_{prop_name}"
                elif prop_type == "integer":
                    test_data[prop_name] = 123
                elif prop_type == "number":
                    test_data[prop_name] = 123.45
                elif prop_type == "boolean":
                    test_data[prop_name] = True
                elif prop_type == "array":
                    test_data[prop_name] = []
            
            # Write test data file
            import json
            data_file = data_dir / f"{schema_name.lower()}_test_data.json"
            with open(data_file, 'w') as f:
                json.dump(test_data, f, indent=2)
            
            print(f"  Generated test data: {data_file}")

if __name__ == "__main__":
    print("OpenAPI to Test Generator")
