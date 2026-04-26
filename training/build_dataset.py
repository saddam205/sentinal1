import os
import json
import pandas as pd
import numpy as np

OUTPUT_FILE = "./final_cyber_dataset.jsonl"

data = []

# ==============================
# FORMAT FUNCTION (IMPROVED)
# ==============================
def format_qa(q, a):
    return {
        "text": f"<|system|>\nYou are a cybersecurity expert.\n<|user|>\n{q}\n<|assistant|>\n{a}"
    }

# ==============================
# 1. CICIDS2017
# ==============================
print("🔹 Loading CICIDS2017...")

try:
    cicids = np.load("../data/cicids2017/train_data.npz")
    X = cicids["X"]
    y = cicids["y"]

    for i in range(min(2000, len(X))):
        label = int(y[i])

        q = "Analyze this network traffic sample. Is it malicious?"
        a = f"This network traffic is classified as class {label}. It may represent a cyber attack."

        data.append(format_qa(q, a))

except Exception as e:
    print("❌ CICIDS failed:", e)

# ==============================
# 2. SOREL
# ==============================
print("🔹 Loading SOREL...")

try:
    sorel_path = "../data/sorel/"
    for file in os.listdir(sorel_path):
        if file.endswith(".jsonl"):
            with open(os.path.join(sorel_path, file)) as f:
                for i, line in enumerate(f):
                    if i > 1000:
                        break
                    obj = json.loads(line)

                    score = obj.get("score", 0)

                    q = "Analyze this file behavior. Is it malicious?"
                    a = f"This file has a malware probability score of {score}."

                    data.append(format_qa(q, a))

except Exception as e:
    print("❌ SOREL failed:", e)

# ==============================
# 3. EMBER
# ==============================
print("🔹 Loading EMBER...")

try:
    with open("../data/ember/ember2018/ember_model_2018.txt") as f:
        lines = f.readlines()

    for line in lines[:1000]:
        q = "Explain malware detection using EMBER dataset"
        a = f"EMBER feature: {line.strip()[:100]}"

        data.append(format_qa(q, a))

except Exception as e:
    print("❌ EMBER failed:", e)

# ==============================
# 4. MITRE ATT&CK (AUTO DETECT)
# ==============================
print("🔹 Loading MITRE ATT&CK...")

try:
    mitre_file = None
    for f in os.listdir("../data"):
        if "enterprise-attack" in f:
            mitre_file = f
            break

    if mitre_file:
        path = os.path.join("../data", mitre_file)

        if mitre_file.endswith(".csv"):
            df = pd.read_csv(path)
        else:
            df = pd.read_excel(path)

        for i, row in df.iterrows():
            q = f"What is technique {row.get('ID', '')}?"
            a = f"{row.get('Name', '')}: {row.get('Description', '')}"

            data.append(format_qa(q, a))

            if i > 1000:
                break
    else:
        print("⚠️ MITRE file not found")

except Exception as e:
    print("❌ MITRE failed:", e)

# ==============================
# SAVE
# ==============================
print(f"\n✅ Total samples: {len(data)}")

os.makedirs(os.path.dirname(OUTPUT_FILE) or ".", exist_ok=True)

with open(OUTPUT_FILE, "w") as f:
    for item in data:
        f.write(json.dumps(item) + "\n")

print(f"📁 Saved → {OUTPUT_FILE}")