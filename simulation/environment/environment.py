from dataclasses import dataclass, asdict
from typing import Dict


@dataclass
class EnvironmentState:
    """Conditions supplied to the simulation from the data layer."""

    body: str = "Mars"
    gravity_m_s2: float = 3.71
    temperature_c: float = -63.0
    pressure_kpa: float = 0.636
    radiation_index: float = 1.0
    solar_flux_w_m2: float = 590.0
    terrain_friction: float = 0.65
    terrain_slope_deg: float = 0.0

    def to_dict(self) -> Dict:
        return asdict(self)


class Environment:
    """Owns the current environmental conditions.

    Later this class can consume the real NASA environment payload
    produced by the data-retrieval pipeline.
    """

    def __init__(self, state: EnvironmentState | None = None):
        self.state = state or EnvironmentState()

    @classmethod
    def from_dict(cls, data: Dict) -> "Environment":
        allowed = {
            key: value
            for key, value in data.items()
            if key in EnvironmentState.__dataclass_fields__
        }
        return cls(EnvironmentState(**allowed))

    def update(self, **changes) -> None:
        for key, value in changes.items():
            if hasattr(self.state, key):
                setattr(self.state, key, value)

    def get_conditions(self) -> Dict:
        return self.state.to_dict()
