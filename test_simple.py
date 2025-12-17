# -*- coding: utf-8 -*-
"""
API测试脚本 - 简化版（无emoji）
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"
access_token = None
test_user_email = "testuser@example.com"
test_user_password = "test123456"


def print_response(response, operation):
    """打印响应信息"""
    print(f"\n{'='*60}")
    print(f"操作: {operation}")
    print(f"状态码: {response.status_code}")
    try:
        data = response.json()
        print(f"响应: {json.dumps(data, ensure_ascii=False, indent=2)}")
    except:
        print(f"响应: {response.text}")
    print(f"{'='*60}")


def get_auth_headers():
    """获取认证请求头"""
    if access_token:
        return {"Authorization": f"Bearer {access_token}"}
    return {}


def test_jwt_authentication():
    """测试JWT认证流程"""
    global access_token
    
    print("\n开始测试JWT认证系统")
    print("="*60)
    
    # 测试1: 注册用户
    print("\n>>> 测试1: 用户注册")
    register_data = {
        "name": "测试用户",
        "email": test_user_email,
        "password": test_user_password,
        "age": 25
    }
    response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    print_response(response, "注册用户")
    
    if response.status_code == 400:
        print("用户已存在，继续测试...")
    
    # 测试2: 登录获取Token
    print("\n>>> 测试2: 用户登录")
    login_data = {
        "email": test_user_email,
        "password": test_user_password
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print_response(response, "用户登录")
    
    if response.status_code == 200:
        data = response.json()
        access_token = data["access_token"]
        print(f"\n登录成功！")
        print(f"Token: {access_token[:50]}...")
        print(f"用户信息: {data['user']['name']} ({data['user']['email']})")
    else:
        print("登录失败，无法继续测试")
        return False
    
    # 测试3: 获取当前用户信息
    print("\n>>> 测试3: 获取当前用户信息")
    response = requests.get(f"{BASE_URL}/users/me", headers=get_auth_headers())
    print_response(response, "获取当前用户信息")
    
    # 测试4: 测试未认证访问
    print("\n>>> 测试4: 未认证访问（应该失败）")
    response = requests.get(f"{BASE_URL}/users/me")
    print_response(response, "未认证访问")
    
    # 测试5: 更新当前用户信息
    print("\n>>> 测试5: 更新当前用户信息")
    update_data = {"name": "测试用户(已更新)", "age": 26}
    response = requests.put(f"{BASE_URL}/users/me", json=update_data, headers=get_auth_headers())
    print_response(response, "更新用户信息")
    
    # 测试6: 获取所有用户
    print("\n>>> 测试6: 获取所有用户列表（需要认证）")
    response = requests.get(f"{BASE_URL}/users", headers=get_auth_headers())
    print_response(response, "获取所有用户")
    
    # 测试7: 获取统计信息
    print("\n>>> 测试7: 获取用户统计")
    response = requests.get(f"{BASE_URL}/stats", headers=get_auth_headers())
    print_response(response, "获取统计信息")
    
    # 测试8: 测试错误密码
    print("\n>>> 测试8: 错误的密码（应该失败）")
    wrong_login = {"email": test_user_email, "password": "wrongpassword"}
    response = requests.post(f"{BASE_URL}/auth/login", json=wrong_login)
    print_response(response, "错误密码登录")
    
    # 测试9: 使用测试账号登录
    print("\n>>> 测试9: 使用数据库测试账号登录")
    test_login = {"email": "zhangsan@example.com", "password": "password123"}
    response = requests.post(f"{BASE_URL}/auth/login", json=test_login)
    print_response(response, "测试账号登录")
    
    return True


def main():
    print("="*60)
    print("FastAPI 用户管理系统 - JWT认证测试")
    print("请确保应用正在运行: http://localhost:8000")
    print("="*60)
    
    # 等待应用启动
    print("\n等待服务器响应...")
    max_retries = 10
    for i in range(max_retries):
        try:
            response = requests.get(BASE_URL, timeout=2)
            if response.status_code == 200:
                print("服务器连接成功！")
                print(f"服务器信息: {response.json()}")
                
                # 运行测试
                if test_jwt_authentication():
                    print("\n"+"="*60)
                    print("所有测试完成！")
                    print("="*60)
                    print("\n提示:")
                    print("1. 访问 http://localhost:8000/docs")
                    print("2. 点击右上角的 'Authorize' 按钮")
                    print("3. 输入邮箱和密码登录")
                    print("4. 即可在Swagger UI中测试所有接口")
                    print("="*60)
                return
        except Exception as e:
            print(f"尝试连接 {i+1}/{max_retries}...")
            time.sleep(2)
    
    print("\n无法连接到服务器")
    print("请确认应用正在运行")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n测试已中断")
    except Exception as e:
        print(f"\n发生错误: {e}")
        import traceback
        traceback.print_exc()

