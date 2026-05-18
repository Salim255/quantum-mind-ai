# logger.py
# -------------------------------------------------------------------
# RAG EVALUATION LOGGER
# -------------------------------------------------------------------
#
# PURPOSE
# -------
# This module records every RAG interaction.
#
# WHY THIS MATTERS
# ----------------
# Production RAG systems MUST be observable.
#
# Without logging:
# - you cannot debug retrieval
# - you cannot evaluate hallucinations
# - you cannot compare prompts
# - you cannot improve chunking
# - you cannot measure reranker quality
#
# This logger becomes the foundation
# of your future RAG evaluation dashboard.
#
# WHAT THIS LOGGER STORES
# -----------------------
# - user query
# - retrieved chunks
# - sources
# - generated answer
# - latency
# - model used
# - retrieval metadata
#
# STORAGE FORMAT
# --------------
# JSON Lines (.jsonl)
#
# Example:
#
# {"query":"What is entanglement?", ...}
# {"query":"Explain qubits", ...}
#
# BENEFITS OF JSONL
# -----------------
# - append-only
# - scalable
# - easy to inspect
# - easy to stream
# - works well with pandas
# - perfect for evaluation pipelines
# -------------------------------------------------------------------

import json
from pathlib import Path
from datetime import datetime

from app.ai_core.structured_outputs.schemas.rag_eval_schema import (
    RAGEvaluationLog
)

# -------------------------------------------------------------------
# LOG FILE LOCATION
# -------------------------------------------------------------------
#
# logs/
#   rag_logs.jsonl
#
# mkdir(parents=True, exist_ok=True)
# automatically creates the directory if missing.
# -------------------------------------------------------------------

LOG_DIR = Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "rag_logs.jsonl"


# -------------------------------------------------------------------
# SAVE RAG EVALUATION LOG
# -------------------------------------------------------------------

def log_rag_evaluation(log: RAGEvaluationLog) -> None:
    """
    Append a RAG evaluation log to the JSONL file.

    PARAMETERS
    ----------
    log : RAGEvaluationLog
        Structured evaluation data for one RAG request.

    WHY APPEND INSTEAD OF OVERWRITE?
    --------------------------------
    We want historical tracking.

    Every query becomes:
    - analyzable
    - measurable
    - debuggable

    This is critical for:
    - retrieval evaluation
    - hallucination analysis
    - prompt testing
    - latency tracking
    """

    # ---------------------------------------------------------------
    # CONVERT PYDANTIC MODEL → DICTIONARY
    # ---------------------------------------------------------------
    #
    # model_dump() converts the structured schema
    # into JSON-serializable Python data.
    # ---------------------------------------------------------------
    data = log.model_dump()

    # ---------------------------------------------------------------
    # ADD TIMESTAMP
    # ---------------------------------------------------------------
    #
    # Useful later for:
    # - analytics
    # - filtering
    # - dashboards
    # - monitoring
    # ---------------------------------------------------------------
    data["timestamp"] = datetime.utcnow().isoformat()

    # ---------------------------------------------------------------
    # APPEND TO JSONL FILE
    # ---------------------------------------------------------------
    #
    # Each line is one independent JSON object.
    #
    # ensure_ascii=False:
    # preserves Unicode correctly.
    #
    # "\n":
    # each log becomes one line.
    # ---------------------------------------------------------------
    with open(LOG_FILE, "a", encoding="utf-8") as f:

        f.write(
            json.dumps(data, ensure_ascii=False)
        )

        f.write("\n")