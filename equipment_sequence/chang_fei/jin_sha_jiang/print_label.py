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
        self.mysql = MySQLDatabase("cyg", "liuwei.520")

    def get_carrier_info(self, call_back: dict):
        """托盘进站时查询托盘里面的产品信息."""
        self.logger.info("call back 信息是: %s", json.dumps(call_back))
        carrier_code = self.get_dv_value_with_id(601)
        carrier_info_list = self.mysql.query_data(table_model.CarrierInfo, {"carrier_code": carrier_code})
        if carrier_info_list:
            self.set_dv_value_with_id(603, 1)

            carrier_info = carrier_info_list[0]
            self.set_dv_value_with_id(610, [carrier_info.get("product_code_1"), carrier_info.get("product_code_2")])
            self.set_dv_value_with_id(611, [carrier_info.get("product_state_1"), carrier_info.get("product_state_2")])
        else:
            self.set_dv_value_with_id(603, 2)
            self.set_dv_value_with_id(610, ["", ""])
            self.set_dv_value_with_id(611, [2, 2])

    def update_carrier_info(self, call_back: dict):
        """托盘出站时更新托盘里面的侧框信息."""
        self.logger.info("call back 信息是: %s", json.dumps(call_back))
        carrier_code = self.get_dv_value_with_id(602)
        filter_dict = {"carrier_code": carrier_code}
        frame_code_list = self.get_sv_value_with_id(608)
        update_data = {
            "frame_code_1": frame_code_list[0],
            "frame_code_2": frame_code_list[1]
        }
        self.mysql_secs.update_data(table_model.CarrierInfo, update_data, filter_dict)

