from passive_equipment.handler_passive import HandlerPassive


class PlaceTwoBridge(HandlerPassive):

    def __init__(self):
        super().__init__()

    def _on_rcmd_carrier_in_reply(
            self, is_allow_carrier_in: int, substrate_codes: str, product_codes: str, steel_sheet_codes: str,
            limit_codes: str, press_block_codes: str, product_states: str, lot_name: str
    ):
        """eap回复回流焊托盘是否可以进站.

        Args:
            is_allow_carrier_in: eap是否允许回流焊托盘进站.
            substrate_codes: 所有的基板码.
            product_codes: 所有的产品码.
            steel_sheet_codes: 所有的吸钢片码.
            limit_codes: 所有的限位框码.
            press_block_codes: 所有的压块码.
            product_states: 所有产品状态.
            lot_name: 工单号.
        """
        self.set_dv_value_with_name("is_allow_carrier_in", int(is_allow_carrier_in))
        self.set_sv_value_with_name("current_lot_name", lot_name)

        self.set_dv_value_with_name(substrate_codes, substrate_codes.split(","))
        self.set_dv_value_with_name(product_codes, product_codes.split(","))
        self.set_dv_value_with_name(steel_sheet_codes, steel_sheet_codes.split(","))
        self.set_dv_value_with_name(limit_codes, limit_codes.split(","))
        self.set_dv_value_with_name(press_block_codes, press_block_codes.split(","))
        self.set_dv_value_with_name(product_states, [int(product_state) for product_state in product_states.split(",")])

        self.set_dv_value_with_name("is_allow_carrier_in_reply", True)

    def _on_rcmd_two_bridge_in_reply(self, is_allow_two_bridge_in, lot_name):
        """eap回复产品是否可以放进回流焊托盘.

        Args:
            is_allow_two_bridge_in: eap是否允许产品放进回流焊托盘.
            lot_name: 工单号.
        """
        self.set_dv_value_with_name("is_allow_two_bridge_in", int(is_allow_two_bridge_in))
        self.set_sv_value_with_name("current_lot_name", lot_name)
        self.set_dv_value_with_name("is_allow_product_in_reply", True)