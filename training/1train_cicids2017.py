# train_cicids2017.py - Optimized CNN for network detection (high recall)
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

# ----------------------------
# Logging setup
# ----------------------------
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# ----------------------------
# Paths
# ----------------------------
DATA_PATH = "../data/data.csv"
MODEL_PATH = "../models/layer2_cnn_optimized.pth"
DATASET_SAVE_PATH = "../models/cnn_dataset_optimized.npz"

# ----------------------------
# CNN model
# ----------------------------
class CNNDetector(nn.Module):
    def __init__(self, input_size):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(input_size, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, 128),
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

    for col in ["InvoiceNo", "Description"]:
        if col in df.columns:
            df.drop(columns=col, inplace=True)

    # Convert categorical to numeric
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].astype("category").cat.codes

    # Convert dates
    if "InvoiceDate" in df.columns:
        df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
        df["InvoiceDate"] = df["InvoiceDate"].astype("int64") // 10**9

    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.dropna(inplace=True)

    df["label"] = ((df["Quantity"] < 0) | (df["UnitPrice"] > 100)).astype(int)

    X = df.drop(columns=["label"]).values
    y = df["label"].values

    logger.info(f"Data shape: X={X.shape}, y={y.shape}")
    return X, y

# ----------------------------
# Training function
# ----------------------------
def train_cnn(batch_size=512, epochs=25, lr=0.001):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    logger.info(f"Using device: {device}")

    X, y = load_data()

    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Convert to tensors
    X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
    y_train_tensor = torch.tensor(y_train, dtype=torch.float32)
    X_test_tensor = torch.tensor(X_test, dtype=torch.float32)
    y_test_tensor = torch.tensor(y_test, dtype=torch.float32)

    # Weighted sampler to handle class imbalance
    class_counts = np.bincount(y_train.astype(int))
    weights = 1. / class_counts
    samples_weight = weights[y_train.astype(int)]
    sampler = WeightedRandomSampler(samples_weight, len(samples_weight), replacement=True)

    train_loader = DataLoader(TensorDataset(X_train_tensor, y_train_tensor), batch_size=batch_size, sampler=sampler)

    # Model
    input_size = X.shape[1]
    model = CNNDetector(input_size).to(device)
    logger.info(f"🧱 Model initialized with input size {input_size}")

    # BCE loss with pos_weight
    pos_weight = torch.tensor([(y_train == 0).sum() / (y_train == 1).sum()]).to(device)
    criterion = nn.BCEWithLogitsLoss(pos_weight=pos_weight)

    optimizer = optim.Adam(model.parameters(), lr=lr)

    logger.info(f"Training for {epochs} epochs with batch size {batch_size}")

    # Training loop
    model.train()
    for epoch in range(epochs):
        running_loss = 0.0
        for batch_X, batch_y in train_loader:
            batch_X, batch_y = batch_X.to(device), batch_y.to(device)

            optimizer.zero_grad()
            outputs = model(batch_X)
            loss = criterion(outputs, batch_y)
            loss.backward()
            optimizer.step()

            running_loss += loss.item() * batch_X.size(0)

        epoch_loss = running_loss / len(train_loader.dataset)
        logger.info(f"Epoch {epoch+1}/{epochs} | Loss: {epoch_loss:.6f}")

    # Save dataset for evaluation
    Path(DATASET_SAVE_PATH).parent.mkdir(parents=True, exist_ok=True)
    np.savez(DATASET_SAVE_PATH, X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test)
    logger.info(f"📦 Test/train datasets saved as .npz for evaluation")

    # Save model
    Path(MODEL_PATH).parent.mkdir(parents=True, exist_ok=True)
    torch.save(model, MODEL_PATH)
    logger.info(f"✅ Model saved → {MODEL_PATH}")

    # ----------------------------
    # Evaluate recall-focused metrics
    # ----------------------------
    model.eval()
    with torch.no_grad():
        preds = torch.sigmoid(model(X_test_tensor.to(device))).cpu()
        threshold = 0.3  # lower threshold to improve recall
        preds_binary = (preds >= threshold).float()

    from sklearn.metrics import classification_report, confusion_matrix
    logger.info("\n=== EVALUATION REPORT ===")
    logger.info(classification_report(y_test_tensor.numpy(), preds_binary.numpy()))
    cm = confusion_matrix(y_test_tensor.numpy(), preds_binary.numpy())
    logger.info(f"Confusion Matrix:\n{cm}")

    return model

# ----------------------------
# Main
# ----------------------------
if __name__ == "__main__":
    logger.info("🚀 Starting Optimized CNN Training Pipeline")
    train_cnn()