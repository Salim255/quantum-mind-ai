import re
from difflib import SequenceMatcher
from typing import Dict


# ------------------------------------------------------------
# SEMANTIC CONCEPT KNOWLEDGE BASE
# ------------------------------------------------------------
# WHY THIS EXISTS:
# Instead of pure keyword matching,
# we define "semantic anchors" per concept.
#
# WHAT THIS SOLVES:
# - improves retrieval categorization
# - enables filtering / reranking
# - helps debugging RAG behavior
CONCEPTS: Dict[str, dict] = {
    "entanglement": {
        "anchors": [
            "entanglement", "entangled", "bell state",
            "bell inequality", "epr", "non-local correlation"
        ],
        "keywords_soft": [
            "spooky action", "instant correlation", "linked qubits"
        ]
    },

    "teleportation": {
        "anchors": [
            "teleportation", "quantum teleport", "state transfer"
        ],
        "keywords_soft": [
            "send qubit", "transfer quantum state"
        ]
    },

    "superdense-coding": {
        "anchors": [
            "superdense", "dense coding"
        ],
        "keywords_soft": [
            "send two bits", "one qubit encoding"
        ]
    },

    "qubits": {
        "anchors": [
            "qubit", "qubits", "bloch sphere", "state vector"
        ],
        "keywords_soft": [
            "two-level system", "quantum state"
        ]
    },

    "algorithms": {
        "anchors": [
            "grover", "shor", "qft",
            "quantum algorithm", "fourier transform"
        ],
        "keywords_soft": [
            "speedup", "factoring", "search algorithm"
        ]
    },

    "quantum-fundamentals": {
        "anchors": [
            "superposition", "measurement",
            "decoherence", "collapse"
        ],
        "keywords_soft": [
            "wave function", "probability amplitude"
        ]
    },

    "quantum-computing": {
        "anchors": [
            "quantum computing", "quantum computer",
            "quantum advantage", "supremacy"
        ],
        "keywords_soft": [
            "quantum processor", "qubit system"
        ]
    }
}


# ------------------------------------------------------------
# TEXT NORMALIZATION
# ------------------------------------------------------------
# WHY:
# ensures consistent matching regardless of casing or spacing
def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower().strip())


# ------------------------------------------------------------
# CONCEPT SCORING FUNCTION
# ------------------------------------------------------------
# PURPOSE:
# compute how strongly a text belongs to a concept
#
# WHY THIS EXISTS:
# chunk labeling improves:
# - retrieval filtering
# - debugging
# - reranking
def score_concept(text: str, concept_data: dict) -> float:

    q = normalize(text)

    score = 0.0

    # --------------------------------------------------------
    # 1. STRONG SIGNAL: exact anchor match
    # --------------------------------------------------------
    # WHY:
    # anchors represent canonical domain terms
    #
    # IMPACT:
    # strongest signal for classification
    for a in concept_data["anchors"]:
        if a in q:
            score += 3.0

    # --------------------------------------------------------
    # 2. SOFT SIGNAL: semantic hints
    # --------------------------------------------------------
    # WHY:
    # captures paraphrased or informal expressions
    for s in concept_data["keywords_soft"]:
        if s in q:
            score += 1.5

    # --------------------------------------------------------
    # 3. FUZZY MATCH (WEAK BACKUP SIGNAL)
    # --------------------------------------------------------
    # WHY:
    # handles misspellings / variations
    #
    # WARNING:
    # not semantic, only similarity-based
    for a in concept_data["anchors"]:

        similarity = SequenceMatcher(None, q, a).ratio()

        score = max(score, similarity * 2.5)

    return score


# ------------------------------------------------------------
# MAIN CONCEPT DETECTOR
# ------------------------------------------------------------
# PURPOSE:
# assign best semantic label to a chunk
#
# WHY THIS IS IMPORTANT IN RAG:
# - helps filtering chunks by topic
# - improves retrieval targeting
# - enables hybrid routing strategies
def detect_concept(text: str) -> str:

    q = normalize(text)

    best_concept = "general-quantum"
    best_score = 0.0

    # --------------------------------------------------------
    # iterate all known concepts
    # --------------------------------------------------------
    for concept, data in CONCEPTS.items():

        score = score_concept(q, data)

        # ----------------------------------------------------
        # update best match
        # ----------------------------------------------------
        if score > best_score:
            best_score = score
            best_concept = concept

    # --------------------------------------------------------
    # SAFETY THRESHOLD
    # --------------------------------------------------------
    # WHY:
    # avoids false classification
    #
    # IF TOO LOW:
    # chunk is too generic → fallback class
    if best_score < 1.2:
        return "general-quantum"

    return best_concept