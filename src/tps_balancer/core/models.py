from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional

class PriorityLevel(Enum):
    CRITICAL = auto()
    HIGH = auto()
    MEDIUM = auto()
    LOW = auto()

@dataclass
class ServiceProfile:
    service_id: str
    priority: PriorityLevel
    current_tps: float = 0.0
    tps_limit: float = 0.0
    queue_size: int = 0
    error_rate: float = 0.0
    last_updated: Optional[float] = None