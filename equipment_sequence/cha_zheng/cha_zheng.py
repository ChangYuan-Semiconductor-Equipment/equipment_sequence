# pylint: skip-file
import json

from socket_cyg.socket_client import SocketClient

from passive_server.passive_equipment import EquipmentPassive
from passive_server import plc_address_operation, models_class


class ChaZheng(EquipmentPassive):
    def __init__(self, mysql_host: str, database_name: str):
        super().__init__(mysql_host, database_name)
        self.scan_client = SocketClient("192.168.6.6", 9102)

    def trigger_scan(self, callback: dict):
        """触发扫码, 扫到码后请求针载具是否可做, 扫码失败则不用请求."""
        if self.scan_client.connect():
            result = self.scan_client.send_data(b"TRIGGER")
            if result[0]:
                pin_carrier_code = result[1]
                self.set_dv_value_with_name("pin_carrier_code", pin_carrier_code)
                self.send_s6f11("pin_carrier_in_request")
            else:
                self.logger.warning("扫码枪未在 3 秒内扫到码")
                if self.scan_client.connect():
                    self.scan_client.send_data(b"RELEASE", False)
                self.set_dv_value_with_name("is_allow_pin_carrier", 2)
                self.set_dv_value_with_name("is_allow_pin_carrier_reply", True)
        else:
            self.logger.warning("扫码枪连接失败")
            self.set_dv_value_with_name("is_allow_pin_carrier", 2)
            self.set_dv_value_with_name("is_allow_pin_carrier_reply", True)

    def _on_rcmd_pin_carrier_in_reply(self, is_allow_pin_carrier: int):
        """工厂回复针载具是否可以生产.

        Args:
            is_allow_pin_carrier: 针载具是否可以生产.
        """
        if str(is_allow_pin_carrier) == 2:
            is_allow_pin_carrier = 3
        self.set_dv_value_with_name("is_allow_pin_carrier", int(is_allow_pin_carrier))
        self.set_dv_value_with_name("is_allow_pin_carrier_reply", True)

    def _on_rcmd_pp_select(self, recipe_name: str):
        """切换配方."""

    def _on_rcmd_stop(self, stop_reason: str):
        """工厂让设备停止."""
        stop_address_info = plc_address_operation.get_address_with_description(self.mysql_secs, "工厂暂停设备")
        self.plc.execute_write(value=1, **stop_address_info)
        reason_address_info = plc_address_operation.get_address_with_description(self.mysql_secs, "工厂暂停原因")
        self.plc.execute_write(value=stop_reason, **reason_address_info)

    def read_multiple_address(self, start_address: int, end_address: int, one_read_count: int = 100) -> list:
        """读取连续地址数据.

        Args:
            start_address: 开始地址.
            end_address: 结束的下一个地址.
            one_read_count: 每次读取的 word 个数, 默认一次读 100 个.
        """
        first_read_start = start_address
        results = []  # 保存读取结果
        expect_read_count = (end_address - first_read_start - 2) // 2
        range_num = expect_read_count // one_read_count + 1
        for _ in range(range_num):
            if (end_address - start_address) < one_read_count:
                one_read_count = (end_address - start_address - 2) // 2
            values = self.plc.read_multiple(start_address // 2, one_read_count)
            results += values
            start_address = 2 * one_read_count + start_address
            if start_address >= end_address - 2:
                break
        self.logger.info("实际读取结果个数 %s, 预期去读结果个数 %s", len(results), expect_read_count)
        return list(results)

    def write_multiple_address(self, start_address: int, values: list, one_write_count: int = 100):
        """写入连续地址数据.

        Args:
            start_address: 开始地址.
            values: 要写入的值列表.
            one_write_count: 每次写入的 word 个数, 默认一次写 100 个.
        """
        expect_write_count = len(values)
        range_num = expect_write_count // one_write_count + 1
        for i in range(range_num):
            do_write_count = 100 * (i + 1)
            write_results = values[i * one_write_count:do_write_count:]
            self.plc.write_multiple(start_address // 2, write_results, len(write_results))
            self.logger.info("要写入 %s 个, 已写入 %s", len(values), do_write_count)
            start_address = 2 * one_write_count + start_address
            if do_write_count >= len(values):
                break

    def write_recipe_info(self, recipe_name: str):
        """写入配方信息."""
        recipe_info_list = self.mysql_secs.query_data(models_class.RecipeInfo, {"recipe_name" : recipe_name})
        if recipe_info_list:
            recipe_info = recipe_info_list[0]
            recipe_name = recipe_info["recipe_name"]
            recipe_body = recipe_info["recipe_body"]
            self.plc.execute_write("str", 11986, recipe_name, size=15)
            recipe_info_1, recipe_info_2, recipe_info_3, recipe_info_4, *_ = json.loads(recipe_body.decode("utf-8"))
            self.write_multiple_address(24004, recipe_info_1)
            self.write_multiple_address(24056, recipe_info_2)
            self.write_multiple_address(45740, recipe_info_3)
            self.write_multiple_address(46500, recipe_info_4)
            self.plc.execute_write("int", 23380, 1)

    async def read_current_recipe_info(self, *args):
        """读取配方信息."""
        address_info = plc_address_operation.get_address_with_description(self.mysql_secs, "当前配方")
        recipe_name = self.plc.execute_read(**address_info)
        recipe_info_list = []
        recipe_info_1 = self.read_multiple_address(1214, 1268)  # 工艺数据
        recipe_info_2 = self.read_multiple_address(1268, 22952)  # 私服位置
        recipe_info_3 = self.read_multiple_address(22952, 23712)  # 机械手位置
        recipe_info_4 = self.read_multiple_address(23712, 23972)  # mis claw 位置
        recipe_info_list.append(recipe_info_1)
        recipe_info_list.append(recipe_info_2)
        recipe_info_list.append(recipe_info_3)
        recipe_info_list.append(recipe_info_4)
        recipe_body = json.dumps(recipe_info_list).encode("UTF-8")
        add_data = [{
            "recipe_name": recipe_name, "recipe_body": recipe_body
        }]
        self.mysql_secs.delete_data(models_class.RecipeInfo, {"recipe_name": recipe_name})
        self.mysql_secs.add_data(models_class.RecipeInfo, add_data)

    async def update_pin_lot(self, pin_lot_info: dict):
        """更新针工单信息."""
        pin_lot_name = pin_lot_info["pin_lot_name"]
        self.set_dv_value_with_name("pin_lot_name", pin_lot_name)

    async def new_lot(self, lot_info: dict):
        """本地开工单.

        Args:
            lot_info: 工单信息.
        """
        self.execute_new_lot(lot_info["lot_name"], lot_info["lot_quantity"])
        self.write_recipe_info(lot_info["recipe_name"])
        return f"开工单 {self.get_sv_value_with_name('lot_name')} 成功"
