from dataclasses import dataclass


@dataclass
class Damage:
    amount: float
    damage_type: str
