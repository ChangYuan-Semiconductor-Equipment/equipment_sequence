"""上料工位."""
from passive_server.passive_equipment import EquipmentPassive


class UploadProduct(EquipmentPassive):
    """UploadProduct class."""
    def __init__(self, mysql_host: str, database_name: str):
        """UploadProduct init 方法.

        Args:
            mysql_host: 数据库 ip.
            database_name: 数据库名称.
        """
        super().__init__(mysql_host, database_name)