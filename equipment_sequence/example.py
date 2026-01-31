# pylint: skip-file
from passive_server.passive_equipment import EquipmentPassive
from passive_server import plc_address_operation


class Example(EquipmentPassive):
    def __init__(self, mysql_host: str, database_name: str):
        super().__init__(mysql_host, database_name)

    def _on_rcmd_carrier_in_reply(self, is_allow_carrier_in: int):
        """工厂回复针载具是否可以生产.

        Args:
            is_allow_carrier_in: 是否允许托盘进站.
        """
        self.set_dv_value_with_name("is_allow_carrier_in", int(is_allow_carrier_in))
        self.set_dv_value_with_name("is_allow_carrier_in_reply", True)

    def _on_rcmd_pp_select(self, recipe_name: str):
        """切换配方."""

    def _on_rcmd_stop(self, stop_reason: str):
        """工厂让设备停止."""
        stop_address_info = plc_address_operation.get_address_with_description(self.mysql_secs, "工厂暂停设备")
        self.plc.execute_write(value=1, **stop_address_info)
        reason_address_info = plc_address_operation.get_address_with_description(self.mysql_secs, "工厂暂停原因")
        self.plc.execute_write(value=stop_reason, **reason_address_info)
