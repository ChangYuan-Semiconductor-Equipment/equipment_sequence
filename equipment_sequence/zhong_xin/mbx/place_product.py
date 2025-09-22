from inovance_tag.tag_communication import TagCommunication
from passive_equipment.handler_passive import HandlerPassive


class PlaceProduct(HandlerPassive):
    def __init__(self):
        control_dict = {"place_product_tag": TagCommunication("")}

        super().__init__(control_dict)