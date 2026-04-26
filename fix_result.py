import shutil
import re
import os

FRONTEND_FILE = "templates/dashboard.html"  # change if needed
BACKUP_FILE = "dashboard_before_scan_fix.html"

print("🧠 Fixing Neural Scan Button...")

# =========================
# BACKUP
# =========================
if not os.path.exists(FRONTEND_FILE):
    print("❌ File not found:", FRONTEND_FILE)
    exit()

shutil.copy(FRONTEND_FILE, BACKUP_FILE)
print(f"✅ Backup created: {BACKUP_FILE}")

with open(FRONTEND_FILE, "r", encoding="utf-8") as f:
    html = f.read()

# =========================
# REMOVE BROKEN JS
# =========================
print("🧹 Removing broken JS...")

# Remove ALL old scanBtn listeners
html = re.sub(
    r"scanBtn\.addEventListener\(.*?\}\);",
    "",
    html,
    flags=re.DOTALL
)

# Remove wrong endpoints
html = re.sub(r"/api/scan/url", "", html)

# =========================
# ADD CLEAN HTML (if missing)
# =========================
print("🔧 Ensuring UI elements...")

if "id=\"scan-btn\"" not in html:
    html += """
<!-- ========================= -->
<!-- 🧠 NEURAL SCAN UI -->
<!-- ========================= -->
<input id="target-input" placeholder="Enter target (127.0.0.1)">
<button id="scan-btn">🧠 Start Neural Scan</button>
<div id="results-display"></div>
"""

# =========================
# ADD CLEAN JS
# =========================
print("⚡ Injecting working JS...")

js_block = """
<script>
document.addEventListener("DOMContentLoaded", () => {

    const scanBtn = document.getElementById("scan-btn");
    const display = document.getElementById("results-display");
    const targetInput = document.getElementById("target-input");

    if (!scanBtn) {
        console.error("❌ scan-btn not found");
        return;
    }

    scanBtn.addEventListener("click", async () => {

        const target = targetInput?.value.trim() || "127.0.0.1";

        scanBtn.disabled = true;
        scanBtn.innerText = "⏳ Scanning...";
        display.innerHTML = "🚀 Starting scan...";

        try {
            const res = await fetch("/api/sentinel/scan", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ target })
            });

            const data = await res.json();
            console.log("SCAN RESULT:", data);

            if (!data.success) {
                display.innerHTML = "❌ Error: " + data.error;
            } else {
                display.innerHTML = `
                    <h3>Target: ${data.target}</h3>
                    <p>Risk: ${data.risk}</p>
                    <p>Open Ports: ${data.open_ports.join(", ")}</p>
                `;
            }

        } catch (err) {
            console.error(err);
            display.innerHTML = "❌ Scan failed";
        }

        scanBtn.disabled = false;
        scanBtn.innerText = "🧠 Start Neural Scan";
    });

});
</script>
"""

# Remove old <script> blocks related to scan (optional aggressive cleanup)
html = re.sub(r"<script>.*?scan.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE)

# Append clean JS
html += js_block

# =========================
# SAVE FILE
# =========================
with open(FRONTEND_FILE, "w", encoding="utf-8") as f:
    f.write(html)

print("✅ Neural Scan Button FIXED!")
print("👉 Restart server and refresh browser (Ctrl+F5)")