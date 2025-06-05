"""数据表模型."""
import datetime

from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import declarative_base


BASE = declarative_base()

class ProductLinkPlastic(BASE):
    """产品和塑料盒绑定模型."""
    __tablename__ = "product_link_plastic"

    id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    product_code = Column(String(50), nullable=True)
    label_info_one = Column(String(150), nullable=True)
    label_info_two = Column(String(150), nullable=True)
    map_number = Column(Integer, nullable=True)
    lot_name = Column(String(50), nullable=True)
    state = Column(Integer, nullable=True)
    updated_at = Column(DateTime, default=lambda: datetime.datetime.now(), onupdate=lambda: datetime.datetime.now())
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



class ProductIn(BASE):
    """产品进站记录模型."""
    __tablename__ = "product_in"

    id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    product_code = Column(String(50), nullable=True)
    state = Column(Integer, nullable=True, comment="1: 可以进站, 2: NG产品, 3: 不在配对表里, 4: MES不允许进站")
    lot_name = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.datetime.now())

    def as_dict(self):
        """获取字典形式的数据."""
        return {column.name: getattr(self, column.name) for column in self.__table__.columns.values()}

