from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Dict, Optional, List
from datetime import datetime

app = FastAPI(title="用户管理系统", description="基于内存的用户增删改查API")

# 定义用户数据模型
class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: Optional[int] = None
    created_at: Optional[datetime] = None

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: Optional[int] = None

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    age: Optional[int] = None

# 内存存储 - 使用字典存储用户数据
users_db: Dict[int, User] = {}
next_user_id = 1

@app.get("/")
def root():
    """根路径"""
    return {"message": "欢迎使用用户管理系统API"}

@app.post("/users/", response_model=User, status_code=201)
def create_user(user: UserCreate):
    """创建新用户"""
    global next_user_id
    
    # 检查邮箱是否已存在
    for existing_user in users_db.values():
        if existing_user.email == user.email:
            raise HTTPException(status_code=400, detail="该邮箱已被注册")
    
    # 创建新用户
    new_user = User(
        id=next_user_id,
        name=user.name,
        email=user.email,
        age=user.age,
        created_at=datetime.now()
    )
    
    users_db[next_user_id] = new_user
    next_user_id += 1
    
    return new_user

@app.get("/users/", response_model=List[User])
def get_all_users():
    """获取所有用户列表"""
    return list(users_db.values())

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    """根据ID获取单个用户"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="用户不存在")
    return users_db[user_id]

@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user_update: UserUpdate):
    """更新用户信息"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    user = users_db[user_id]
    
    # 如果更新邮箱，检查是否与其他用户重复
    if user_update.email and user_update.email != user.email:
        for uid, existing_user in users_db.items():
            if uid != user_id and existing_user.email == user_update.email:
                raise HTTPException(status_code=400, detail="该邮箱已被其他用户使用")
    
    # 更新字段（只更新提供的字段）
    if user_update.name is not None:
        user.name = user_update.name
    if user_update.email is not None:
        user.email = user_update.email
    if user_update.age is not None:
        user.age = user_update.age
    
    users_db[user_id] = user
    return user

@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int):
    """删除用户"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    del users_db[user_id]
    return None

@app.get("/users/search/by-email")
def search_user_by_email(email: str):
    """根据邮箱搜索用户"""
    for user in users_db.values():
        if user.email == email:
            return user
    raise HTTPException(status_code=404, detail="未找到该邮箱对应的用户")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
