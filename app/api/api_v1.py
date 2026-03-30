"""
API路由汇总文件
路由分发的核心：统一注册所有业务模块的子路由，实现接口版本管理
"""
from fastapi import APIRouter

# 导入各业务模块的子路由
from app.api.endpoints.book import router as book_router
from app.api.endpoints.common import router as common_router

# 创建v1版本的根路由，统一添加接口前缀
api_router = APIRouter(
    prefix="/api/v1"  # 所有接口的统一前缀，方便版本迭代
)

# 注册所有子路由
api_router.include_router(book_router)
api_router.include_router(common_router)
