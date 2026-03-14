from exceptions import EquipmentWornOutError

DAMAGE_TYPES = ("laser", "fragmentation", "electromagnetic", "plasma")


class Equipment:
    def __init__(self, name: str, taken_capacity: int, wear_condition: int = 0) -> None:
        self.name = name
        self.wear_condition = wear_condition
        self.taken_capacity = taken_capacity

    @property
    def wear_condition(self) -> int:
        return self._wear_condition

    @wear_condition.setter
    def wear_condition(self, value: int) -> None:
        if not (0 <= value <= 100):
            raise ValueError("wear_condition должен быть в диапазоне от 0 до 100.")
        self._wear_condition = value

    @property
    def taken_capacity(self) -> int:
        return self._taken_capacity

    @taken_capacity.setter
    def taken_capacity(self, value: int) -> None:
        if not (30 <= value <= 100):
            raise ValueError("taken_capacity должен быть в диапазоне от 30 до 100.")
        self._taken_capacity = value

    def action(self) -> None:
        if self.wear_condition >= 100:
            raise EquipmentWornOutError(f"{self.name}: оборудование полностью изношено.")
        self.wear_condition = min(100, self.wear_condition + 10)

    def value_with_wear(self, value: float) -> float:
        return value - value * self.wear_condition / 100

    def info(self) -> str:
        return f"{self.name} | Изношенность: {self.wear_condition}%"
