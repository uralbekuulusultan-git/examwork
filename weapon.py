import random

from damage import Damage
from equipment import DAMAGE_TYPES, Equipment


class Weapon(Equipment):
    def __init__(
        self,
        name: str,
        taken_capacity: int,
        min_damage: int,
        critical_hit_chance: int,
        damage_type: str,
        wear_condition: int = 0,
    ) -> None:
        super().__init__(name, taken_capacity, wear_condition)
        self.min_damage = min_damage
        self.critical_hit_chance = critical_hit_chance
        self.damage_type = damage_type

    @property
    def min_damage(self) -> int:
        return self._min_damage

    @min_damage.setter
    def min_damage(self, value: int) -> None:
        if not (5 <= value <= 40):
            raise ValueError("min_damage должен быть в диапазоне от 5 до 40.")
        self._min_damage = value

    @property
    def max_damage(self) -> float:
        return self.min_damage * 1.4

    @property
    def critical_hit_chance(self) -> int:
        return self._critical_hit_chance

    @critical_hit_chance.setter
    def critical_hit_chance(self, value: int) -> None:
        if not (1 <= value <= 70):
            raise ValueError("critical_hit_chance должен быть в диапазоне от 1 до 70.")
        self._critical_hit_chance = value

    @property
    def damage_type(self) -> str:
        return self._damage_type

    @damage_type.setter
    def damage_type(self, value: str) -> None:
        if value not in DAMAGE_TYPES:
            raise ValueError(f"damage_type должен быть одним из: {', '.join(DAMAGE_TYPES)}")
        self._damage_type = value

    def action(self) -> Damage:
        super().action()
        damage = random.uniform(self.min_damage, self.max_damage)
        if random.randint(1, 100) <= self.critical_hit_chance:
            damage = self.max_damage * 1.4
            print(f"  [ОРУЖИЕ] {self.name}: критический урон!")
        if random.randint(1, 100) <= 15:
            print(f"  [ОРУЖИЕ] {self.name}: осечка, выстрел не произошёл.")
            damage = 0
        damage = self.value_with_wear(damage)
        print(f"  [ОРУЖИЕ] {self.name}: наносит {damage:.2f} ({self.damage_type}).")
        return Damage(damage, self.damage_type)

    def info(self) -> str:
        return (
            f"{super().info()} | Тип урона: {self.damage_type} | "
            f"Урон: {self.min_damage:.1f}-{self.max_damage:.1f} | "
            f"Шанс крита: {self.critical_hit_chance}%"
        )
