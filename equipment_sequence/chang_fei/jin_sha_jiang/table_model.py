# pylint: skip-file
"""数据表模型."""
import datetime

from mysql_api.mysql_database import MySQLDatabase
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import declarative_base

BASE = declarative_base()
mysql_api = MySQLDatabase("root", "liuwei.520")


class CarrierInfo(BASE):
    """Mes 状态模型."""
    __tablename__ = "carrier_info"
    __table_args__ = {"comment": "托盘信息"}

    id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    carrier_code = Column(String(50), nullable=True, comment="托盘码")
    product_code_1 = Column(String(50), nullable=True, comment="穴位1产品码")
    product_code_2 = Column(String(50), nullable=True, comment="穴位2产品码")
    frame_code_1 = Column(String(50), nullable=True, comment="穴位1侧框码")
    frame_code_2 = Column(String(50), nullable=True, comment="穴位2侧框码")
    product_state_1 = Column(Integer, nullable=True, comment="穴位1产品状态")
    product_state_2 = Column(Integer, nullable=True, comment="穴位2产品状态")
    lot_name = Column(String(50), nullable=True, comment="工单名称")
    recipe_name = Column(String(50), nullable=True, comment="配方名称")
    product_type = Column(String(50), nullable=True, comment="产品类型")
    year_code = Column(String(50), nullable=True, comment="工单投单年份的后两位")
    week_code = Column(String(50), nullable=True, comment="工单投单日期当周周别")
    flow_water_code = Column(String(50), nullable=True, comment="流水码")

    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    created_at = Column(DateTime, default=datetime.datetime.now)


if __name__ == '__main__':
    mysql_api.create_table(BASE)
