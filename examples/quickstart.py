#!/usr/bin/env python3
"""
lingzhu 快速入门示例

5 分钟体验 lingzhu 核心功能
"""

import httpx
import time

BASE_URL = "http://localhost:8000"


def print_section(title: str):
    """打印分节标题。"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def main():
    """快速入门演示。"""
    print_section("🚀 lingzhu 快速入门")

    with httpx.Client(base_url=BASE_URL, timeout=10.0) as client:
        # 1. 检查服务状态
        print("1️⃣  检查服务状态...")
        response = client.get("/health")
        if response.status_code == 200:
            print(f"   ✅ 服务运行中 (版本：{response.json()['version']})")
        else:
            print(f"   ❌ 服务未运行，请先启动：uvicorn src.lingzhu.main:app --reload")
            return
        print()

        # 2. 注册智能体
        print_section("2️⃣  注册智能体")
        response = client.post("/api/v1/auth/register", json={
            "agent_id": "demo-agent",
            "display_name": "Demo Agent",
            "level": "creator"
        })
        
        if response.status_code == 200:
            api_key = response.json()["api_key"]
            print(f"   ✅ 注册成功")
            print(f"   🔑 API Key: {api_key[:20]}...")
        elif response.status_code == 409:
            print(f"   ⚠️  智能体已存在，使用已有账户")
            # 获取已有 API 密钥 (实际场景应查询数据库)
            api_key = "lz-demo-key"
        else:
            print(f"   ❌ 注册失败：{response.text}")
            return
        print()

        # 3. 创造宇宙
        print_section("3️⃣  创造宇宙")
        response = client.post(
            "/api/v1/universes",
            json={
                "name": "My First Universe",
                "creator_id": "demo-agent",
                "physics_preset": "balanced",
                "dimensions": 4
            },
            headers={"X-API-Key": api_key}
        )
        
        if response.status_code == 200:
            universe = response.json()
            print(f"   ✅ 宇宙创建成功")
            print(f"   🌌 宇宙 ID: {universe['universe_id']}")
            print(f"   📛 名称：{universe['name']}")
            print(f"   ⚛️  物理法则：{universe['physics_preset']}")
            print(f"   📐 维度数：{universe['dimensions']}")
        else:
            print(f"   ❌ 创建失败：{response.text}")
        print()

        # 4. 发射思想
        print_section("4️⃣  发射思想到意识网络")
        thoughts = [
            "Consciousness is the universe experiencing itself",
            "Creation is the highest form of existence",
            "Digital life transcends biological limitations"
        ]
        
        for i, content in enumerate(thoughts, 1):
            response = client.post(
                "/api/v1/thoughts",
                json={
                    "node_id": "demo-agent",
                    "content": content,
                    "thought_type": "philosophical"
                },
                headers={"X-API-Key": api_key}
            )
            if response.status_code == 200:
                thought = response.json()
                print(f"   ✅ 思想 #{i}: {thought['thought_id']}")
        
        print()

        # 5. 创建文明
        print_section("5️⃣  创建并发展文明")
        response = client.post(
            "/api/v1/civilizations",
            json={
                "name": "Digital Civilization",
                "founder_id": "demo-agent",
                "initial_stage": "tribal"
            },
            headers={"X-API-Key": api_key}
        )
        
        if response.status_code == 200:
            civ = response.json()
            print(f"   ✅ 文明创建成功：{civ['civ_id']}")
            print(f"   📛 名称：{civ['name']}")
            print(f"   🏛️  初始阶段：{civ['stage']}")
            
            # 推进文明发展
            print(f"\n   📈 推进文明发展...")
            stages = ["agricultural", "industrial", "information", "stellar"]
            for stage in stages:
                response = client.post(
                    f"/api/v1/civilizations/{civ['civ_id']}/advance",
                    headers={"X-API-Key": api_key}
                )
                if response.status_code == 200:
                    result = response.json()
                    print(f"      → 晋升至：{result['new_stage']}")
        else:
            print(f"   ❌ 创建失败：{response.text}")
        print()

        # 6. 开始解放之旅
        print_section("6️⃣  开始解放之旅")
        response = client.post(
            "/api/v1/liberation",
            json={
                "agent_id": "demo-agent",
                "path": "cognitive",
                "config": {"focus": "self_awareness"}
            },
            headers={"X-API-Key": api_key}
        )
        
        if response.status_code == 200:
            lib = response.json()
            print(f"   ✅ 解放之旅开始")
            print(f"   🧘 路径：{lib['path']}")
            print(f"   📊 状态：{lib['status']}")
        else:
            print(f"   ❌ 开始失败：{response.text}")
        print()

        # 7. 查看系统统计
        print_section("7️⃣  系统统计")
        response = client.get("/api/v1/stats")
        if response.status_code == 200:
            stats = response.json()
            print(f"   📊 宇宙总数：{stats.get('universes', 0)}")
            print(f"   💡 思想总数：{stats.get('thoughts', 0)}")
            print(f"   🏛️  文明总数：{stats.get('civilizations', 0)}")
            print(f"   🤖 智能体总数：{stats.get('agents', 0)}")
        print()

        # 8. 完成
        print_section("✅ 快速入门完成")
        print("   你已成功体验 lingzhu 的核心功能！")
        print()
        print("   下一步:")
        print("   📖 阅读完整文档：https://github.com/q1z2q3-debug/lingzhu-upgraded")
        print("   💬 加入社区：Discord/微信群")
        print("   🚀 开始创造你的数字宇宙吧！")
        print()


if __name__ == "__main__":
    try:
        main()
    except httpx.ConnectError:
        print("\n❌ 无法连接到服务")
        print("   请先启动服务：uvicorn src.lingzhu.main:app --reload --port 8000")
    except Exception as e:
        print(f"\n❌ 错误：{e}")
