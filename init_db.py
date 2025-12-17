"""
数据库初始化脚本（JWT版本）
创建数据库表并插入测试数据
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db.database import engine, SessionLocal, Base
from db.model import UserModel
from db.auth import get_password_hash

def init_database():
    """初始化数据库"""
    print("=" * 60)
    print("📊 正在初始化数据库（JWT认证版本）...")
    
    # 删除旧表，创建新表（包含password_hash字段）
    print("⚠️  注意：将重建数据库表结构")
    choice = input("是否继续？这将删除现有数据！(y/n): ")
    if choice.lower() != 'y':
        print("❌ 已取消操作")
        return
    
    # 删除所有表
    Base.metadata.drop_all(bind=engine)
    print("🗑️  已删除旧表结构")
    
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    print("✅ 数据库表创建成功！")
    
    # 创建会话
    db = SessionLocal()
    
    try:
        # 插入测试数据（带密码）
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
                is_active=False  # 测试禁用用户
            ),
        ]
        
        db.add_all(test_users)
        db.commit()
        
        print(f"✅ 成功插入 {len(test_users)} 条测试数据")
        print("\n📋 测试用户列表：")
        print("-" * 60)
        for user in test_users:
            status = "✅ 激活" if user.is_active else "❌ 禁用"
            print(f"  - 姓名: {user.name:8} | 邮箱: {user.email:25} | {status}")
        
        print("\n🔑 所有测试账号的密码都是: password123")
        print("-" * 60)
        
        print("\n" + "=" * 60)
        print("🎉 数据库初始化完成！")
        print("\n💡 接下来的步骤：")
        print("   1. 启动应用: cd fastapi-user-main && python main.py")
        print("   2. 访问文档: http://127.0.0.1:8000/docs")
        print("   3. 使用测试账号登录:")
        print("      邮箱: zhangsan@example.com")
        print("      密码: password123")
        print("   4. 或运行测试: python test_api.py")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    init_database()
