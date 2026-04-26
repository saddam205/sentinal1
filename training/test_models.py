# test_models.py

import joblib
import torch
import json
import numpy as np
from pathlib import Path


def extract_features(sample, expected_size=256):
    """
    Extract usable features from EMBER JSON sample
    """
    try:
        # Case 1: Already vector
        if isinstance(sample, list):
            return sample[:expected_size]

        # Case 2: EMBER structured JSON
        if isinstance(sample, dict):

            # Try histogram (common simple fallback)
            if 'histogram' in sample:
                return sample['histogram'][:expected_size]

            # Try combining multiple fields (better fallback)
            features = []
            for key in ['histogram', 'byteentropy']:
                if key in sample:
                    features.extend(sample[key])

            if features:
                return features[:expected_size]

    except Exception:
        return None

    return None


def test_models():
    model_dir = Path("./models")

    print("=" * 60)
    print("MODEL VERIFICATION")
    print("=" * 60)

    # =========================
    # Load EMBER model
    # =========================
    ember_model_path = model_dir / "layer4_bayesian.pkl"
    ember_model = None
    expected_features = 256

    if ember_model_path.exists():
        try:
            ember_model = joblib.load(ember_model_path)
            if hasattr(ember_model, 'n_features_in_'):
                expected_features = ember_model.n_features_in_
                print(f"✅ EMBER Model: {expected_features} features")
            else:
                print("⚠️ EMBER Model: No feature count attribute")
        except Exception as e:
            print(f"❌ EMBER Model load error: {e}")
    else:
        print("❌ EMBER Model not found")

    # =========================
    # Feature info
    # =========================
    feature_info_path = model_dir / "ember_feature_size.json"

    if feature_info_path.exists():
        try:
            with open(feature_info_path) as f:
                info = json.load(f)
            print(f"   Feature info: {info.get('feature_size')} features, {info.get('num_samples')} samples")
        except Exception as e:
            print(f"❌ Feature info error: {e}")

    # =========================
    # CNN model
    # =========================
    cnn_model_path = model_dir / "layer2_cnn.pth"

    if cnn_model_path.exists():
        try:
            checkpoint = torch.load(cnn_model_path, map_location='cpu')
            print("✅ CNN Model: Loaded successfully")
            if isinstance(checkpoint, dict):
                print(f"   Checkpoint keys: {list(checkpoint.keys())[:5]}")
        except Exception as e:
            print(f"❌ CNN Model error: {e}")

    print("\n" + "=" * 60)
    print("QUICK PERFORMANCE CHECK")
    print("=" * 60)

    # =========================
    # Try loading .npy (BEST)
    # =========================
    npy_file = Path("../data/ember/X_test.npy")

    if npy_file.exists() and ember_model is not None:
        print("✅ Using preprocessed NumPy test data...")
        try:
            X_test = np.load(npy_file)

            if X_test.shape[1] != expected_features:
                print(f"⚠️ Feature mismatch: expected {expected_features}, got {X_test.shape[1]}")
                return

            preds = ember_model.predict(X_test[:5])
            probs = ember_model.predict_proba(X_test[:5])

            print("Predictions:", preds)
            print("Malware probabilities:", probs[:, 1])

            return

        except Exception as e:
            print(f"❌ NPY load error: {e}")

    # =========================
    # Fallback: JSONL
    # =========================
    test_file = Path("../data/ember/ember2018/test_features.jsonl")

    if test_file.exists() and ember_model is not None:
        print("⚠️ Using raw JSONL (approximate features)...")

        samples = []

        try:
            with open(test_file) as f:
                for i, line in enumerate(f):
                    if i >= 5:
                        break

                    try:
                        sample = json.loads(line)
                        features = extract_features(sample, expected_features)

                        if features and len(features) == expected_features:
                            samples.append(features)

                    except Exception:
                        continue

            if samples:
                X_test = np.array(samples)

                preds = ember_model.predict(X_test)
                probs = ember_model.predict_proba(X_test)

                print("Predictions:", preds)
                print("Malware probabilities:", probs[:, 1])

            else:
                print("❌ Could not extract valid features from JSONL")

        except Exception as e:
            print(f"❌ Test data error: {e}")

    else:
        print("⚠️ Test file not found or EMBER model not loaded")


if __name__ == "__main__":
    test_models()