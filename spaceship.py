import random
from typing import List

from armor import Armor
from damage import Damage
from exceptions import EquipmentWornOutError, FreeSlotError, TotalVolumeError
from healing_drone import HealingDrone
from navigator import Navigator
from weapon import Weapon


class Spaceship:
    def __init__(
        self,
        name: str,
        spaciousness: int,
        accuracy: int,
        armor_slots: int,
        weapon_slots: int,
        navigator_slots: int,
        drone_slots: int,
        health: float = 1000,
    ) -> None:
        self.name = name
        self.spaciousness = spaciousness
        self.accuracy = accuracy
        self.armor_slots = armor_slots
        self.weapon_slots = weapon_slots
        self.navigator_slots = navigator_slots
        self.drone_slots = drone_slots
        self.health = max(0, health)

        self.armors: List[Armor] = []
        self.weapons: List[Weapon] = []
        self.navigators: List[Navigator] = []
        self.drones: List[HealingDrone] = []

    @property
    def spaciousness(self) -> int:
        return self._spaciousness

    @spaciousness.setter
    def spaciousness(self, value: int) -> None:
        if not (300 <= value <= 1000):
            raise ValueError("spaciousness должен быть в диапазоне от 300 до 1000.")
        self._spaciousness = value

    @property
    def accuracy(self) -> int:
        return self._accuracy

    @accuracy.setter
    def accuracy(self, value: int) -> None:
        if not (0 <= value <= 5):
            raise ValueError("Базовая accuracy должна быть в диапазоне от 0 до 5.")
        self._accuracy = value

    @property
    def armor_slots(self) -> int:
        return self._armor_slots

    @armor_slots.setter
    def armor_slots(self, value: int) -> None:
        if not (1 <= value <= 3):
            raise ValueError("armor_slots должен быть в диапазоне от 1 до 3.")
        self._armor_slots = value

    @property
    def weapon_slots(self) -> int:
        return self._weapon_slots

    @weapon_slots.setter
    def weapon_slots(self, value: int) -> None:
        if not (1 <= value <= 4):
            raise ValueError("weapon_slots должен быть в диапазоне от 1 до 4.")
        self._weapon_slots = value

    @property
    def navigator_slots(self) -> int:
        return self._navigator_slots

    @navigator_slots.setter
    def navigator_slots(self, value: int) -> None:
        if not (1 <= value <= 2):
            raise ValueError("navigator_slots должен быть в диапазоне от 1 до 2.")
        self._navigator_slots = value

    @property
    def drone_slots(self) -> int:
        return self._drone_slots

    @drone_slots.setter
    def drone_slots(self, value: int) -> None:
        if not (0 <= value <= 2):
            raise ValueError("drone_slots должен быть в диапазоне от 0 до 2.")
        self._drone_slots = value

    @property
    def base_defence(self) -> float:
        return (1 / (self.spaciousness * self.armor_slots)) * 10**4

    def _used_capacity(self) -> int:
        return sum(e.taken_capacity for e in [*self.armors, *self.weapons, *self.navigators, *self.drones])

    def _check_capacity(self, equipment) -> None:
        if self._used_capacity() + equipment.taken_capacity > self.spaciousness:
            raise TotalVolumeError(
                f"{self.name}: объём превышен ({self._used_capacity()} + {equipment.taken_capacity} > {self.spaciousness})."
            )

    def install_equipment(self, equipment) -> None:
        self._check_capacity(equipment)

        if isinstance(equipment, Armor):
            if len(self.armors) >= self.armor_slots:
                raise FreeSlotError(f"{self.name}: нет свободных слотов под броню.")
            self.armors.append(equipment)

        elif isinstance(equipment, Weapon):
            if len(self.weapons) >= self.weapon_slots:
                raise FreeSlotError(f"{self.name}: нет свободных слотов под оружие.")
            self.weapons.append(equipment)

        elif isinstance(equipment, Navigator):
            if len(self.navigators) >= self.navigator_slots:
                raise FreeSlotError(f"{self.name}: нет свободных слотов под навигатор.")
            self.navigators.append(equipment)

        elif isinstance(equipment, HealingDrone):
            if len(self.drones) >= self.drone_slots:
                raise FreeSlotError(f"{self.name}: нет свободных слотов под дроны.")
            self.drones.append(equipment)

        else:
            raise ValueError("Неизвестный тип оборудования.")

        print(f"[УСТАНОВКА] {self.name}: установлено оборудование -> {equipment.name}")

    def _total_accuracy(self) -> float:
        total = self.accuracy
        for navigator in self.navigators:
            try:
                total += navigator.action()
            except EquipmentWornOutError as exc:
                print(f"  [ОШИБКА] {exc}")
        return min(100, total)

    def attack(self, target: "Spaceship") -> None:
        print(f"\n[АТАКА] {self.name} начинает атаку по {target.name}!")
        for weapon in self.weapons:
            try:
                final_accuracy = self._total_accuracy()
                roll = random.randint(1, 100)
                print(
                    f"  [ПРИЦЕЛ] Итоговая точность: {final_accuracy:.2f}. Бросок: {roll}."
                )
                if roll <= final_accuracy:
                    damage = weapon.action()
                    target.defend(damage)
                else:
                    print(f"  [ПРОМАХ] {self.name}: {weapon.name} промахнулся.")
            except EquipmentWornOutError as exc:
                print(f"  [ОШИБКА] {exc}")

    def defend(self, damage: Damage) -> None:
        print(
            f"[ОБОРОНА] {self.name}: входящий урон {damage.amount:.2f} ({damage.damage_type})."
        )

        total_defence = self.base_defence
        print(f"  [КОРПУС] Базовая защита: {self.base_defence:.2f}")

        for armor in self.armors:
            if armor.protected_damage_type != damage.damage_type:
                continue
            try:
                total_defence += armor.action()
            except EquipmentWornOutError as exc:
                print(f"  [ОШИБКА] {exc}")

        actual_damage = max(0.0, damage.amount - total_defence)
        self.health = max(0.0, self.health - actual_damage)
        print(
            f"  [ИТОГ] Общая защита: {total_defence:.2f}. "
            f"Полученный урон: {actual_damage:.2f}. Текущее состояние: {self.health:.2f}."
        )

        if damage.damage_type == "electromagnetic" and damage.amount > 0:
            for drone in self.drones:
                try:
                    healed = drone.action(damage.amount)
                    self.health = min(1000.0, self.health + healed)
                except EquipmentWornOutError as exc:
                    print(f"  [ОШИБКА] {exc}")
            print(f"  [ПОСЛЕ ДРОНОВ] Текущее состояние: {self.health:.2f}")

    def is_destroyed(self) -> bool:
        return self.health <= 0

    def info(self) -> str:
        lines = [
            f"\n=== {self.name} ===",
            f"Состояние: {self.health:.2f}",
            f"Вместительность: {self.spaciousness} ({self._used_capacity()} занято)",
            f"Базовая защита: {self.base_defence:.2f}",
            f"Базовая точность: {self.accuracy}",
            "-- Оружие --",
        ]
        lines.extend([f"  * {item.info()}" for item in self.weapons] or ["  * нет"])
        lines.append("-- Броня --")
        lines.extend([f"  * {item.info()}" for item in self.armors] or ["  * нет"])
        lines.append("-- Навигаторы --")
        lines.extend([f"  * {item.info()}" for item in self.navigators] or ["  * нет"])
        lines.append("-- Дроны --")
        lines.extend([f"  * {item.info()}" for item in self.drones] or ["  * нет"])
        return "\n".join(lines)
