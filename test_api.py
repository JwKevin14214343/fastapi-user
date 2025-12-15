"""
简单的API测试脚本
运行前请确保FastAPI应用正在运行
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def print_response(response, operation):
    """打印响应信息"""
    print(f"\n{'='*50}")
    print(f"操作: {operation}")
    print(f"状态码: {response.status_code}")
    try:
        print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
    except:
        print(f"响应: {response.text}")
    print(f"{'='*50}")

def test_user_crud():
    """测试用户CRUD操作"""
    
    # 1. 创建用户
    print("\n🔹 测试1: 创建用户")
    user_data = {
        "name": "张三",
        "email": "zhangsan@example.com",
        "age": 25
    }
    response = requests.post(f"{BASE_URL}/users/", json=user_data)
    print_response(response, "创建用户1")
    user1_id = response.json()["id"] if response.status_code == 201 else None
    
    # 创建第二个用户
    user_data2 = {
        "name": "李四",
        "email": "lisi@example.com",
        "age": 30
    }
    response = requests.post(f"{BASE_URL}/users/", json=user_data2)
    print_response(response, "创建用户2")
    
    # 创建第三个用户
    user_data3 = {
        "name": "王五",
        "email": "wangwu@example.com"
    }
    response = requests.post(f"{BASE_URL}/users/", json=user_data3)
    print_response(response, "创建用户3（不含年龄）")
    
    # 2. 测试重复邮箱
    print("\n🔹 测试2: 尝试创建重复邮箱的用户（应该失败）")
    response = requests.post(f"{BASE_URL}/users/", json=user_data)
    print_response(response, "创建重复邮箱用户")
    
    # 3. 获取所有用户
    print("\n🔹 测试3: 获取所有用户")
    response = requests.get(f"{BASE_URL}/users/")
    print_response(response, "获取所有用户")
    
    # 4. 获取单个用户
    if user1_id:
        print("\n🔹 测试4: 获取单个用户")
        response = requests.get(f"{BASE_URL}/users/{user1_id}")
        print_response(response, f"获取用户ID: {user1_id}")
    
    # 5. 更新用户
    if user1_id:
        print("\n🔹 测试5: 更新用户信息")
        update_data = {
            "name": "张三（已更新）",
            "age": 26
        }
        response = requests.put(f"{BASE_URL}/users/{user1_id}", json=update_data)
        print_response(response, f"更新用户ID: {user1_id}")
    
    # 6. 根据邮箱搜索
    print("\n🔹 测试6: 根据邮箱搜索用户")
    response = requests.get(f"{BASE_URL}/users/search/by-email", params={"email": "lisi@example.com"})
    print_response(response, "搜索邮箱: lisi@example.com")
    
    # 7. 获取不存在的用户
    print("\n🔹 测试7: 获取不存在的用户（应该返回404）")
    response = requests.get(f"{BASE_URL}/users/9999")
    print_response(response, "获取不存在的用户ID: 9999")
    
    # 8. 删除用户
    if user1_id:
        print("\n🔹 测试8: 删除用户")
        response = requests.delete(f"{BASE_URL}/users/{user1_id}")
        print_response(response, f"删除用户ID: {user1_id}")
        
        # 验证删除
        response = requests.get(f"{BASE_URL}/users/{user1_id}")
        print_response(response, f"验证删除（应该返回404）")
    
    # 9. 最终用户列表
    print("\n🔹 测试9: 最终用户列表")
    response = requests.get(f"{BASE_URL}/users/")
    print_response(response, "获取所有剩余用户")

if __name__ == "__main__":
    print("=" * 50)
    print("开始测试 FastAPI 用户管理系统")
    print("请确保应用正在运行: http://localhost:8000")
    print("=" * 50)
    
    try:
        # 测试服务器是否运行
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            print("✅ 服务器连接成功！")
            test_user_crud()
            print("\n" + "=" * 50)
            print("✅ 所有测试完成！")
            print("=" * 50)
        else:
            print("❌ 服务器响应异常")
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器")
        print("请先运行: cd fastapi-user && python main.py")
    except Exception as e:
        print(f"❌ 发生错误: {e}")

