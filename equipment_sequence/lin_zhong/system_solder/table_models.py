"""数据表模型."""
import datetime

from mysql_api.mysql_database import MySQLDatabase
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import declarative_base


BASE = declarative_base()
mysql_api = MySQLDatabase("root", "liuwei.520")


class Uploading(BASE):
    """上料设备数据表模型."""
    __tablename__ = "uploading"
    __table_args__ = {"comment": "上料设备"}

    id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)

    product_code = Column(String(50), nullable=True, comment="基板产品码")

    solder_carrier_code = Column(String(50), nullable=True, comment="焊接托盘码")
    solder_carrier_in_time_uploading = Column(String(50), comment="焊接托盘进站时间")
    solder_carrier_out_time_uploading = Column(String(50), comment="焊接托盘出站时间")

    solder_jig_code = Column(String(50), nullable=True, comment="治具码")

    lot_name = Column(String(50), nullable=True, comment="工单号")
    circulate_name = Column(String(50), nullable=True, comment="流转单号")

    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    created_at = Column(DateTime, default=datetime.datetime.now)


class Bridge(BASE):
    """放半桥设备数据表模型."""
    __tablename__ = "bride"
    __table_args__ = {"comment": "放半桥设备"}

    id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)

    bridge_code = Column(String(50), nullable=True, comment="半桥码")
    product_code = Column(String(50), nullable=True, comment="基板产品码")

    solder_carrier_code = Column(String(50), nullable=True, comment="焊接托盘码")
    solder_carrier_in_time_bridge = Column(String(50), comment="焊接托盘进站时间")
    solder_carrier_out_time_bridge = Column(String(50), comment="焊接托盘出站时间")

    lot_name = Column(String(50), nullable=True, comment="工单号")
    circulate_name = Column(String(50), nullable=True, comment="流转单号")

    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    created_at = Column(DateTime, default=datetime.datetime.now)


class Cutting(BASE):
    """下料设备表模型."""
    __tablename__ = "cutting"
    __table_args__ = {"comment": "下料设备"}

    id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)

    solder_carrier_code = Column(String(50), nullable=True, comment="焊接托盘码")

    solder_carrier_in_time_cutting = Column(String(50), comment="焊接托盘进站时间")
    solder_carrier_out_time_cutting = Column(String(50), comment="焊接托盘出站时间")

    lot_name = Column(String(50), nullable=True, comment="工单号")
    circulate_name = Column(String(50), nullable=True, comment="流转单号")

    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    created_at = Column(DateTime, default=datetime.datetime.now)


class KeyCarrierCutting(BASE):
    """下料设备键合托盘数据表模型."""
    __tablename__ = "key_carrier_cutting"
    __table_args__ = {"comment": "下料设备键合托盘出站"}

    id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)

    bridge_code = Column(String(50), nullable=True, comment="半桥码")
    product_code = Column(String(50), nullable=True, comment="基板产品码")
    solder_carrier_code = Column(String(50), nullable=True, comment="焊接托盘码")

    solder_carrier_in_time = Column(String(50), comment="焊接托盘进站时间")
    solder_carrier_out_time = Column(String(50), comment="焊接托盘出站时间")

    key_carrier_code = Column(String(50), nullable=True, comment="键合托盘码")

    lot_name = Column(String(50), nullable=True, comment="工单号")
    circulate_name = Column(String(50), nullable=True, comment="流转单号")

    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    created_at = Column(DateTime, default=datetime.datetime.now)


class Records(BASE):
    """长期保存的数据总表模型."""
    __tablename__ = "records"
    __table_args__ = {"comment": "长期保存的数据总表"}

    id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    solder_carrier_code = Column(String(50), nullable=True, comment="焊接托盘码")

    product_code = Column(String(50), nullable=True, comment="基板产品码")
    solder_jig_code = Column(String(50), nullable=True, comment="焊接治具码")

    bridge_code = Column(String(50), nullable=True, comment="半桥码")

    solder_carrier_in_time_uploading = Column(String(50), comment="焊接托盘进上料设备时间")
    solder_carrier_out_time_uploading = Column(String(50), comment="焊接托盘出上料设备时间")
    solder_carrier_in_time_bridge = Column(String(50), comment="焊接托盘进半桥设备时间")
    solder_carrier_out_time_bridge = Column(String(50), comment="焊接托盘出半桥设备时间")
    solder_carrier_in_time_cutting = Column(String(50), comment="焊接托盘进下料设备时间")
    solder_carrier_out_time_cutting = Column(String(50), comment="焊接托盘出下料设备时间")

    lot_name = Column(String(50), nullable=True, comment="工单号")
    circulate_name = Column(String(50), nullable=True, comment="流转单号")

    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    created_at = Column(DateTime, default=datetime.datetime.now)


if __name__ == '__main__':

    mysql_api.create_table(BASE)