# FastAPI 学习项目

## 项目介绍

这是一个FastAPI学习项目，包含了FastAPI框架的各种核心功能和使用方法。项目通过多个示例文件，详细展示了FastAPI的基本用法、参数处理、响应类型、中间件、依赖注入以及ORM数据库操作等功能。

## 项目结构

```
FastAPI/
├── main.py                  # 基础FastAPI应用示例
├── 入门与参数介绍.py           # FastAPI参数处理示例
├── 响应类型介绍.py             # FastAPI响应类型示例
├── 中间件和依赖注入.py          # 中间件和依赖注入示例
├── ORM-介绍及建表.py           # ORM概念和建表示例
├── ORM-增删改.py              # ORM数据增删改操作示例
├── ORM-查询.py                # ORM数据查询操作示例
└── .gitignore                # Git忽略文件
```

## 安装依赖

```bash
# 安装FastAPI
pip install fastapi

# 安装uvicorn（ASGI服务器）
pip install uvicorn

# 安装Pydantic（数据验证）
pip install pydantic

# 安装SQLAlchemy和aiomysql（ORM和数据库连接）
pip install sqlalchemy[asyncio] aiomysql
```

## 运行项目

### 运行单个文件

```bash
# 例如运行main.py
uvicorn main:app --reload

# 或者直接运行Python文件
python main.py
```

### 访问API文档

FastAPI自动生成交互式API文档：
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## 功能模块介绍

### 1. 基础应用（main.py）

展示了FastAPI的最基本用法，创建一个简单的API端点。

### 2. 参数处理（入门与参数介绍.py）

- **路径参数**：URL路径的一部分，用于标识特定资源
- **查询参数**：用于过滤、排序、分页等操作
- **请求体参数**：用于创建、更新资源，携带大量数据

### 3. 响应类型（响应类型介绍.py）

- **JSON响应**：默认响应类型
- **HTML响应**：返回HTML内容
- **文件响应**：返回文件下载
- **纯文本响应**：返回纯文本内容
- **重定向响应**：重定向到其他URL
- **自定义响应类型**：使用Pydantic模型定义响应结构
- **异常响应**：处理错误情况

### 4. 中间件和依赖注入（中间件和依赖注入.py）

- **中间件**：在请求到达和响应返回时执行的函数，用于添加统一处理逻辑
- **依赖注入**：共享通用逻辑，减少代码重复，用于参数处理、业务逻辑、数据库连接等

### 5. ORM数据库操作

#### ORM-介绍及建表.py
- ORM概念介绍
- 数据库引擎创建
- 模型类定义
- 数据库表创建

#### ORM-增删改.py
- 数据新增操作
- 数据更新操作
- 数据删除操作

#### ORM-查询.py
- 简单查询
- 条件查询
- 模糊查询
- 多条件联合查询
- 聚合查询
- 分页查询

## 数据库配置

项目使用MySQL数据库，配置信息如下：

```python
# 数据库连接URL格式
# mysql+aiomysql://用户名:用户密码@数据库地址:端口号/数据库名称?charset=编码

# 示例配置
ASYNC_DATABASE_URL = "mysql+aiomysql://root:20060420@127.0.0.1:3306/fastapi01?charset=utf8"
```

## 示例API端点

### 基础端点
- `GET /` - 返回Hello World

### 参数处理示例
- `GET /hello/{name}` - 路径参数示例
- `GET /book/{id}` - 带验证的路径参数示例
- `GET /query/book` - 查询参数示例
- `POST /add_book` - 请求体参数示例

### 响应类型示例
- `GET /html` - HTML响应示例
- `GET /taohuoluo` - 文件响应示例
- `GET /password` - 纯文本响应示例
- `GET /github` - 重定向响应示例
- `POST /user` - 自定义响应类型示例
- `GET /news/{id}` - 异常响应示例

### ORM操作示例
- `GET /book/books` - 查询所有书籍
- `POST /book/add_book` - 新增书籍
- `PUT /book/update_book/{book_id}` - 更新书籍
- `DELETE /book/delete_book/{book_id}` - 删除书籍
- `GET /books/get_book/{book_id}` - 根据ID查询书籍
- `GET /books/search_price_ge50` - 条件查询示例
- `GET /books/search_like_python` - 模糊查询示例
- `GET /book/book_func` - 聚合查询示例
- `GET /book/book_offset` - 分页查询示例

## 学习资源

- [FastAPI官方文档](https://fastapi.tiangolo.com/)
- [SQLAlchemy官方文档](https://docs.sqlalchemy.org/)
- [Pydantic官方文档](https://docs.pydantic.dev/)

## 注意事项

1. 运行ORM相关示例前，需要确保MySQL数据库已启动，并且创建了对应的数据库
2. 数据库连接信息需要根据实际情况修改
3. 项目仅用于学习目的，实际生产环境需要考虑更多安全因素
