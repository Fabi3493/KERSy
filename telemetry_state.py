
from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class TelemetryState:
    # Telemetry (ID 6)
    speed: int = 0
    throttle: float = 0.0
    steer: float = 0.0
    brake: float = 0.0
    gear: int = 0
    rpm: int = 0
    drs_active: int = 0
    tyres_surf: List[Optional[int]] = field(default_factory=lambda: [None, None, None, None])  # RL, RR, FL, FR

    # Status (ID 7)
    fuel_laps: Optional[float] = None
    drs_allowed: int = 0
    ers_j: Optional[float] = None
