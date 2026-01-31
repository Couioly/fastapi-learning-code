import uvicorn
from fastapi import FastAPI, Path, Query
from pydantic import BaseModel, Field

# 创建 FastAPI 实例
app = FastAPI()


# 根  async关键字表示该路径操作函数是异步函数
@app.get("/")  # 装饰器 -> @FastAPI实例.请求方法(请求路径)
async def root():
    return {"message": "Hello World"}  # 响应结果


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


"""
路由是 URL 地址和处理函数之间的映射关系

命令行启动方式: uvicorn main:app --reload
    uvicorn : FastAPI高性能服务器,用于运行FastAPI项目
    main:app : FastAPI文件名:FastAPI实例名
    --reload : 当代码修改后自动重启服务器(可选)

FastAPI自动生成的交互式文档: http://127.0.0.1:8000/docs
"""


# 黑马练习：访问路径 /user/hello，响应结果是 {"msg":"我正在学习 FastAPI..."}
@app.get("/hello")
async def say_doing():
    return {"msg": "我正在学习 FastAPI..."}


"""
路径参数：URL路径的一部分，指向唯一的、特定的资源 GET
路径参数-类型注解Path(导入FastAPI的Path函数)
    - ... : 必填(可以在此处替换为默认值)
    - gt/ge : 大于/大于等于
    - lt/le : 小于/小于等于
    - description : 描述
    - min_length/max_length : 长度限制 
"""


# 路径参数
@app.get("/book/{id}")  # 路径操作函数(参数id:原生注解=Path注解)
async def get_book(id: int = Path(..., ge=1, le=100, description="书籍id，取值范围是1~100")):
    return {"id": id, "msg": f"这是第{id}本书"}


# 黑马练习：以用户 id 为路径参数设计 URL，要求响应结果包含用户 id 和 名称 (普通用户 id)
@app.get("/user/{userid}")
async def get_user(userid: int):
    return {"userid": userid, "username": f'普通用户{userid}'}


"""
查询参数：声明的参数不是路径参数时，路径操作函数会把该函数自动解释为查询参数
    位置在URL的"?"之后，如"k1=v1&k2=v2"，参数之间使用"&"分割
    作用是对资源集合进行过滤、排序、分页等操作 (GET请求)
"""


# 需求：设计接口查询图书，要求携带两个查询参数：
#       图书分类：默认值为 Python开发，长度限制5~255
#       价格：限制大小范围 50~100
@app.get("/query/book")
async def query_book(
        classification: str = Query("Python开发", min_length=5, max_length=255),
        price: int = Query(..., gt=49, lt=101)
):
    return {"classification": classification, "price": price}


"""
请求体参数：位置在HTTP请求的消息体(body)中
作用：创建、更新资源、携带大量数据，如json
请求方法：POST、PUT等
请求由三部分组成：
    - 请求行：包含方法、URL、协议版本
    - 请求头：元数据信息(Content-Type、Authorization等)
    - 请求体：实际要发送的数据内容
代码：
    from pydantic import BaseModel
    class 类名(BaseModel):
        参数1:注解
        参数2:注解
        ...
    直接在接口的路径操作函数中以原生注解的方式传入,即(形参:类名)
请求体参数添加类型注解：从pydantic类导入Field
    from pydantic import BaseModel
    class 类名(BaseModel):
        参数1:原生注解=Field(...,default=None,gt=None,ge=None,...)
        参数2:原生注解=Field(...,default=None,gt=None,ge=None,...)
        ...
"""


# 需求：设计接口新增图书，图书信息包含：书名、作者、出版社、售价
# 定义类型
class Book(BaseModel):
    name: str = Field(..., min_length=5, max_length=255)
    author: str = Field(..., min_length=2, max_length=10)
    press: str = Field(..., min_length=2, max_length=10)
    price: int = Field(..., gt=49, lt=101)


@app.post("/add_book")
async def add_book(book: Book):
    return book

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)