"""
图书相关Pydantic模型
核心作用：请求体校验、响应数据格式化，是FastAPI数据校验的核心
"""
from pydantic import BaseModel, Field
from typing import Optional

# 1. 基础模型：所有模型的公共字段
class BookBase(BaseModel):
    title: str = Field(min_length=1, max_length=100, description="图书名称，长度1-100")
    author: str = Field(min_length=1, max_length=50, description="作者名称，长度1-50")
    price: float = Field(gt=0, description="图书价格，必须大于0")
    description: Optional[str] = Field(default=None, description="图书简介，可选")

# 2. 创建图书的请求模型：创建时需要提交的字段
class BookCreate(BookBase):
    """创建图书的请求体模型"""
    pass

# 3. 更新图书的请求模型：所有字段可选，支持部分更新
class BookUpdate(BaseModel):
    """更新图书的请求体模型，仅传入需要修改的字段即可"""
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    author: Optional[str] = Field(None, min_length=1, max_length=50)
    price: Optional[float] = Field(None, gt=0)
    description: Optional[str] = None

# 4. 图书响应模型：接口返回的数据结构
class BookResponse(BookBase):
    """图书查询的响应体模型"""
    id: int = Field(description="图书主键ID")

    # 开启ORM模式：支持直接将SQLAlchemy对象转换为Pydantic模型
    model_config = {"from_attributes": True}
