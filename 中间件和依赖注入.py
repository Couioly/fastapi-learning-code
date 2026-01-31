import uvicorn
from fastapi import FastAPI, Depends, Query
from starlette.responses import PlainTextResponse

app = FastAPI()
"""
中间件：一个在每次请求进入FastAPI应用时都会被执行的函数(中间件)
它在请求到达实际的路径操作函数之前运行，并且在响应返回给客户端之前再运行一次
作用：为每个请求添加统一的处理逻辑（记录日志、身份认证、跨域、设置响应头、性能监控等）
中间件定义：函数顶部使用装饰器 @app.middleware("http")，此处的http是固定的
    request: 请求
    call_next: 传递请求给路径处理函数
代码：
@app.middleware("http")
async def middleware(request, call_next):
    print("中间件开始处理 —— start")
    response = await call_next(request)
    print("中间件处理完成 —— end")
    return response
多个中间件的执行顺序是 ——> 自下而上
"""

@app.middleware("http")
async def middleware1(request, call_next):
    print("中间件1开始处理->start")
    response = await call_next(request)    # 注意call_next()是采用异步方式await
    print("中间件1结束处理->end")
    return response

@app.middleware("http")
async def middleware2(request, call_next):
    print("中间件2开始处理->start")
    response = await call_next(request)
    print("中间件2结束处理->end")
    return response

@app.get("/")
async def root():
    return PlainTextResponse("Hello World!")

"""
依赖注入的路由是程序员自行控制的，而中间件是面向每一个路由的(核心区别)
使用依赖注入系统来共享通用逻辑，减少代码的重复
依赖项：可重用的组件（函数/类），负责提供某种功能或数据
注入：FastAPI自动帮忙调用依赖项，并将结果注入到路径操作函数中
优点：1. 代码复用  2. 解耦  3. 易于测试
依赖注入的应用场景：
    - 处理请求参数：从请求中提取和验证参数（路径参数、查询参数、请求体）
    - 共享业务逻辑：抽取封装多个路由公共的逻辑代码
    - 共享数据库链接：管理数据库会话的创建、使用、关闭
    - 安全和认证：验证用户身份、检查权限和角色要求等
"""
# 依赖注入的步骤
# 1. 创建依赖项(创建依赖函数)
async def common_parameters(
        skip: int = Query(0, ge=0),
        limit: int = Query(10, le=60)
):
    return {"skip": skip, "limit": limit}

# 2. 导入Depends
#    from fastapi import Depends

# 3. 声明依赖项(依赖注入)
@app.get("/common/news")
async def common_news(commons = Depends(common_parameters)):
    return commons

@app.get("/common/user")
async def common_user(commons = Depends(common_parameters)):
    return commons

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)