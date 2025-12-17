# -*- coding: utf-8 -*-
"""
本地数据库初始化脚本（在fastapi-user-main目录运行）
"""
import sys
import os

# 添加父目录到路径以导入db模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.database import engine, SessionLocal, Base
from db.model import UserModel
from db.auth import get_password_hash

def init_database():
    """初始化数据库"""
    print("=" * 60)
    print("正在初始化数据库(在应用目录)...")
    
    # 删除所有表
    Base.metadata.drop_all(bind=engine)
    print("已删除旧表结构")
    
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    print("数据库表创建成功!")
    
    # 创建会话
    db = SessionLocal()
    
    try:
        # 插入测试数据
        test_users = [
            UserModel(
                name="张三",
                email="zhangsan@example.com",
                password_hash=get_password_hash("password123"),
                age=25,
                is_active=True
            ),
            UserModel(
                name="李四",
                email="lisi@example.com",
                password_hash=get_password_hash("password123"),
                age=30,
                is_active=True
            ),
            UserModel(
                name="王五",
                email="wangwu@example.com",
                password_hash=get_password_hash("password123"),
                age=28,
                is_active=True
            ),
            UserModel(
                name="赵六",
                email="zhaoliu@example.com",
                password_hash=get_password_hash("password123"),
                age=35,
                is_active=False
            ),
        ]
        
        db.add_all(test_users)
        db.commit()
        
        print(f"成功插入 {len(test_users)} 条测试数据")
        print("\n测试用户列表:")
        print("-" * 60)
        for user in test_users:
            status = "激活" if user.is_active else "禁用"
            print(f"  - {user.name} | {user.email:30} | {status}")
        
        print("\n密码: password123")
        print("-" * 60)
        print("\n数据库初始化完成!")
        print(f"数据库位置: {os.path.abspath('users.db')}")
        
    except Exception as e:
        print(f"初始化失败: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    init_database()


