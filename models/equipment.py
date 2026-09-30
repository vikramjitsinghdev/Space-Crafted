from dataclasses import dataclass, field, asdict
from typing import Optional, Any


@dataclass
class Source:
    title: str
    url: Optional[str] = None
    source_type: str = "unknown"
    page: Optional[int] = None
    citation_id: Optional[str] = None


@dataclass
class Provenance:
    value: Any
    unit: Optional[str] = None

    # NASA_OFFICIAL
    # NASA_DOCUMENT
    # NASA_DATASET
    # AI_EXTRACTED
    # CALCULATED
    # ESTIMATED
    provenance_type: str = "unknown"

    source_title: Optional[str] = None
    source_url: Optional[str] = None
    page: Optional[int] = None
    evidence: Optional[str] = None


@dataclass
class Equipment:
    name: str

    description: Optional[str] = None
    mission: Optional[str] = None
    manufacturer: Optional[str] = None

    category: Optional[str] = None
    subsystem: Optional[str] = None

    # Physical
    mass_kg: Optional[float] = None
    length_m: Optional[float] = None
    width_m: Optional[float] = None
    height_m: Optional[float] = None
    diameter_m: Optional[float] = None

    # Electrical
    power_w: Optional[float] = None
    voltage_v: Optional[float] = None

    # Thermal
    operating_temperature_min_c: Optional[float] = None
    operating_temperature_max_c: Optional[float] = None

    # Materials
    materials: list[str] = field(default_factory=list)

    # Other specifications
    specifications: dict[str, Any] = field(default_factory=dict)

    # Derived values
    calculated: dict[str, Any] = field(default_factory=dict)

    # Sources
    sources: list[Source] = field(default_factory=list)

    # Field-level provenance
    provenance: dict[str, Provenance] = field(default_factory=dict)

    # Extraction information
    extraction_methods: list[str] = field(default_factory=list)

    ai_extracted: bool = False

    confidence: Optional[float] = None

    def to_dict(self):
        return asdict(self)