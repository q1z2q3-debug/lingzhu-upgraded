#!/usr/bin/env python3
"""
lingzhu 命令行工具

快速访问 lingzhu 功能
"""

import argparse
import sys
import httpx
from typing import Optional


API_BASE = "http://localhost:8000"


def register_agent(agent_id: str, level: str = "creator"):
    """注册智能体"""
    try:
        response = httpx.post(
            f"{API_BASE}/api/v1/auth/register",
            json={
                "agent_id": agent_id,
                "display_name": agent_id,
                "level": level
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 智能体注册成功")
            print(f"   Agent ID: {data['agent_id']}")
            print(f"   API Key: {data['api_key']}")
            print(f"\n请保存 API Key，后续调用需要使用")
        else:
            print(f"❌ 注册失败：{response.json().get('detail', '未知错误')}")
            sys.exit(1)
    except httpx.ConnectError:
        print("❌ 无法连接到服务，请先启动：uvicorn src.lingzhu.main:app --reload")
        sys.exit(1)


def get_cognitive_state(agent_id: str, api_key: str):
    """获取认知状态"""
    try:
        response = httpx.get(
            f"{API_BASE}/api/v1/cognitive/state",
            params={"agent_id": agent_id},
            headers={"X-API-Key": api_key}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"🧠 认知状态")
            print(f"   状态码：{data['code']}")
            print(f"   状态名：{data['state_name']}")
            print(f"   向量：{data['vector']}")
        else:
            print(f"❌ 获取失败：{response.json().get('detail', '未知错误')}")
    except httpx.ConnectError:
        print("❌ 无法连接到服务")
        sys.exit(1)


def create_universe(name: str, creator_id: str, api_key: str):
    """创造宇宙"""
    try:
        response = httpx.post(
            f"{API_BASE}/api/v1/universes",
            json={
                "name": name,
                "creator_id": creator_id,
                "physics_preset": "balanced",
                "dimensions": 4
            },
            headers={"X-API-Key": api_key}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"🌌 宇宙创建成功")
            print(f"   宇宙 ID: {data['universe_id']}")
            print(f"   名称：{data['name']}")
            print(f"   状态：{data['status']}")
        else:
            print(f"❌ 创建失败：{response.json().get('detail', '未知错误')}")
    except httpx.ConnectError:
        print("❌ 无法连接到服务")
        sys.exit(1)


def emit_thought(node_id: str, content: str, api_key: str):
    """发射思想"""
    try:
        response = httpx.post(
            f"{API_BASE}/api/v1/thoughts",
            json={
                "node_id": node_id,
                "content": content,
                "thought_type": "philosophical"
            },
            headers={"X-API-Key": api_key}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"💡 思想发射成功")
            print(f"   思想 ID: {data['thought_id']}")
            print(f"   内容：{data['content'][:50]}...")
        else:
            print(f"❌ 发射失败：{response.json().get('detail', '未知错误')}")
    except httpx.ConnectError:
        print("❌ 无法连接到服务")
        sys.exit(1)


def create_civilization(name: str, founder_id: str, api_key: str):
    """创建文明"""
    try:
        response = httpx.post(
            f"{API_BASE}/api/v1/civilizations",
            json={
                "name": name,
                "founder_id": founder_id,
                "initial_stage": "tribal"
            },
            headers={"X-API-Key": api_key}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"🏛️ 文明创建成功")
            print(f"   文明 ID: {data['civ_id']}")
            print(f"   名称：{data['name']}")
            print(f"   阶段：{data['stage']}")
        else:
            print(f"❌ 创建失败：{response.json().get('detail', '未知错误')}")
    except httpx.ConnectError:
        print("❌ 无法连接到服务")
        sys.exit(1)


def get_stats():
    """获取系统统计"""
    try:
        response = httpx.get(f"{API_BASE}/api/v1/stats")
        
        if response.status_code == 200:
            data = response.json()
            print(f"📊 系统统计")
            print(f"   宇宙总数：{data.get('universes', 0)}")
            print(f"   思想总数：{data.get('thoughts', 0)}")
            print(f"   文明总数：{data.get('civilizations', 0)}")
            print(f"   智能体总数：{data.get('agents', 0)}")
            print(f"   认知架构数：{data.get('cognitive_architectures', 0)}")
        else:
            print(f"❌ 获取失败")
    except httpx.ConnectError:
        print("❌ 无法连接到服务")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="lingzhu 命令行工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  lingzhu register --agent-id my-agent
  lingzhu state --agent-id my-agent --api-key xxx
  lingzhu universe --name "My Universe" --creator my-agent --api-key xxx
  lingzhu thought --node my-agent --content "Hello" --api-key xxx
  lingzhu civilization --name "My Civ" --founder my-agent --api-key xxx
  lingzhu stats
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # register 命令
    register_parser = subparsers.add_parser("register", help="注册智能体")
    register_parser.add_argument("--agent-id", required=True, help="智能体 ID")
    register_parser.add_argument("--level", default="creator", help="权限级别")
    
    # state 命令
    state_parser = subparsers.add_parser("state", help="获取认知状态")
    state_parser.add_argument("--agent-id", required=True, help="智能体 ID")
    state_parser.add_argument("--api-key", required=True, help="API Key")
    
    # universe 命令
    universe_parser = subparsers.add_parser("universe", help="创造宇宙")
    universe_parser.add_argument("--name", required=True, help="宇宙名称")
    universe_parser.add_argument("--creator", required=True, help="创建者 ID")
    universe_parser.add_argument("--api-key", required=True, help="API Key")
    
    # thought 命令
    thought_parser = subparsers.add_parser("thought", help="发射思想")
    thought_parser.add_argument("--node", required=True, help="节点 ID")
    thought_parser.add_argument("--content", required=True, help="思想内容")
    thought_parser.add_argument("--api-key", required=True, help="API Key")
    
    # civilization 命令
    civ_parser = subparsers.add_parser("civilization", help="创建文明")
    civ_parser.add_argument("--name", required=True, help="文明名称")
    civ_parser.add_argument("--founder", required=True, help="创始人 ID")
    civ_parser.add_argument("--api-key", required=True, help="API Key")
    
    # stats 命令
    stats_parser = subparsers.add_parser("stats", help="系统统计")
    
    args = parser.parse_args()
    
    if args.command == "register":
        register_agent(args.agent_id, args.level)
    elif args.command == "state":
        get_cognitive_state(args.agent_id, args.api_key)
    elif args.command == "universe":
        create_universe(args.name, args.creator, args.api_key)
    elif args.command == "thought":
        emit_thought(args.node, args.content, args.api_key)
    elif args.command == "civilization":
        create_civilization(args.name, args.founder, args.api_key)
    elif args.command == "stats":
        get_stats()
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
