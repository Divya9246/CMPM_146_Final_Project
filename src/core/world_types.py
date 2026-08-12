from dataclasses import dataclass

@dataclass
class Cell:
    x: int
    y: int
    elevation: float
    biome: str
    temperature: float
    moisture: float