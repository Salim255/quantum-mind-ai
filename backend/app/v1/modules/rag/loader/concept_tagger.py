def detect_concept(text: str) -> str:
    text = text.lower()

    if "entanglement" in text:
        return "entanglement"

    if "teleportation" in text:
        return "teleportation"

    if "superdense" in text:
        return "superdense-coding"

    if "qubit" in text:
        return "qubits"

    return "general-quantum"