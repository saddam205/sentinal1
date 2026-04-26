import json
import numpy as np
import joblib
import logging
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer

from sentence_transformers import SentenceTransformer
import lightgbm as lgb

# ----------------------------
# Config
# ----------------------------
DATA_DIR = Path("../data/sorel")
MODEL_PATH = Path("../models/sorel.pkl")

MAX_SAMPLES = 100000
PCA_COMPONENTS = 128
TFIDF_FEATURES = 5000   # 🔥 tune (3000–10000)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ----------------------------
# Load Data
# ----------------------------
def load_sorel_data(max_samples=100000):
    texts, labels = [], []
    total = 0

    for file in DATA_DIR.glob("*.jsonl"):
        logger.info(f"Reading {file.name}")
        with open(file) as f:
            for line in f:
                try:
                    sample = json.loads(line)
                    if "text" in sample and "label" in sample:
                        text = sample["text"].strip()

                        # 🔥 Filter bad samples
                        if len(text) < 20:
                            continue

                        texts.append(text)
                        labels.append(sample["label"])
                        total += 1

                        if total >= max_samples:
                            return texts, np.array(labels)
                except:
                    continue

    return texts, np.array(labels)

# ----------------------------
# Embeddings
# ----------------------------
def embed_texts(texts, batch_size=64):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = []

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        emb = model.encode(batch, show_progress_bar=False)
        embeddings.extend(emb)

        if i % 5000 == 0:
            logger.info(f"Embedded {i}/{len(texts)}")

    return np.array(embeddings, dtype=np.float32)

# ----------------------------
# Train
# ----------------------------
def train():
    logger.info("🚀 Loading SOREL data...")
    texts, labels = load_sorel_data(MAX_SAMPLES)

    logger.info(f"Loaded {len(texts)} samples")

    # ============================
    # 🔹 EMBEDDINGS
    # ============================
    logger.info("🔍 Generating embeddings...")
    X_embed = embed_texts(texts)
    logger.info(f"Embedding shape: {X_embed.shape}")

    # ============================
    # 🔹 TF-IDF
    # ============================
    logger.info("🧠 Generating TF-IDF features...")

    tfidf = TfidfVectorizer(
        max_features=TFIDF_FEATURES,
        ngram_range=(1, 2),
        stop_words='english'
    )

    X_tfidf = tfidf.fit_transform(texts).toarray()
    logger.info(f"TF-IDF shape: {X_tfidf.shape}")

    # ============================
    # 🔥 FUSION
    # ============================
    logger.info("⚡ Combining features (Fusion)...")
    X = np.hstack([X_embed, X_tfidf])

    logger.info(f"Fusion shape: {X.shape}")

    # ============================
    # 🔹 PCA
    # ============================
    logger.info(f"⚡ Applying PCA → {PCA_COMPONENTS}")
    pca = PCA(n_components=PCA_COMPONENTS, random_state=42)
    X = pca.fit_transform(X)

    logger.info(f"PCA shape: {X.shape}")

    # ============================
    # Split
    # ============================
    X_train, X_test, y_train, y_test = train_test_split(
        X, labels, test_size=0.2, random_state=42
    )

    # ============================
    # Model
    # ============================
    logger.info("🌲 Training LightGBM...")

    model = lgb.LGBMClassifier(
        n_estimators=1200,
        learning_rate=0.03,
        num_leaves=256,
        subsample=0.9,
        colsample_bytree=0.9,
        class_weight='balanced',
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    # ============================
    # Evaluation
    # ============================
    logger.info("📊 Evaluating...")
    preds = model.predict(X_test)

    print("\n=== CLASSIFICATION REPORT ===")
    print(classification_report(y_test, preds))

    print("\n=== CONFUSION MATRIX ===")
    print(confusion_matrix(y_test, preds))

    # ============================
    # Save EVERYTHING
    # ============================
    MODEL_PATH.parent.mkdir(exist_ok=True)

    joblib.dump({
        "model": model,
        "pca": pca,
        "tfidf": tfidf,
        "feature_size": PCA_COMPONENTS
    }, MODEL_PATH)

    logger.info(f"✅ Model saved → {MODEL_PATH}")


if __name__ == "__main__":
    train()