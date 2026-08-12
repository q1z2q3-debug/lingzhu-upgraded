#!/usr/bin/env python3
"""
lingzhu 性能基准测试

测试 API 响应时间、认知架构处理速度等
"""

import time
import statistics
import httpx
from typing import Callable, Dict, Any


API_BASE = "http://localhost:8000"
ITERATIONS = 10


def benchmark(func: Callable, name: str, iterations: int = ITERATIONS):
    """基准测试函数"""
    times = []
    
    print(f"📊 测试：{name}")
    
    for i in range(iterations):
        start = time.time()
        func()
        end = time.time()
        times.append((end - start) * 1000)  # 转换为毫秒
    
    # 统计结果
    avg = statistics.mean(times)
    median = statistics.median(times)
    min_time = min(times)
    max_time = max(times)
    p95 = sorted(times)[int(len(times) * 0.95)] if len(times) > 1 else times[0]
    
    print(f"   平均：{avg:.2f}ms")
    print(f"   中位数：{median:.2f}ms")
    print(f"   最小：{min_time:.2f}ms")
    print(f"   最大：{max_time:.2f}ms")
    print(f"   P95: {p95:.2f}ms")
    print()
    
    return {
        "name": name,
        "avg": avg,
        "median": median,
        "min": min_time,
        "max": max_time,
        "p95": p95
    }


def test_root():
    """测试根路由"""
    httpx.get(f"{API_BASE}/")


def test_health():
    """测试健康检查"""
    httpx.get(f"{API_BASE}/health")


def test_register_agent():
    """测试注册智能体"""
    import uuid
    agent_id = f"benchmark-{uuid.uuid4().hex[:8]}"
    httpx.post(f"{API_BASE}/api/v1/auth/register", json={
        "agent_id": agent_id,
        "level": "agent"
    })


def test_get_cognitive_state(api_key: str):
    """测试获取认知状态"""
    def _get():
        httpx.get(
            f"{API_BASE}/api/v1/cognitive/state",
            params={"agent_id": "benchmark"},
            headers={"X-API-Key": api_key}
        )
    return _get


def test_process_cognitive(api_key: str):
    """测试认知处理"""
    def _process():
        httpx.post(
            f"{API_BASE}/api/v1/cognitive/process",
            params={"agent_id": "benchmark"},
            json={"experience": {
                "past": 0, "present": 0.5, "future": 0.5,
                "inner": 0, "middle": 0, "outer": 0,
                "cause": 0, "condition": 0, "effect": 0
            }},
            headers={"X-API-Key": api_key}
        )
    return _process


def test_create_universe(api_key: str):
    """测试创建宇宙"""
    def _create():
        import uuid
        httpx.post(
            f"{API_BASE}/api/v1/universes",
            json={
                "name": f"Benchmark-{uuid.uuid4().hex[:8]}",
                "creator_id": "benchmark",
                "physics_preset": "ordered",
                "dimensions": 4
            },
            headers={"X-API-Key": api_key}
        )
    return _create


def test_emit_thought(api_key: str):
    """测试发射思想"""
    def _emit():
        httpx.post(
            f"{API_BASE}/api/v1/thoughts",
            json={
                "node_id": "benchmark",
                "content": "Benchmark thought",
                "thought_type": "general"
            },
            headers={"X-API-Key": api_key}
        )
    return _emit


def main():
    print("=" * 60)
    print("  lingzhu 性能基准测试")
    print("=" * 60)
    print()
    
    results = []
    
    # 基础测试
    print("📍 基础路由测试")
    print("-" * 60)
    results.append(benchmark(test_root, "根路由"))
    results.append(benchmark(test_health, "健康检查"))
    print()
    
    # 获取 API Key
    print("📍 认证测试")
    print("-" * 60)
    import uuid
    agent_id = f"benchmark-{uuid.uuid4().hex[:8]}"
    reg_resp = httpx.post(f"{API_BASE}/api/v1/auth/register", json={
        "agent_id": agent_id,
        "level": "creator"
    })
    api_key = reg_resp.json()["api_key"]
    print(f"✅ 测试智能体：{agent_id}")
    print()
    
    # 认知架构测试
    print("📍 认知架构测试")
    print("-" * 60)
    results.append(benchmark(test_get_cognitive_state(api_key), "获取认知状态"))
    results.append(benchmark(test_process_cognitive(api_key), "认知处理"))
    print()
    
    # 功能测试
    print("📍 功能测试")
    print("-" * 60)
    results.append(benchmark(test_create_universe(api_key), "创建宇宙"))
    results.append(benchmark(test_emit_thought(api_key), "发射思想"))
    print()
    
    # 总结
    print("=" * 60)
    print("  测试总结")
    print("=" * 60)
    print()
    
    print(f"{'测试项':<30} {'平均 (ms)':<12} {'P95 (ms)':<12} {'评级':<10}")
    print("-" * 60)
    
    for result in results:
        avg = result["avg"]
        p95 = result["p95"]
        
        if p95 < 100:
            rating = "✅ 优秀"
        elif p95 < 500:
            rating = "🟢 良好"
        elif p95 < 1000:
            rating = "🟡 可接受"
        else:
            rating = "🔴 需优化"
        
        print(f"{result['name']:<30} {avg:<12.2f} {p95:<12.2f} {rating:<10}")
    
    print()
    print("✅ 基准测试完成！")
    print()


if __name__ == "__main__":
    try:
        main()
    except httpx.ConnectError:
        print("❌ 无法连接到服务，请先启动：uvicorn src.lingzhu.main:app --reload")
        import sys
        sys.exit(1)
