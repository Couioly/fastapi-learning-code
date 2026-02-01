from datetime import datetime
import uvicorn
from fastapi import FastAPI, Depends, Query
from sqlalchemy import String, Integer, Float, DateTime, func, select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


ASYNC_DATABASE_URL = "mysql+aiomysql://root:20060420@127.0.0.1:3306/fastapi01?charset=utf8"
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,
    pool_size=10,
    max_overflow=2
)

class Base(DeclarativeBase):
    create_time: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now(), default=datetime.now,comment="创建时间")
    update_time: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now(), default=datetime.now,comment="修改时间", onupdate=func.now())

class Book(Base):
    __tablename__ = "book"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, comment="书籍id")
    bookname: Mapped[str] = mapped_column(String(50), comment="书名")
    author: Mapped[str] = mapped_column(String(32), comment="作者")
    price: Mapped[float] = mapped_column(Float, comment="价格")
    press: Mapped[str] = mapped_column(String(32), comment="出版社")


SyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_tb():
    async with SyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


"""
简单查询
核心语句：await db.execute(select(模型类)), 返回一个 ORM 对象
获取所有数据：ORM对象.scalars().all()
获取单条数据：ORM对象.scalars().first()
"""


@app.get("/book/books")
async def get_book_list(db: AsyncSession = Depends(get_tb)):
    # 调用查询语句获取ORM对象
    orm_result = await db.execute(select(Book))
    # 获取所有图书信息
    book = orm_result.scalars().all()
    # 获取首条图书信息
    # book = orm_result.scalars().first()
    return book


"""
条件查询：
1. 根据指定模型类的指定id信息查询：AsyncSession对象.get(模型类,主键值)
2. 使用比较判断(==,>,<,>=,<=) -> 基础语法: select(模型类).where(条件1, 条件2, ...)
3. 使用模糊查询(%匹配任意字符, _匹配单个字符) -> 基础语法: select(模型类).where(表字段.like(模糊查询))
4. 多条件联合查询(|、&、~) -> 基础语法： select(模型类).where(条件1 | 条件2)
"""


# 根据图书id查询书籍
@app.get("/books/get_book/{book_id}")
async def get_book(book_id: int, db: AsyncSession = Depends(get_tb)):
    # 直接使用AsyncSession对象提供的get函数获取指定模型类的指定id信息
    # return await db.get(Book,book_id)
    result = await db.execute(select(Book).where(Book.id == book_id))
    book = result.scalar_one_or_none()
    return book


# 查询图书价格大于等于50的书籍
@app.get("/books/search_price_ge50")
async def get_book_search(db: AsyncSession = Depends(get_tb)):
    result = await db.execute(select(Book).where(Book.price >= 50))
    books = result.scalars().all()
    return books


# 查询图书名称包含“Python”字样的书籍
@app.get("/books/search_like_python")
async def get_book_search(db: AsyncSession = Depends(get_tb)):
    result = await db.execute(select(Book).where(Book.bookname.like("%python%")))
    books = result.scalars().all()
    return books


# 查询书名包含“Python”字样并且价格小于66的书籍
@app.get("/books/search_like_python_price_lt66")
async def get_book_search(db: AsyncSession = Depends(get_tb)):
    result = await db.execute(select(Book).where(Book.bookname.like("%python%") & ~(Book.price >= 66)))
    books = result.scalars().all()
    return books


# 查询指定列表中包含的书籍
@app.get("/books/search_list")
async def get_book_list(db: AsyncSession = Depends(get_tb)):
    book_list = [1, 3, 5, 7]
    result = await db.execute(select(Book).where(Book.id.in_(book_list)))
    books = result.scalars().all()
    return books


"""
聚合查询
聚合查询语法：func.方法(模型类.属性)
- count: 统计行数量
- avg: 求平均值
- max: 求最大值
- min: 求最小值
- sum: 求和
语法位置参考：await db.execute(select(func.方法(模型类.属性))
"""


@app.get("/book/book_func")
async def get_book_func(db: AsyncSession = Depends(get_tb)):
    book_count = await db.execute(select(func.count(Book.id)))
    price_avg = await db.execute(select(func.avg(Book.price)))
    price_max = await db.execute(select(func.max(Book.price)))
    price_min = await db.execute(select(func.min(Book.price)))
    price_sum = await db.execute(select(func.sum(Book.price)))
    countP = book_count.scalar()
    avgP = price_avg.scalar()
    maxP = price_max.scalar()
    minP = price_min.scalar()
    sumP = price_sum.scalar()
    return {"book_count": countP, "price_avg": avgP, "price_max": maxP, "price_min": minP, "price_sum": sumP}


"""
分页查询
分页查询语法：select().offset().limit()
- offset: 跳过的记录数    offset值=(当前页码-1)*每页数量limit
- limit: 返回的记录数
"""


@app.get("/book/book_offset")
async def get_book_offset(
        page: int = Query(1, ge=1),
        page_size: int = Query(1, ge=1),
        db: AsyncSession = Depends(get_tb)):
    skip = (page - 1) * page_size
    result = await db.execute(select(Book).offset(skip).limit(page_size))
    books = result.scalars().all()
    return books


"""
从ORM对象获取数据的方式
获取所有数据 - scalars().all()
获取单条数据 
- scalars().first():提取第一条数据
- scalar_one_or_none():提取一个或null
- scalar():提取标量值(配合聚合查询使用)
"""

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)