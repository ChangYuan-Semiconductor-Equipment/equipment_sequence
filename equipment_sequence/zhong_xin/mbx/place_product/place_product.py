from passive_equipment.handler_passive import HandlerPassive


class PlaceProduct(HandlerPassive):

    def __init__(self):
        super().__init__()

    def _on_rcmd_new_lot(self, lot_name, lot_quality):
        """eap回复回流焊托盘是否可以进站.

        Args:
            lot_name: 工单号.
            lot_quality: 要生产的工单数量.
        """
        self.set_sv_value_with_name("current_lot_name", lot_name)
        self.set_sv_value_with_name("lot_quality", lot_quality)

    def _on_rcmd_carrier_in_reply(self, is_allow_carrier_in, lot_name):
        """eap回复回流焊托盘是否可以进站.

        Args:
            is_allow_carrier_in: eap是否允许回流焊托盘进站.
            lot_name: 工单号.
        """
        self.set_dv_value_with_name("is_allow_carrier_in", is_allow_carrier_in)
        self.set_sv_value_with_name("current_lot_name", lot_name)
        self.set_dv_value_with_name("is_allow_carrier_in_reply", True)

    def _on_rcmd_product_in_carrier_reply(self, is_allow_product_in, lot_name):
        """eap回复产品是否可以放进回流焊托盘.

        Args:
            is_allow_product_in: eap是否允许产品放进回流焊托盘.
            lot_name: 工单号.
        """
        self.set_dv_value_with_name("is_allow_product_in", is_allow_product_in)
        self.set_sv_value_with_name("current_lot_name", lot_name)
        self.set_dv_value_with_name("is_allow_product_in_reply", True)