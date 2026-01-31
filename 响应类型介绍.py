from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, PlainTextResponse, RedirectResponse
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"} # 默认转换为JSON格式

"""
默认情况，FastAPI会自动将路径操作函数返回的Python对象(字典、列表、Pydantic模型等)
由jsonable_encoder转换为JSON兼容格式，并包装为JSONResponse返回
    响应类型            用途                      示例
    JSONResponse       默认响应，返回JSON数据      return {"key":"value"}
    HTMLResponse       返回HTML内容               return HTMLResponse(html_content)
    PlainTextResponse  返回纯文本                 return PlainTextResponse("text")
    FileResponse       返回文件下载               return FileResponse(path)
    StreamingResponse  流式响应                   生成器函数返回数据
    RedirectResponse   重定向                     return RedirectResponse(url) 
"""

# 装饰器指定响应类 (提前在fastapi.responses包中导入HTMLResponse)
@app.get("/html", response_class=HTMLResponse)
async def html():
    return "<h1>你是我儿！！！</h1><h4>不接受反驳</h4>"

# 返回类型指定响应对象(在return后指定响应对象)
@app.get("/taohuoluo")
async def file():
    path = "./file/桃花诺.mp3"
    return FileResponse(path)

@app.get("/password")
async def password():
    return PlainTextResponse("儿子，叫声爸爸听听！！！")

# 重定向
@app.get("/github")
async def github():
    return RedirectResponse("/html")

# 自定义返回类型->三步骤: 导包、定义类、使用类型
# 1. 导包：from pydantic import BaseModel
# 2. 定义类型
class User(BaseModel):
    name: str
    age: int
    sex: str
    address: str
# 3. 使用类型 方法->路径操作函数(api路径,response_model=类型名)
@app.post("/user", response_model=User)
async def get_user(user: User):
    # return 返回的类型必须与User一致(顺序不做要求)，否则会报错
    return {"name": user.name,"sex":user.sex,"age": user.age,"address": user.address}

"""
异常响应处理：从fastapi导入HTTPException
在异常处直接使用raise HTTPException(status_code=状态码, detail=错误描述)
"""
# 查看新闻内容，新闻id范围是1~6
@app.get("/news/{id}")
async def news(id:int):
    new_list = [i for i in range(1,7)]
    if id not in new_list:
        raise HTTPException(status_code=404,detail=f"未查询到新闻信息")
    return {"id": id, "content":f"查询到{id}的信息" }