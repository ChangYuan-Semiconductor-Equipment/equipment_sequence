"""数据表模型."""
import datetime

from mysql_api.mysql_database import MySQLDatabase
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import declarative_base


BASE = declarative_base()
mysql_api = MySQLDatabase("root", "liuwei.520")


class EquipmentState(BASE):
    """Mes 状态模型."""
    __tablename__ = "equipment_state"
    __table_args__ = {"comment": "设备状态表"}

    id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    control_state = Column(Integer, nullable=True, comment="0: plc 离线, 1: 本地模式, 2: 远程模式")
    control_state_message = Column(String(50), nullable=True, comment="设备控制状态描述信息")
    machine_state = Column(Integer, nullable=True, comment="1: Manual, 2: Auto, 3: Auto Run, 4: Alarm")
    machine_state_message = Column(String(50), nullable=True, comment="设备运行状态描述信息")
    eap_connect_state = Column(Integer, nullable=True, comment="0: 未连接, 1: eap 已连接")
    eap_connect_state_message = Column(String(50), nullable=True, comment="eap 连接 mes 服务描述信息")
    mes_state = Column(Integer, nullable=True, comment="0: 设备 MES 服务未打开, 1: 设备 MES 服务已打开")
    mes_state_message = Column(String(50), nullable=True, comment="设备 MES 服务状态信息")

    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    created_at = Column(DateTime, default=datetime.datetime.now)


class LotList(BASE):
    """工单列表模型."""
    __tablename__ = "lot_list"
    __table_args__ = {"comment": "工单列表"}

    id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    lot_name = Column(String(50), nullable=True, comment="工单名称")
    lot_state = Column(Integer, nullable=True, default=1, comment="工单状态")
    circulate_name = Column(String(50), nullable=True, comment="流转单名称")
    recipe_name = Column(String(50), nullable=True, comment="配方名称")
    lot_state_message = Column(String(50), nullable=True, default="运行中", comment="工单状态信息")
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    created_at = Column(DateTime, default=datetime.datetime.now)


class SolderSheetInfo(BASE):
    """焊片材料号模型."""
    __tablename__ = "solder_sheet_info"
    __table_args__ = {"comment": "焊片材料号信息"}

    id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    solder_sheet_material_name = Column(String(50), nullable=True, comment="焊片材料号")
    solder_sheet_lot_name = Column(String(50), nullable=True, comment="焊片工单号")
    state = Column(Integer, nullable=True, default=1, comment="状态, 1: 使用中, 0: 已用完")
    recipe_name = Column(String(50), nullable=True, comment="配方名称")
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    created_at = Column(DateTime, default=datetime.datetime.now)


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
    recipe_name = Column(String(50), nullable=True, comment="配方名称")
    product_type = Column(String(50), nullable=True, comment="产品类型")

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
    recipe_name = Column(String(50), nullable=True, comment="配方名称")
    product_type = Column(String(50), nullable=True, comment="产品类型")

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
    recipe_name = Column(String(50), nullable=True, comment="配方名称")
    product_type = Column(String(50), nullable=True, comment="产品类型")

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
    recipe_name = Column(String(50), nullable=True, comment="配方名称")
    product_type = Column(String(50), nullable=True, comment="产品类型")

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
    recipe_name = Column(String(50), nullable=True, comment="配方名称")
    product_type = Column(String(50), nullable=True, comment="产品类型")

    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    created_at = Column(DateTime, default=datetime.datetime.now)


if __name__ == '__main__':

    mysql_api.create_table(BASE)