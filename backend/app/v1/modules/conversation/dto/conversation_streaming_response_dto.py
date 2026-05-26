from dataclasses import dataclass

@dataclass
class StreamingResponseDto:
    message: str
    response: str