from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any

@dataclass
class Equipment:

    name: str

    description: Optional[str] = None

    # Physical dimensions
    length_m: Optional[float] = None
    width_m: Optional[float] = None
    height_m: Optional[float] = None

    # Calculated or directly reported
    volume_m3: Optional[float] = None

    # Mass
    mass_kg: Optional[float] = None

    # Physical properties
    diameter_m: Optional[float] = None
    footprint_m2: Optional[float] = None

    # Operational specifications
    power_w: Optional[float] = None
    voltage_v: Optional[float] = None

    # Environmental information
    operating_temperature_min_c: Optional[float] = None
    operating_temperature_max_c: Optional[float] = None

    # Other specifications
    material: Optional[str] = None
    manufacturer: Optional[str] = None
    mission: Optional[str] = None
    subsystem: Optional[str] = None

    # Source information
    source_url: Optional[str] = None
    source_title: Optional[str] = None

    # Raw extra information
    additional_specs: Optional[Dict[str, Any]] = None

    # Confidence
    ai_extracted: bool = False

    def to_dict(self):
        return asdict(self)