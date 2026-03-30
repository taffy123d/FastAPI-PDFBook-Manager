"""
图书表ORM模型
对应数据库中的book表，定义表结构与字段约束
"""
from sqlalchemy import Column, Integer, String, Float, Text
from app.database.db import Base

class Book(Base):
    """图书表模型"""
    # 数据库中的表名
    __tablename__ = "book"

    # 主键ID，自增整数
    id = Column(Integer, primary_key=True, autoincrement=True, comment="图书主键ID")
    # 图书名称，非空、不可重复
    title = Column(String(100), nullable=False, unique=True, comment="图书名称")
    # 作者名称，非空
    author = Column(String(50), nullable=False, comment="作者")
    # 图书价格，非空
    price = Column(Float, nullable=False, comment="图书价格")
    # 图书简介，可选
    description = Column(Text, nullable=True, comment="图书简介")
