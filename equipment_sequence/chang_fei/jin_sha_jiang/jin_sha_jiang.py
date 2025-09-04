from passive_equipment.handler_passive import HandlerPassive


class JinShaJiang(HandlerPassive):
    def __init__(self):
        control_dict = {
            "cutting": "socket"
        }
        super().__init__(control_dict)
