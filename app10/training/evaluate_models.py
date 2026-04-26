# evaluate_models.py - PRODUCTION READY FINAL VERSION (WITH DOUBLE LOADING FIX)

import torch
import joblib
import json
import numpy as np
import random
import time
import logging
import argparse
from pathlib import Path
from sklearn.metrics import (
    accuracy_score, classification_report, roc_auc_score, 
    confusion_matrix, roc_curve, precision_score, recall_score, f1_score
)
from collections import defaultdict
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')



    
# Set seeds for reproducibility
SEED = 42
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(SEED)

# Configure logging with date-based rotation
log_filename = f"evaluation_{datetime.now().strftime('%Y%m%d')}.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
logger.info(f"Logging to {log_filename}")

# Optional imports
try:
    from sentence_transformers import SentenceTransformer
    EMBEDDING = True
except ImportError:
    EMBEDDING = False
    logger.warning("sentence-transformers not available - text embedding disabled")

try:
    from ember import PEFeatureExtractor
    EMBER_AVAILABLE = True
except ImportError:
    EMBER_AVAILABLE = False
    logger.warning("EMBER not available - using fallback feature extraction")

# Global caching
_embedding_model = None
_ember_extractor = None

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "models"
DATA_DIR = BASE_DIR / "../data"

# Device configuration
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
logger.info(f"Using device: {DEVICE}")


# ================= MODEL CACHE =================
class ModelCache:
    """Singleton cache for heavy models with version tracking"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.models = {}
        self.version_info = {}
        self.optimal_thresholds = {}
        self.feature_sizes = {}  # Cache feature sizes
        
    def get_ember_model(self):
        """Get or load EMBER model (singleton)"""
        if "ember" not in self.models:
            model_path = MODEL_DIR / "layer4_bayesian.pkl"
            if model_path.exists():
                try:
                    logger.info("Loading EMBER model...")
                    self.models["ember"] = joblib.load(model_path)
                    self.version_info["ember"] = {
                        "version": "v1.0",
                        "type": "file",
                        "path": str(model_path),
                        "loaded_at": datetime.now().isoformat()
                    }
                    
                    # Cache feature size
                    if hasattr(self.models["ember"], 'n_features_in_'):
                        self.feature_sizes["ember"] = self.models["ember"].n_features_in_
                        logger.info(f"EMBER model expects {self.feature_sizes['ember']} features")
                    
                    logger.info("EMBER model loaded successfully")
                except Exception as e:
                    logger.error(f"Failed to load EMBER model: {e}")
                    return None
        return self.models.get("ember")
    
    def get_cnn_model(self, input_size=None):
        """Get or load CNN model with proper architecture (singleton)"""
        if "cnn" not in self.models or self.feature_sizes.get("cnn") != input_size:
            cnn_path = MODEL_DIR / "layer2_cnn.pth"
            if cnn_path.exists():
                try:
                    logger.info(f"Loading CNN model (input_size={input_size})...")
                    model = CNNModel(input_size).to(DEVICE)
                    state_dict = torch.load(cnn_path, map_location=DEVICE)
                    
                    # Handle 'model.' prefix if present
                    new_state_dict = {}
                    for key, value in state_dict.items():
                        if key.startswith('model.'):
                            new_state_dict[key[6:]] = value
                        else:
                            new_state_dict[key] = value
                    
                    # Check for missing/unexpected keys
                    missing, unexpected = model.load_state_dict(new_state_dict, strict=False)
                    if missing:
                        logger.warning(f"Missing keys in CNN: {missing[:5]}")
                    if unexpected:
                        logger.warning(f"Unexpected keys in CNN: {unexpected[:5]}")
                    
                    model.eval()
                    self.models["cnn"] = model
                    self.version_info["cnn"] = {
                        "version": "v2.1",
                        "type": "network",
                        "path": str(cnn_path),
                        "input_size": input_size,
                        "loaded_at": datetime.now().isoformat()
                    }
                    self.feature_sizes["cnn"] = input_size
                    logger.info("CNN model loaded successfully")
                except Exception as e:
                    logger.error(f"Failed to load CNN model: {e}")
                    return None
        return self.models.get("cnn")
    
    def get_sorel_model(self):
        """Get or load SOREL model (singleton)"""
        if "sorel" not in self.models:
            model_path = MODEL_DIR / "sorel_model.pkl"
            if model_path.exists():
                try:
                    logger.info("Loading SOREL model...")
                    data = joblib.load(model_path)

                    self.models["sorel"] = data["model"]
                    self.pca = data.get("pca")

                    self.feature_sizes["sorel"] = data.get("feature_size", 128)
                    self.scaler = data.get("scaler")

                    # cache feature size
                    if hasattr(self.models["sorel"], 'n_features_in_'):
                        self.feature_sizes["sorel"] = self.models["sorel"].n_features_in_
                    self.version_info["sorel"] = {
                        "version": "v1.0",
                        "type": "text",
                        "path": str(model_path),
                        "loaded_at": datetime.now().isoformat()
                    }
                    
                    # Cache feature size if available
                    if hasattr(self.models["sorel"], 'n_features_in_'):
                        self.feature_sizes["sorel"] = self.models["sorel"].n_features_in_
                        logger.info(f"SOREL model expects {self.feature_sizes['sorel']} features")
                    
                    logger.info("SOREL model loaded successfully")
                except Exception as e:
                    logger.error(f"Failed to load SOREL model: {e}")
                    return None
        return self.models.get("sorel")
    
    def get_feature_size(self, model_name):
        """Get cached feature size for a model"""
        return self.feature_sizes.get(model_name)
    
    def set_optimal_threshold(self, model_name, threshold, metrics):
        """Store optimal threshold for a model"""
        self.optimal_thresholds[model_name] = {
            "threshold": float(threshold),
            "metrics": metrics,
            "set_at": datetime.now().isoformat()
        }
        logger.info(f"Set optimal threshold for {model_name}: {threshold:.4f}")


# ================= CNN MODEL DEFINITION =================
class CNNModel(torch.nn.Module):
    def __init__(self, input_size):
        super().__init__()

        self.input_size = input_size

        self.conv1 = torch.nn.Conv1d(1, 32, kernel_size=3, padding=1)
        self.act1 = torch.nn.LeakyReLU()

        self.conv2 = torch.nn.Conv1d(32, 32, kernel_size=3, padding=1)
        self.act2 = torch.nn.LeakyReLU()

        self.flatten = torch.nn.Flatten()

        # ✅ FIXED
        self.fc = torch.nn.Linear(32 * input_size, 2)

    def forward(self, x):
        x = x.unsqueeze(1)  # (batch, 1, features)

        x = self.act1(self.conv1(x))
        x = self.act2(self.conv2(x))

        x = self.flatten(x)
        return self.fc(x)


# ================= UTILITIES =================
def get_embedding_model():
    """Lazy load embedding model with caching"""
    global _embedding_model
    if _embedding_model is None and EMBEDDING:
        logger.info("Loading embedding model...")
        _embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        logger.info("Embedding model loaded")
    return _embedding_model

def get_ember_extractor():
    """Lazy load EMBER extractor"""
    global _ember_extractor
    if _ember_extractor is None and EMBER_AVAILABLE:
        try:
            _ember_extractor = PEFeatureExtractor()
            logger.info("EMBER extractor loaded")
        except Exception as e:
            logger.warning(f"Failed to load EMBER extractor: {e}")
    return _ember_extractor

def embed_in_batches(model, texts, batch_size=64, show_progress=True):
    """Embed texts in batches to avoid memory issues"""
    embeddings = []
    total_batches = (len(texts) + batch_size - 1) // batch_size
    
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        batch_embeddings = model.encode(batch, show_progress_bar=False)
        embeddings.extend(batch_embeddings)
        
        if show_progress and (i // batch_size) % 10 == 0:
            logger.debug(f"Embedding progress: {i}/{len(texts)}")
    
    return np.array(embeddings)

def batch_inference(model, X, batch_size=512):
    """Batch inference to avoid OOM"""
    if not isinstance(X, torch.Tensor):
        X = torch.tensor(X, dtype=torch.float32, pin_memory=True)
    
    outputs = []
    model.eval()
    
    with torch.no_grad():
        for i in range(0, len(X), batch_size):
            batch = X[i:i+batch_size].to(DEVICE)
            logits = model(batch)
            probs = torch.sigmoid(logits)
            outputs.append(probs.cpu().numpy())
    
    return np.vstack(outputs)

def find_best_threshold(y_true, y_scores, return_metrics=False):
    """Find optimal threshold using Youden's J statistic"""
    fpr, tpr, thresholds = roc_curve(y_true, y_scores)
    youden_j = tpr - fpr
    best_idx = np.argmax(youden_j)
    best_threshold = thresholds[best_idx]
    
    # Calculate metrics at optimal threshold
    preds_optimized = (y_scores > best_threshold).astype(int)
    metrics = {
        "accuracy": float(accuracy_score(y_true, preds_optimized)),
        "precision": float(precision_score(y_true, preds_optimized, zero_division=0)),
        "recall": float(recall_score(y_true, preds_optimized, zero_division=0)),
        "f1": float(f1_score(y_true, preds_optimized, zero_division=0)),
        "youden_j": float(youden_j[best_idx])
    }
    
    logger.info(f"Optimal threshold: {best_threshold:.4f}")
    logger.info(f"Metrics at optimal threshold: {metrics}")
    
    if return_metrics:
        return best_threshold, metrics
    return best_threshold


# ================= LOAD EMBER (WITHOUT DOUBLE LOADING) =================
def load_ember_test(max_samples=50000):
    """Load EMBER test data with reservoir sampling (true streaming)
    ✅ FIXED: No model loading here - gets feature size from cache"""
    
    data_paths = [
        Path(DATA_DIR) / "ember/ember2018/test_features.jsonl",
        Path(DATA_DIR) / "ember/test_features.jsonl",
        Path("../data/ember/ember2018/test_features.jsonl"),
        Path("/mnt/c/Users/sksad/Desktop/venv_hackinhg_test/venv_hackinhg_test/valnarabilites/data/ember/ember2018/test_features.jsonl")
    ]
    
    file = None
    for path in data_paths:
        if path.exists():
            file = path
            break
    
    if file is None:
        logger.warning("EMBER test data not found")
        return None, None

    # Reservoir sampling
    reservoir_X = []
    reservoir_y = []
    extractor = get_ember_extractor()
    total_processed = 0
    
    logger.info(f"Streaming EMBER data from {file}")
    
    with open(file) as f:
        for line_num, line in enumerate(f):
            if not line.strip():
                continue
            
            try:
                sample = json.loads(line)
                if sample.get("label", -1) == -1:
                    continue
                
                feature_vector = None
                
                # Correct order: precomputed features first
                if "features" in sample:
                    feature_vector = sample["features"]
                elif extractor and "raw" in sample:
                    try:
                        feature_vector = extractor.feature_vector(sample["raw"])
                    except Exception:
                        pass
                elif "histogram" in sample:
                    feature_vector = sample["histogram"]
                else:
                    # Fallback numeric extraction
                    numeric_values = []
                    for v in sample.values():
                        if isinstance(v, (int, float)):
                            numeric_values.append(v)
                        elif isinstance(v, list):
                            numeric_values.extend([x for x in v if isinstance(x, (int, float))])
                    
                    if len(numeric_values) > 20:
                        MAX_FEATURES = 256
                        if len(numeric_values) >= MAX_FEATURES:
                            feature_vector = numeric_values[:MAX_FEATURES]
                        else:
                            feature_vector = numeric_values + [0] * (MAX_FEATURES - len(numeric_values))
                
                if feature_vector is None:
                    continue
                
                # Reservoir sampling
                if len(reservoir_X) < max_samples:
                    reservoir_X.append(feature_vector)
                    reservoir_y.append(sample["label"])
                else:
                    j = random.randint(0, total_processed)
                    if j < max_samples:
                        reservoir_X[j] = feature_vector
                        reservoir_y[j] = sample["label"]
                
                total_processed += 1
                
                if total_processed % 100000 == 0:
                    logger.info(f"Processed {total_processed} samples...")
                    
            except json.JSONDecodeError:
                continue
            except Exception as e:
                logger.debug(f"Skipping sample: {e}")
    
    logger.info(f"Loaded {len(reservoir_X)} test samples (from {total_processed} total)")
    
    if len(reservoir_X) == 0:
        return None, None
    
    # ✅ FIXED: Get feature size from cache, not by loading model
    cache = ModelCache()
    feature_size = cache.get_feature_size("ember")
    
    # Fallback to default if not cached
    if feature_size is None:
        feature_size = 256
        logger.warning(f"Feature size not cached, using default: {feature_size}")
        logger.warning("This may cause mismatch if training used different size!")
    if feature_size is None:
        raise ValueError("EMBER feature size not available. Model must be loaded first.")
    # Normalize all vectors
    X_normalized = []
    for x in reservoir_X:
        if len(x) >= feature_size:
            X_normalized.append(x[:feature_size])
        else:
            padded = x + [0] * (feature_size - len(x))
            X_normalized.append(padded)
    
    X = np.array(X_normalized, dtype=np.float32)
    y = np.array(reservoir_y, dtype=np.int32)
    
    logger.info(f"Final test shape: {X.shape}")
    return X, y


# ================= LOAD SOREL =================
def load_sorel_test(max_samples=50000):
    """Load SOREL test data with reservoir sampling"""
    sorel_path = Path(DATA_DIR) / "sorel"
    
    if not sorel_path.exists():
        alt_paths = [
            Path("../data/sorel"),
            Path("/mnt/c/Users/sksad/Desktop/venv_hackinhg_test/venv_hackinhg_test/valnarabilites/data/sorel")
        ]
        for alt in alt_paths:
            if alt.exists():
                sorel_path = alt
                break
    
    files = list(sorel_path.glob("*.jsonl"))
    if not files:
        logger.warning("SOREL test data not found")
        return None, None
    
    reservoir_X = []
    reservoir_y = []
    total_processed = 0
    
    for file in files:
        logger.info(f"Processing {file.name}")
        with open(file) as f:
            for line in f:
                try:
                    sample = json.loads(line)
                    if "label" not in sample:
                        continue
                    
                    text = sample.get("text")
                    if not text:
                        continue
                    
                    # Reservoir sampling
                    if len(reservoir_X) < max_samples:
                        reservoir_X.append(text)
                        reservoir_y.append(sample["label"])
                    else:
                        j = random.randint(0, total_processed)
                        if j < max_samples:
                            reservoir_X[j] = text
                            reservoir_y[j] = sample["label"]
                    
                    total_processed += 1
                    
                except json.JSONDecodeError:
                    continue
    
    logger.info(f"Loaded {len(reservoir_X)} SOREL samples (from {total_processed} total)")
    
    if len(reservoir_X) == 0:
        return None, None
    
    return reservoir_X, np.array(reservoir_y)


# ================= LOAD CNN TEST DATA =================
def load_cnn_test_data(max_samples=50000):
    """Load CNN test data with sampling"""
    test_paths = [
        DATA_DIR / "cicids2017/test_data.npz",
        Path("../data/cicids2017/test_data.npz"),
        Path("/mnt/c/Users/sksad/Desktop/venv_hackinhg_test/venv_hackinhg_test/valnarabilites/data/cicids2017/test_data.npz")
    ]
    
    for test_file in test_paths:
        if test_file.exists():
            try:
                data = np.load(test_file)
                X = data['X']
                y = data['y']
                
                # Sample if needed
                if len(X) > max_samples:
                    indices = np.random.choice(len(X), max_samples, replace=False)
                    X = X[indices]
                    y = y[indices]
                
                logger.info(f"Loaded CNN test data: {X.shape}")
                return X, y
            except Exception as e:
                logger.error(f"Error loading {test_file}: {e}")
    
    logger.warning("No CNN test data found")
    return None, None


# ================= EVALUATION =================
def evaluate_model(name, model, X, y, model_type="file", 
                   find_threshold=False, cache=None, batch_size=512):
    """Evaluate a single model with comprehensive metrics"""
    logger.info(f"Evaluating {name} ({model_type} detection)")
    
    # Time prediction
    start_time = time.time()
    
    # Handle different model types
    if hasattr(model, 'predict'):
        # sklearn model
        preds = model.predict(X)
        try:
            probs = model.predict_proba(X)
            if probs.shape[1] == 2:
                probs = probs[:, 1]
            else:
                probs = None
        except Exception:
            probs = None
    else:
        # PyTorch model - use batch inference
        if not isinstance(X, torch.Tensor):
            X_tensor = torch.tensor(X, dtype=torch.float32)
        else:
            X_tensor = X
        
        probs = batch_inference(model, X_tensor, batch_size=batch_size).flatten()
        preds = (probs > 0.5).astype(int)
    
    predict_time = time.time() - start_time
    logger.info(f"Prediction time: {predict_time:.3f}s for {len(y)} samples")
    logger.info(f"Avg: {predict_time/len(y)*1000:.2f}ms per sample")
    
    # Calculate metrics
    acc = accuracy_score(y, preds)
    precision = precision_score(y, preds, zero_division=0)
    recall = recall_score(y, preds, zero_division=0)
    f1 = f1_score(y, preds, zero_division=0)
    
    logger.info(f"Accuracy: {acc:.4f}")
    logger.info(f"Precision: {precision:.4f}")
    logger.info(f"Recall: {recall:.4f}")
    logger.info(f"F1 Score: {f1:.4f}")
    
    # AUC if probabilities available
    auc = None
    if probs is not None:
        try:
            auc = roc_auc_score(y, probs)
            logger.info(f"AUC: {auc:.4f}")
        except Exception as e:
            logger.warning(f"Cannot compute AUC: {e}")
    
    # Confusion matrix
    cm = confusion_matrix(y, preds)
    logger.info(f"Confusion Matrix:\n{cm}")
    
    result = {
        "model": name,
        "model_type": model_type,
        "accuracy": float(acc),
        "precision": float(precision),
        "recall": float(recall),
        "f1_score": float(f1),
        "auc": float(auc) if auc else None,
        "predict_time_seconds": predict_time,
        "predict_time_ms_per_sample": (predict_time / len(y)) * 1000,
        "n_samples": len(y),
        "confusion_matrix": cm.tolist(),
        "default_threshold": 0.5
    }
    
    # Find optimal threshold if probabilities available
    if find_threshold and probs is not None and cache:
        best_threshold, threshold_metrics = find_best_threshold(y, probs, return_metrics=True)
        cache.set_optimal_threshold(name, best_threshold, threshold_metrics)
        result["optimal_threshold"] = float(best_threshold)
        result["threshold_metrics"] = threshold_metrics
    
    return result


# ================= MAIN =================
def run_evaluation(args=None):
    """Main evaluation pipeline with domain isolation"""
    parser = argparse.ArgumentParser(description="Evaluate malware detection models")
    parser.add_argument("--model", choices=["ember", "cnn", "sorel", "all"], default="all",
                       help="Which model to evaluate")
    parser.add_argument("--samples", type=int, default=50000,
                       help="Maximum samples to use for evaluation")
    parser.add_argument("--threshold-tuning", action="store_true",
                       help="Find optimal threshold for each model")
    parser.add_argument("--batch-size", type=int, default=512,
                       help="Batch size for inference")
    parser.add_argument("--save-predictions", action="store_true",
                       help="Save predictions to file")
    args = parser.parse_args(args)
    
    logger.info("🚀 Starting Model Evaluation Pipeline")
    logger.info(f"Device: {DEVICE}")
    logger.info(f"Arguments: {vars(args)}")
    logger.info(f"Random seed: {SEED}")
    
    # Initialize cache (singleton)
    cache = ModelCache()
    results = []
    all_predictions = {}
    
    # ===== FILE-BASED DETECTION (EMBER) =====
    if args.model in ["ember", "all"]:
        try:
            logger.info("="*60)
            logger.info("📁 FILE-BASED DETECTION EVALUATION")
            logger.info("="*60)
            
            # ✅ First load the model (caches feature size)
            model = cache.get_ember_model()
            if model is None:
                logger.error("EMBER model not available")
                return
            
            # ✅ Then load data (uses cached feature size)
            X_ember, y_ember = load_ember_test(max_samples=args.samples)
            
            if X_ember is not None:
                result = evaluate_model("EMBER Bayesian", model, X_ember, y_ember, 
                                       model_type="file", 
                                       find_threshold=args.threshold_tuning,
                                       cache=cache,
                                       batch_size=args.batch_size)
                if result:
                    results.append(result)
                    if args.save_predictions:
                        all_predictions["ember"] = {
                            "true_labels": y_ember.tolist(),
                            "predictions": model.predict(X_ember).tolist()
                        }
            else:
                logger.warning("Skipping file-based evaluation - no data")
        except Exception as e:
            logger.error(f"EMBER evaluation failed: {e}", exc_info=True)
    
    # ===== NETWORK-BASED DETECTION (CNN) =====
    if args.model in ["cnn", "all"]:
        try:
            logger.info("="*60)
            logger.info("🌐 NETWORK-BASED DETECTION EVALUATION")
            logger.info("="*60)
            
            # Load data first to get input size
            X_cnn, y_cnn = load_cnn_test_data(max_samples=args.samples)
            if X_cnn is not None:
                # Load model with correct input size
                model = cache.get_cnn_model(input_size=X_cnn.shape[1])
                if model:
                    result = evaluate_model("CNN Network Detector", model, X_cnn, y_cnn,
                                           model_type="network",
                                           find_threshold=args.threshold_tuning,
                                           cache=cache,
                                           batch_size=args.batch_size)
                    if result:
                        results.append(result)
                        
                        if args.save_predictions:
                            # Get predictions for saving
                            X_tensor = torch.tensor(X_cnn, dtype=torch.float32)
                            probs = batch_inference(model, X_tensor, batch_size=args.batch_size).flatten()
                            all_predictions["cnn"] = {
                                "true_labels": y_cnn.tolist(),
                                "probabilities": probs.tolist(),
                                "predictions": (probs > 0.5).astype(int).tolist()
                            }
            else:
                logger.warning("Skipping network-based evaluation - no data")
        except Exception as e:
            logger.error(f"CNN evaluation failed: {e}", exc_info=True)
    
    # ===== TEXT-BASED DETECTION (SOREL) =====
    if args.model in ["sorel", "all"]:
        try:
            logger.info("="*60)
            logger.info("📝 TEXT-BASED DETECTION EVALUATION")
            logger.info("="*60)
            
            # Load model first
            model = cache.get_sorel_model()
            if model is None:
                logger.error("SOREL model not available")
                return
            
            # Load data
            X_sorel, y_sorel = load_sorel_test(max_samples=args.samples)
            
            if X_sorel is not None and len(X_sorel) > 0:
                # Embed text in batches to avoid memory issues
                embedding_model = get_embedding_model()
                if embedding_model:
                    start_time = time.time()
                    X_embedded = embed_in_batches(embedding_model, X_sorel, batch_size=64)
     # ✅ -----------------------------Apply PCA------------------------------------------
                    if hasattr(cache, "pca") and cache.pca:
                        X_embedded = cache.pca.transform(X_embedded)

                    # Align (safety)
                    expected_size = cache.get_feature_size("sorel")
                    X_embedded = align_features(X_embedded, expected_size)
                    # Align features
                    expected_size = cache.get_feature_size("sorel") or 384
                    X_embedded = align_features(X_embedded, expected_size)
            #--------------------------------------------------------------------------------------
                    # ✅ Apply scaler
                    if hasattr(cache, "scaler") and cache.scaler:
                     X_embedded = cache.scaler.transform(X_embedded)
                    # ✅ FIX
                    expected_size = cache.get_feature_size("sorel")

                    if expected_size is None:
                        logger.warning("SOREL feature size not cached, assuming 256")
                        expected_size = 256

                    X_embedded = align_features(X_embedded, expected_size)

                    logger.info(f"SOREL features aligned: {X_embedded.shape}")
                    logger.info(f"Embedding time: {time.time() - start_time:.2f}s")
                    
                    result = evaluate_model("SOREL Text Detector", model, X_embedded, y_sorel,
                                           model_type="text",
                                           find_threshold=args.threshold_tuning,
                                           cache=cache,
                                           batch_size=args.batch_size)
                    if result:
                        results.append(result)
                        
                        if args.save_predictions:
                            all_predictions["sorel"] = {
                                "true_labels": y_sorel.tolist(),
                                "predictions": model.predict(X_embedded).tolist()
                            }
            else:
                logger.warning("Skipping text-based evaluation - no data")
        except Exception as e:
            logger.error(f"SOREL evaluation failed: {e}", exc_info=True)
    
    # ===== SAVE REPORT =====
    if results:
        report_dir = Path("./reports")
        report_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Prepare full report
        full_report = {
            "timestamp": timestamp,
            "seed": SEED,
            "args": vars(args),
            "device": str(DEVICE),
            "model_versions": cache.version_info,
            "optimal_thresholds": cache.optimal_thresholds,
            "results": results
        }
        
        # Save detailed report
        report_path = report_dir / f"evaluation_report_{timestamp}.json"
        with open(report_path, "w") as f:
            json.dump(full_report, f, indent=2)
        
        # Save predictions if requested
        if args.save_predictions and all_predictions:
            pred_path = report_dir / f"predictions_{timestamp}.json"
            with open(pred_path, "w") as f:
                json.dump(all_predictions, f, indent=2)
            logger.info(f"Predictions saved to {pred_path}")
        
        # Save summary report
        summary_path = report_dir / f"evaluation_summary_{timestamp}.txt"
        with open(summary_path, "w") as f:
            f.write("MALWARE DETECTION EVALUATION SUMMARY\n")
            f.write("="*60 + "\n")
            f.write(f"Timestamp: {timestamp}\n")
            f.write(f"Seed: {SEED}\n")
            f.write(f"Device: {DEVICE}\n")
            f.write(f"Arguments: {vars(args)}\n\n")
            
            for result in results:
                f.write(f"Model: {result['model']}\n")
                f.write(f"Type: {result['model_type']}\n")
                f.write(f"Accuracy: {result['accuracy']:.4f}\n")
                f.write(f"Precision: {result['precision']:.4f}\n")
                f.write(f"Recall: {result['recall']:.4f}\n")
                f.write(f"F1 Score: {result['f1_score']:.4f}\n")
                if result.get('auc'):
                    f.write(f"AUC: {result['auc']:.4f}\n")
                if result.get('optimal_threshold'):
                    f.write(f"Optimal Threshold: {result['optimal_threshold']:.4f}\n")
                f.write(f"Samples: {result['n_samples']}\n")
                if result.get('predict_time_seconds'):
                    f.write(f"Time: {result['predict_time_seconds']:.3f}s\n")
                f.write("-"*40 + "\n")
        
        logger.info(f"✅ Evaluation complete → {report_path}")
        
        # Summary table
        logger.info("\n📊 SUMMARY:")
        logger.info("-"*80)
        logger.info(f"{'Model':<25} {'Accuracy':<10} {'Precision':<10} {'Recall':<10} {'F1':<10}")
        logger.info("-"*80)
        for result in results:
            logger.info(f"{result['model']:<25} {result['accuracy']:<10.4f} "
                       f"{result['precision']:<10.4f} {result['recall']:<10.4f} "
                       f"{result['f1_score']:<10.4f}")
        
        # Security recommendations
        logger.info("\n🔒 SECURITY RECOMMENDATIONS:")
        for result in results:
            if result['recall'] < 0.9:
                logger.warning(f"  ⚠️ {result['model']} has low recall ({result['recall']:.4f}) - risk of false negatives")
            if result.get('optimal_threshold'):
                logger.info(f"  ✅ {result['model']} optimal threshold: {result['optimal_threshold']:.4f}")
        
    else:
        logger.warning("No models were successfully evaluated")
        
        #----------------------------------------------------------------------------------------------------------
        
def align_features(X, expected_size):
    """Ensure feature size matches model expectation"""
    if X.shape[1] == expected_size:
        return X
    
    if X.shape[1] > expected_size:
        logger.warning(f"Truncating features: {X.shape[1]} → {expected_size}")
        return X[:, :expected_size]
    
    else:
        logger.warning(f"Padding features: {X.shape[1]} → {expected_size}")
        pad_width = expected_size - X.shape[1]
        return np.hstack([X, np.zeros((X.shape[0], pad_width))])
#--------------------------------------------------------------------------------------------------------------
#----------------------------

#--------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    run_evaluation()