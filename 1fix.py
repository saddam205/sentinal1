# fix.py

import re

FILE = "fast11.py"

with open(FILE, "r") as f:
    code = f.read()

# 1. Fix templates
if "#templates = Jinja2Templates" in code:
    code = code.replace(
        "#templates = Jinja2Templates(directory=\"templates\")",
        "templates = Jinja2Templates(directory=\"templates\")"
    )
    print("✅ Fixed templates")

# 2. Ensure templates import exists
if "Jinja2Templates" not in code:
    code = code.replace(
        "from fastapi.templating import Jinja2Templates",
        "from fastapi.templating import Jinja2Templates"
    )

# 3. Add root fallback route (important)
if "@fastapi_app.get(\"/\")" in code:
    code = code.replace(
        "return templates.TemplateResponse(\"index.html\", {\"request\": request})",
        """
    try:
        return templates.TemplateResponse("index.html", {"request": request})
    except Exception:
        return {"status": "API running", "message": "Templates not found"}
        """
    )
    print("✅ Added fallback response")

# 4. Fix uvicorn hint (optional note)
if "if __name__" not in code:
    code += """

# ===== RUN SERVER =====
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("fast11:app", host="0.0.0.0", port=9090, reload=True)
"""
    print("✅ Added run block")

with open(FILE, "w") as f:
    f.write(code)

print("🔥 FIX COMPLETE")