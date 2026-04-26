import pandas as pd
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import os

# ==============================
# CONFIG
# ==============================
EXCEL_FILE = "data/enterprise-attack-v18.1-analytics.xlsx"
INDEX_FILE = "mitre_index.faiss"
TEXT_FILE = "mitre_texts.json"

# Load model once
model = SentenceTransformer("all-MiniLM-L6-v2")


# ==============================
# BUILD RAG
# ==============================
def build_rag():
    print("📊 Reading MITRE Excel...")

    if not os.path.exists(EXCEL_FILE):
        raise FileNotFoundError(f"❌ Excel file not found: {EXCEL_FILE}")

    df = pd.read_excel(EXCEL_FILE)

    # Convert rows → text
    texts = []
    for _, row in df.iterrows():
        text = " ".join([str(x) for x in row.values if pd.notna(x)])
        texts.append(text)

    print(f"🧠 Encoding {len(texts)} entries...")

    # 🔥 SAFE encoding for FAISS
    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        convert_to_numpy=True
    )

    # 🔥 CRITICAL FIX (FAISS requirement)
    embeddings = np.array(embeddings).astype("float32")

    # Create FAISS index
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)

    index.add(embeddings)

    # Save index
    faiss.write_index(index, INDEX_FILE)

    # Save texts
    with open(TEXT_FILE, "w") as f:
        json.dump(texts, f)

    print("🔥 RAG built successfully!")


# ==============================
# LOAD RAG
# ==============================
def load_rag():
    if not os.path.exists(INDEX_FILE) or not os.path.exists(TEXT_FILE):
        print("⚠ No index found. Building RAG...")
        build_rag()

    index = faiss.read_index(INDEX_FILE)

    with open(TEXT_FILE, "r") as f:
        texts = json.load(f)

    print(f"🔥 RAG loaded with {len(texts)} entries")

    return index, texts


# ==============================
# SEARCH
# ==============================
def search_rag(query, index, texts, k=3):
    if not query:
        return []

    # Encode query
    query_vec = model.encode(
        [query],
        convert_to_numpy=True
    )

    # 🔥 FIX for FAISS
    query_vec = np.array(query_vec).astype("float32")

    distances, indices = index.search(query_vec, k)

    results = []
    for i in indices[0]:
        if 0 <= i < len(texts):
            results.append(texts[i])

    return results


# ==============================
# TEST (optional)
# ==============================
if __name__ == "__main__":
    index, texts = load_rag()

    query = "privilege escalation attack"
    results = search_rag(query, index, texts)

    print("\n🔍 Results:")
    for r in results:
        print("-", r[:200])