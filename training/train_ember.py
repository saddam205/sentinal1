# train_ember.py - CORRECTED VERSION

import json
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.calibration import CalibratedClassifierCV
import joblib
from pathlib import Path
import os

DATA_PATH = "../data/ember/ember2018"

def load_data():
    X, y = [], []
    
    # Try both possible file locations
    data_paths = [
        Path(DATA_PATH),
        Path("../data/ember/ember2018"),
        Path("data/ember/ember2018"),
        Path("/mnt/c/Users/sksad/Desktop/venv_hackinhg_test/venv_hackinhg_test/valnarabilites/data/ember/ember2018")
    ]
    
    # Find the correct path
    data_dir = None
    for path in data_paths:
        if path.exists():
            data_dir = path
            break
    
    if data_dir is None:
        print("❌ Could not find EMBER data directory!")
        print(f"Tried paths: {[str(p) for p in data_paths]}")
        return np.array([]), np.array([])
    
    print(f"📁 Using data directory: {data_dir}")
    
    # Track feature sizes to determine correct dimension
    feature_sizes = []
    
    # Check for all possible file naming patterns
    for i in range(6):
        file_patterns = [
            data_dir / f"train_features_{i}.jsonl",
            data_dir / f"train_features_{i}.json",
            data_dir / f"ember_train_features_{i}.jsonl",
            data_dir / f"features_{i}.jsonl"
        ]
        
        file = None
        for pattern in file_patterns:
            if pattern.exists():
                file = pattern
                break
        
        if file is None:
            print(f"⚠ Skipping missing file for index {i}")
            continue
            
        print(f"Loading {file}")
        
        try:
            with open(file, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f):
                    if not line.strip():
                        continue
                        
                    try:
                        sample = json.loads(line)
                        
                        # Skip unlabeled samples
                        if sample.get("label", -1) == -1:
                            continue
                        
                        # Extract features - EMBER 2018 format
                        feature_vector = None
                        
                        # Method 1: Check for "features" key (precomputed)
                        if "features" in sample:
                            feature_vector = sample["features"]
                        
                        # Method 2: Check for "histogram" key
                        elif "histogram" in sample:
                            feature_vector = sample["histogram"]
                            
                        else:
                            # Extract all numeric values
                            numeric_values = []
                            for v in sample.values():
                                if isinstance(v, (int, float)):
                                    numeric_values.append(v)
                                elif isinstance(v, list):
                                    numeric_values.extend([x for x in v if isinstance(x, (int, float))])
                            
                            # 🔥 IMPORTANT: Use ALL numeric values, not truncated
                            if len(numeric_values) > 20:
                                feature_vector = numeric_values  # Keep all features
                            else:
                                continue
                        
                        if feature_vector is None:
                            if line_num == 0:
                                print(f"Sample keys: {list(sample.keys())}")
                            continue
                        
                        # Track feature sizes
                        feature_sizes.append(len(feature_vector))
                        X.append(feature_vector)
                        y.append(sample["label"])
                        
                        if len(X) % 100000 == 0:
                            print(f"  Loaded {len(X)} samples...")
                        
                    except json.JSONDecodeError as e:
                        print(f"⚠ JSON decode error at line {line_num}: {e}")
                        continue
                        
        except Exception as e:
            print(f"⚠ Error reading {file}: {e}")
            continue
    
    if len(X) == 0:
        print("❌ No samples loaded!")
        return np.array([]), np.array([])
    
    print(f"\n✅ Loaded raw samples: {len(X)}")
    
    # 🔥 CRITICAL: Determine the correct feature size
    feature_sizes_array = np.array(feature_sizes)
    print(f"\n📊 Feature size analysis:")
    print(f"  Min size: {feature_sizes_array.min()}")
    print(f"  Max size: {feature_sizes_array.max()}")
    print(f"  Mean size: {feature_sizes_array.mean():.1f}")
    print(f"  Std dev: {feature_sizes_array.std():.1f}")
    
    # EMBER 2018 typically has either 2351 or 2381 features
    # Use the most common feature size
    from collections import Counter
    size_counts = Counter(feature_sizes)
    most_common_size = size_counts.most_common(1)[0][0]
    
    print(f"\n🔧 Most common feature size: {most_common_size}")
    print(f"   This appears in {size_counts[most_common_size]} samples ({size_counts[most_common_size]/len(X)*100:.1f}%)")
    
    # Use the most common size
    feature_size = most_common_size
    
    # Filter samples that don't match the most common size
    filtered_X = []
    filtered_y = []
    
    for i, (vec, label) in enumerate(zip(X, y)):
        if len(vec) == feature_size:
            filtered_X.append(vec)
            filtered_y.append(label)
    
    print(f"\n🔧 Keeping {len(filtered_X)} samples with consistent feature size")
    print(f"   Discarded {len(X) - len(filtered_X)} samples with unusual sizes")
    
    if len(filtered_X) == 0:
        print("❌ No samples with consistent feature size!")
        return np.array([]), np.array([])
    
    # Convert to numpy array
    X = np.array(filtered_X, dtype=np.float32)
    y = np.array(filtered_y, dtype=np.int32)
    
    print(f"✅ Final training data shape: X={X.shape}, y={y.shape}")
    print(f"📈 Class distribution: {np.bincount(y)}")
    
    return X, y


def train_bayesian_on_ember():
    print("🚀 Starting EMBER training...")
    X, y = load_data()
    
    if len(X) == 0:
        print("❌ No data loaded. Training aborted.")
        return None, None
    
    print(f"\n📊 Training data: {X.shape[0]} samples, {X.shape[1]} features")
    
    print("\n🔄 Training RandomForest...")
    model = RandomForestClassifier(
        n_estimators=100,  # Increased for better performance
        max_depth=20,      # Limit depth to prevent overfitting
        n_jobs=-1,
        random_state=42,
        verbose=1
    )
    
    try:
        model.fit(X, y)
        print("✅ RandomForest training completed!")
        
        print("\n🔄 Calibrating (sigmoid)...")
        calibrator = CalibratedClassifierCV(model, method='sigmoid', cv=3)
        calibrator.fit(X, y)
        
        # Create models directory
        model_dir = Path("./models")
        model_dir.mkdir(exist_ok=True)
        
        # Save the model
        model_path = model_dir / "layer4_bayesian.pkl"
        joblib.dump(calibrator, model_path)
        print(f"✅ Model saved to {model_path}")
        
        # 🔥 CRITICAL: Save the feature size for evaluation
        feature_info = {
            "feature_size": X.shape[1],
            "num_samples": X.shape[0],
            "num_features": X.shape[1],
            "classes": [0, 1],
            "model_type": "RandomForestCalibrated",
            "n_estimators": 100,
            "max_depth": 20
        }
        
        feature_info_path = model_dir / "ember_feature_size.json"
        with open(feature_info_path, "w") as f:
            json.dump(feature_info, f, indent=2)
        print(f"✅ Feature info saved to {feature_info_path}")
        
        # Verify the model
        print(f"\n✅ Model verification:")
        print(f"  - Expected features: {model.n_features_in_}")
        print(f"  - Actual features: {X.shape[1]}")
        
        # Quick test prediction
        test_sample = X[0:1]
        pred = model.predict(test_sample)
        proba = model.predict_proba(test_sample)
        print(f"  - Sample prediction: {pred[0]} (probabilities: {proba[0]})")
        
        return model, calibrator
        
    except Exception as e:
        print(f"❌ Error during training: {e}")
        import traceback
        traceback.print_exc()
        return None, None


if __name__ == "__main__":
    model, calibrator = train_bayesian_on_ember()
    
    if model is not None:
        print("\n✅ Training completed successfully!")
        
        # Final verification
        model_path = Path("./models/layer4_bayesian.pkl")
        feature_path = Path("./models/ember_feature_size.json")
        
        if model_path.exists() and feature_path.exists():
            with open(feature_path) as f:
                info = json.load(f)
            print(f"\n📁 Saved configuration:")
            print(f"  - Feature size: {info['feature_size']}")
            print(f"  - Training samples: {info['num_samples']}")
            print(f"  - Model type: {info['model_type']}")
    else:
        print("\n❌ Training failed. Please check the errors above.")