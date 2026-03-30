"""
database连接与会话管理模块
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
