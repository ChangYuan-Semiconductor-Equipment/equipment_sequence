"""
X-Ray键合托盘数据: liuwei#0#0#0#0#0#0#0#0#0
"""
import time
from threading import Thread

from passive_equipment.handler_passive import HandlerPassive
from socket_cyg.socket_client import SocketClient


class Cutting(HandlerPassive):

    def __init__(self):
        super().__init__(open_flag=True)

        # 监控 X-RAY 的客户端 10.75.0.85
        self.socket_client_xray = SocketClient("10.75.0.85", 8080, self.receive_x_ray_data)
        self.socket_client_xray.logger.addHandler(self.file_handler)
        self.socket_client_xray.connect()
        self.lower_computer_instance.execute_write("int", 252, 1998, 3)
        self.monitor_x_ray()

    def monitor_x_ray(self):
        """监控 x-ray 服务端的线程."""

        def _monitor_x_ray_thread():
            while True:
                if not self.socket_client_xray.is_connected:
                    time.sleep(3)
                    self.logger.info("X-ray 服务端关闭, 等待3s后重连.")
                    self.socket_client_xray.connect()

        Thread(target=_monitor_x_ray_thread, daemon=True).start()

    def receive_x_ray_data(self, data: bytes):
        """接收到 X-Ray 数据后的回调函数.

        Args:
            data: 接收到的数据.
        """
        data_str = data.decode("UTF-8")
        dcb_info = data_str.split("#")

        self.set_dv_value_with_name("is_allow_carrier_in", 1)
        self.config_instance.update_config_dv_value("is_allow_carrier_in", 1)

        recipe_name = dcb_info[0]
        self.set_sv_value_with_name("pp_select_recipe_name", recipe_name)
        self.config_instance.update_config_sv_value("pp_select_recipe_name", recipe_name)

        pp_select_recipe_id = self.get_recipe_id_with_name(recipe_name)
        self.set_sv_value_with_name("pp_select_recipe_id", pp_select_recipe_id)
        self.config_instance.update_config_sv_value("pp_select_recipe_id", pp_select_recipe_id)
        self.execute_call_backs(self.config["signal_address"]["pp_select"]["call_back"])

        dbc_state_list = dcb_info[1:]
        dbc_state_list_real = [1 if int(state) == 0 else 2 for state in dbc_state_list]
        self.set_dv_value_with_name("dbc_state_list", dbc_state_list_real)
        self.config_instance.update_config_dv_value("dbc_state_list", dbc_state_list_real)

        dbc_code_list = [f"dbc_{i}" for i in range(1, 11)]
        self.set_dv_value_with_name("dbc_code_list", dbc_code_list)
        self.config_instance.update_config_dv_value("dbc_code_list", dbc_code_list)

        self.set_dv_value_with_name("carrier_in_key_reply", True)

    def _on_rcmd_carrier_in_key_reply(
            self, recipe_name:str, is_allow_carrier_in: int, product_codes: str, product_indexes: str, product_states: str
    ):
        """eap回复键合托盘里的dbc状态.

        Args:
            recipe_name: 配方名称
            is_allow_carrier_in: 是否允许进站.
            product_codes: 所有的dbc码.
            product_indexes: 所有的dbc所在键合托盘穴位.
            product_states: 产品状态.
        """
        self.set_sv_value_with_name("pp_select_recipe_name", recipe_name)
        self.config_instance.update_config_sv_value("pp_select_recipe_name", recipe_name)

        pp_select_recipe_id = self.get_recipe_id_with_name(recipe_name)
        self.set_sv_value_with_name("pp_select_recipe_id", pp_select_recipe_id)
        self.config_instance.update_config_sv_value("pp_select_recipe_id", pp_select_recipe_id)

        self.set_dv_value_with_name("is_allow_carrier_in", int(is_allow_carrier_in))
        self.config_instance.update_config_dv_value("is_allow_carrier_in", int(is_allow_carrier_in))

        dbc_code_list = [product_code for product_code in product_codes.split(",")]
        self.set_dv_value_with_name("dbc_code_list", dbc_code_list)
        self.config_instance.update_config_dv_value("dbc_code_list", dbc_code_list)

        dbc_index_list = [int(product_index) for product_index in product_indexes.split(",")]
        self.set_dv_value_with_name("dbc_index_list", dbc_index_list)
        self.config_instance.update_config_dv_value("dbc_index_list", dbc_index_list)

        dbc_state_list = [int(state) for state in product_states.split(",")]
        self.set_dv_value_with_name("dbc_state_list", dbc_state_list)
        self.config_instance.update_config_dv_value("dbc_state_list", dbc_state_list)

        self.set_dv_value_with_name("carrier_in_key_reply", True)




