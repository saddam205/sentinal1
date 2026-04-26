# train_cnn.py - PRODUCTION READY (FIXED)

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
DATA_PATH = "../data/data.csv"
MODEL_PATH = "../models/layer2_model.pth"
SCALER_PATH = "../models/cnn_scaler.pkl"
DATASET_SAVE_PATH = "../models/cnn_dataset.npz"

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
    logger.info("📂 Loading and preprocessing data...")
    df = pd.read_csv(DATA_PATH, encoding="ISO-8859-1")

    # Drop useless columns
    for col in ["InvoiceNo", "Description"]:
        if col in df.columns:
            df.drop(columns=col, inplace=True)

    # Convert categorical → numeric
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].astype("category").cat.codes

    # Convert date
    if "InvoiceDate" in df.columns:
        df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
        df["InvoiceDate"] = df["InvoiceDate"].astype("int64") // 10**9

    # Clean
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.dropna(inplace=True)

    # Label (custom logic)
    df["label"] = ((df["Quantity"] < 0) | (df["UnitPrice"] > 100)).astype(int)

    X = df.drop(columns=["label"]).values
    y = df["label"].values

    logger.info(f"Data shape: X={X.shape}, y={y.shape}")
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
        X, y, test_size=0.2, random_state=42
    )

    # Tensor conversion
    X_train = torch.tensor(X_train, dtype=torch.float32)
    y_train = torch.tensor(y_train, dtype=torch.float32)
    X_test = torch.tensor(X_test, dtype=torch.float32)
    y_test = torch.tensor(y_test, dtype=torch.float32)

    # Handle imbalance
    class_counts = np.bincount(y_train.numpy().astype(int))
    weights = 1. / class_counts
    sample_weights = weights[y_train.numpy().astype(int)]
    sampler = WeightedRandomSampler(sample_weights, len(sample_weights))

    train_loader = DataLoader(
        TensorDataset(X_train, y_train),
        batch_size=batch_size,
        sampler=sampler
    )

    # Model
    input_size = X.shape[1]
    model = NetworkDetector(input_size).to(device)
    logger.info(f"🧱 Model initialized with input size {input_size}")

    # Loss (recall-focused)
    pos_weight = torch.tensor([(y_train == 0).sum() / (y_train == 1).sum()]).to(device)
    criterion = nn.BCEWithLogitsLoss(pos_weight=pos_weight)

    optimizer = optim.Adam(model.parameters(), lr=lr)

    # ----------------------------
    # Training loop
    # ----------------------------
    logger.info(f"🚀 Training for {epochs} epochs...")

    for epoch in range(epochs):
        model.train()
        total_loss = 0

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
    np.savez(DATASET_SAVE_PATH,
             X_train=X_train.numpy(),
             y_train=y_train.numpy(),
             X_test=X_test.numpy(),
             y_test=y_test.numpy())

    # ----------------------------
    # Save model (CORRECT WAY)
    # ----------------------------
    Path(MODEL_PATH).parent.mkdir(parents=True, exist_ok=True)
    torch.save({
        "model_state_dict": model.state_dict(),
        "input_size": input_size
    }, MODEL_PATH)

    logger.info(f"✅ Model saved → {MODEL_PATH}")

    # ----------------------------
    # Evaluation
    # ----------------------------
    model.eval()
    with torch.no_grad():
        preds = torch.sigmoid(model(X_test.to(device))).cpu()

        threshold = 0.3
        preds_binary = (preds >= threshold).float()

    from sklearn.metrics import classification_report, confusion_matrix

    logger.info("\n=== EVALUATION REPORT ===")
    logger.info(classification_report(y_test.numpy(), preds_binary.numpy()))

    cm = confusion_matrix(y_test.numpy(), preds_binary.numpy())
    logger.info(f"Confusion Matrix:\n{cm}")

    return model

# ----------------------------
# Run
# ----------------------------
if __name__ == "__main__":
    train_model()