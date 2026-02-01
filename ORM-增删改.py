from datetime import datetime
import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import DateTime, func, Integer, String, Float
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_session, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.testing.schema import mapped_column

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
# 数据库路径
ASYNC_DATABASE_URL = "mysql+aiomysql://root:20060420@127.0.0.1:3306/fastapi01?charset=utf8"
# 创建异步引擎
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,
    pool_size=10,
    max_overflow=2
)
# 创建基类
class Base(DeclarativeBase):
    create_time: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now(), default=datetime.now,comment="创建时间")
    update_time: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now(), default=datetime.now,comment="修改时间", onupdate=func.now())
# 创建模型类
class Book(Base):
    __tablename__ = "book"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, comment="书籍id")
    bookname: Mapped[str] = mapped_column(String(50), comment="书名")
    author: Mapped[str] = mapped_column(String(32), comment="作者")
    price: Mapped[float] = mapped_column(Float, comment="价格")
    press: Mapped[str] = mapped_column(String(32), comment="出版社")

# 创建会话工厂
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)
# 创建依赖项
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

"""
数据库操作——新增
步骤：定义ORM对象 -> 添加对象到事务: add(对象) -> commit 提交到数据库
"""
# 需求：用户输入图书信息（id、书名、作者、价格、出版社）-> 新增
# 用户新增 -> 参数 -> 请求体
class BookBase(BaseModel):
    id: int
    bookname: str
    author: str
    price: float
    press: str

@app.post("/book/add_book")
async def add_book(book: BookBase, db: AsyncSession=Depends(get_db)):
    # ORM对象 -> add -> commit
    book_orm = Book(**book.__dict__)
    db.add(book_orm)
    await db.commit()
    return book

"""
数据库操作——更新
步骤：先查后改     定义新的类->查询id->若存在则更新数据->提交
"""
class BookUpdate(BaseModel):
    bookname: str
    author: str
    price: float
    press: str

@app.put("/book/update_book/{book_id}")
async def update_book(book_id: int, data: BookUpdate, db: AsyncSession=Depends(get_db)):
    # 根据id查询该书籍
    db_info = await db.get(Book, book_id)
    # 若不存在则抛出异常
    if db_info is None:
        raise HTTPException(status_code=404,detail="查无此书")
    # 执行更新操作：重新赋值
    db_info.bookname = data.bookname
    db_info.author = data.author
    db_info.price = data.price
    db_info.press = data.press
    # 提交至数据库
    await db.commit()
    return db_info

"""
数据库操作——删除
步骤：先查再删     查询id->若存在则执行delete删除操作->提交
"""
@app.delete("/book/delete_book/{book_id}")
async def delete_book(book_id: int, db: AsyncSession=Depends(get_db)):
    # 根据id查询该书籍
    db_info = await db.get(Book, book_id)
    # 若不存在则抛出异常
    if db_info is None:
        raise HTTPException(status_code=404,detail="查无此书")

    await db.delete(db_info)
    await db.commit()
    return {"msg":"删除成功"}

if __name__ == '__main__':
    uvicorn.run(app)