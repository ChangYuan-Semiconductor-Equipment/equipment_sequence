"""将模块从黑盒转移到白盒工位, 包含 AOI 检测."""
from passive_server.passive_equipment import EquipmentPassive


class TransferProduct(EquipmentPassive):
    def __init__(self):
        super().__init__()