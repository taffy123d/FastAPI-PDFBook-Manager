from sqlalchemy import Column, Integer, String, Float, Text

from app.database.db import Base


class Book(Base):
    """图书表模型"""
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="图书主键ID")
    title = Column(String(100), nullable=False, unique=True, comment="图书名称")
    author = Column(String(50), nullable=False, comment="作者")
    price = Column(Float, nullable=False, comment="图书价格")
    description = Column(Text, nullable=True, comment="图书简介")
    
    # 【新增】PDF 文件名
    filename = Column(String(200), nullable=True, comment="PDF文件名")