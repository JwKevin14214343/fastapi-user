# FastAPI 用户管理系统

基于 **SQLite 数据库** 的用户增删改查（CRUD）API

## 环境要求

- Python 3.11
- pip (Python包管理器)
- SQLite（Python内置，无需单独安装）

## 项目结构

```
fastapi-user/
├── db/                      # 数据库模块
│   ├── __init__.py         # 包初始化文件
│   ├── database.py         # 数据库连接配置
│   └── model.py            # ORM数据模型
├── fastapi-user-main/       # 主应用目录
│   ├── main.py             # FastAPI应用主文件
│   └── requirements.txt    # 项目依赖
├── init_db.py              # 数据库初始化脚本
├── test_api.py             # API测试脚本
├── users.db                # SQLite数据库文件（运行后自动生成）
└── README.md               # 项目说明文档
```

## 🚀 快速开始

```bash
# 1. 激活Python 3.11环境
conda activate py311

# 2. 进入项目目录
cd D:\aproduct\fastapi-user

# 3. 安装依赖
cd fastapi-user-main
pip install -r requirements.txt

# 4. （可选）初始化数据库并插入测试数据
cd ..
python init_db.py

# 5. 运行应用
cd fastapi-user-main
python -m uvicorn main:app --reload

# 6. 访问API文档
# 浏览器打开: http://127.0.0.1:8000/docs
```

## 💾 数据库说明

### 数据库类型
- **SQLite**：轻量级文件数据库，无需额外安装和配置
- **数据库文件**：`users.db`（自动创建在项目根目录）
- **ORM框架**：SQLAlchemy 2.0

### 数据库表结构

**表名：** `users`

| 字段名 | 类型 | 说明 | 约束 |
|--------|------|------|------|
| id | INTEGER | 用户ID | 主键、自增 |
| name | VARCHAR(100) | 用户姓名 | 非空 |
| email | VARCHAR(255) | 用户邮箱 | 非空、唯一、索引 |
| age | INTEGER | 用户年龄 | 可空 |
| created_at | DATETIME | 创建时间 | 自动生成 |
| updated_at | DATETIME | 更新时间 | 自动更新 |

### 初始化数据库

首次运行或需要重置数据库时：

```bash
python init_db.py
```

该脚本会：
1. 创建数据库表结构
2. （可选）清空现有数据
3. 插入测试数据（张三、李四、王五、赵六）
```

## 运行应用

**方法1：直接运行（推荐）**
```bash
cd fastapi-user-main
python main.py
```

**方法2：使用uvicorn**
```bash
cd fastapi-user-main
python -m uvicorn main:app --reload
```

应用将在 http://127.0.0.1:8000 启动

## API 文档

启动应用后，可以访问：
- **Swagger UI**: http://localhost:8000/docs （交互式API文档）
- **ReDoc**: http://localhost:8000/redoc （更美观的文档展示）

### HTTP 状态码说明

| 状态码 | 说明 | 使用场景 |
|--------|------|----------|
| 200 | OK | 请求成功（查询、更新） |
| 201 | Created | 创建成功 |
| 204 | No Content | 删除成功（无返回内容） |
| 400 | Bad Request | 请求参数错误（邮箱重复、格式错误等） |
| 404 | Not Found | 资源不存在（用户不存在） |
| 422 | Unprocessable Entity | 请求格式错误（字段类型错误） |

## API 接口

### 1. 创建用户
**POST** `/users/`

**请求体：**
```json
{
  "name": "张三",
  "email": "zhangsan@example.com",
  "age": 25
}
```

**响应 (201 Created)：**
```json
{
  "id": 1,
  "name": "张三",
  "email": "zhangsan@example.com",
  "age": 25,
  "created_at": "2024-12-15T10:30:00.123456"
}
```

**错误响应 (400 Bad Request)：**
```json
{
  "detail": "该邮箱已被注册"
}
```

---

### 2. 获取所有用户
**GET** `/users/`

**响应 (200 OK)：**
```json
[
  {
    "id": 1,
    "name": "张三",
    "email": "zhangsan@example.com",
    "age": 25,
    "created_at": "2024-12-15T10:30:00.123456"
  },
  {
    "id": 2,
    "name": "李四",
    "email": "lisi@example.com",
    "age": 30,
    "created_at": "2024-12-15T10:31:00.123456"
  }
]
```

---

### 3. 获取单个用户
**GET** `/users/{user_id}`

**示例：** `GET /users/1`

**响应 (200 OK)：**
```json
{
  "id": 1,
  "name": "张三",
  "email": "zhangsan@example.com",
  "age": 25,
  "created_at": "2024-12-15T10:30:00.123456"
}
```

**错误响应 (404 Not Found)：**
```json
{
  "detail": "用户不存在"
}
```

---

### 4. 更新用户
**PUT** `/users/{user_id}`

**请求体（所有字段可选）：**
```json
{
  "name": "李四",
  "email": "lisi@example.com",
  "age": 30
}
```

**响应 (200 OK)：**
```json
{
  "id": 1,
  "name": "李四",
  "email": "lisi@example.com",
  "age": 30,
  "created_at": "2024-12-15T10:30:00.123456"
}
```

**错误响应：**
- `404 Not Found`: 用户不存在
- `400 Bad Request`: 邮箱已被其他用户使用

---

### 5. 删除用户
**DELETE** `/users/{user_id}`

**响应 (204 No Content)：** 无响应体

**错误响应 (404 Not Found)：**
```json
{
  "detail": "用户不存在"
}
```

---

### 6. 根据邮箱搜索用户
**GET** `/users/search/by-email?email=zhangsan@example.com`

**响应 (200 OK)：**
```json
{
  "id": 1,
  "name": "张三",
  "email": "zhangsan@example.com",
  "age": 25,
  "created_at": "2024-12-15T10:30:00.123456"
}
```

**错误响应 (404 Not Found)：**
```json
{
  "detail": "未找到该邮箱对应的用户"
}
```

---

### 7. 获取用户统计 🆕
**GET** `/stats/count`

**响应 (200 OK)：**
```json
{
  "total_users": 10
}
```

### 🔍 分页查询

获取所有用户接口支持分页参数：

**GET** `/users/?skip=0&limit=10`

- `skip`：跳过前N条记录（默认0）
- `limit`：返回最多N条记录（默认100）

**示例：**
```bash
# 获取第1-10条用户
GET /users/?skip=0&limit=10

# 获取第11-20条用户
GET /users/?skip=10&limit=10
```

## 示例使用

### 方式1：使用测试脚本（推荐）

```bash
# 确保应用正在运行，然后在新终端执行
python test_api.py
```

### 方式2：使用 Swagger UI

1. 启动应用后访问：http://localhost:8000/docs
2. 在页面上直接测试各个API接口
3. 点击 "Try it out" 按钮即可交互式测试

### 方式3：使用 curl 命令

**Windows PowerShell：**
```powershell
# 创建用户
Invoke-RestMethod -Uri "http://localhost:8000/users/" -Method Post -ContentType "application/json" -Body '{"name":"张三","email":"zhangsan@example.com","age":25}'

# 获取所有用户
Invoke-RestMethod -Uri "http://localhost:8000/users/"

# 获取指定用户
Invoke-RestMethod -Uri "http://localhost:8000/users/1"

# 更新用户
Invoke-RestMethod -Uri "http://localhost:8000/users/1" -Method Put -ContentType "application/json" -Body '{"name":"张三（已更新）","age":26}'

# 删除用户
Invoke-RestMethod -Uri "http://localhost:8000/users/1" -Method Delete
```

**使用 curl（需安装curl）：**
```bash
# 创建用户
curl -X POST "http://localhost:8000/users/" -H "Content-Type: application/json" -d "{\"name\":\"张三\",\"email\":\"zhangsan@example.com\",\"age\":25}"

# 获取所有用户
curl http://localhost:8000/users/

# 获取指定用户
curl http://localhost:8000/users/1

# 更新用户
curl -X PUT "http://localhost:8000/users/1" -H "Content-Type: application/json" -d "{\"name\":\"张三（已更新）\",\"age\":26}"

# 删除用户
curl -X DELETE http://localhost:8000/users/1
```

### 方式4：使用 Python requests

```python
import requests

# 创建用户
response = requests.post(
    "http://localhost:8000/users/",
    json={"name": "张三", "email": "zhangsan@example.com", "age": 25}
)
print(response.json())

# 获取所有用户
response = requests.get("http://localhost:8000/users/")
print(response.json())
```

## 功能特性

### 🎯 核心功能
- ✅ 创建用户（自动生成ID和创建时间）
- ✅ 获取所有用户列表（支持分页）
- ✅ 根据ID获取单个用户
- ✅ 更新用户信息（支持部分更新）
- ✅ 删除用户
- ✅ 根据邮箱搜索用户
- ✅ 获取用户统计信息

### 🛡️ 数据验证
- ✅ 邮箱唯一性验证（数据库级别）
- ✅ 邮箱格式验证（Pydantic）
- ✅ 字段类型验证
- ✅ 完整的错误处理（404、400、422等）

### 💾 数据库特性
- ✅ **SQLite持久化存储**（数据不会丢失）
- ✅ SQLAlchemy ORM（对象关系映射）
- ✅ 自动创建/更新时间戳
- ✅ 数据库索引优化（email字段）
- ✅ 事务管理和回滚
- ✅ 数据库会话管理（依赖注入）

### 📊 其他特性
- ✅ 交互式API文档（Swagger UI）
- ✅ 完整的类型注解
- ✅ RESTful API设计
- ✅ 分页查询支持

## ⚠️ 注意事项

### 数据持久化
- ✅ **本项目已使用SQLite数据库**，数据会持久化保存在 `users.db` 文件中
- ✅ 重启应用后数据**不会丢失**
- ✅ 删除 `users.db` 文件可以清空所有数据

### 生产环境建议
如需部署到生产环境，建议：
1. 使用 PostgreSQL 或 MySQL 替代 SQLite
2. 添加用户认证和授权机制
3. 配置HTTPS
4. 添加日志记录
5. 配置CORS（跨域资源共享）
6. 添加数据备份策略

## ❓ 常见问题

### 1. ModuleNotFoundError: No module named 'fastapi'

**原因：** 没有安装依赖包

**解决：**
```bash
pip install -r requirements.txt
```

### 2. 端口 8000 已被占用

**原因：** 端口被其他应用占用

**解决方式1：** 关闭占用端口的程序
```bash
# Windows查看端口占用
netstat -ano | findstr :8000

# 结束进程（PID是上面命令查到的进程ID）
taskkill /PID <进程ID> /F
```

**解决方式2：** 修改端口
在 `main.py` 最后一行修改端口：
```python
uvicorn.run(app, host="0.0.0.0", port=8001)  # 改为8001或其他端口
```

### 3. uvicorn 安装失败或编译慢

**解决：** 使用预编译版本
```bash
pip install fastapi uvicorn[standard] pydantic[email] requests
```

### 4. 如何停止应用？

在运行应用的终端按 `Ctrl + C`

### 5. 数据保存在哪里？

数据保存在 **SQLite 数据库文件** 中：
- **文件位置：** 项目根目录下的 `users.db`
- **持久化：** 重启应用后数据不会丢失
- **查看数据：** 可以使用 SQLite 客户端工具查看
  - [DB Browser for SQLite](https://sqlitebrowser.org/)（推荐）
  - [SQLite Viewer](https://inloop.github.io/sqlite-viewer/)（在线）

**清空数据库：**
```bash
# 方法1: 删除数据库文件（应用会自动重建）
del users.db  # Windows
rm users.db   # Linux/Mac

# 方法2: 运行初始化脚本并选择清空
python init_db.py
```

### 5.1 如何切换到其他数据库？

修改 `db/database.py` 中的连接字符串：

**PostgreSQL：**
```python
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/dbname"
```

**MySQL：**
```python
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://user:password@localhost/dbname"
```

### 6. 如何允许外网访问？

默认配置 `host="0.0.0.0"` 已允许外网访问，需要：
1. 确保防火墙开放 8000 端口
2. 路由器配置端口转发（如果在内网）
3. 使用公网IP或域名访问

**安全建议：** 生产环境请添加认证和HTTPS

### 7. API 返回的时间格式是什么？

ISO 8601 格式：`2024-12-15T10:30:00.123456`

可以在 Python 中解析：
```python
from datetime import datetime
dt = datetime.fromisoformat("2024-12-15T10:30:00.123456")
```

## 📚 扩展学习

- [FastAPI 官方文档](https://fastapi.tiangolo.com/zh/)
- [Pydantic 官方文档](https://docs.pydantic.dev/)
- [Uvicorn 官方文档](https://www.uvicorn.org/)

## 📝 开发建议

### 添加数据库支持

可以使用 SQLAlchemy + SQLite：

```bash
pip install sqlalchemy
```

### 添加用户认证

可以使用 JWT Token：

```bash
pip install python-jose[cryptography] passlib[bcrypt]
```

### 添加日志记录

FastAPI 内置支持 Python logging：

```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

## 📄 许可证

本项目仅供学习使用。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**最后更新：** 2024-12-15

