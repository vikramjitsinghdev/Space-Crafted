from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from .environment.environment import Environment, EnvironmentState
from .equipment.equipment import Equipment
from .physics.physics_engine import PhysicsEngine
from .resources.resource_manager import ResourceManager, ResourceState


class Simulator:
    """Main coordinator for the SpaceCrafted simulation prototype.

    Pipeline:

        NASA data
           ↓
        Environment + Equipment
           ↓
        PhysicsEngine
           ↓
        ResourceManager
           ↓
        World state

    The class is intentionally independent from the data-retrieval
    implementation so the two systems can evolve separately.
    """

    def __init__(
        self,
        environment: Environment | None = None,
        equipment: Equipment | None = None,
        resources: ResourceManager | None = None,
    ):
        self.environment = environment or Environment()
        self.equipment = equipment or Equipment(
            name="Prototype Mars Rover",
            mass_kg=1025.0,
            power_w=450.0,
            max_speed_m_s=0.042,
            battery_capacity_wh=5000.0,
            operating_temperature_min_c=-50.0,
            operating_temperature_max_c=50.0,
        )
        self.resources = resources or ResourceManager(
            ResourceState(power_wh=self.equipment.battery_capacity_wh)
        )

        self.physics = PhysicsEngine()
        self.time_seconds = 0.0
        self.tick_count = 0
        self.running = False
        self.events: list[str] = []

    @classmethod
    def from_payload(cls, payload: Dict[str, Any]) -> "Simulator":
        """Create a simulator from a data-layer payload."""

        environment = Environment.from_dict(
            payload.get("environment", {})
        )

        equipment_data = dict(payload.get("equipment", {}))
        equipment = Equipment.from_dict(equipment_data)

        resource_data = payload.get("resources", {})
        resources = ResourceManager(
            ResourceState(
                **{
                    key: value
                    for key, value in resource_data.items()
                    if key in ResourceState.__dataclass_fields__
                }
            )
        )

        return cls(environment, equipment, resources)

    @classmethod
    def from_json(cls, path: str | Path) -> "Simulator":
        path = Path(path)
        with path.open("r", encoding="utf-8") as file:
            return cls.from_payload(json.load(file))

    def start(self) -> None:
        self.running = True
        self.events.append("Simulation started.")

    def stop(self) -> None:
        self.running = False
        self.events.append("Simulation stopped.")

    def step(
        self,
        dt_seconds: float = 1.0,
        throttle: float = 0.0,
        direction=(1.0, 0.0),
    ) -> Dict[str, Any]:

        if not self.running:
            self.start()

        result = self.physics.step(
            equipment=self.equipment,
            environment=self.environment,
            dt_seconds=dt_seconds,
            throttle=throttle,
            direction=direction,
        )

        consumed = self.resources.consume_power(result.energy_used_wh)

        self.equipment.state.position_x_m += result.dx_m
        self.equipment.state.position_y_m += result.dy_m
        self.equipment.state.battery_wh = self.resources.state.power_wh
        self.equipment.state.temperature_c += result.thermal_change_c
        self.equipment.state.health = max(
            0.0,
            min(100.0, self.equipment.state.health + result.health_change),
        )

        self.time_seconds += dt_seconds
        self.tick_count += 1

        self._update_resources(dt_seconds)
        self._check_events()

        return self.world_state(last_energy_used_wh=consumed)

    def _update_resources(self, dt_seconds: float) -> None:
        # Placeholder crew/life-support consumption.
        # Keep these numbers soft-coded until the AI mission model exists.
        self.resources.consume(
            oxygen_kg=0.00001 * dt_seconds,
            water_kg=0.00002 * dt_seconds,
            food_kg=0.00001 * dt_seconds,
        )

    def _check_events(self) -> None:
        if self.equipment.state.battery_wh <= 0:
            self.equipment.state.power_on = False
            self.equipment.state.active = False
            self.events.append("CRITICAL: rover power depleted.")

        critical = self.resources.critical_resources()
        for resource in critical:
            message = f"WARNING: low {resource}."
            if message not in self.events[-3:]:
                self.events.append(message)

        if self.equipment.state.health <= 0:
            self.equipment.state.active = False
            self.events.append("CRITICAL: equipment health reached zero.")

    def world_state(self, last_energy_used_wh: float = 0.0) -> Dict[str, Any]:
        return {
            "simulation": {
                "time_seconds": round(self.time_seconds, 2),
                "tick": self.tick_count,
                "running": self.running,
            },
            "environment": self.environment.get_conditions(),
            "equipment": self.equipment.to_dict(),
            "resources": self.resources.status(),
            "last_step": {
                "energy_used_wh": round(last_energy_used_wh, 6),
            },
            "events": self.events[-10:],
        }


def demo() -> None:
    """Run a tiny command-line demonstration."""

    simulator = Simulator()
    simulator.start()

    print("\n=== SPACECRAFTED SIMULATION PROTOTYPE ===")

    for second in range(10):
        state = simulator.step(
            dt_seconds=1.0,
            throttle=0.75,
            direction=(1.0, 0.2),
        )

        rover = state["equipment"]["state"]

        print(
            f"t={second + 1:02d}s | "
            f"pos=({rover['position_x_m']:.3f}, "
            f"{rover['position_y_m']:.3f}) m | "
            f"battery={rover['battery_wh']:.2f} Wh | "
            f"temp={rover['temperature_c']:.2f} C | "
            f"health={rover['health']:.2f}%"
        )

    print("\nResources:")
    print(json.dumps(simulator.resources.status(), indent=2))

    print("\nEvents:")
    for event in simulator.events:
        print("-", event)


if __name__ == "__main__":
    demo()
