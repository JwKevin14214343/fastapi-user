"""
FastAPI用户管理系统 - JWT认证版本
"""
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
import sys
import os

# 添加父目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.database import engine, get_db, Base
from db.model import UserModel
from db.auth import (
    get_password_hash,
    authenticate_user,
    create_access_token,
    get_current_user,
    get_current_active_user
)
from schemas import (
    UserRegister,
    UserLogin,
    UserUpdate,
    UserResponse,
    Token,
    MessageResponse,
    UserStats
)

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="用户管理系统（JWT认证版）",
    description="基于SQLite数据库和JWT认证的用户管理API",
    version="2.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源（开发环境）
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有HTTP方法
    allow_headers=["*"],  # 允许所有请求头
)


@app.get("/", response_model=MessageResponse)
def root():
    """根路径"""
    return {
        "message": "欢迎使用用户管理系统API（JWT认证版本）",
        "detail": "请访问 /docs 查看API文档"
    }


# ============ 认证相关接口 ============

@app.post("/auth/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED, tags=["认证"])
def register(user: UserRegister, db: Session = Depends(get_db)):
    """
    用户注册
    
    - **name**: 用户姓名
    - **email**: 用户邮箱（唯一）
    - **password**: 密码（6-50个字符）
    - **age**: 用户年龄（可选）
    """
    # 检查邮箱是否已存在
    existing_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该邮箱已被注册"
        )
    
    # 创建新用户
    db_user = UserModel(
        name=user.name,
        email=user.email,
        password_hash=get_password_hash(user.password),
        age=user.age,
        is_active=True
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user


@app.post("/auth/login", response_model=Token, tags=["认证"])
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """
    用户登录
    
    - **email**: 用户邮箱
    - **password**: 密码
    
    返回JWT访问令牌
    """
    # 验证用户凭证
    user = authenticate_user(db, user_credentials.email, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="邮箱或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="账号已被禁用"
        )
    
    # 创建访问令牌
    access_token = create_access_token(data={"sub": str(user.id)})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


@app.post("/auth/login/form", response_model=Token, tags=["认证"])
def login_form(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    用户登录（OAuth2表单格式）
    
    用于Swagger UI的"Authorize"功能
    - **username**: 用户邮箱
    - **password**: 密码
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="邮箱或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="账号已被禁用"
        )
    
    access_token = create_access_token(data={"sub": str(user.id)})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


# ============ 用户信息接口 ============

@app.get("/users/me", response_model=UserResponse, tags=["用户"])
async def get_current_user_info(current_user: UserModel = Depends(get_current_active_user)):
    """
    获取当前登录用户信息
    
    需要JWT认证
    """
    return current_user


@app.put("/users/me", response_model=UserResponse, tags=["用户"])
async def update_current_user(
    user_update: UserUpdate,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    更新当前用户信息
    
    需要JWT认证
    - 可以更新姓名、邮箱、年龄、密码
    - 如果更新邮箱，会检查是否与其他用户重复
    """
    # 如果更新邮箱，检查是否与其他用户重复
    if user_update.email and user_update.email != current_user.email:
        existing_user = db.query(UserModel).filter(
            UserModel.email == user_update.email,
            UserModel.id != current_user.id
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="该邮箱已被其他用户使用"
            )
    
    # 更新字段
    if user_update.name is not None:
        current_user.name = user_update.name
    if user_update.email is not None:
        current_user.email = user_update.email
    if user_update.age is not None:
        current_user.age = user_update.age
    if user_update.password is not None:
        current_user.password_hash = get_password_hash(user_update.password)
    
    db.commit()
    db.refresh(current_user)
    
    return current_user


@app.delete("/users/me", status_code=status.HTTP_204_NO_CONTENT, tags=["用户"])
async def delete_current_user(
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    删除当前用户账号
    
    需要JWT认证
    """
    db.delete(current_user)
    db.commit()
    return None


# ============ 管理接口（仅用于演示，生产环境应添加管理员权限） ============

@app.get("/users", response_model=List[UserResponse], tags=["管理"])
async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    获取所有用户列表（需要认证）
    
    - **skip**: 跳过前N条记录
    - **limit**: 最多返回N条记录
    
    ⚠️ 生产环境应添加管理员权限检查
    """
    users = db.query(UserModel).offset(skip).limit(limit).all()
    return users


@app.get("/users/search/by-email", response_model=UserResponse, tags=["管理"])
async def search_user_by_email(
    email: str,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    根据邮箱搜索用户（需要认证）
    
    ⚠️ 生产环境应添加管理员权限检查
    """
    user = db.query(UserModel).filter(UserModel.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="未找到该邮箱对应的用户"
        )
    return user


@app.get("/stats", response_model=UserStats, tags=["统计"])
async def get_user_stats(
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    获取用户统计信息（需要认证）
    
    返回总用户数、活跃用户数、非活跃用户数
    """
    total_users = db.query(UserModel).count()
    active_users = db.query(UserModel).filter(UserModel.is_active == True).count()
    inactive_users = total_users - active_users
    
    return {
        "total_users": total_users,
        "active_users": active_users,
        "inactive_users": inactive_users
    }


if __name__ == "__main__":
    import uvicorn
    print("=" * 60)
    print("🚀 用户管理系统启动中（JWT认证版本）...")
    print("📊 数据库类型: SQLite")
    print("📁 数据库文件: users.db")
    print("🔐 认证方式: JWT Bearer Token")
    print("🌐 API文档: http://127.0.0.1:8000/docs")
    print("🔓 CORS策略: 已启用（允许所有来源）")
    print("💡 使用说明:")
    print("   1. 先注册账号: POST /auth/register")
    print("   2. 登录获取token: POST /auth/login")
    print("   3. 在Swagger UI点击'Authorize'按钮输入token")
    print("   4. 或在请求头添加: Authorization: Bearer <token>")
    print("=" * 60)
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
