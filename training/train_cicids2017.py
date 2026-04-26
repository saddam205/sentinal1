# train_cicids2017.py - PRODUCTION READY
# Trains a network intrusion detection model on the CICIDS2017 dataset.
# Dataset source: https://www.unb.ca/cic/datasets/ids-2017.html
# Expected CSV columns include network flow features such as:
#   Flow Duration, Total Fwd Packets, Total Backward Packets,
#   Flow Bytes/s, Flow Packets/s, Label, etc.

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset, WeightedRandomSampler
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import logging
import joblib

# ----------------------------
# Logging setup
# ----------------------------
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# ----------------------------
# Paths
# ----------------------------
# CICIDS2017 CSV — download from https://www.unb.ca/cic/datasets/ids-2017.html
# Combine all per-day CSVs into one file, or point to a single day file.
DATA_PATH = "../data/cicids2017/cicids2017_combined.csv"
MODEL_PATH = "../models/layer2_cnn.pth"
SCALER_PATH = "../models/cnn_scaler.pkl"
DATASET_SAVE_PATH = "../models/cnn_dataset.npz"

# CICIDS2017 label column name (may vary slightly by CSV source)
LABEL_COLUMN = " Label"   # Note leading space — common in the raw CSVs
BENIGN_LABEL = "BENIGN"

# Columns to drop (non-feature metadata columns in CICIDS2017)
DROP_COLUMNS = [
    " Flow ID", "Flow ID",
    " Source IP", "Source IP",
    " Destination IP", "Destination IP",
    " Timestamp", "Timestamp",
]

# ----------------------------
# Model (MLP for tabular data)
# ----------------------------
class NetworkDetector(nn.Module):
    def __init__(self, input_size):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(input_size, 256),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.Dropout(0.3),

            nn.Linear(256, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Dropout(0.3),

            nn.Linear(128, 64),
            nn.ReLU(),

            nn.Linear(64, 1)
        )

    def forward(self, x):
        return self.model(x).squeeze()


# ----------------------------
# Load & preprocess data
# ----------------------------
def load_data():
    logger.info("📂 Loading and preprocessing CICIDS2017 data...")
    df = pd.read_csv(DATA_PATH, encoding="utf-8", low_memory=False)
    logger.info(f"Loaded {len(df)} rows, {len(df.columns)} columns")

    # Normalize column names (strip whitespace)
    df.columns = df.columns.str.strip()

    # Determine label column
    label_col = None
    for candidate in ["Label", "label", " Label"]:
        if candidate.strip() in df.columns:
            label_col = candidate.strip()
            break
    if label_col is None:
        raise ValueError(
            f"Could not find a Label column in the CSV. "
            f"Available columns: {list(df.columns[:10])}"
        )

    # Binary label: 0 = BENIGN, 1 = ATTACK
    df["label"] = (df[label_col].str.strip() != BENIGN_LABEL).astype(int)
    logger.info(f"Class distribution:\n{df['label'].value_counts()}")

    # Drop non-feature columns
    cols_to_drop = [c.strip() for c in DROP_COLUMNS if c.strip() in df.columns]
    cols_to_drop.append(label_col)
    df.drop(columns=cols_to_drop, inplace=True)

    # Convert all remaining columns to numeric, coerce errors to NaN
    for col in df.columns:
        if col != "label":
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Clean
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.dropna(inplace=True)

    X = df.drop(columns=["label"]).values.astype(np.float32)
    y = df["label"].values.astype(np.int32)

    logger.info(f"Final data shape: X={X.shape}, y={y.shape}")
    return X, y


# ----------------------------
# Training
# ----------------------------
def train_model(batch_size=512, epochs=25, lr=0.001):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    logger.info(f"Using device: {device}")

    X, y = load_data()

    # Normalize
    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    # Save scaler
    Path(SCALER_PATH).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(scaler, SCALER_PATH)
    logger.info(f"✅ Scaler saved → {SCALER_PATH}")

    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Tensor conversion
    X_train_t = torch.tensor(X_train, dtype=torch.float32)
    y_train_t = torch.tensor(y_train, dtype=torch.float32)
    X_test_t  = torch.tensor(X_test,  dtype=torch.float32)
    y_test_t  = torch.tensor(y_test,  dtype=torch.float32)

    # Handle class imbalance via weighted sampler
    class_counts = np.bincount(y_train)
    weights = 1.0 / class_counts
    sample_weights = weights[y_train]
    sampler = WeightedRandomSampler(sample_weights, len(sample_weights))

    train_loader = DataLoader(
        TensorDataset(X_train_t, y_train_t),
        batch_size=batch_size,
        sampler=sampler
    )

    # Model
    input_size = X.shape[1]
    model = NetworkDetector(input_size).to(device)
    logger.info(f"🧱 Model initialized with input size {input_size}")

    # Loss (recall-focused: upweight minority class)
    pos_weight = torch.tensor(
        [(y_train == 0).sum() / max((y_train == 1).sum(), 1)]
    ).to(device)
    criterion = nn.BCEWithLogitsLoss(pos_weight=pos_weight)
    optimizer = optim.Adam(model.parameters(), lr=lr)

    # ----------------------------
    # Training loop
    # ----------------------------
    logger.info(f"🚀 Training for {epochs} epochs...")
    for epoch in range(epochs):
        model.train()
        total_loss = 0.0

        for batch_X, batch_y in train_loader:
            batch_X, batch_y = batch_X.to(device), batch_y.to(device)
            optimizer.zero_grad()
            outputs = model(batch_X)
            loss = criterion(outputs, batch_y)
            loss.backward()
            optimizer.step()
            total_loss += loss.item() * batch_X.size(0)

        epoch_loss = total_loss / len(train_loader.dataset)
        logger.info(f"Epoch {epoch+1}/{epochs} | Loss: {epoch_loss:.6f}")

    # ----------------------------
    # Save dataset for evaluation
    # ----------------------------
    Path(DATASET_SAVE_PATH).parent.mkdir(parents=True, exist_ok=True)
    np.savez(
        DATASET_SAVE_PATH,
        X_train=X_train, y_train=y_train,
        X_test=X_test,   y_test=y_test
    )

    # ----------------------------
    # Save model
    # ----------------------------
    Path(MODEL_PATH).parent.mkdir(parents=True, exist_ok=True)
    torch.save(
        {"model_state_dict": model.state_dict(), "input_size": input_size},
        MODEL_PATH
    )
    logger.info(f"✅ Model saved → {MODEL_PATH}")

    # ----------------------------
    # Evaluation
    # ----------------------------
    model.eval()
    with torch.no_grad():
        preds = torch.sigmoid(model(X_test_t.to(device))).cpu()
        threshold = 0.3
        preds_binary = (preds >= threshold).float()

    from sklearn.metrics import classification_report, confusion_matrix
    logger.info("\n=== EVALUATION REPORT ===")
    logger.info(classification_report(y_test_t.numpy(), preds_binary.numpy(),
                                      target_names=["BENIGN", "ATTACK"]))
    cm = confusion_matrix(y_test_t.numpy(), preds_binary.numpy())
    logger.info(f"Confusion Matrix:\n{cm}")

    return model


# Alias expected by train_pipeline.py
train_cnn_on_cicids2017 = train_model


# ----------------------------
# Run
# ----------------------------
if __name__ == "__main__":
    train_model()
