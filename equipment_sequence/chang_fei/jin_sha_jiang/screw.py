import json

from mysql_api.mysql_database import MySQLDatabase
from passive_equipment.handler_passive import HandlerPassive
from siemens_plc.s7_plc import S7PLC

from equipment_sequence.chang_fei.jin_sha_jiang import table_model


class Screw(HandlerPassive):
    def __init__(self):
        control_dict = {
            "upload_snap7": S7PLC("192.168.180.190")
        }
        super().__init__(control_dict)
        self.mysql = MySQLDatabase(
            self.get_ec_value_with_name("mysql_user_name"),
            self.get_ec_value_with_name("mysql_password"),
            host=self.get_ec_value_with_name("mysql_host")
        )
    def get_carrier_info_front(self, call_back: dict):
        """前工位托盘进站时查询托盘里面的产品信息."""
        self.logger.info("call back 信息是: %s", json.dumps(call_back))
        carrier_code = self.get_dv_value_with_name("carrier_code_in_front")
        carrier_info_list = self.mysql.query_data(table_model.CarrierInfo, {"carrier_code": carrier_code})
        if carrier_info_list:
            is_allow_carrier_in_front = 1
            carrier_info = carrier_info_list[0]
            product_code_list_front_reply = [carrier_info.get("product_code_1"), carrier_info.get("product_code_2")]
            frame_code_list_front_reply = [carrier_info.get("frame_code_1"), carrier_info.get("frame_code_2")]
            product_state_list_front_reply = [carrier_info.get("product_state_1"), carrier_info.get("product_state_2")]
        else:
            is_allow_carrier_in_front = 2
            product_code_list_front_reply = ["", ""]
            frame_code_list_front_reply = ["", ""]
            product_state_list_front_reply = [2, 2]

        self.set_dv_value_with_name("is_allow_carrier_in_front", is_allow_carrier_in_front)
        self.set_dv_value_with_name("product_code_list_front_reply", product_code_list_front_reply)
        self.set_dv_value_with_name("frame_code_list_front_reply", frame_code_list_front_reply)
        self.set_dv_value_with_name("product_state_list_front_reply", product_state_list_front_reply)

    def get_carrier_info_back(self, call_back: dict):
        """后工位托盘进站时查询托盘里面的产品信息."""
        self.logger.info("call back 信息是: %s", json.dumps(call_back))
        carrier_code = self.get_dv_value_with_name("carrier_code_in_back")
        carrier_info_list = self.mysql.query_data(table_model.CarrierInfo, {"carrier_code": carrier_code})
        if carrier_info_list:
            is_allow_carrier_in_back = 1
            carrier_info = carrier_info_list[0]
            product_code_list_back_reply = [carrier_info.get("product_code_1"), carrier_info.get("product_code_2")]
            frame_code_list_back_reply = [carrier_info.get("frame_code_1"), carrier_info.get("frame_code_2")]
            product_state_list_back_reply = [carrier_info.get("product_state_1"), carrier_info.get("product_state_2")]
        else:
            is_allow_carrier_in_back = 2
            product_code_list_back_reply = ["", ""]
            frame_code_list_back_reply = ["", ""]
            product_state_list_back_reply = [2, 2]

        self.set_dv_value_with_name("is_allow_carrier_in_back", is_allow_carrier_in_back)
        self.set_dv_value_with_name("product_code_list_back_reply", product_code_list_back_reply)
        self.set_dv_value_with_name("frame_code_list_back_reply", frame_code_list_back_reply)
        self.set_dv_value_with_name("product_state_list_back_reply", product_state_list_back_reply)






