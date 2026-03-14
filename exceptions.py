class EquipmentWornOutError(Exception):
    """Raised when equipment is fully worn out and can no longer be used."""


class FreeSlotError(ValueError):
    """Raised when there are no free slots for equipment."""


class TotalVolumeError(ValueError):
    """Raised when total equipment capacity exceeds spaceship spaciousness."""
