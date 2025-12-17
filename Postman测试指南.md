# Postman 测试指南 - JWT认证系统

## 📋 准备工作

### 1. 确认应用正在运行
- 应用地址：`http://127.0.0.1:8000` 或 `http://localhost:8000`
- 检查方法：浏览器访问 http://localhost:8000 应该看到欢迎信息

### 2. 常见失败原因

| 错误 | 原因 | 解决方法 |
|------|------|----------|
| 无法连接 | 应用未启动 | 启动应用：`python main.py` |
| 422 错误 | 请求格式错误 | 检查JSON格式和字段 |
| 400 错误 | 邮箱已存在 | 换一个新邮箱 |
| 401 错误 | Token无效或过期 | 重新登录获取Token |

---

## 🎯 步骤1：用户注册

### 请求配置

```
方法：POST
URL：http://localhost:8000/auth/register
```

### Headers设置

```
Content-Type: application/json
```

### Body设置（选择 raw + JSON）

```json
{
  "name": "测试用户",
  "email": "test123@example.com",
  "password": "password123",
  "age": 25
}
```

### 字段要求

| 字段 | 类型 | 是否必填 | 要求 |
|------|------|----------|------|
| name | string | ✅ 必填 | 1-100个字符 |
| email | string | ✅ 必填 | 有效的邮箱格式 |
| password | string | ✅ 必填 | 6-50个字符 |
| age | integer | ❌ 可选 | 0-150之间的整数 |

### 成功响应（201 Created）

```json
{
  "id": 5,
  "name": "测试用户",
  "email": "test123@example.com",
  "age": 25,
  "is_active": true,
  "created_at": "2024-12-16T13:00:00",
  "updated_at": "2024-12-16T13:00:00"
}
```

### 失败响应示例

#### 邮箱已存在（400）
```json
{
  "detail": "该邮箱已被注册"
}
```

#### 字段验证失败（422）
```json
{
  "detail": [
    {
      "loc": ["body", "password"],
      "msg": "String should have at least 6 characters",
      "type": "string_too_short"
    }
  ]
}
```

---

## 🔑 步骤2：用户登录

### 请求配置

```
方法：POST
URL：http://localhost:8000/auth/login
```

### Headers设置

```
Content-Type: application/json
```

### Body设置（选择 raw + JSON）

```json
{
  "email": "test123@example.com",
  "password": "password123"
}
```

### 成功响应（200 OK）

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjUsImV4cCI6MTcwMzA2NDAwMH0.abc123...",
  "token_type": "bearer",
  "user": {
    "id": 5,
    "name": "测试用户",
    "email": "test123@example.com",
    "age": 25,
    "is_active": true,
    "created_at": "2024-12-16T13:00:00",
    "updated_at": "2024-12-16T13:00:00"
  }
}
```

⚠️ **重要**：复制 `access_token` 的值，后续所有需要认证的接口都要用到！

### 失败响应

#### 密码错误（401）
```json
{
  "detail": "邮箱或密码错误"
}
```

---

## 🔒 步骤3：使用Token访问需要认证的接口

### 3.1 获取当前用户信息

#### 请求配置

```
方法：GET
URL：http://localhost:8000/users/me
```

#### Headers设置（关键！）

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

⚠️ **注意**：
使用Postman的Authorization功能**
1. 切换到 `Authorization` 标签
2. Type选择：`Bearer Token`
3. Token输入框粘贴你的token（不需要写Bearer）

#### 成功响应（200 OK）

```json
{
  "id": 5,
  "name": "测试用户",
  "email": "test123@example.com",
  "age": 25,
  "is_active": true,
  "created_at": "2024-12-16T13:00:00",
  "updated_at": "2024-12-16T13:00:00"
}
```

#### 失败响应（401）

```json
{
  "detail": "无法验证凭证"
}
```

---

## 📝 步骤4：更新当前用户信息

### 请求配置

```
方法：PUT
URL：http://localhost:8000/users/me
```

### Headers设置

```
Content-Type: application/json
Authorization: Bearer <你的token>
```

### Body设置（选择 raw + JSON）

所有字段都是可选的，只传你要更新的字段：

```json
{
  "name": "测试用户（已更新）",
  "age": 26
}
```

或者更新密码：

```json
{
  "password": "newpassword123"
}
```

### 成功响应（200 OK）

```json
{
  "id": 5,
  "name": "测试用户（已更新）",
  "email": "test123@example.com",
  "age": 26,
  "is_active": true,
  "created_at": "2024-12-16T13:00:00",
  "updated_at": "2024-12-16T13:05:00"
}
```

---

## 📊 其他接口测试

### 获取所有用户列表

```
方法：GET
URL：http://localhost:8000/users
Headers：Authorization: Bearer <token>
```

### 分页查询

```
方法：GET
URL：http://localhost:8000/users?skip=0&limit=10
Headers：Authorization: Bearer <token>
```

### 根据邮箱搜索用户

```
方法：GET
URL：http://localhost:8000/users/search/by-email?email=test123@example.com
Headers：Authorization: Bearer <token>
```

### 获取统计信息

```
方法：GET
URL：http://localhost:8000/stats
Headers：Authorization: Bearer <token>
```

### 删除当前用户

```
方法：DELETE
URL：http://localhost:8000/users/me
Headers：Authorization: Bearer <token>
```

成功返回：204 No Content（无响应体）

---

## 🔧 Postman调试技巧

### 1. 使用环境变量

在Postman中设置环境变量可以避免重复复制token：

1. 点击右上角的齿轮图标 ⚙️
2. 新建环境，命名为 "FastAPI Dev"
3. 添加变量：
   - `base_url`: `http://localhost:8000`
   - `token`: （留空，稍后自动填充）

4. 在登录请求的 **Tests** 标签添加脚本：
```javascript
if (pm.response.code === 200) {
    var jsonData = pm.response.json();
    pm.environment.set("token", jsonData.access_token);
    console.log("Token已保存");
}
```

5. 其他请求的URL改为：`{{base_url}}/users/me`
6. Authorization的Token改为：`{{token}}`

### 2. 查看详细错误信息

如果请求失败：
1. 查看 `Body` 标签的响应内容
2. 查看 `Headers` 标签确认请求头正确
3. 查看 `Console`（View → Show Postman Console）查看详细请求信息

### 3. 保存请求到Collection

建议创建一个Collection保存所有请求：
1. 点击左侧 `Collections`
2. 新建Collection："FastAPI User Management"
3. 将所有请求保存到这个Collection

---

## ❌ 常见错误排查

### 错误1：无法连接到localhost

**症状：**
```
Could not get any response
```

**原因：**应用没有启动

**解决：**
```bash
cd D:\aproduct\fastapi-user\fastapi-user-main
python main.py
```

### 错误2：422 Unprocessable Entity

**症状：**
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

**原因：**字段格式不正确

**解决：**
- 检查邮箱格式是否正确
- 检查密码是否至少6个字符
- 检查age是否是数字（如果提供）

### 错误3：401 Unauthorized

**症状：**
```json
{
  "detail": "无法验证凭证"
}
```

**原因：**
- Token没有添加或格式错误
- Token已过期（24小时）

**解决：**
1. 确认Headers中有 `Authorization: Bearer <token>`
2. 确认 `Bearer` 和 token 之间有空格
3. 如果token过期，重新登录获取新token

### 错误4：400 Bad Request - 邮箱已注册

**症状：**
```json
{
  "detail": "该邮箱已被注册"
}
```

**解决：**换一个新的邮箱地址

---

## 📋 完整测试流程示例

```
1. 注册
   POST /auth/register
   Body: {"name":"张三","email":"zhang@test.com","password":"pass123"}
   
2. 登录
   POST /auth/login
   Body: {"email":"zhang@test.com","password":"pass123"}
   复制返回的 access_token
   
3. 获取个人信息
   GET /users/me
   Headers: Authorization: Bearer <token>
   
4. 更新个人信息
   PUT /users/me
   Headers: Authorization: Bearer <token>
   Body: {"name":"张三（已更新）"}
   
5. 查看所有用户
   GET /users
   Headers: Authorization: Bearer <token>
   
6. 获取统计
   GET /stats
   Headers: Authorization: Bearer <token>
```

---

## 💡 测试建议

1. **先测试数据库中的账号**：
   - 邮箱：`zhangsan@example.com`
   - 密码：`password123`
   - 这样可以跳过注册步骤直接测试登录

2. **使用不同的邮箱**：
   - 每次注册用不同的邮箱
   - 或者删除数据库文件重新初始化

3. **保存Token**：
   - Token有效期24小时
   - 建议使用Postman环境变量自动保存

4. **对比Swagger UI**：
   - 访问 http://localhost:8000/docs
   - 对比Postman和Swagger的请求格式

---

**需要帮助？**
- 查看详细文档：`JWT认证使用指南.md`
- 查看API文档：http://localhost:8000/docs
- 运行测试脚本：`python test_simple.py`

