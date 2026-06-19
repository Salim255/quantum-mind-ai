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
    "spin": {
        "anchors": [
            "spin", "spin state", "spin up", "spin down",
            "stern-gerlach", "quantum clock"
        ],
        "keywords_soft": [
            "angular momentum",
            "spin measurement"
        ]
    },

    "measurement": {
        "anchors": [
            "measurement",
            "measurements",
            "observable",
            "measurement basis",
            "same direction",
            "different directions"
        ],
        "keywords_soft": [
            "collapse",
            "measurement outcome",
            "state reduction"
        ]
    },

    "linear-algebra": {
        "anchors": [
            "vector", "vectors",
            "matrix", "matrices",
            "basis", "bases",
            "orthogonal",
            "orthonormal",
            "unitary",
            "bra", "ket",
            "bra-ket",
            "inner product",
            "tensor product",
            "state vector"
        ],
        "keywords_soft": [
            "linear combination",
            "vector space",
            "complex numbers"
        ]
    },

    "qubits": {
        "anchors": [
            "qubit", "qubits",
            "quantum state",
            "state vector",
            "basis state",
            "bloch sphere"
        ],
        "keywords_soft": [
            "two-level system",
            "superposition"
        ]
    },

    "probability-and-interference": {
        "anchors": [
            "probability",
            "probability amplitude",
            "interference",
            "randomness"
        ],
        "keywords_soft": [
            "amplitude",
            "quantum probability"
        ]
    },

    "polarization": {
        "anchors": [
            "photon",
            "photons",
            "polarization",
            "polarized filter",
            "polarized filters"
        ],
        "keywords_soft": [
            "polarized light"
        ]
    },

    "quantum-cryptography": {
        "anchors": [
            "bb84",
            "ekert",
            "quantum key distribution",
            "qkd",
            "alice",
            "bob",
            "eve"
        ],
        "keywords_soft": [
            "secure communication",
            "cryptography"
        ]
    },

    "entanglement": {
        "anchors": [
            "entanglement",
            "entangled",
            "bell state",
            "epr",
            "tensor product"
        ],
        "keywords_soft": [
            "nonlocal correlation",
            "spooky action",
            "linked qubits"
        ]
    },

    "bells-inequality": {
        "anchors": [
            "bell inequality",
            "bell's inequality",
            "local realism",
            "hidden variables"
        ],
        "keywords_soft": [
            "einstein",
            "classical explanation",
            "local hidden variables"
        ]
    },

    "quantum-gates": {
        "anchors": [
            "quantum gate",
            "cnot",
            "controlled not",
            "hadamard",
            "pauli",
            "universal quantum gates"
        ],
        "keywords_soft": [
            "unitary operation",
            "gate operation"
        ]
    },

    "quantum-circuits": {
        "anchors": [
            "quantum circuit",
            "bell circuit",
            "circuit model"
        ],
        "keywords_soft": [
            "quantum computation",
            "circuit"
        ]
    },

    "teleportation": {
        "anchors": [
            "teleportation",
            "quantum teleportation",
            "teleport quantum state"
        ],
        "keywords_soft": [
            "state transfer"
        ]
    },

    "superdense-coding": {
        "anchors": [
            "superdense coding",
            "superdense",
            "dense coding"
        ],
        "keywords_soft": [
            "send two bits",
            "one qubit encoding"
        ]
    },

    "error-correction": {
        "anchors": [
            "error correction",
            "quantum error correction"
        ],
        "keywords_soft": [
            "fault tolerance",
            "error recovery"
        ]
    },

    "no-cloning": {
        "anchors": [
            "no cloning theorem",
            "no-cloning theorem"
        ],
        "keywords_soft": [
            "cannot copy quantum state",
            "cloning quantum states"
        ]
    },

    "quantum-algorithms": {
        "anchors": [
            "quantum algorithm",
            "deutsch algorithm",
            "deutsch-jozsa",
            "simon algorithm",
            "shor algorithm",
            "grover algorithm",
            "qft",
            "quantum fourier transform"
        ],
        "keywords_soft": [
            "speedup",
            "factoring",
            "search algorithm"
        ]
    },

    "complexity-theory": {
        "anchors": [
            "complexity class",
            "complexity classes",
            "query complexity",
            "p",
            "np"
        ],
        "keywords_soft": [
            "computational complexity"
        ]
    },

    "quantum-computing": {
        "anchors": [
            "quantum computing",
            "quantum computer",
            "quantum computation",
            "quantum advantage",
            "quantum supremacy"
        ],
        "keywords_soft": [
            "quantum processor"
        ]
    },

    "quantum-hardware": {
        "anchors": [
            "quantum hardware",
            "hardware",
            "quantum processor"
        ],
        "keywords_soft": [
            "physical qubits",
            "hardware implementation"
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