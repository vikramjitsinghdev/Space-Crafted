from dataclasses import dataclass
import math

from ..environment import Environment
from ..equipment import Equipment


@dataclass
class PhysicsResult:
    """Calculated effects for one simulation step."""

    dx_m: float = 0.0
    dy_m: float = 0.0
    energy_used_wh: float = 0.0
    thermal_change_c: float = 0.0
    health_change: float = 0.0


class PhysicsEngine:
    """Small deterministic physics layer for the prototype.

    This is deliberately simple:
      - gravity affects required movement energy
      - slope increases movement cost
      - terrain friction reduces practical speed
      - temperature outside equipment limits damages health
      - radiation slowly damages health
      - active equipment consumes power

    These formulas are placeholders, not mission-grade physics.
    """

    def step(
        self,
        equipment: Equipment,
        environment: Environment,
        dt_seconds: float,
        throttle: float = 0.0,
        direction=(1.0, 0.0),
    ) -> PhysicsResult:

        throttle = max(0.0, min(1.0, throttle))
        dx, dy = direction

        magnitude = math.hypot(dx, dy)
        if magnitude == 0:
            dx, dy = 0.0, 0.0
        else:
            dx, dy = dx / magnitude, dy / magnitude

        env = environment.state
        speed = (
            equipment.max_speed_m_s
            * throttle
            * max(0.05, 1.0 - env.terrain_slope_deg / 90.0)
            * max(0.05, env.terrain_friction)
        )

        distance = speed * dt_seconds
        movement_energy = (
            equipment.mass_kg
            * env.gravity_m_s2
            * distance
            * (1.0 + env.terrain_slope_deg / 45.0)
            / 3600.0
            * 0.002
        )

        idle_energy = equipment.power_w * dt_seconds / 3600.0
        energy_used = max(0.0, idle_energy + movement_energy)

        thermal_target = env.temperature_c + 35.0
        thermal_change = (thermal_target - equipment.state.temperature_c) * 0.02
        thermal_change *= dt_seconds

        health_change = 0.0

        if env.temperature_c < equipment.operating_temperature_min_c:
            health_change -= 0.02 * dt_seconds
        elif env.temperature_c > equipment.operating_temperature_max_c:
            health_change -= 0.02 * dt_seconds

        health_change -= env.radiation_index * 0.001 * dt_seconds

        return PhysicsResult(
            dx_m=dx * distance,
            dy_m=dy * distance,
            energy_used_wh=energy_used,
            thermal_change_c=thermal_change,
            health_change=health_change,
        )
