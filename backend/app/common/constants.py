
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


ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 30

 # ============================================================
# SECURITY POLICY
# ============================================================

MAX_FAILED_LOGIN_ATTEMPTS = 5

LOCK_DURATION_MINUTES = 15


ACCESS_TOKEN_COOKIE = "access_token"
REFRESH_TOKEN_COOKIE = "refresh_token"