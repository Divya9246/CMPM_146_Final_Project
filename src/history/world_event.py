from dataclasses import dataclass
from typing import Optional, Tuple, Any


@dataclass
class WorldEvent:
    year: int
    event_type: str
    description: str
    location: Optional[Tuple[int, int]] = None
    cause: Optional[str] = None
    data: Any = None