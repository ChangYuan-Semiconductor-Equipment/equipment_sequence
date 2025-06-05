from passive_equipment.handler_passive import HandlerPassive
from socket_cyg.socket_client import SocketClient


class DbcInTray(HandlerPassive):

    def __init__(self):
        super().__init__(open_flag=True)

        # 10.75.0.85
        self.socket_client_xray = SocketClient("10.75.0.85", 8080)
        self.socket_client_xray.connect()
        self.lower_computer_instance.execute_write("int", 252, 1998, 3)

    def _on_rcmd_carrier_in_roll_reply(
            self, is_allow_carrier_roll_in: int, product_codes: str, product_indexes: str, product_states: str
    ):
        """下发回流焊托盘里的产品信息.

        Args:
            is_allow_carrier_roll_in: 是否允许回流焊托盘进站.
            product_codes: 回流焊里面的dbc码.
            product_indexes: 回流焊里面的dbc穴位.
            product_states: 回流焊里面的dbc状态.
        """
        self.set_dv_value_with_name("is_allow_carrier_roll_in", int(is_allow_carrier_roll_in))
        self.config_instance.update_config_dv_value("is_allow_carrier_roll_in", int(is_allow_carrier_roll_in))

        product_code_list = product_codes.split(",")
        product_index_list = [int(index) for index in product_indexes.split(",")]
        product_state_list = [int(state) for state in product_states.split(",")]

        self.set_dv_value_with_name("dbc_code_list", product_code_list)
        self.config_instance.update_config_dv_value("dbc_code_list", product_code_list)

        self.set_dv_value_with_name("dbc_index_list", product_index_list)
        self.config_instance.update_config_dv_value("dbc_index_list", product_index_list)

        self.set_dv_value_with_name("dbc_state_list", product_state_list)
        self.config_instance.update_config_dv_value("dbc_state_list", product_state_list)

        self.set_dv_value_with_name("carrier_in_roll_reply", True)

    def send_carrier_info_to_xray(self, call_back):
        """带有产品的键合托盘出站时给 X-ray 发送数据.

        Args:
            call_back: 要执行的 call_back 信息.
        """
        self.logger.info("执行 %s", call_back.get("description"))
        carrier_code_key = self.get_dv_value_with_name("carrier_code_key")
        dbc_code_list_key = self.get_dv_value_with_name("dbc_code_list_key")
        dbc_code_list_send = [code if code and "dbc_" not in code else "NOCODE" for code in dbc_code_list_key]
        data = f"{carrier_code_key}#{'#'.join(dbc_code_list_send)}"
        self.logger.info("要发给 X-RAY 的数据: %s", data)

        if not self.socket_client_xray.is_connected:
            self.socket_client_xray.connect()
        self.socket_client_xray.send_data(data.encode("UTF-8"))

    def wait_eap_reply(self, call_back: dict):
        """等待 eap 反馈.

        Args:
            call_back: 要执行的 call_back 信息.
        """
        self.set_dv_value_with_name("is_allow_carrier_roll_in", 1)
        self.set_sv_value_with_name("current_recipe_id", 1)

        dbc_state_list = [1 for _ in range(36)]
        self.set_dv_value_with_name("dbc_state_list", dbc_state_list)

        dbc_code_list = [f"dbc_{_ + 1}" for _ in range(36)]
        self.set_dv_value_with_name("dbc_code_list", dbc_code_list)

        # dbc_code_list = ["" for _ in range(36)]
        # self.set_dv_value_with_name("dbc_code_list", dbc_code_list)

