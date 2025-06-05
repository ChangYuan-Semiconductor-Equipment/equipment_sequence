from passive_equipment.handler_passive import HandlerPassive


class ZheWan(HandlerPassive):

    def __init__(self):
        super().__init__()

    def _on_rcmd_track_in_reply(self, track_in_state: int):
        """进站反馈.

        Args:
            track_in_state: 是否允许进站.
        """
        self.set_dv_value_with_name("track_in_state", track_in_state)

        self.set_dv_value_with_name("track_in_reply", True)
