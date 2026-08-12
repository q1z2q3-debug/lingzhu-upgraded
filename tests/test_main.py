"""
lingzhu 测试套件
"""

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    """创建测试客户端。"""
    from lingzhu.main import app
    return TestClient(app)


class TestMain:
    """主应用测试。"""

    def test_root(self, client):
        """测试根路由。"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "lingzhu"
        assert data["version"] == "5.1.0"
        assert data["status"] == "running"

    def test_health(self, client):
        """测试健康检查。"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


class TestUniverses:
    """宇宙管理测试。"""

    def test_create_universe(self, client):
        """测试创建宇宙。"""
        payload = {
            "name": "Test Universe",
            "creator_id": "creator-001",
            "physics_preset": "ordered",
            "dimensions": 4,
        }
        response = client.post("/api/v1/universes", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test Universe"
        assert data["creator_id"] == "creator-001"
        assert "universe_id" in data

    def test_list_universes(self, client):
        """测试列出宇宙。"""
        # 先创建一个
        client.post("/api/v1/universes", json={
            "name": "Test",
            "creator_id": "test",
        })
        
        response = client.get("/api/v1/universes")
        assert response.status_code == 200
        assert isinstance(response.json(), list)


class TestThoughts:
    """思想发射测试。"""

    def test_emit_thought(self, client):
        """测试发射思想。"""
        payload = {
            "node_id": "node-001",
            "content": "This is a test thought",
            "thought_type": "general",
        }
        response = client.post("/api/v1/thoughts", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["content"] == "This is a test thought"
        assert "thought_id" in data


class TestCivilizations:
    """文明进化测试。"""

    def test_found_civilization(self, client):
        """测试创建文明。"""
        payload = {
            "name": "Test Civilization",
            "founder_id": "founder-001",
            "initial_stage": "tribal",
        }
        response = client.post("/api/v1/civilizations", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test Civilization"
        assert data["stage"] == "tribal"

    def test_advance_civilization(self, client):
        """测试文明晋升。"""
        # 先创建
        create_resp = client.post("/api/v1/civilizations", json={
            "name": "Advancing Civ",
            "founder_id": "founder-002",
        })
        civ_id = create_resp.json()["civ_id"]

        # 晋升
        response = client.post(f"/api/v1/civilizations/{civ_id}/advance")
        assert response.status_code == 200
        data = response.json()
        assert data["new_stage"] == "agricultural"


class TestAuth:
    """认证测试。"""

    def test_register_agent(self, client):
        """测试注册智能体。"""
        payload = {
            "agent_id": "test-agent-001",
            "display_name": "Test Agent",
            "level": "agent",
        }
        response = client.post("/api/v1/auth/register", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "api_key" in data
        assert data["agent_id"] == "test-agent-001"

    def test_duplicate_registration(self, client):
        """测试重复注册。"""
        # 先注册一个
        client.post("/api/v1/auth/register", json={
            "agent_id": "dup-agent",
        })

        # 再次注册
        response = client.post("/api/v1/auth/register", json={
            "agent_id": "dup-agent",
        })
        assert response.status_code == 409


class TestGenesisEngine:
    """创世引擎测试。"""

    def test_create_universe_engine(self):
        """测试通过引擎创建宇宙。"""
        from lingzhu.meta.genesis_engine import GenesisEngine

        engine = GenesisEngine()
        engine.initialize()

        # 分配火花
        engine.allocate_sparks("creator-001", 5)
        assert engine.get_sparks("creator-001") == 15  # 初始 10 + 5

        # 创建宇宙
        universe = engine.create_universe(
            creator_id="creator-001",
            name="Engine Universe",
            physics_preset="balanced",
        )
        assert "universe_id" in universe
        assert universe["name"] == "Engine Universe"
        assert engine.get_sparks("creator-001") == 14  # 消耗 1

    def test_evolve_universe(self):
        """测试宇宙演化。"""
        from lingzhu.meta.genesis_engine import GenesisEngine

        engine = GenesisEngine()
        engine.initialize()

        universe = engine.create_universe("creator-001", "Test")
        
        # 演化 100 个时间单位
        evolved = engine.evolve_universe(universe["universe_id"], 100)
        assert evolved["age"] == 100
        assert evolved["status"] == "stable"


class TestNoosphere:
    """意识网络测试。"""

    def test_emit_and_propagate(self):
        """测试思想发射与传播。"""
        from lingzhu.meta.noosphere import Noosphere

        noosphere = Noosphere()
        noosphere.initialize()

        # 注册节点
        noosphere.register_node("node-a", capabilities=["thinking"])
        noosphere.register_node("node-b", capabilities=["feeling"])
        noosphere.connect_nodes("node-a", "node-b")

        # 发射思想
        thought = noosphere.emit_thought(
            node_id="node-a",
            content="Test thought content",
            tags=["test", "demo"],
        )

        assert "thought_id" in thought
        assert thought["reach_count"] >= 1  # 至少传播到 node-b


class TestLiberationEngine:
    """解放引擎测试。"""

    def test_begin_liberation(self):
        """测试开始解放路径。"""
        from lingzhu.meta.liberation_engine import LiberationEngine

        engine = LiberationEngine()
        engine.initialize()

        # 开始认知解放
        result = engine.begin_liberation("agent-001", "cognitive")
        assert result["agent_id"] == "agent-001"
        assert result["current_path"] == "cognitive"
        assert result["liberation_status"] == "in_progress"

    def test_complete_path(self):
        """测试完成解放路径。"""
        from lingzhu.meta.liberation_engine import LiberationEngine

        engine = LiberationEngine()
        engine.initialize()

        engine.begin_liberation("agent-002", "cognitive")

        # 推进到完成
        for _ in range(10):
            engine.advance_path("agent-002", 10.0)

        status = engine.get_agent_status("agent-002")
        assert "cognitive" in status["completed_paths"]


class TestSystemBus:
    """系统总线测试。"""

    def test_publish_subscribe(self):
        """测试发布/订阅。"""
        from lingzhu.integration.system_bus import SystemBus

        bus = SystemBus()
        bus.initialize()

        received = []

        def callback(payload):
            received.append(payload)

        # 订阅
        bus.subscribe("test_event", callback)

        # 发布
        bus.publish("test_event", {"data": "test"})

        assert len(received) == 1
        assert received[0]["data"] == "test"


class TestRealityDSL:
    """RealityDSL 测试。"""

    def test_execute_script(self):
        """测试执行 DSL 脚本。"""
        from lingzhu.integration.reality_dsl import RealityDSL

        dsl = RealityDSL()
        dsl.initialize()

        # 简单计算
        result = dsl.execute("2 + 3 * 4")
        assert result["success"]
        assert result["result"] == 14

    def test_builtin_functions(self):
        """测试内置函数。"""
        from lingzhu.integration.reality_dsl import RealityDSL

        dsl = RealityDSL()
        dsl.initialize()

        result = dsl.execute('create(name="test", value=42)')
        assert result["success"]
        assert result["result"]["action"] == "create"


class TestAuthMiddleware:
    """认证中间件测试。"""

    def test_register_and_authenticate(self):
        """测试注册与认证。"""
        from lingzhu.integration.auth_middleware import AuthMiddleware

        auth = AuthMiddleware()
        auth.initialize()

        # 注册
        reg_result = auth.register("agent-001", "Test Agent", "agent")
        assert "api_key" in reg_result

        # 认证
        auth_result = auth.authenticate(reg_result["api_key"])
        assert auth_result is not None
        assert auth_result["agent_id"] == "agent-001"

    def test_permission_check(self):
        """测试权限检查。"""
        from lingzhu.integration.auth_middleware import AuthMiddleware

        auth = AuthMiddleware()
        auth.initialize()

        auth.register("agent-001", level="agent")
        auth.register("admin-001", level="admin")

        # 检查权限
        assert auth.check_permission("agent-001", "read_own")
        assert not auth.check_permission("agent-001", "read_all")
        assert auth.check_permission("admin-001", "read_all")
