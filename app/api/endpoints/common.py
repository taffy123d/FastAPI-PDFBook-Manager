"""
通用接口模块
专门演示FastAPI核心特性：Request对象的全用法
"""
from fastapi import APIRouter, Request
from typing import Dict

# 创建子路由实例
router = APIRouter(
    prefix="/common",
    tags=["通用接口-核心特性演示"]
)

# Request对象核心用法演示
@router.get("/request-info", summary="Request对象全属性演示")
async def get_request_info(request: Request) -> Dict:
    """
    演示FastAPI中Request对象的所有核心用法
    可获取请求的全部信息：方法、URL、请求头、客户端IP、查询参数、Cookies等
    """
    # 提取Request对象的核心信息
    request_info = {
        # 基础请求信息
        "请求方法": request.method,
        "请求完整URL": str(request.url),
        "请求路径": request.url.path,
        "查询参数": dict(request.query_params),
        # 客户端信息
        "客户端IP": request.client.host if request.client else None,
        "客户端端口": request.client.port if request.client else None,
        # 请求头与Cookies
        "请求头": dict(request.headers),
        "Cookies": dict(request.cookies),
        # 协议信息
        "HTTP版本": request.scope.get("http_version"),
        "请求协议": request.scope.get("scheme")
    }

    return request_info
