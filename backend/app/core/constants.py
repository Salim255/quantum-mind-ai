
# ------------------------------------------------------------
# CONFIGURATION
# ------------------------------------------------------------
# Controls batching size for inference safety.
# Large batches can cause:
# - memory spikes
# - GPU/CPU saturation
# ------------------------------------------------------------
BATCH_SIZE = 32

HIGH_CONFIDENCE = 5.0
MEDIUM_CONFIDENCE = 2.5
LOW_CONFIDENCE = 1.0
