# pylint: skip-file
import asyncio
import json

from passive_server.passive_equipment import EquipmentPassive


class Example(EquipmentPassive):
    """Example class."""

    def __init__(self, mysql_host: str, database_name: str):
        super().__init__(mysql_host, database_name)

    def _on_rcmd_new_lot(self, lot_name: str, lot_quantity: int):
        """开工单.

        Args:
            lot_name: 工单号.
            lot_quantity: 工单数量.
        """
        self.execute_new_lot(lot_name, lot_quantity)
        data = {"new_lot": {"lot_name": lot_name, "lot_quantity": lot_quantity}}
        asyncio.run(self.send_data_to_socket_client(self.socket_server_low, "127.0.0.1", json.dumps(data)))

    def _on_rcmd_pp_select(self, recipe_name: str) -> bool:
        """切换配方.

        Args:
            recipe_name: 配方名称.
        """
        if self.get_ec_value_with_name("is_monitor_plc"):
            self.execute_pp_select(recipe_name)
        self.logger.info("要切换的配方是: %s", recipe_name)
        if self.get_sv_value_with_name("pp_select_state") == 1:
            return True
        return False

    def _on_rcmd_stop(self, stop_reason: str):
        """工厂让设备停止."""
        self.write_plc_with_address_description("工厂暂停设备", 1)
        self.write_plc_with_address_description("工厂暂停原因", stop_reason)

    def _on_rcmd_carrier_in_reply(self, is_allow_carrier_in: int):
        """工厂回复托盘是否可以生产.

        Args:
            is_allow_carrier_in: 是否允许托盘进站.
        """
        self.set_dv_value_with_name("is_allow_carrier_in", int(is_allow_carrier_in))
        self.set_dv_value_with_name("is_allow_carrier_in_reply", True)

    def _on_rcmd_carrier_out_reply(self, is_allow_carrier_out: int):
        """工厂回复托盘是否可以出站.

        Args:
            is_allow_carrier_out: 是否允许托盘进站.
        """
        self.set_dv_value_with_name("is_allow_carrier_out", int(is_allow_carrier_out))
        self.set_dv_value_with_name("is_allow_carrier_out_reply", True)

    def _on_rcmd_product_in_reply(self, is_allow_product_in: int):
        """工厂回复产品是否可以生产.

        Args:
            is_allow_product_in: 是否允许托盘进站.
        """
        self.set_dv_value_with_name("is_allow_product_in", int(is_allow_product_in))
        self.set_dv_value_with_name("is_allow_product_in_reply", True)
