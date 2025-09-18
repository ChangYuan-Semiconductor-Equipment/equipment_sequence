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
        self.mysql = MySQLDatabase("cyg", "liuwei.520")

    def get_carrier_info_front(self, call_back: dict):
        """前工位托盘进站时查询托盘里面的产品信息."""
        self.logger.info("call back 信息是: %s", json.dumps(call_back))
        carrier_code = self.get_dv_value_with_id(601)
        carrier_info_list = self.mysql.query_data(table_model.CarrierInfo, {"carrier_code": carrier_code})
        if carrier_info_list:
            self.set_dv_value_with_id(605, 1)

            carrier_info = carrier_info_list[0]
            self.set_dv_value_with_id(613, [carrier_info.get("product_code_1"), carrier_info.get("product_code_2")])
            self.set_dv_value_with_id(615, [carrier_info.get("frame_code_1"), carrier_info.get("frame_code_2")])
            self.set_dv_value_with_id(617, [carrier_info.get("product_state_1"), carrier_info.get("product_state_2")])
        else:
            self.set_dv_value_with_id(605, 2)
            self.set_dv_value_with_id(613, ["", ""])
            self.set_dv_value_with_id(615, ["", ""])
            self.set_dv_value_with_id(617, [2, 2])


    def get_carrier_info_back(self, call_back: dict):
        """后工位托盘进站时查询托盘里面的产品信息."""
        self.logger.info("call back 信息是: %s", json.dumps(call_back))
        carrier_code = self.get_dv_value_with_id(602)
        carrier_info_list = self.mysql.query_data(table_model.CarrierInfo, {"carrier_code": carrier_code})
        if carrier_info_list:
            self.set_dv_value_with_id(606, 1)

            carrier_info = carrier_info_list[0]
            self.set_dv_value_with_id(614, [carrier_info.get("product_code_1"), carrier_info.get("product_code_2")])
            self.set_dv_value_with_id(616, [carrier_info.get("frame_code_1"), carrier_info.get("frame_code_2")])
            self.set_dv_value_with_id(618, [carrier_info.get("product_state_1"), carrier_info.get("product_state_2")])
        else:
            self.set_dv_value_with_id(606, 2)
            self.set_dv_value_with_id(614, ["", ""])
            self.set_dv_value_with_id(616, ["", ""])
            self.set_dv_value_with_id(618, [2, 2])



