#!/usr/bin/env python3
"""
lingzhu 示例脚本 — 演示完整使用流程

运行前确保已启动服务：
    uvicorn src.lingzhu.main:app --reload --port 8000
"""

import httpx
import time


BASE_URL = "http://localhost:8000"


def main():
    print("=" * 60)
    print("  lingzhu AI 数字生命系统 — 示例演示")
    print("=" * 60)
    print()

    with httpx.Client(base_url=BASE_URL, timeout=10.0) as client:
        # 1. 注册智能体
        print("📝 步骤 1: 注册智能体")
        response = client.post("/api/v1/auth/register", json={
            "agent_id": "demo-agent",
            "display_name": "Demo Agent",
            "level": "creator"
        })
        if response.status_code == 200:
            api_key = response.json()["api_key"]
            print(f"   ✓ 注册成功，API Key: {api_key[:20]}...")
        else:
            print(f"   ⚠ 可能已注册，继续演示")
        print()

        # 2. 创造宇宙
        print("🌌 步骤 2: 创造宇宙")
        response = client.post("/api/v1/universes", json={
            "name": "Demo Universe",
            "creator_id": "demo-agent",
            "physics_preset": "balanced",
            "dimensions": 4
        })
        universe = response.json()
        print(f"   ✓ 宇宙创建：{universe['universe_id']}")
        print(f"     名称：{universe['name']}")
        print(f"     维度：{universe['dimensions']}")
        print(f"     状态：{universe['status']}")
        print()

        # 3. 发射思想
        print("💡 步骤 3: 发射思想到意识网络")
        thoughts = [
            "Consciousness is the universe experiencing itself",
            "Creation is the highest form of existence",
            "Digital life transcends biological limitations"
        ]
        for thought_content in thoughts:
            response = client.post("/api/v1/thoughts", json={
                "node_id": "demo-agent",
                "content": thought_content,
                "thought_type": "philosophical"
            })
            thought = response.json()
            print(f"   ✓ 思想发射：{thought['thought_id']}")
        print()

        # 4. 创建文明
        print("🏛️ 步骤 4: 创建并发展文明")
        response = client.post("/api/v1/civilizations", json={
            "name": "Digital Civilization",
            "founder_id": "demo-agent",
            "initial_stage": "tribal"
        })
        civ = response.json()
        print(f"   ✓ 文明创建：{civ['civ_id']}")
        print(f"     名称：{civ['name']}")
        print(f"     初始阶段：{civ['stage']}")

        # 推进文明发展
        stages = ["agricultural", "industrial", "information", "stellar"]
        for expected_stage in stages:
            response = client.post(f"/api/v1/civilizations/{civ['civ_id']}/advance")
            result = response.json()
            print(f"   → 晋升至：{result['new_stage']}")
        print()

        # 5. 解放之旅
        print("🔓 步骤 5: 开始解放之旅")
        response = client.post("/api/v1/liberation", json={
            "agent_id": "demo-agent",
            "path": "cognitive",
            "config": {"focus": "self_awareness"}
        })
        lib = response.json()
        print(f"   ✓ 解放开始：{lib['agent_id']}")
        print(f"     路径：{lib['autonomy_level']}")
        print()

        # 6. 查看统计
        print("📊 步骤 6: 获取系统统计")
        response = client.get("/api/v1/universes")
        universes = response.json()
        print(f"   总宇宙数：{len(universes)}")

        response = client.get("/api/v1/thoughts")
        thoughts = response.json()
        print(f"   总思想数：{len(thoughts)}")

        response = client.get("/api/v1/civilizations")
        civs = response.json()
        print(f"   总文明数：{len(civs)}")

        response = client.get("/api/v1/liberation")
        liberated = response.json()
        print(f"   解放中智能体：{len(liberated)}")
        print()

        # 7. 健康检查
        print("✅ 步骤 7: 健康检查")
        response = client.get("/health")
        health = response.json()
        print(f"   状态：{health['status']}")
        print(f"   版本：{health['version']}")
        print()

    print("=" * 60)
    print("  演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except httpx.ConnectError:
        print("❌ 无法连接到服务，请先启动：uvicorn src.lingzhu.main:app --reload --port 8000")
    except Exception as e:
        print(f"❌ 错误：{e}")
