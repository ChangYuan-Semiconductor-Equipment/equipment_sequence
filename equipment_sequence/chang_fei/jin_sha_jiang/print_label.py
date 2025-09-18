import json

from mysql_api.mysql_database import MySQLDatabase
from passive_equipment.handler_passive import HandlerPassive
from siemens_plc.s7_plc import S7PLC

from equipment_sequence.chang_fei.jin_sha_jiang import table_model


class PrintLabel(HandlerPassive):
    def __init__(self):
        control_dict = {
            "upload_snap7": S7PLC("192.168.180.180")
        }
        super().__init__(control_dict)
        self.mysql = MySQLDatabase(
            self.get_ec_value_with_name("mysql_user_name"),
            self.get_ec_value_with_name("mysql_password"),
            host=self.get_ec_value_with_name("mysql_host")
        )

    def get_carrier_info(self, call_back: dict):
        """托盘进站时查询托盘里面的产品信息."""
        self.logger.info("call back 信息是: %s", json.dumps(call_back))
        carrier_code = self.get_dv_value_with_name("carrier_code_in")
        carrier_info_list = self.mysql.query_data(table_model.CarrierInfo, {"carrier_code": carrier_code})
        if carrier_info_list:
            is_allow_carrier_in = 1
            carrier_info = carrier_info_list[0]
            product_code_reply_list = [carrier_info.get("product_code_1"), carrier_info.get("product_code_2")]
            product_state_reply_list = [carrier_info.get("product_state_1"), carrier_info.get("product_state_2")]
        else:
            is_allow_carrier_in = 2
            product_code_reply_list = ["", ""]
            product_state_reply_list = [2, 2]

        self.set_dv_value_with_name("is_allow_carrier_in", is_allow_carrier_in)
        self.set_dv_value_with_name("product_code_reply_list", product_code_reply_list)
        self.set_dv_value_with_name("product_state_reply_list", product_state_reply_list)

    def update_carrier_info(self, call_back: dict):
        """托盘出站时更新托盘里面的侧框信息."""
        self.logger.info("call back 信息是: %s", json.dumps(call_back))
        carrier_code = self.get_dv_value_with_name("carrier_code_out")
        filter_dict = {"carrier_code": carrier_code}
        frame_code_list = self.get_dv_value_with_name("frame_code_list")
        update_data = {
            "frame_code_1": frame_code_list[0],
            "frame_code_2": frame_code_list[1]
        }
        self.mysql_secs.update_data(table_model.CarrierInfo, update_data, filter_dict)

