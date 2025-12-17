"""
测试JWT token生成和验证
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from db.auth import create_access_token, SECRET_KEY, ALGORITHM
from jose import jwt
from datetime import datetime, timedelta

# 测试1: 创建token
print("=" * 60)
print("测试1: 创建JWT token")
test_user_id = 1
token = create_access_token(data={"sub": test_user_id})
print(f"生成的token: {token[:50]}...")
print(f"Token长度: {len(token)}")

# 测试2: 解码token
print("\n" + "=" * 60)
print("测试2: 解码JWT token")
try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    print(f"解码成功!")
    print(f"Payload: {payload}")
    print(f"用户ID (sub): {payload.get('sub')}")
    print(f"用户ID类型: {type(payload.get('sub'))}")
    print(f"过期时间 (exp): {payload.get('exp')}")
    
    # 检查过期时间
    exp_timestamp = payload.get('exp')
    exp_datetime = datetime.fromtimestamp(exp_timestamp)
    now = datetime.now()
    print(f"当前时间: {now}")
    print(f"过期时间: {exp_datetime}")
    print(f"是否已过期: {now > exp_datetime}")
    
except Exception as e:
    print(f"解码失败: {e}")
    import traceback
    traceback.print_exc()

# 测试3: 测试一个真实的登录流程
print("\n" + "=" * 60)
print("测试3: 模拟登录流程")

from db.database import SessionLocal
from db.model import UserModel

db = SessionLocal()
try:
    # 查找测试用户
    user = db.query(UserModel).filter(UserModel.email == "zhangsan@example.com").first()
    if user:
        print(f"找到用户: {user.name} (ID: {user.id})")
        print(f"用户ID类型: {type(user.id)}")
        print(f"是否激活: {user.is_active}")
        
        # 生成token
        token = create_access_token(data={"sub": user.id})
        print(f"\n为用户生成token: {token[:50]}...")
        
        # 验证token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id_from_token = payload.get("sub")
        print(f"从token中解码的用户ID: {user_id_from_token}")
        print(f"类型: {type(user_id_from_token)}")
        
        # 查询数据库
        user_from_token = db.query(UserModel).filter(UserModel.id == user_id_from_token).first()
        if user_from_token:
            print(f"✅ 成功通过token查到用户: {user_from_token.name}")
        else:
            print(f"❌ 无法通过token查到用户")
    else:
        print("❌ 找不到测试用户")
except Exception as e:
    print(f"❌ 错误: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()

print("\n" + "=" * 60)
print("测试完成!")

