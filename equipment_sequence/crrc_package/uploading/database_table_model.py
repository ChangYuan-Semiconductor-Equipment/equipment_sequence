"""工单数据表模型."""
import datetime

from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import declarative_base

BASE = declarative_base()


class CurrentLotInfo(BASE):
    """当前工单模型."""
    __tablename__ = "current_lot_info"

    id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    lot_name = Column(String(50), nullable=True)
    lot_state = Column(Integer, nullable=True)
    lot_state_message = Column(String(50), nullable=True)
    updated_at = Column(DateTime, default=lambda: datetime.datetime.now(), onupdate=lambda: datetime.datetime.now())
    created_at = Column(DateTime, default=lambda: datetime.datetime.now())

    def as_dict(self):
        """获取字典形式的数据."""
        return {column.name: getattr(self, column.name) for column in self.__table__.columns.values()}


class LotList(BASE):
    """工单列表模型."""
    __tablename__ = "lot_list"

    id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    lot_name = Column(String(50), nullable=True)
    lot_state = Column(Integer, nullable=True)
    lot_state_message = Column(String(50), nullable=True)
    updated_at = Column(DateTime, default=lambda: datetime.datetime.now(), onupdate=lambda: datetime.datetime.now())
    created_at = Column(DateTime, default=lambda: datetime.datetime.now())

    def as_dict(self):
        """获取字典形式的数据."""
        return {column.name: getattr(self, column.name) for column in self.__table__.columns.values()}


class OriginMapData(BASE):
    """上传的原始数据模型."""
    __tablename__ = "origin_map_data"

    id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    product_code = Column(String(50), nullable=True)
    ices_ua_upper = Column(Float, nullable=True)
    ices_ua_lower = Column(Float, nullable=True)
    ices_ma_upper = Column(Float, nullable=True)
    ices_ma_lower = Column(Float, nullable=True)
    vge_upper = Column(Float, nullable=True)
    vge_lower = Column(Float, nullable=True)
    iges_plus_upper = Column(Float, nullable=True)
    iges_plus_lower = Column(Float, nullable=True)
    iges_minus_upper = Column(Float, nullable=True)
    iges_minus_lower = Column(Float, nullable=True)
    vce_25_upper = Column(Float, nullable=True)
    vce_25_lower = Column(Float, nullable=True)
    vce_150_upper = Column(Float, nullable=True)
    vce_150_lower = Column(Float, nullable=True)
    vf_25_upper = Column(Float, nullable=True)
    vf_25_lower = Column(Float, nullable=True)
    vf_150_upper = Column(Float, nullable=True)
    vf_150_lower = Column(Float, nullable=True)
    td_on_upper = Column(Float, nullable=True)
    td_on_lower = Column(Float, nullable=True)
    tr_upper = Column(Float, nullable=True)
    tr_lower = Column(Float, nullable=True)
    ton_upper = Column(Float, nullable=True)
    ton_lower = Column(Float, nullable=True)
    eon_upper = Column(Float, nullable=True)
    eon_lower = Column(Float, nullable=True)
    td_off_upper = Column(Float, nullable=True)
    td_off_lower = Column(Float, nullable=True)
    tf_upper = Column(Float, nullable=True)
    tf_lower = Column(Float, nullable=True)
    toff_upper = Column(Float, nullable=True)
    toff_lower = Column(Float, nullable=True)
    eoff_upper = Column(Float, nullable=True)
    eoff_lower = Column(Float, nullable=True)
    qrr_upper = Column(Float, nullable=True)
    qrr_lower = Column(Float, nullable=True)
    lrr_upper = Column(Float, nullable=True)
    lrr_lower = Column(Float, nullable=True)
    erec_upper = Column(Float, nullable=True)
    erec_lower = Column(Float, nullable=True)
    map_number = Column(Integer, nullable=True)
    year_week = Column(String(50), nullable=True)
    is_label_print = Column(Integer, nullable=True)
    label_type = Column(String(50), nullable=True)
    is_laser_print = Column(Integer, nullable=True)
    laser_type = Column(Integer, nullable=True)
    product_type = Column(String(50), nullable=True)
    updated_at = Column(DateTime, default=lambda: datetime.datetime.now(), onupdate=lambda: datetime.datetime.now())
    created_at = Column(DateTime, default=lambda: datetime.datetime.now())

    def as_dict(self):
        """获取字典形式的数据."""
        return {column.name: getattr(self, column.name) for column in self.__table__.columns.values()}

    def as_dict_specify(self, include_fields: list = None) -> dict:
        """获取字典形式的数据，支持排除指定字段.

        Args:
            include_fields: 返回数据包含的字段.

        Returns:
            dict: 字典形式的数据.
        """
        if include_fields is None:
            return self.as_dict()
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns.values()
            if column.name in include_fields
        }


class NgProduct(BASE):
    """上传的 NG 产品模型."""
    __tablename__ = "ng_product"

    id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    product_code = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.datetime.now())

    def as_dict(self):
        """获取字典形式的数据."""
        return {column.name: getattr(self, column.name) for column in self.__table__.columns.values()}


class ProductIn(BASE):
    """产品进站记录模型."""
    __tablename__ = "product_in"

    id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    product_code = Column(String(50), nullable=True)
    state = Column(Integer, nullable=True, comment="1: 可以进站, 2: NG产品, 3: 不在配对表里, 4: MES不允许进站")
    created_at = Column(DateTime, default=lambda: datetime.datetime.now())

    def as_dict(self):
        """获取字典形式的数据."""
        return {column.name: getattr(self, column.name) for column in self.__table__.columns.values()}


class CurrentOriginPath(BASE):
    """产品进站记录模型."""
    __tablename__ = "current_origin_path"

    id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    path = Column(String(200), nullable=True)
    updated_at = Column(DateTime, default=lambda: datetime.datetime.now(), onupdate=lambda: datetime.datetime.now())
    created_at = Column(DateTime, default=lambda: datetime.datetime.now())

    def as_dict(self):
        """获取字典形式的数据."""
        return {column.name: getattr(self, column.name) for column in self.__table__.columns.values()}


class ProductInStationLeft(BASE):
    """产品放进左侧工位模型."""
    __tablename__ = "product_in_station_left"

    id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    product_code = Column(String(50), nullable=True)
    station_index = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.datetime.now())

    def as_dict(self):
        """获取字典形式的数据."""
        return {column.name: getattr(self, column.name) for column in self.__table__.columns.values()}


class ProductInStationRight(BASE):
    """产品放进左侧工位模型."""
    __tablename__ = "product_in_station_right"

    id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    product_code = Column(String(50), nullable=True)
    station_index = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.datetime.now())

    def as_dict(self):
        """获取字典形式的数据."""
        return {column.name: getattr(self, column.name) for column in self.__table__.columns.values()}


class MapDataInfo(BASE):
    """上传的原始数据模型."""
    __tablename__ = "map_data_info"

    id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    product_code = Column(String(50), nullable=True)
    vge_upper = Column(Float, nullable=True)
    vge_lower = Column(Float, nullable=True)
    vce_25_upper = Column(Float, nullable=True)
    vce_25_lower = Column(Float, nullable=True)
    vf_25_upper = Column(Float, nullable=True)
    vf_25_lower = Column(Float, nullable=True)
    group_index = Column(Integer, nullable=True)
    station_index = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.datetime.now())

    def as_dict(self):
        """获取字典形式的数据."""
        return {column.name: getattr(self, column.name) for column in self.__table__.columns.values()}

    def as_dict_specify(self, exclude_fields: list = None) -> dict:
        """获取字典形式的数据，支持排除指定字段。

        Args:
            exclude_fields: 需要排除的字段列表，默认为 ["id", "updated_at", "created_at"]

        Returns:
            dict: 字典形式的数据.
        """
        if exclude_fields is None:
            exclude_fields = ["id", "updated_at", "created_at"]  # 默认排除的字段
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns.values()
            if column.name not in exclude_fields
        }


class ProductLinkPlastic(BASE):
    """产品和塑料盒绑定模型."""
    __tablename__ = "product_link_plastic"

    id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    product_code = Column(String(50), nullable=True)
    label_info_one = Column(String(150), nullable=True)
    label_info_two = Column(String(150), nullable=True)
    map_number = Column(Integer, nullable=True)
    state = Column(Integer, nullable=True)
    updated_at = Column(DateTime, default=lambda: datetime.datetime.now(), onupdate=lambda: datetime.datetime.now())
    created_at = Column(DateTime, default=lambda: datetime.datetime.now())

    def as_dict(self):
        """获取字典形式的数据."""
        return {column.name: getattr(self, column.name) for column in self.__table__.columns.values()}


class ProductLabelInfo(BASE):
    """产品和塑料盒绑定模型."""
    __tablename__ = "product_label_info"

    id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    product_code = Column(String(50), nullable=True)
    product_index = Column(String(150), nullable=True)
    first_row_info = Column(String(150), nullable=True)
    second_row_info = Column(String(150), nullable=True)
    bar_code = Column(String(150), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.datetime.now())

    def as_dict(self):
        """获取字典形式的数据."""
        return {column.name: getattr(self, column.name) for column in self.__table__.columns.values()}


