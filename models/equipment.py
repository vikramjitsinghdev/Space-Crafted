from dataclasses import dataclass, field, asdict
from typing import Optional, Any


@dataclass
class Source:
    title: str
    url: Optional[str] = None
    source_type: str = "unknown"


@dataclass
class Equipment:

    name: str

    description: Optional[str] = None

    # -------------------------
    # Identity
    # -------------------------

    mission: Optional[str] = None
    manufacturer: Optional[str] = None
    subsystem: Optional[str] = None
    category: Optional[str] = None

    # -------------------------
    # Physical
    # -------------------------

    mass_kg: Optional[float] = None

    length_m: Optional[float] = None
    width_m: Optional[float] = None
    height_m: Optional[float] = None

    diameter_m: Optional[float] = None

    volume_m3: Optional[float] = None
    footprint_m2: Optional[float] = None

    # -------------------------
    # Electrical
    # -------------------------

    power_w: Optional[float] = None
    voltage_v: Optional[float] = None

    # -------------------------
    # Thermal
    # -------------------------

    operating_temperature_min_c: Optional[float] = None
    operating_temperature_max_c: Optional[float] = None

    # -------------------------
    # Materials
    # -------------------------

    materials: list[str] = field(default_factory=list)

    # -------------------------
    # Other specifications
    # -------------------------

    specifications: dict[str, Any] = field(
        default_factory=dict
    )

    # -------------------------
    # Provenance
    # -------------------------

    sources: list[Source] = field(
        default_factory=list
    )

    extraction_methods: list[str] = field(
        default_factory=list
    )

    ai_extracted: bool = False

    confidence: Optional[float] = None

    def to_dict(self):
        return asdict(self)