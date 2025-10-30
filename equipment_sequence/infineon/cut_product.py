"""打标后下料工位."""
from passive_server.passive_equipment import EquipmentPassive



class CutProduct(EquipmentPassive):
    def __init__(self):
        super().__init__()
