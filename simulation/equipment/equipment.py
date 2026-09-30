from dataclasses import dataclass, field, asdict
from typing import Dict, Any


@dataclass
class EquipmentState:
    """Runtime state of one simulated piece of equipment."""

    power_on: bool = True
    battery_wh: float = 1000.0
    temperature_c: float = 20.0
    position_x_m: float = 0.0
    position_y_m: float = 0.0
    health: float = 100.0
    active: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Equipment:
    """Static + runtime representation of an equipment object."""

    name: str
    mass_kg: float = 1000.0
    power_w: float = 500.0
    max_speed_m_s: float = 0.1
    battery_capacity_wh: float = 1000.0
    operating_temperature_min_c: float = -40.0
    operating_temperature_max_c: float = 50.0

    # Optional values that can come directly from the data pipeline.
    dimensions_m: Dict[str, float] = field(default_factory=dict)
    specifications: Dict[str, Any] = field(default_factory=dict)

    state: EquipmentState = field(default_factory=EquipmentState)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Equipment":
        """Build an equipment object from a retrieved JSON-like record."""

        state_data = data.pop("state", {}) if isinstance(data, dict) else {}
        allowed = {
            key: value
            for key, value in data.items()
            if key in cls.__dataclass_fields__ and key != "state"
        }

        equipment = cls(**allowed)
        equipment.state = EquipmentState(
            battery_wh=data.get(
                "battery_wh",
                equipment.battery_capacity_wh,
            ),
            **{
                key: value
                for key, value in state_data.items()
                if key in EquipmentState.__dataclass_fields__
                and key != "battery_wh"
            },
        )
        return equipment

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "mass_kg": self.mass_kg,
            "power_w": self.power_w,
            "max_speed_m_s": self.max_speed_m_s,
            "battery_capacity_wh": self.battery_capacity_wh,
            "operating_temperature_min_c": self.operating_temperature_min_c,
            "operating_temperature_max_c": self.operating_temperature_max_c,
            "dimensions_m": self.dimensions_m,
            "specifications": self.specifications,
            "state": self.state.to_dict(),
        }
