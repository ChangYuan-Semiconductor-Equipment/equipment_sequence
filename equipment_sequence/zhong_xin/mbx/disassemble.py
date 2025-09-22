from inovance_tag.tag_communication import TagCommunication
from passive_equipment.handler_passive import HandlerPassive


class Disassemble(HandlerPassive):
    def __init__(self):
        control_dict = {"disassemble_tag": TagCommunication("")}

        super().__init__(control_dict)
