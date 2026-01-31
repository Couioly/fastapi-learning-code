from datetime import datetime
from fastapi import FastAPI, Depends
from sqlalchemy import func, DateTime, Integer, String, Float, select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

"""
ORM(Object-RelationalMapping,对象关系映射)是一种编程技术，
用于在面向对象编程语言和关系型数据库之间建立映射
它允许开发者通过操作对象的方式与数据库进行交互，而无需直接编写复杂的SQL语句
优势：
    - 减少重复的SQL代码
    - 代码更简洁易读
    - 自动处理数据库链接和事务
    - 自动防止SQL注入攻击
分类：
    ORM工具               特点                     适用场景
    SQLAlchemy ORM       功能最强、最灵活、企业级    各类API、微服务、数据应用
    Django ORM           封装好、上手快             Django项目、管理后台
    Tortoise ORM         全异步                    异步Web服务，高并发API
"""

# 安装sqlalchemy -> pip install sqlalchemy[asyncio] aiomysql
# ORM建表三步走

"""
1. 创建数据库引擎
使用 create_async_engine 创建异步引擎
"""
# 导包
# from sqlalchemy.ext.asyncio import create_async_engine
# 定义数据库url
# ASYNC_DATABASE_URL = "mysql+aiomysql://用户名:用户密码@数据库地址:端口号/数据库名称?charset=编码"
ASYNC_DATABASE_URL = "mysql+aiomysql://root:20060420@127.0.0.1:3306/fastapi01?charset=utf8"
# 创建异步引擎
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,          # 可选 输出SQL日志
    pool_size=10,       # 设置连接池中保持的持久连接数
    max_overflow=20     # 设置连接池允许创建的额外连接数
)

"""
2. 定义模型类
    - 基类，继承DeclarativeBase（包含通用属性和字段的映射）
    - 定义数据库表的模型类
"""
class Base(DeclarativeBase):
    # 字段名: Mapped[类型] = mapped_column(数据库列字段类型, 插入默认数值...) mapped_column->关联数据库列
    create_time: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now(), default=datetime.now, comment="创建时间")
    update_time: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now(), default=datetime.now, comment="修改时间", onupdate=func.now())

class Book(Base):
    __tablename__ = "book"  # 表名称

    id: Mapped[int] = mapped_column(Integer, primary_key=True, comment="书籍id")
    bookname: Mapped[str] = mapped_column(String(50), comment="书名")
    author: Mapped[str] = mapped_column(String(32), comment="作者")
    price: Mapped[float] = mapped_column(Float,comment="价格")
    press: Mapped[str] = mapped_column(String(32), comment="出版社")

"""
3. 启动应用时建表
    - 从连接池获取异步连接，开启事务，执行ORM操作
    - FastAPI应用启动时，创建数据库表
"""
async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("startup")
async def startup_event():
    await create_tables()

# 需求：使用SQLAlchemy ORM创建用户表，必包含字段：id, name, password, crate_time, update_time
class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, comment="主键")
    name: Mapped[str] = mapped_column(String(10), comment="用户名")
    password: Mapped[str] = mapped_column(String(255), comment="密码")
    phone: Mapped[str] = mapped_column(String(11),comment="手机号")
    address: Mapped[str] = mapped_column(String(128), comment="住址")

# 需求：查询功能的接口，查询图书 -> 依赖注入：创建依赖项获取数据库会话 + Depends 注入路由处理函数
# 1. 导入所需模块 -> from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
# 2. 创建异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,      # 绑定数据库引擎
    class_=AsyncSession,    # 指定会话类
    expire_on_commit=False  # 提交后会话不过期，不会重新查询数据库
)
# 3. 依赖项
async def get_database():
    async with AsyncSessionLocal() as session:
        try:
            yield session              # 返回数据库会话给路由处理函数
            await session.commit()     # 提交事务
        except Exception:
            await session.rollback()   # 异常回滚
            raise
        finally:
            await session.close()      # 关闭会话，防止泄露

@app.get("/book/books")
async def get_book_list(db=Depends(get_database)): # 注入依赖项
    # 查询
    result = await db.execute(select(Book))
    books = result.scalars().all()
    return books