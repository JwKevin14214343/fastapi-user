"""
API测试脚本（JWT认证版本）
测试完整的JWT认证流程
"""

import requests
import json

BASE_URL = "http://localhost:8000"

# 全局变量存储token
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
    
    print("\n" + "🔐 " * 20)
    print("开始测试JWT认证系统")
    print("🔐 " * 20)
    
    # ============ 测试1: 注册用户 ============
    print("\n\n📝 测试1: 用户注册")
    register_data = {
        "name": "测试用户",
        "email": test_user_email,
        "password": test_user_password,
        "age": 25
    }
    response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    print_response(response, "注册用户")
    
    if response.status_code == 400:
        print("ℹ️  用户已存在，继续测试...")
    
    # ============ 测试2: 登录获取Token ============
    print("\n\n🔑 测试2: 用户登录")
    login_data = {
        "email": test_user_email,
        "password": test_user_password
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print_response(response, "用户登录")
    
    if response.status_code == 200:
        data = response.json()
        access_token = data["access_token"]
        print(f"\n✅ 登录成功！获取到Token:")
        print(f"Token: {access_token[:50]}...")
        print(f"用户信息: {data['user']['name']} ({data['user']['email']})")
    else:
        print("❌ 登录失败，无法继续测试")
        return
    
    # ============ 测试3: 获取当前用户信息 ============
    print("\n\n👤 测试3: 获取当前用户信息")
    response = requests.get(
        f"{BASE_URL}/users/me",
        headers=get_auth_headers()
    )
    print_response(response, "获取当前用户信息")
    
    # ============ 测试4: 测试未认证访问 ============
    print("\n\n🚫 测试4: 未认证访问（应该失败）")
    response = requests.get(f"{BASE_URL}/users/me")
    print_response(response, "未认证访问")
    
    # ============ 测试5: 更新当前用户信息 ============
    print("\n\n✏️ 测试5: 更新当前用户信息")
    update_data = {
        "name": "测试用户（已更新）",
        "age": 26
    }
    response = requests.put(
        f"{BASE_URL}/users/me",
        json=update_data,
        headers=get_auth_headers()
    )
    print_response(response, "更新当前用户信息")
    
    # ============ 测试6: 注册第二个用户 ============
    print("\n\n📝 测试6: 注册第二个用户")
    register_data2 = {
        "name": "测试用户2",
        "email": "testuser2@example.com",
        "password": "test654321",
        "age": 30
    }
    response = requests.post(f"{BASE_URL}/auth/register", json=register_data2)
    print_response(response, "注册第二个用户")
    
    # ============ 测试7: 获取所有用户列表 ============
    print("\n\n📋 测试7: 获取所有用户列表（需要认证）")
    response = requests.get(
        f"{BASE_URL}/users",
        headers=get_auth_headers()
    )
    print_response(response, "获取所有用户列表")
    
    # ============ 测试8: 分页查询 ============
    print("\n\n📄 测试8: 分页查询（前2条）")
    response = requests.get(
        f"{BASE_URL}/users?skip=0&limit=2",
        headers=get_auth_headers()
    )
    print_response(response, "分页查询")
    
    # ============ 测试9: 根据邮箱搜索用户 ============
    print("\n\n🔍 测试9: 根据邮箱搜索用户")
    response = requests.get(
        f"{BASE_URL}/users/search/by-email?email=testuser2@example.com",
        headers=get_auth_headers()
    )
    print_response(response, "根据邮箱搜索")
    
    # ============ 测试10: 获取统计信息 ============
    print("\n\n📊 测试10: 获取用户统计")
    response = requests.get(
        f"{BASE_URL}/stats",
        headers=get_auth_headers()
    )
    print_response(response, "获取用户统计")
    
    # ============ 测试11: 修改密码 ============
    print("\n\n🔒 测试11: 修改密码")
    update_password = {
        "password": "newpassword123"
    }
    response = requests.put(
        f"{BASE_URL}/users/me",
        json=update_password,
        headers=get_auth_headers()
    )
    print_response(response, "修改密码")
    
    # ============ 测试12: 用新密码登录 ============
    print("\n\n🔑 测试12: 使用新密码登录")
    login_data_new = {
        "email": test_user_email,
        "password": "newpassword123"
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data_new)
    print_response(response, "使用新密码登录")
    
    if response.status_code == 200:
        print("✅ 新密码有效")
    
    # ============ 测试13: 尝试重复注册 ============
    print("\n\n❌ 测试13: 尝试重复注册（应该失败）")
    response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    print_response(response, "重复注册")
    
    # ============ 测试14: 错误的密码登录 ============
    print("\n\n❌ 测试14: 错误的密码（应该失败）")
    wrong_login = {
        "email": test_user_email,
        "password": "wrongpassword"
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=wrong_login)
    print_response(response, "错误密码登录")
    
    # ============ 测试15: 使用无效Token ============
    print("\n\n❌ 测试15: 使用无效Token（应该失败）")
    invalid_headers = {"Authorization": "Bearer invalid_token_here"}
    response = requests.get(f"{BASE_URL}/users/me", headers=invalid_headers)
    print_response(response, "无效Token访问")
    
    # ============ 测试16: 删除当前用户 ============
    print("\n\n🗑️  测试16: 删除当前用户账号")
    choice = input("\n⚠️  是否删除测试用户？(y/n): ")
    if choice.lower() == 'y':
        response = requests.delete(
            f"{BASE_URL}/users/me",
            headers=get_auth_headers()
        )
        print_response(response, "删除当前用户")
        
        # 验证删除
        print("\n验证删除...")
        response = requests.get(
            f"{BASE_URL}/users/me",
            headers=get_auth_headers()
        )
        print_response(response, "删除后尝试访问（应该返回401）")
    else:
        print("⏭️  跳过删除测试")


def test_swagger_oauth2_flow():
    """测试Swagger UI的OAuth2流程"""
    print("\n\n📘 测试Swagger OAuth2登录流程")
    form_data = {
        "username": test_user_email,
        "password": test_user_password
    }
    response = requests.post(
        f"{BASE_URL}/auth/login/form",
        data=form_data
    )
    print_response(response, "OAuth2表单登录")


if __name__ == "__main__":
    print("=" * 60)
    print("🧪 FastAPI 用户管理系统 - JWT认证测试")
    print("请确保应用正在运行: http://localhost:8000")
    print("=" * 60)
    
    try:
        # 测试服务器是否运行
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            print("✅ 服务器连接成功！")
            print(f"📝 服务器信息: {response.json()}")
            
            # 运行JWT认证测试
            test_jwt_authentication()
            
            # 测试OAuth2流程
            test_swagger_oauth2_flow()
            
            print("\n\n" + "=" * 60)
            print("✅ 所有测试完成！")
            print("=" * 60)
            print("\n💡 提示:")
            print("1. 访问 http://localhost:8000/docs")
            print("2. 点击右上角的 'Authorize' 按钮")
            print("3. 输入邮箱和密码登录")
            print("4. 即可在Swagger UI中测试所有需要认证的接口")
            print("=" * 60)
        else:
            print("❌ 服务器响应异常")
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器")
        print("请先运行: cd fastapi-user-main && python main.py")
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
