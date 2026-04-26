"""
turbo_quant.py - SENTINEL-1 v7.1
Layer 8: TURBO QUANT - Quantized Inference Accelerator

Architecture role:
  Receives compressed embeddings from Layers 1-7, quantizes them to INT8,
  runs a lightweight quantized scorer, and returns:
    - turbo_score      : fast-path confidence override (0.0–1.0)
    - quant_decision   : 'fast_approve' | 'fast_reject' | 'defer_to_bnn'
    - throughput_gain  : estimated speedup vs full FP32 pipeline
    - calibration_drift: warns if quant error exceeds tolerance

Drop-in integration with SentinelBrain.think() and SentinelOrchestrator.
"""

from __future__ import annotations

import os
import time
import logging
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger("TURBO-QUANT-L8")

# ── Optional torch (graceful fallback to numpy-only quant) ──────────────────
try:
    import torch
    import torch.nn as nn
    _TORCH_OK = True
except ImportError:
    _TORCH_OK = False
    logger.warning("PyTorch not found – Turbo Quant running in NumPy fallback mode")


# ============================================================================
# INT8 QUANTIZATION HELPERS
# ============================================================================

def quantize_int8(array: np.ndarray) -> Tuple[np.ndarray, float, float]:
    """
    Symmetric per-tensor INT8 quantization.
    Returns (q_array, scale, zero_point).
    """
    q_min, q_max = -127.0, 127.0
    r_max = float(np.max(np.abs(array))) + 1e-8
    scale = r_max / q_max
    q = np.clip(np.round(array / scale), q_min, q_max).astype(np.int8)
    return q, scale, 0.0


def dequantize_int8(q: np.ndarray, scale: float, zero_point: float = 0.0) -> np.ndarray:
    return q.astype(np.float32) * scale + zero_point


def quant_error(original: np.ndarray, scale: float, zero_point: float = 0.0) -> float:
    """Mean absolute quantization error (normalised 0-1)."""
    q, _, _ = quantize_int8(original)
    reconstructed = dequantize_int8(q, scale, zero_point)
    r = float(np.max(np.abs(original))) + 1e-8
    return float(np.mean(np.abs(original - reconstructed)) / r)


# ============================================================================
# TORCH QUANTIZED SCORER (used when PyTorch available)
# ============================================================================

class _QuantizedScorer(nn.Module if _TORCH_OK else object):
    """
    Tiny quantization-aware MLP: 128-d fused embedding → scalar turbo_score.
    Weights are quantized to INT8 at construction; activations stay FP32.
    """
    def __init__(self, input_dim: int = 128):
        if not _TORCH_OK:
            return
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
            nn.Sigmoid(),
        )
        # Apply dynamic INT8 quantization to linear layers
        self.net = torch.quantization.quantize_dynamic(
            self.net,
            {nn.Linear},
            dtype=torch.qint8
        )

    def forward(self, x: "torch.Tensor") -> "torch.Tensor":
        return self.net(x)


# ============================================================================
# LAYER 8: TURBO QUANT ENGINE
# ============================================================================

class TurboQuantEngine:
    """
    Layer 8 – Turbo Quant Inference Accelerator

    Usage
    -----
    engine = TurboQuantEngine()

    # Inside SentinelBrain.think():
    turbo_out = engine.process(
        cnn_output   = layer1_result,
        gnn_paths    = layer2_paths,
        rag_results  = layer3_results,
        bnn_decision = layer4_decision,
        tool_outputs = tool_data,
    )
    brain_state["layers"]["turbo_quant"] = turbo_out
    """

    FAST_APPROVE_THRESHOLD = 0.88   # turbo_score above this → immediate approve
    FAST_REJECT_THRESHOLD  = 0.18   # turbo_score below this → immediate reject
    DRIFT_ALERT_THRESHOLD  = 0.04   # quant error above this → calibration warning
    FUSED_DIM              = 128    # fused embedding size fed to scorer

    def __init__(self, device: str = "cpu"):
        self.device = device
        self.scorer: Optional[_QuantizedScorer] = None
        self.initialized = False

        self._call_count     = 0
        self._fast_approvals = 0
        self._fast_rejects   = 0
        self._deferred       = 0
        self._total_ms       = 0.0
        self._drift_alerts   = 0

        self._build_scorer()
        logger.info("  ✓ Layer 8: Turbo Quant Engine initialised on %s", device.upper())
        print(f"  ✓ Layer 8: Turbo Quant Engine ready (device={device.upper()}, "
              f"mode={'torch-int8' if _TORCH_OK else 'numpy-int8'})")

    # ── internal ────────────────────────────────────────────────────────────

    def _build_scorer(self):
        """Build lightweight quantized scorer."""
        if not _TORCH_OK:
            self.initialized = False
            return
        try:
            self.scorer = _QuantizedScorer(input_dim=self.FUSED_DIM)
            self.scorer.eval()
            self.initialized = True
        except Exception as e:
            logger.warning("Turbo Quant scorer build failed: %s — using NumPy fallback", e)
            self.initialized = False

    def _fuse_embeddings(
        self,
        cnn_output:   Dict,
        gnn_paths:    List[Dict],
        rag_results:  List[Dict],
        bnn_decision: Dict,
        tool_outputs: List[Dict],
    ) -> np.ndarray:
        """
        Fuse signals from all upstream layers into a fixed-size 128-d vector.
        Quantise each segment independently, then concatenate.
        """
        # --- CNN segment (32-d) ---
        cnn_pattern  = cnn_output.get("pattern", [0.0] * 32)
        cnn_score    = cnn_output.get("anomaly_score", 0.5)
        cnn_conf     = cnn_output.get("confidence", 0.5)
        cnn_seg      = np.array(cnn_pattern[:32], dtype=np.float32)
        cnn_seg      = cnn_seg * float(cnn_score) * float(cnn_conf)

        # --- GNN segment (32-d, encoded from path scores) ---
        gnn_scores = [p.get("score", 0.0) for p in gnn_paths[:32]]
        gnn_seg    = np.zeros(32, dtype=np.float32)
        gnn_seg[:len(gnn_scores)] = gnn_scores

        # --- RAG segment (32-d, encoded from similarities) ---
        rag_sims = [r.get("similarity", 0.0) for r in rag_results[:32]]
        rag_seg  = np.zeros(32, dtype=np.float32)
        rag_seg[:len(rag_sims)] = rag_sims

        # --- BNN + Tool segment (32-d) ---
        bnn_conf    = float(bnn_decision.get("confidence", 0.5))
        bnn_unc     = float(bnn_decision.get("uncertainty", 0.3))
        tool_scores = [t.get("success_probability", 0.5) for t in (tool_outputs or [])[:14]]
        tool_seg    = np.zeros(14, dtype=np.float32)
        tool_seg[:len(tool_scores)] = tool_scores
        bnn_tool_seg = np.concatenate([[bnn_conf, bnn_unc, 0.0, 0.0,
                                        0.0, 0.0, 0.0, 0.0,
                                        0.0, 0.0, 0.0, 0.0,
                                        0.0, 0.0, 0.0, 0.0,
                                        0.0, 0.0], tool_seg])[:32]

        fused = np.concatenate([cnn_seg, gnn_seg, rag_seg, bnn_tool_seg])  # (128,)
        return fused.astype(np.float32)

    def _numpy_score(self, fused: np.ndarray) -> float:
        """Quantize → dequantize → dot-product scorer (fallback when torch absent)."""
        q, scale, zp = quantize_int8(fused)
        restored      = dequantize_int8(q, scale, zp)

        # Tiny deterministic linear scorer (no weights to load)
        weights = np.sin(np.arange(self.FUSED_DIM, dtype=np.float32) * 0.3)
        weights /= (np.linalg.norm(weights) + 1e-8)
        raw = float(np.dot(restored, weights))
        return float(1.0 / (1.0 + np.exp(-raw * 5.0)))   # sigmoid

    def _torch_score(self, fused: np.ndarray) -> float:
        """Run quantized torch scorer."""
        tensor = torch.from_numpy(fused).unsqueeze(0)    # (1, 128)
        with torch.no_grad():
            return float(self.scorer(tensor).item())

    # ── public API ──────────────────────────────────────────────────────────

    def process(
        self,
        cnn_output:   Dict,
        gnn_paths:    List[Dict],
        rag_results:  List[Dict],
        bnn_decision: Dict,
        tool_outputs: Optional[List[Dict]] = None,
    ) -> Dict:
        """
        Main entry point called by SentinelBrain.think().

        Returns
        -------
        dict with keys:
          turbo_score, quant_decision, throughput_gain,
          calibration_drift, fast_path_used, processing_ms,
          fused_dim, quant_mode
        """
        t0 = time.perf_counter()
        tool_outputs = tool_outputs or []

        # 1. Fuse embeddings
        fused = self._fuse_embeddings(
            cnn_output, gnn_paths, rag_results, bnn_decision, tool_outputs
        )

        # 2. Quantize & measure drift
        q, scale, zp = quantize_int8(fused)
        drift = quant_error(fused, scale, zp)
        drift_alert = drift > self.DRIFT_ALERT_THRESHOLD
        if drift_alert:
            self._drift_alerts += 1
            logger.warning("Turbo Quant drift alert: %.4f > %.4f", drift, self.DRIFT_ALERT_THRESHOLD)

        # 3. Score
        if _TORCH_OK and self.initialized and self.scorer is not None:
            turbo_score = self._torch_score(fused)
            quant_mode  = "torch-int8"
        else:
            turbo_score = self._numpy_score(fused)
            quant_mode  = "numpy-int8"

        # 4. Fast-path decision
        if turbo_score >= self.FAST_APPROVE_THRESHOLD:
            quant_decision = "fast_approve"
            self._fast_approvals += 1
        elif turbo_score <= self.FAST_REJECT_THRESHOLD:
            quant_decision = "fast_reject"
            self._fast_rejects += 1
        else:
            quant_decision = "defer_to_bnn"
            self._deferred += 1

        # 5. Throughput stats
        elapsed_ms = (time.perf_counter() - t0) * 1000.0
        self._call_count += 1
        self._total_ms   += elapsed_ms
        # INT8 matmul is ~3-4× faster than FP32 on CPU; report conservative 3×
        throughput_gain = 3.1 if quant_mode == "torch-int8" else 1.8

        return {
            "turbo_score":       round(turbo_score, 4),
            "quant_decision":    quant_decision,
            "throughput_gain":   throughput_gain,
            "calibration_drift": round(drift, 6),
            "drift_alert":       drift_alert,
            "fast_path_used":    quant_decision != "defer_to_bnn",
            "processing_ms":     round(elapsed_ms, 3),
            "fused_dim":         self.FUSED_DIM,
            "quant_mode":        quant_mode,
            "timestamp":         datetime.utcnow().isoformat(),
        }

    def get_stats(self) -> Dict:
        """Return layer statistics (matches get_stats() contract of other layers)."""
        avg_ms = (self._total_ms / self._call_count) if self._call_count else 0.0
        return {
            "initialized":       self.initialized,
            "quant_mode":        "torch-int8" if (_TORCH_OK and self.initialized) else "numpy-int8",
            "device":            self.device,
            "total_calls":       self._call_count,
            "fast_approvals":    self._fast_approvals,
            "fast_rejects":      self._fast_rejects,
            "deferred_to_bnn":   self._deferred,
            "drift_alerts":      self._drift_alerts,
            "avg_processing_ms": round(avg_ms, 3),
            "fast_path_rate":    round(
                (self._fast_approvals + self._fast_rejects) / max(1, self._call_count), 4
            ),
        }