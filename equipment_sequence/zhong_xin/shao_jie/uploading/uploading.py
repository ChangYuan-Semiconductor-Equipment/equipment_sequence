
from modbus_api.modbus_api import ModbusApi
from passive_equipment.handler_passive import HandlerPassive


class ShaoJieUploading(HandlerPassive):

    def __init__(self):
        control_dict = {
            "uploading_modbus": ModbusApi("127.0.0.1"),
        }
        super().__init__(__file__, control_dict, open_flag=True)

    def on_sv_value_request(self, svid, status_variable):
        """Host 请求查询当前配方时, 从 plc 获取实时配方."""
        if str(status_variable.svid) == "505":
            plc = self.control_instance_dict["uploading_modbus"]
            current_recipe_id = plc.execute_read("int", "")
            current_recipe_name = self.config_instance.get_recipe_name_with_id(current_recipe_id)

            self.set_sv_value_with_name("current_recipe_id", current_recipe_id)
            self.set_sv_value_with_name("current_recipe_name", current_recipe_name)

            self.config_instance.update_config_sv_value("current_recipe_id", current_recipe_id)
            self.config_instance.update_config_sv_value("current_recipe_name", current_recipe_name)

        return status_variable.value_type(status_variable.value)
