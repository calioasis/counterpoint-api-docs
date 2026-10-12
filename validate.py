import json, pathlib, re
root = pathlib.Path(__file__).parent
spec = json.loads((root / "openapi.json").read_text())
assert spec["openapi"] == "3.1.0"
assert spec["info"]["version"] and spec["servers"]
assert {"/v1/health", "/v1/events", "/v1/tasks"} <= set(spec["paths"])
seen = set()
def visit(value):
    if isinstance(value, dict):
        if "$ref" in value:
            ref = value["$ref"]
            assert ref.startswith("#/"), "External schema reference requires review"
            target = spec
            for part in ref[2:].split("/"):
                target = target[part.replace("~1", "/").replace("~0", "~")]
        for item in value.values(): visit(item)
    elif isinstance(value, list):
        for item in value: visit(item)
visit(spec)
for path, item in spec["paths"].items():
    for method, op in item.items():
        if method not in ("get", "post"): continue
        assert op["operationId"] not in seen
        seen.add(op["operationId"])
        assert op["responses"] and op["tags"]
for name in ("index.html", "reference.html", "quickstart.template.html", "quickstart.js", "site.js", "site.css", "changelog.html", "vendor/redoc-2.5.4.standalone.js", "vendor/LICENSE.redoc"):
    assert (root / name).is_file(), name
for name in ("openapi.json", "index.html", "reference.html", "quickstart.template.html", "quickstart.js", "site.js", "site.css", "changelog.html", "README.md"):
    content = (root / name).read_text()
    assert not re.search(r"cp_sf_(?:test|production)_[A-Za-z0-9_-]{20,}|onetimesecret\.com/secret/|-----BEGIN .*PRIVATE KEY", content), "Credential material in " + name
print("Documentation checks passed: JSON, local references, operation IDs, assets, and credential-pattern scan.")
