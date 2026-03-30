"""
项目全局配置文件
统一管理所有常量，避免代码硬编码
"""
import os
from pathlib import Path

# 项目根目录（app文件夹的上级目录）
BASE_DIR = Path(__file__).parent.parent.parent

# 项目基础信息（自动同步到接口文档）
PROJECT_NAME = "FastAPI 学习项目-图书管理系统"
PROJECT_VERSION = "1.0.0"
PROJECT_DESCRIPTION = "专为FastAPI入门打造，覆盖路由分发、数据库、模板渲染等核心知识点"

# SQLite数据库配置（文件型数据库，无需额外安装服务）
SQLITE_URL = f"sqlite+aiosqlite:///{os.path.join(BASE_DIR, 'learn.db')}"

# 模板与静态文件路径配置
TEMPLATES_DIR = os.path.join(BASE_DIR, "app", "templates")
STATIC_DIR = os.path.join(BASE_DIR, "app", "static")
STATIC_URL = "/static"  # 静态文件访问的URL前缀
