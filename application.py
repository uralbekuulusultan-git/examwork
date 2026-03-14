import random
from typing import List

from armor import Armor
from equipment import DAMAGE_TYPES, Equipment
from exceptions import FreeSlotError, TotalVolumeError
from healing_drone import HealingDrone
from navigator import Navigator
from spaceship import Spaceship
from weapon import Weapon


class Application:
    def __init__(self) -> None:
        self.round_limit = 20

    def _generate_weapons(self, count: int = 20) -> List[Weapon]:
        weapons = []
        for i in range(count):
            weapons.append(
                Weapon(
                    name=f"Орудие-{i+1}",
                    taken_capacity=random.randint(30, 100),
                    min_damage=random.randint(5, 40),
                    critical_hit_chance=random.randint(1, 70),
                    damage_type=random.choice(DAMAGE_TYPES),
                )
            )
        return weapons

    def _generate_armors(self, count: int = 20) -> List[Armor]:
        armors = []
        for i in range(count):
            armors.append(
                Armor(
                    name=f"Броня-{i+1}",
                    taken_capacity=random.randint(30, 100),
                    defence=random.randint(1, 10),
                    protected_damage_type=random.choice(DAMAGE_TYPES),
                )
            )
        return armors

    def _generate_navigators(self, count: int = 20) -> List[Navigator]:
        return [
            Navigator(
                name=f"Навигатор-{i+1}",
                taken_capacity=random.randint(30, 100),
                accuracy=random.randint(5, 40),
            )
            for i in range(count)
        ]

    def _generate_drones(self, count: int = 20) -> List[HealingDrone]:
        return [
            HealingDrone(
                name=f"Дрон-{i+1}",
                taken_capacity=random.randint(30, 100),
                efficiency=random.randint(50, 200),
            )
            for i in range(count)
        ]

    def _generate_ship(self, name: str) -> Spaceship:
        return Spaceship(
            name=name,
            spaciousness=random.randint(300, 1000),
            accuracy=random.randint(0, 5),
            armor_slots=random.randint(1, 3),
            weapon_slots=random.randint(1, 4),
            navigator_slots=random.randint(1, 2),
            drone_slots=random.randint(0, 2),
        )

    @staticmethod
    def _fill_ship(ship: Spaceship, equipment_list: List[Equipment], expected_type: type) -> None:
        for equipment in equipment_list:
            if not isinstance(equipment, expected_type):
                continue
            try:
                ship.install_equipment(equipment)
            except (FreeSlotError, TotalVolumeError, ValueError) as exc:
                print(f"[ПРЕДУПРЕЖДЕНИЕ] {exc}")

            if (
                (expected_type is Weapon and len(ship.weapons) >= ship.weapon_slots)
                or (expected_type is Armor and len(ship.armors) >= ship.armor_slots)
                or (expected_type is Navigator and len(ship.navigators) >= ship.navigator_slots)
                or (expected_type is HealingDrone and len(ship.drones) >= ship.drone_slots)
            ):
                break

    def run(self) -> None:
        print("\n=== Запуск симуляции: Космический бой ===")

        weapons = self._generate_weapons()
        armors = self._generate_armors()
        navigators = self._generate_navigators()
        drones = self._generate_drones()

        ship1 = self._generate_ship("Крейсер-Альфа")
        ship2 = self._generate_ship("Крейсер-Омега")

        for ship in (ship1, ship2):
            print(f"\n[КОРАБЛЬ] Компоновка корабля: {ship.name}")
            self._fill_ship(ship, weapons, Weapon)
            self._fill_ship(ship, armors, Armor)
            self._fill_ship(ship, navigators, Navigator)
            self._fill_ship(ship, drones, HealingDrone)
            print(ship.info())

        attacker, defender = ship1, ship2

        for round_num in range(1, self.round_limit + 1):
            print(f"\n{'=' * 20} РАУНД {round_num} {'=' * 20}")
            print(f"Ход атакующего: {attacker.name}")
            attacker.attack(defender)
            print(defender.info())

            if defender.is_destroyed():
                print(f"\n[ФИНАЛ] Победа! Корабль {defender.name} уничтожен.")
                print(f"[ПОБЕДИТЕЛЬ] {attacker.name}")
                return

            attacker, defender = defender, attacker

        print("\n[ФИНАЛ] Лимит раундов достигнут.")
        if ship1.health > ship2.health:
            winner = ship1
        elif ship2.health > ship1.health:
            winner = ship2
        else:
            winner = None

        if winner:
            print(f"[ПОБЕДИТЕЛЬ] {winner.name} по лучшему техническому состоянию.")
        else:
            print("[НИЧЬЯ] Оба корабля в одинаковом техническом состоянии.")
