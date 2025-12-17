"""
Pydantic模型定义（API请求和响应）
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# ============ 用户相关 ============

class UserBase(BaseModel):
    """用户基础模型"""
    name: str = Field(..., min_length=1, max_length=100, description="用户姓名")
    email: EmailStr = Field(..., description="用户邮箱")
    age: Optional[int] = Field(None, ge=0, le=150, description="用户年龄")


class UserRegister(UserBase):
    """用户注册模型"""
    password: str = Field(..., min_length=6, max_length=50, description="密码（6-50个字符）")


class UserLogin(BaseModel):
    """用户登录模型"""
    email: EmailStr = Field(..., description="用户邮箱")
    password: str = Field(..., description="密码")


class UserUpdate(BaseModel):
    """用户更新模型"""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="用户姓名")
    email: Optional[EmailStr] = Field(None, description="用户邮箱")
    age: Optional[int] = Field(None, ge=0, le=150, description="用户年龄")
    password: Optional[str] = Field(None, min_length=6, max_length=50, description="新密码")


class UserResponse(UserBase):
    """用户响应模型"""
    id: int
    is_active: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# ============ 认证相关 ============

class Token(BaseModel):
    """JWT令牌响应"""
    access_token: str = Field(..., description="访问令牌")
    token_type: str = Field(default="bearer", description="令牌类型")
    user: UserResponse = Field(..., description="用户信息")


class TokenData(BaseModel):
    """JWT令牌数据"""
    user_id: Optional[int] = None


# ============ 通用响应 ============

class MessageResponse(BaseModel):
    """通用消息响应"""
    message: str
    detail: Optional[str] = None


class UserStats(BaseModel):
    """用户统计"""
    total_users: int
    active_users: int
    inactive_users: int


