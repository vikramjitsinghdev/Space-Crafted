from dataclasses import dataclass, asdict
from typing import Dict


@dataclass
class ResourceState:
    """Mission resources available to the simulation."""

    power_wh: float = 5000.0
    oxygen_kg: float = 20.0
    water_kg: float = 50.0
    food_kg: float = 30.0

    def to_dict(self) -> Dict[str, float]:
        return asdict(self)


class ResourceManager:
    """Tracks consumable mission resources."""

    def __init__(self, state: ResourceState | None = None):
        self.state = state or ResourceState()

    def consume_power(self, amount_wh: float) -> float:
        consumed = min(max(amount_wh, 0.0), self.state.power_wh)
        self.state.power_wh -= consumed
        return consumed

    def consume(self, oxygen_kg=0.0, water_kg=0.0, food_kg=0.0) -> None:
        self.state.oxygen_kg = max(0.0, self.state.oxygen_kg - oxygen_kg)
        self.state.water_kg = max(0.0, self.state.water_kg - water_kg)
        self.state.food_kg = max(0.0, self.state.food_kg - food_kg)

    def status(self) -> Dict[str, float]:
        return self.state.to_dict()

    def critical_resources(self) -> list[str]:
        thresholds = {
            "power_wh": 0.10,
            "oxygen_kg": 0.15,
            "water_kg": 0.15,
            "food_kg": 0.15,
        }

        current = self.status()
        critical = []

        for name, ratio in thresholds.items():
            initial = {
                "power_wh": 5000.0,
                "oxygen_kg": 20.0,
                "water_kg": 50.0,
                "food_kg": 30.0,
            }[name]

            if current[name] <= initial * ratio:
                critical.append(name)

        return critical
