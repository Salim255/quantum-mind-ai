import re
from difflib import SequenceMatcher


# --- Concept knowledge base (semantic anchors, not just keywords) ---
CONCEPTS = {
    "entanglement": {
        "anchors": [
            "entanglement", "entangled", "bell state", "bell inequality",
            "non-local correlation", "quantum correlation", "epr"
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
            "send two bits using one qubit"
        ]
    },

    "qubits": {
        "anchors": [
            "qubit", "qubits", "quantum bit", "bloch sphere", "state vector"
        ],
        "keywords_soft": [
            "two-level system", "quantum state representation"
        ]
    },

    "algorithms": {
        "anchors": [
            "grover", "shor", "qft", "quantum algorithm", "fourier transform"
        ],
        "keywords_soft": [
            "speedup", "factoring", "search algorithm"
        ]
    },

    "quantum-fundamentals": {
        "anchors": [
            "superposition", "measurement", "decoherence", "collapse"
        ],
        "keywords_soft": [
            "wave function", "probability amplitude"
        ]
    },

    "quantum-computing": {
        "anchors": [
            "quantum computing", "quantum computer", "quantum advantage", "supremacy"
        ],
        "keywords_soft": [
            "quantum processor", "n qubit system"
        ]
    }
}


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower().strip())


# --- scoring function ---
def score_concept(query: str, concept_data: dict) -> float:
    q = normalize(query)

    score = 0.0

    # 1. exact anchor match (strong signal)
    for a in concept_data["anchors"]:
        if a in q:
            score += 3.0

    # 2. soft semantic match
    for s in concept_data["keywords_soft"]:
        if s in q:
            score += 1.5

    # 3. fuzzy similarity boost (handles paraphrases)
    for a in concept_data["anchors"]:
        score = max(score, SequenceMatcher(None, q, a).ratio() * 2.5)

    return score

def detect_concept(text: str) -> str:
    q = normalize(text)

    best_concept = "general-quantum"
    best_score = 0.0

    for concept, data in CONCEPTS.items():
        s = score_concept(q, data)

        if s > best_score:
            best_score = s
            best_concept = concept

    # --- safety thresholds ---
    if best_score < 1.2:
        return "general-quantum"

    return best_concept