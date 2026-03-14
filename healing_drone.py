from equipment import Equipment
from exceptions import EquipmentWornOutError


class HealingDrone(Equipment):
    def __init__(self, name: str, taken_capacity: int, efficiency: int, wear_condition: int = 0) -> None:
        super().__init__(name, taken_capacity, wear_condition)
        self.efficiency = efficiency

    @property
    def efficiency(self) -> int:
        return self._efficiency

    @efficiency.setter
    def efficiency(self, value: int) -> None:
        if not (50 <= value <= 200):
            raise ValueError("efficiency должен быть в диапазоне от 50 до 200.")
        self._efficiency = value

    def action(self, electromagnetic_damage: float) -> float:
        if self.wear_condition >= 100:
            raise EquipmentWornOutError(f"{self.name}: дрон полностью изношен.")
        self.wear_condition = min(100, self.wear_condition + 20)
        healed = self.value_with_wear(electromagnetic_damage * self.efficiency / 100)
        print(f"  [ДРОН] {self.name}: восстановил {healed:.2f} единиц состояния.")
        return healed

    def info(self) -> str:
        return f"{super().info()} | Эффективность: {self.efficiency}%"
