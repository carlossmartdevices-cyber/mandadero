from dataclasses import dataclass

@dataclass
class User:
    """User model."""
    id: int
    username: str