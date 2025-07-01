from dataclasses import dataclass
from enum import Enum

class PriorityLevel(Enum):
    CRITICAL = 4
    HIGH = 3
    MEDIUM = 2
    LOW = 1

@dataclass
class ServiceProfile:
    service_id: str
    priority: PriorityLevel
    current_tps: float = 0.0
    tps_limit: float = 0.0
    queue_size: int = 0
    error_rate: float = 0.0