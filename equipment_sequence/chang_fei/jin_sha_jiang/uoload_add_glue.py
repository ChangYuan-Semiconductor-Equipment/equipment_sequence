import json

from passive_equipment.handler_passive import HandlerPassive
from siemens_plc.s7_plc import S7PLC

from equipment_sequence.chang_fei.jin_sha_jiang import table_model


class UploadAddGlue(HandlerPassive):
    def __init__(self):
        control_dict = {
            "upload_snap7": S7PLC("192.168.180.170")
        }
        super().__init__(control_dict)

    def save_carrier_info(self, call_back: dict):
        self.logger.info("call back 信息是: %s", json.dumps(call_back))
        carrier_code = self.get_dv_value_with_name("carrier_code_out")
        product_code_list = self.get_dv_value_with_name("product_code_list")
        product_state_list = self.get_dv_value_with_name("product_state_list")

        self.mysql_secs.delete_data(table_model.CarrierInfo, {"carrier_code": carrier_code})
        add_data = [{
            "carrier_code": carrier_code,
            "product_code_1": product_code_list[0], "product_code_2": product_code_list[1],
            "product_state_1": product_state_list[0], "product_state_2": product_state_list[1],
            "lot_name": self.get_sv_value_with_name("lot_name"),
            "recipe_name": self.get_sv_value_with_name("recipe_name'"),
            "product_type": self.get_dv_value_with_name("product_type"),
            "flow_water_code": self.get_dv_value_with_name("flow_water_code"),
            "year_code": self.get_dv_value_with_name("year_code"),
            "week_code": self.get_dv_value_with_name("week_code")
        }]
        self.mysql_secs.insert_data(table_model.CarrierInfo, add_data)

