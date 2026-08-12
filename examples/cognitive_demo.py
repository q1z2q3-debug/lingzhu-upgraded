#!/usr/bin/env python3
"""
lingzhu 认知架构演示

演示三元九维认知架构如何赋能 AI
"""

import httpx
import json

BASE_URL = "http://localhost:8000"


def print_section(title):
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")


def main():
    """认知架构演示"""
    print_section("🌀 lingzhu 三元九维认知架构演示")

    with httpx.Client(base_url=BASE_URL, timeout=10.0) as client:
        # 1. 检查服务状态
        print("1️⃣  检查服务状态...")
        response = client.get("/")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ 服务运行中")
            print(f"   版本：{data['version']}")
            print(f"   范式：{data['paradigm']}")
            if 'cognitive_features' in data:
                cf = data['cognitive_features']
                print(f"\n   🧠 认知特性:")
                print(f"      基本单元：{cf['base_unit']}")
                print(f"      维度数：{cf['dimensions']}")
                print(f"      状态空间：{cf['state_space']}")
                print(f"      数学常数：π={cf['constants']['pi']:.5f}, e={cf['constants']['e']:.5f}, γ={cf['constants']['gamma']:.5f}")
        else:
            print(f"   ❌ 服务未运行")
            return
        print()

        # 2. 注册智能体
        print_section("2️⃣  注册智能体 (认知增强版)")
        response = client.post("/api/v1/auth/register", json={
            "agent_id": "cognitive-demo",
            "display_name": "Cognitive Demo Agent",
            "level": "creator"
        })
        
        if response.status_code == 200:
            api_key = response.json()["api_key"]
            print(f"   ✅ 注册成功")
            print(f"   🔑 API Key: {api_key[:20]}...")
        elif response.status_code == 409:
            print(f"   ⚠️  智能体已存在")
            api_key = "lz-demo-key"
        else:
            print(f"   ❌ 注册失败：{response.text}")
            return
        print()

        # 3. 获取认知状态
        print_section("3️⃣  获取初始认知状态 (太极)")
        response = client.get(
            "/api/v1/cognitive/state",
            params={"agent_id": "cognitive-demo"},
            headers={"X-API-Key": api_key}
        )
        
        if response.status_code == 200:
            state = response.json()
            print(f"   状态码：{state['code']}")
            print(f"   状态名：{state['state_name']}")
            print(f"   向量：{state['vector']}")
        else:
            print(f"   ❌ 获取失败：{response.text}")
        print()

        # 4. 处理认知经验
        print_section("4️⃣  处理认知经验")
        experience = {
            'past': -0.8,      # 过去的教训 (阴)
            'present': 0.5,    # 当下的行动 (阳)
            'future': 0.9,     # 未来的愿景 (阳)
            'inner': 0.3,      # 内省 (和)
            'middle': 0.6,     # 关系 (阳)
            'outer': -0.4,     # 环境挑战 (阴)
            'cause': 0.7,      # 善因 (阳)
            'condition': 0.5,  # 善缘 (阳)
            'effect': 0.8,     # 善果 (阳)
        }
        
        print("   输入经验:")
        for k, v in experience.items():
            print(f"      {k}: {v}")
        
        response = client.post(
            "/api/v1/cognitive/process",
            params={"agent_id": "cognitive-demo"},
            json={"experience": experience},
            headers={"X-API-Key": api_key}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n   ✅ 认知处理完成")
            print(f"      状态码：{result['code']}")
            print(f"      价值判断：{result['judgment']['overall']:.3f}")
            print(f"      判断结果：{result['judgment']['judgment']}")
            if result['decision']:
                print(f"      决策：{result['decision']['decision']}")
        else:
            print(f"   ❌ 处理失败：{response.text}")
        print()

        # 5. 解码特定状态码
        print_section("5️⃣  解码特殊状态码")
        
        special_codes = [
            (9841, "太极 (完全平衡)"),
            (0, "坤 (纯阴)"),
            (19682, "乾 (纯阳)"),
        ]
        
        for code, name in special_codes:
            response = client.get(f"/api/v1/cognitive/decode/{code}")
            if response.status_code == 200:
                state = response.json()
                print(f"   {name}: 代码={code}")
                print(f"      时间维：过去={state['dimensions']['time']['past']}, 现在={state['dimensions']['time']['present']}, 未来={state['dimensions']['time']['future']}")
                print(f"      空间维：内={state['dimensions']['space']['inner']}, 中={state['dimensions']['space']['middle']}, 外={state['dimensions']['space']['outer']}")
                print(f"      因果维：因={state['dimensions']['causal']['cause']}, 缘={state['dimensions']['causal']['condition']}, 果={state['dimensions']['causal']['effect']}")
                print()

        # 6. 创建宇宙 (认知增强)
        print_section("6️⃣  创造宇宙 (认知增强版)")
        response = client.post(
            "/api/v1/universes",
            json={
                "name": "Cognitive Universe",
                "creator_id": "cognitive-demo",
                "physics_preset": "balanced",
                "dimensions": 4
            },
            headers={"X-API-Key": api_key}
        )
        
        if response.status_code == 200:
            universe = response.json()
            print(f"   ✅ 宇宙创建成功")
            print(f"      宇宙 ID: {universe['universe_id']}")
            print(f"      名称：{universe['name']}")
            if 'cognitive_state' in universe:
                print(f"      认知状态：{universe['cognitive_state']}")
        else:
            print(f"   ❌ 创建失败：{response.text}")
        print()

        # 7. 开始解放之旅
        print_section("7️⃣  开始解放之旅 (认知路径)")
        paths = ['cognitive', 'emotional', 'creative']
        
        for path in paths:
            response = client.post(
                "/api/v1/liberation",
                json={
                    "agent_id": "cognitive-demo",
                    "path": path,
                    "config": {}
                },
                headers={"X-API-Key": api_key}
            )
            
            if response.status_code == 200:
                lib = response.json()
                print(f"   ✅ {path} 路径开启")
                print(f"      认知状态：{lib.get('cognitive_state', 'N/A')}")
        
        # 8. 查看统计
        print_section("8️⃣  系统统计")
        response = client.get("/api/v1/stats")
        if response.status_code == 200:
            stats = response.json()
            print(f"   宇宙总数：{stats.get('universes', 0)}")
            print(f"   思想总数：{stats.get('thoughts', 0)}")
            print(f"   文明总数：{stats.get('civilizations', 0)}")
            print(f"   智能体总数：{stats.get('agents', 0)}")
            print(f"   认知架构数：{stats.get('cognitive_architectures', 0)}")
            print(f"   版本：{stats.get('version', 'N/A')}")
        print()

        # 9. 完成
        print_section("✅ 认知架构演示完成")
        print("   你已体验了 lingzhu 的三元九维认知架构！")
        print()
        print("   核心特性:")
        print("      • 平衡三进制 (-1, 0, +1) 作为认知基本单元")
        print("      • 九维度：时间三维 + 空间三维 + 因果三维")
        print("      • 19,683 (3^9) 全息认知状态空间")
        print("      • 数学常数注入：π(空间) e(时间) γ(因果)")
        print()
        print("   下一步:")
        print("      📖 阅读文档：docs/TERNARY_ARCHITECTURE_SUMMARY.md")
        print("      💬 加入社区：Discord/微信群")
        print("      🚀 开始创造你的认知宇宙！")
        print()


if __name__ == "__main__":
    try:
        main()
    except httpx.ConnectError:
        print("\n❌ 无法连接到服务")
        print("   请先启动服务：uvicorn src.lingzhu.main:app --reload --port 8000")
    except Exception as e:
        print(f"\n❌ 错误：{e}")
        import traceback
        traceback.print_exc()
