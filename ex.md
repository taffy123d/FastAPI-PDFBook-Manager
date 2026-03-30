
# 按照下面项目结构和代码 完成 整个项目
### 不用关心环境依赖
## 一、项目整体说明
### 项目主题
极简**图书管理系统**，业务仅包含图书的增删改查（CRUD），无复杂逻辑，完全聚焦FastAPI的核心特性学习。

### 覆盖的核心知识点
✅ 路由分发与模块化开发  
✅ 自动生成交互式接口文档  
✅ Request对象全用法演示  
✅ 静态文件挂载与访问  
✅ Jinja2模板渲染（含模板继承）  
✅ SQLite数据库集成（SQLAlchemy 2.0异步ORM）  
✅ Pydantic数据校验与模型设计  
✅ 依赖注入系统  
✅ 标准HTTP状态码与异常处理  

### 工程化项目结构
```
fastapi_learn_project/
├── app/                          # 项目核心代码包
│   ├── __init__.py               # Python包标识文件
│   ├── main.py                   # 项目入口（APP实例创建、全局注册）
│   ├── core/                     # 全局配置目录
│   │   ├── __init__.py
│   │   └── config.py             # 项目常量、数据库/路径配置
│   ├── database/                 # 数据库相关
│   │   ├── __init__.py
│   │   └── db.py                 # SQLite连接、会话管理、依赖注入
│   ├── models/                   # ORM模型（数据库表结构）
│   │   ├── __init__.py
│   │   └── book.py               # 图书表ORM模型
│   ├── schemas/                  # Pydantic模型（请求/响应校验）
│   │   ├── __init__.py
│   │   └── book.py               # 图书相关数据模型
│   ├── api/                      # 路由分发核心目录
│   │   ├── __init__.py
│   │   ├── api_v1.py             # 路由汇总注册（版本管理）
│   │   └── endpoints/            # 业务模块接口
│   │       ├── __init__.py
│   │       ├── book.py           # 图书CRUD接口
│   │       └── common.py         # 通用接口（Request对象演示）
│   ├── templates/                # Jinja2模板目录
│   │   ├── base.html             # 基础模板（继承复用）
│   │   ├── index.html            # 项目首页
│   │   └── book_list.html        # 图书列表页
│   └── static/                   # 静态文件目录
│       └── css/
│           └── style.css         # 页面样式
├── .gitignore                    # Git忽略配置
└── requirements.txt              # 项目依赖清单
```

---

## 二、完整代码实现（全注释）
### 1. 项目依赖文件 `requirements.txt`
```txt
fastapi>=0.109.0
uvicorn[standard]>=0.27.0
sqlalchemy>=2.0.0
aiosqlite>=0.19.0
jinja2>=3.1.0
python-multipart>=0.0.6
```

### 2. Git忽略文件 `.gitignore`
```
# Python缓存
__pycache__/
*.py[cod]
*.egg-info/

# 数据库文件
*.db

# 虚拟环境
venv/
env/

# IDE配置
.idea/
.vscode/

# 环境变量
.env
.env.local
```

### 3. 包标识文件 `app/__init__.py`
```python
"""
FastAPI 学习项目核心包
包含项目所有业务代码、配置、路由、模型等
"""
```

### 4. 全局配置 `app/core/config.py`
```python
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
```

### 5. 数据库核心 `app/database/db.py`
```python
"""
数据库连接与会话管理模块
负责SQLite数据库的连接、会话创建、表结构自动生成
"""
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.core.config import SQLITE_URL

# 1. 创建异步数据库引擎
# echo=True：开启SQL语句打印，方便学习调试，生产环境关闭
engine = create_async_engine(
    SQLITE_URL,
    echo=True,
    connect_args={"check_same_thread": False}  # SQLite必填配置，解决多线程问题
)

# 2. 创建异步会话工厂：所有数据库操作都通过会话执行
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)

# 3. ORM基础模型类：所有数据库表模型都必须继承这个类
class Base(DeclarativeBase):
    pass

# 4. 数据库依赖注入函数
# FastAPI依赖系统：每个请求自动创建会话，请求结束自动关闭
async def get_db() -> AsyncSession:
    """
    路由中注入数据库会话的依赖
    用法：在路由参数中添加 db: AsyncSession = Depends(get_db)
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session  # 将会话注入到路由函数
        finally:
            await session.close()  # 无论是否异常，最终都会关闭会话

# 5. 自动创建数据表函数
async def create_tables():
    """
    项目启动时自动创建所有表，表已存在则不重复创建
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all, checkfirst=True)
```

### 6. ORM表模型 `app/models/book.py`
```python
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
```

### 7. Pydantic数据模型 `app/schemas/book.py`
```python
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
```

### 8. 图书模块接口 `app/api/endpoints/book.py`
```python
"""
图书模块API接口
实现图书完整的增删改查（CRUD），演示路由、依赖、数据校验核心用法
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

# 导入数据库依赖
from app.database.db import get_db
# 导入ORM模型
from app.models.book import Book
# 导入Pydantic模型
from app.schemas.book import BookCreate, BookUpdate, BookResponse

# 创建子路由实例
# prefix：该模块所有接口的URL前缀，自动拼接
# tags：接口文档中的分类标签，自动分组
router = APIRouter(
    prefix="/books",
    tags=["图书管理接口"]
)

# 1. 查询所有图书
@router.get("/", response_model=list[BookResponse], summary="获取所有图书列表")
async def get_all_books(db: AsyncSession = Depends(get_db)):
    """
    查询数据库中所有的图书数据
    - 返回值：符合BookResponse模型的图书数组
    """
    # 执行异步查询
    result = await db.execute(select(Book))
    # 提取查询结果
    books = result.scalars().all()
    return books

# 2. 根据ID查询单本图书
@router.get("/{book_id}", response_model=BookResponse, summary="根据ID查询图书详情")
async def get_book_by_id(
    book_id: int,  # 路径参数，自动校验为整数
    db: AsyncSession = Depends(get_db)
):
    """
    根据图书ID查询单本图书详情
    - book_id：图书主键ID
    - 404错误：图书不存在时返回
    """
    # 根据ID查询图书
    result = await db.execute(select(Book).where(Book.id == book_id))
    book = result.scalar_one_or_none()

    # 图书不存在，抛出404异常
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ID为{book_id}的图书不存在"
        )
    return book

# 3. 创建新图书
@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED, summary="创建新图书")
async def create_book(
    book_data: BookCreate,  # 请求体，自动按照BookCreate模型校验
    db: AsyncSession = Depends(get_db)
):
    """
    创建一本新的图书
    - book_data：符合BookCreate模型的JSON请求体
    - 400错误：图书名称已存在时返回
    - 201状态码：创建成功返回（资源创建成功标准状态码）
    """
    # 检查图书名称是否已存在，避免重复
    result = await db.execute(select(Book).where(Book.title == book_data.title))
    existing_book = result.scalar_one_or_none()
    if existing_book:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"图书《{book_data.title}》已存在"
        )

    # 创建ORM对象
    new_book = Book(**book_data.model_dump())
    # 添加到数据库会话
    db.add(new_book)
    # 提交事务
    await db.commit()
    # 刷新对象，获取数据库生成的ID
    await db.refresh(new_book)

    return new_book

# 4. 更新图书信息
@router.put("/{book_id}", response_model=BookResponse, summary="更新图书信息")
async def update_book(
    book_id: int,
    book_data: BookUpdate,  # 更新的请求体，所有字段可选
    db: AsyncSession = Depends(get_db)
):
    """
    根据ID更新图书信息，支持部分更新
    - book_id：要更新的图书ID
    - book_data：仅传入需要修改的字段即可
    - 404错误：图书不存在时返回
    """
    # 查询要更新的图书
    result = await db.execute(select(Book).where(Book.id == book_id))
    book = result.scalar_one_or_none()

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ID为{book_id}的图书不存在"
        )

    # 仅更新传入的字段
    update_data = book_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(book, key, value)

    # 提交事务
    await db.commit()
    # 刷新对象
    await db.refresh(book)

    return book

# 5. 删除图书
@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT, summary="删除图书")
async def delete_book(
    book_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    根据ID删除图书
    - book_id：要删除的图书ID
    - 404错误：图书不存在时返回
    - 204状态码：删除成功返回（无内容标准状态码）
    """
    # 查询要删除的图书
    result = await db.execute(select(Book).where(Book.id == book_id))
    book = result.scalar_one_or_none()

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ID为{book_id}的图书不存在"
        )

    # 删除图书
    await db.delete(book)
    # 提交事务
    await db.commit()

    return
```

### 9. 通用接口（Request对象演示）`app/api/endpoints/common.py`
```python
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
```

### 10. 路由汇总注册 `app/api/api_v1.py`
```python
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
```

### 11. 项目入口 `app/main.py`
```python
"""
项目入口核心文件
创建FastAPI应用实例，注册路由、中间件、静态文件、模板，配置启动事件
是项目启动的唯一入口
"""
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from sqlalchemy.future import select

# 导入项目配置
from app.core.config import (
    PROJECT_NAME,
    PROJECT_VERSION,
    PROJECT_DESCRIPTION,
    TEMPLATES_DIR,
    STATIC_DIR,
    STATIC_URL
)
# 导入汇总路由
from app.api.api_v1 import api_router
# 导入数据库启动函数与依赖
from app.database.db import create_tables, get_db
from app.models.book import Book

# 1. 创建FastAPI应用实例
# 这里的配置会自动同步到接口文档中
app = FastAPI(
    title=PROJECT_NAME,
    version=PROJECT_VERSION,
    description=PROJECT_DESCRIPTION,
    docs_url="/docs",    # Swagger UI文档地址，默认就是/docs
    redoc_url="/redoc"   # ReDoc规范文档地址，默认就是/redoc
)

# 2. 挂载静态文件目录
# 所有以STATIC_URL开头的请求，都会去STATIC_DIR目录查找静态文件
# 例如访问 /static/css/style.css 会返回 app/static/css/style.css
app.mount(
    STATIC_URL,
    StaticFiles(directory=STATIC_DIR),
    name="static"
)

# 3. 初始化Jinja2模板引擎
# 指定模板文件存放目录
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# 4. 注册汇总路由（路由分发的最终步骤）
app.include_router(api_router)

# 5. 项目启动事件：项目启动时自动执行
@app.on_event("startup")
async def startup_event():
    print("===== FastAPI学习项目启动成功 =====")
    # 自动创建数据库表
    await create_tables()
    print("===== 数据库表创建完成 =====")

# 6. 模板渲染接口：项目首页
@app.get("/", response_class=HTMLResponse, summary="项目首页-模板渲染演示")
async def index(request: Request):
    """
    演示Jinja2模板渲染基础用法
    返回项目首页HTML页面
    """
    # 渲染模板，必须传入request对象（FastAPI模板渲染强制要求）
    return templates.TemplateResponse(
        name="index.html",  # 模板文件名，位于templates目录下
        context={
            "request": request,  # 必须传入
            "project_name": PROJECT_NAME,
            "project_version": PROJECT_VERSION
        }
    )

# 7. 模板渲染接口：图书列表页（模板+数据库结合）
@app.get("/book-list", response_class=HTMLResponse, summary="图书列表页-模板+数据库演示")
async def book_list_page(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """
    演示模板渲染与数据库查询结合
    从数据库查询所有图书，渲染到HTML页面中
    """
    # 查询所有图书
    result = await db.execute(select(Book))
    books = result.scalars().all()

    # 渲染模板，传入图书数据
    return templates.TemplateResponse(
        name="book_list.html",
        context={
            "request": request,
            "books": books
        }
    )
```

### 12. 模板文件
#### 基础模板 `app/templates/base.html`
```html
<!-- 基础模板，所有页面继承该模板，实现代码复用 -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}FastAPI学习项目{% endblock %}</title>
    <!-- 引入静态CSS文件 -->
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <!-- 顶部导航栏 -->
    <header class="header">
        <div class="container">
            <h1>FastAPI 学习项目</h1>
            <nav class="nav">
                <a href="/">首页</a>
                <a href="/book-list">图书列表</a>
                <a href="/docs">接口文档</a>
                <a href="/redoc">Redoc文档</a>
            </nav>
        </div>
    </header>

    <!-- 主内容区：子页面通过block填充 -->
    <main class="main">
        <div class="container">
            {% block content %}{% endblock %}
        </div>
    </main>

    <!-- 页脚 -->
    <footer class="footer">
        <div class="container">
            <p>© 2024 FastAPI 学习项目 - 专为入门打造</p>
        </div>
    </footer>
</body>
</html>
```

#### 首页模板 `app/templates/index.html`
```html
<!-- 首页模板，继承基础模板 -->
{% extends "base.html" %}

<!-- 页面标题 -->
{% block title %}首页 - {{ project_name }}{% endblock %}

<!-- 页面主内容 -->
{% block content %}
<div class="welcome-card">
    <h2>欢迎来到 FastAPI 学习项目</h2>
    <p>项目版本：<strong>{{ project_version }}</strong></p>
    <p>本项目专为FastAPI入门打造，覆盖以下核心知识点：</p>
    <ul class="feature-list">
        <li>✅ 路由分发与模块化开发</li>
        <li>✅ 自动生成交互式接口文档</li>
        <li>✅ Request对象核心用法</li>
        <li>✅ 静态文件与Jinja2模板渲染</li>
        <li>✅ SQLite数据库集成（SQLAlchemy ORM）</li>
        <li>✅ Pydantic数据校验与模型设计</li>
        <li>✅ 依赖注入系统</li>
        <li>✅ 完整CRUD接口开发</li>
    </ul>
    <div class="btn-group">
        <a href="/docs" class="btn primary-btn">查看接口文档</a>
        <a href="/book-list" class="btn secondary-btn">查看图书列表</a>
    </div>
</div>
{% endblock %}
```

#### 图书列表模板 `app/templates/book_list.html`
```html
<!-- 图书列表页模板，继承基础模板 -->
{% extends "base.html" %}

<!-- 页面标题 -->
{% block title %}图书列表 - FastAPI学习项目{% endblock %}

<!-- 页面主内容 -->
{% block content %}
<div class="page-header">
    <h2>图书列表</h2>
    <p>从SQLite数据库中查询的所有图书数据</p>
</div>

{% if books %}
<div class="book-grid">
    {% for book in books %}
    <div class="book-card">
        <h3 class="book-title">{{ book.title }}</h3>
        <p class="book-author">作者：{{ book.author }}</p>
        <p class="book-price">价格：¥ {{ book.price }}</p>
        {% if book.description %}
        <p class="book-desc">{{ book.description }}</p>
        {% else %}
        <p class="book-desc">暂无简介</p>
        {% endif %}
    </div>
    {% endfor %}
</div>
{% else %}
<div class="empty-card">
    <h3>暂无图书数据</h3>
    <p>请先通过 <a href="/docs">接口文档</a> 创建图书数据</p>
</div>
{% endif %}
{% endblock %}
```

### 13. 静态样式文件 `app/static/css/style.css`
```css
/* 全局样式重置 */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    line-height: 1.6;
    color: #333;
    background-color: #f5f7fa;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

.container {
    width: 90%;
    max-width: 1200px;
    margin: 0 auto;
}

/* 头部样式 */
.header {
    background-color: #2563eb;
    color: white;
    padding: 1rem 0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.nav {
    display: flex;
    gap: 1.5rem;
    margin-top: 0.5rem;
}

.nav a {
    color: white;
    text-decoration: none;
    font-weight: 500;
    transition: opacity 0.2s;
}

.nav a:hover {
    opacity: 0.8;
}

/* 主内容区 */
.main {
    flex: 1;
    padding: 2rem 0;
}

/* 欢迎卡片 */
.welcome-card {
    background: white;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.1);
}

.welcome-card h2 {
    color: #2563eb;
    margin-bottom: 1rem;
}

.feature-list {
    margin: 1.5rem 0;
    padding-left: 1.5rem;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 0.5rem;
}

.btn-group {
    margin-top: 1.5rem;
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
}

.btn {
    padding: 0.75rem 1.5rem;
    border-radius: 6px;
    text-decoration: none;
    font-weight: 500;
    transition: all 0.2s;
    display: inline-block;
}

.primary-btn {
    background-color: #2563eb;
    color: white;
}

.primary-btn:hover {
    background-color: #1d4ed8;
}

.secondary-btn {
    background-color: #f1f5f9;
    color: #333;
    border: 1px solid #e2e8f0;
}

.secondary-btn:hover {
    background-color: #e2e8f0;
}

/* 图书列表 */
.page-header {
    margin-bottom: 2rem;
}

.page-header h2 {
    color: #2563eb;
}

.book-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 1.5rem;
}

.book-card {
    background: white;
    padding: 1.5rem;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    transition: transform 0.2s;
}

.book-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(0,0,0,0.12);
}

.book-title {
    color: #2563eb;
    margin-bottom: 0.5rem;
}

.book-author {
    color: #64748b;
    margin-bottom: 0.5rem;
}

.book-price {
    color: #dc2626;
    font-weight: 600;
    margin-bottom: 0.75rem;
}

.book-desc {
    color: #64748b;
    font-size: 0.9rem;
}

.empty-card {
    background: white;
    padding: 3rem;
    border-radius: 8px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.1);
    text-align: center;
}

/* 页脚 */
.footer {
    background-color: #1e293b;
    color: #94a3b8;
    padding: 1.5rem 0;
    text-align: center;
    margin-top: auto;
}
```

---

