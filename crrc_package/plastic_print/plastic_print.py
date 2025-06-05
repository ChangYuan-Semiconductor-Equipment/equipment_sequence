
from passive_equipment.handler_passive import HandlerPassive
from webservice_api.webservice_api import WebserviceAPI
from zebra_api.zebra_api import ZebraPrinterClient

from crrc_package.plastic_print.database_table_model import ProductLinkPlastic, ProductIn


class PlasticPrint(HandlerPassive):

    def __init__(self):
        super().__init__()
        # self.webservice_api = WebserviceAPI("http://10.96.141.69:7456/M1AutoPackageNotLogo.asmx?wsdl")
        self.zebra = ZebraPrinterClient("192.168.250.148", 6101)

    def label_print_request_one(self, call_back: dict):
        """塑料盒请求打印第一次标签码.

        Args:
            call_back: 要执行的 call_back 信息.
        """
        self.logger.info("正在执行 %s 函数", call_back["operation_func"])
        self.set_dv_value_with_name("label_print_info_one", "one")
        products_state = self.get_dv_value_with_name("products_state")

        pins_state = self.get_dv_value_with_name("product_pins_state_in_plastic")
        if 3 in pins_state or 3 in products_state:
            self.set_dv_value_with_name("is_ng_plastic", 2)
        else:
            self.set_dv_value_with_name("is_ng_plastic", 1)

        self.set_dv_value_with_name("label_print_info_one", "onesffdgg")

        data = self._get_add_info()
        self.mysql.add_data_multiple(ProductLinkPlastic, data)

    def label_print_request_second(self, call_back: dict):
        """塑料盒请求打印第二次标签码.

        Args:
            call_back: 要执行的 call_back 信息.
        """
        self.logger.info("正在执行 %s 函数", call_back["operation_func"])
        self.set_dv_value_with_name("label_print_info_second", "two")
        label_info_second = self.get_dv_value_with_name("label_print_info_second")
        self.mysql.update_data(
            ProductLinkPlastic, "label_info_second", label_info_second,
            {"label_info_one": self.get_dv_value_with_name("label_print_info_one")}
        )

    def _get_add_info(self) -> list:
        """获取写入 ProductLinkPlastic 表数据."""
        product_list = self.get_dv_value_with_name("product_codes_in_plastic")
        instance = self.mysql.query_data_one(ProductIn, product_code=product_list[0])
        lot_name = instance.as_dict()["lot_name"]
        result_list = []
        for product in product_list:
            result_list.append({
                "product_code": product,
                "label_info_one": self.get_dv_value_with_name("label_print_info_one"),
                "map_number": len(product_list),
                "state": self.get_dv_value_with_name("is_ng_plastic"),
                "lot_name": lot_name
            })
        return result_list

    def read_multiple_update_dv_snap7(self, call_back: dict):
        """读取 Snap7 plc 多个数据更新 dv 值.
        Args:
            call_back: 要执行的 call_back 信息.
        """
        value_list = []
        count_num = call_back["count_num"]
        gap = call_back.get("gap", 1)
        start_address = call_back.get("address")
        dv_name = call_back.get("dv_name")
        if dv_name == "product_pins_state_in_plastic":
            for i in range(self.get_dv_value_with_name("current_count") * 8):
                address_info = {
                    "address": start_address + i * gap,
                    "data_type": call_back.get("data_type"),
                    "db_num": self.get_ec_value_with_name("db_num"),
                    "size": call_back.get("size", 1),
                    "bit_index": call_back.get("bit_index", 0)
                }
                plc_value = self.lower_computer_instance.execute_read(**address_info)
                if plc_value:
                    value_list.append(plc_value)
            self.set_dv_value_with_name(dv_name, value_list)
            self.logger.info("当前 dv %s 值 %s, 个数: %s", call_back.get("dv_name"), value_list, len(value_list))
        else:
            for i in range(count_num):
                address_info = {
                    "address": start_address + i * gap,
                    "data_type": call_back.get("data_type"),
                    "db_num": self.get_ec_value_with_name("db_num"),
                    "size": call_back.get("size", 1),
                    "bit_index": call_back.get("bit_index", 0)
                }
                plc_value = self.lower_computer_instance.execute_read(**address_info)
                if plc_value:
                    value_list.append(plc_value)
            self.set_dv_value_with_name(dv_name, value_list)
            self.logger.info("当前 dv %s 值 %s, 个数: %s", call_back.get("dv_name"), value_list, len(value_list))
            self.set_dv_value_with_name("current_count", len(value_list))
