import random

from equipment import Equipment


class Navigator(Equipment):
    def __init__(self, name: str, taken_capacity: int, accuracy: int, wear_condition: int = 0) -> None:
        super().__init__(name, taken_capacity, wear_condition)
        self.accuracy = accuracy

    @property
    def accuracy(self) -> int:
        return self._accuracy

    @accuracy.setter
    def accuracy(self, value: int) -> None:
        if not (5 <= value <= 40):
            raise ValueError("accuracy должен быть в диапазоне от 5 до 40.")
        self._accuracy = value

    def action(self) -> float:
        super().action()
        acc = self.value_with_wear(self.accuracy)
        if random.randint(1, 100) <= 20:
            acc *= 0.5
            print(f"  [НАВИГАТОР] {self.name}: ЭМИ-помехи, эффективность снижена вдвое.")
        print(f"  [НАВИГАТОР] {self.name}: бонус точности {acc:.2f}.")
        return acc

    def info(self) -> str:
        return f"{super().info()} | Точность: +{self.accuracy}"
