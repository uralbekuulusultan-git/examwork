from equipment import DAMAGE_TYPES, Equipment


class Armor(Equipment):
    def __init__(
        self,
        name: str,
        taken_capacity: int,
        defence: int,
        protected_damage_type: str,
        wear_condition: int = 0,
    ) -> None:
        super().__init__(name, taken_capacity, wear_condition)
        self.defence = defence
        self.protected_damage_type = protected_damage_type

    @property
    def defence(self) -> int:
        return self._defence

    @defence.setter
    def defence(self, value: int) -> None:
        if not (1 <= value <= 10):
            raise ValueError("defence должен быть в диапазоне от 1 до 10.")
        self._defence = value

    @property
    def protected_damage_type(self) -> str:
        return self._protected_damage_type

    @protected_damage_type.setter
    def protected_damage_type(self, value: str) -> None:
        if value not in DAMAGE_TYPES:
            raise ValueError(f"Тип защиты должен быть одним из: {', '.join(DAMAGE_TYPES)}")
        self._protected_damage_type = value

    def action(self) -> float:
        super().action()
        result = self.value_with_wear(self.defence)
        print(
            f"  [БРОНЯ] {self.name}: защита {result:.2f} от {self.protected_damage_type} урона."
        )
        return result

    def info(self) -> str:
        return (
            f"{super().info()} | Защита: {self.defence} | "
            f"Тип защиты: {self.protected_damage_type}"
        )
