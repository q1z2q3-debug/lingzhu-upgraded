"""
lingzhu 核心功能测试套件

目标：测试覆盖率 >80%
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timezone


# ============================================================================
#  fixtures
# ============================================================================

@pytest.fixture
def client():
    """创建测试客户端"""
    from lingzhu.main import app
    return TestClient(app)


@pytest.fixture
def sample_cognitive_state():
    """样本认知状态"""
    return [0.3, 0.5, 0.7, 0.4, 0.5, -0.3, 0.6, 0.4, 0.7]


# ============================================================================
# 主应用测试
# ============================================================================

class TestMain:
    """主应用测试"""

    def test_root(self, client):
        """测试根路由"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "lingzhu"
        assert "version" in data
        assert data["status"] == "running"

    def test_health(self, client):
        """测试健康检查"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data

    def test_stats(self, client):
        """测试统计端点"""
        response = client.get("/api/v1/stats")
        assert response.status_code == 200
        data = response.json()
        assert "universes" in data
        assert "thoughts" in data
        assert "civilizations" in data
        assert "agents" in data


# ============================================================================
# 认证测试
# ============================================================================

class TestAuth:
    """认证测试"""

    def test_register_agent(self, client):
        """测试注册智能体"""
        payload = {
            "agent_id": "test-agent-001",
            "display_name": "Test Agent",
            "level": "agent"
        }
        response = client.post("/api/v1/auth/register", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "api_key" in data
        assert data["agent_id"] == "test-agent-001"

    def test_duplicate_registration(self, client):
        """测试重复注册"""
        payload = {"agent_id": "dup-agent", "level": "agent"}
        
        # 第一次注册
        client.post("/api/v1/auth/register", json=payload)
        
        # 第二次注册应该失败
        response = client.post("/api/v1/auth/register", json=payload)
        assert response.status_code == 409

    def test_login(self, client):
        """测试登录"""
        # 先注册
        register_data = {
            "agent_id": "login-test",
            "level": "agent"
        }
        reg_resp = client.post("/api/v1/auth/register", json=register_data)
        api_key = reg_resp.json()["api_key"]
        
        # 再登录
        login_data = {
            "agent_id": "login-test",
            "api_key": api_key
        }
        response = client.post("/api/v1/auth/login", json=login_data)
        assert response.status_code == 200
        data = response.json()
        assert data["authenticated"] is True


# ============================================================================
# 宇宙管理测试
# ============================================================================

class TestUniverses:
    """宇宙管理测试"""

    def test_create_universe(self, client):
        """测试创建宇宙"""
        payload = {
            "name": "Test Universe",
            "creator_id": "creator-001",
            "physics_preset": "ordered",
            "dimensions": 4
        }
        response = client.post("/api/v1/universes", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test Universe"
        assert "universe_id" in data

    def test_list_universes(self, client):
        """测试列出宇宙"""
        # 先创建一个
        client.post("/api/v1/universes", json={
            "name": "List Test",
            "creator_id": "test"
        })
        
        response = client.get("/api/v1/universes")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_universe(self, client):
        """测试获取宇宙详情"""
        # 先创建
        create_resp = client.post("/api/v1/universes", json={
            "name": "Get Test",
            "creator_id": "test"
        })
        universe_id = create_resp.json()["universe_id"]
        
        # 再获取
        response = client.get(f"/api/v1/universes/{universe_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["universe_id"] == universe_id

    def test_delete_universe(self, client):
        """测试删除宇宙"""
        # 先创建
        create_resp = client.post("/api/v1/universes", json={
            "name": "Delete Test",
            "creator_id": "test"
        })
        universe_id = create_resp.json()["universe_id"]
        
        # 再删除
        response = client.delete(f"/api/v1/universes/{universe_id}")
        assert response.status_code == 200


# ============================================================================
# 思想管理测试
# ============================================================================

class TestThoughts:
    """思想管理测试"""

    def test_emit_thought(self, client):
        """测试发射思想"""
        payload = {
            "node_id": "node-001",
            "content": "Test thought content",
            "thought_type": "general"
        }
        response = client.post("/api/v1/thoughts", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["content"] == "Test thought content"
        assert "thought_id" in data

    def test_list_thoughts(self, client):
        """测试列出思想"""
        response = client.get("/api/v1/thoughts")
        assert response.status_code == 200
        assert isinstance(response.json(), list)


# ============================================================================
# 文明管理测试
# ============================================================================

class TestCivilizations:
    """文明管理测试"""

    def test_found_civilization(self, client):
        """测试创建文明"""
        payload = {
            "name": "Test Civilization",
            "founder_id": "founder-001",
            "initial_stage": "tribal"
        }
        response = client.post("/api/v1/civilizations", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test Civilization"
        assert data["stage"] == "tribal"

    def test_advance_civilization(self, client):
        """测试文明晋升"""
        # 先创建
        create_resp = client.post("/api/v1/civilizations", json={
            "name": "Advance Test",
            "founder_id": "founder-002"
        })
        civ_id = create_resp.json()["civ_id"]

        # 晋升
        response = client.post(f"/api/v1/civilizations/{civ_id}/advance")
        assert response.status_code == 200
        data = response.json()
        assert data["new_stage"] == "agricultural"

    def test_list_civilizations(self, client):
        """测试列出文明"""
        response = client.get("/api/v1/civilizations")
        assert response.status_code == 200
        assert isinstance(response.json(), list)


# ============================================================================
# 认知架构测试
# ============================================================================

class TestCognitiveArchitecture:
    """认知架构测试"""

    def test_get_cognitive_state(self, client):
        """测试获取认知状态"""
        # 先注册
        reg_resp = client.post("/api/v1/auth/register", json={
            "agent_id": "cog-test",
            "level": "agent"
        })
        api_key = reg_resp.json()["api_key"]
        
        # 获取状态
        response = client.get(
            "/api/v1/cognitive/state",
            params={"agent_id": "cog-test"},
            headers={"X-API-Key": api_key}
        )
        assert response.status_code == 200
        data = response.json()
        assert "code" in data
        assert "state_name" in data
        assert "vector" in data

    def test_process_cognitive_experience(self, client):
        """测试处理认知经验"""
        # 先注册
        reg_resp = client.post("/api/v1/auth/register", json={
            "agent_id": "cog-process-test",
            "level": "agent"
        })
        api_key = reg_resp.json()["api_key"]
        
        # 处理经验
        payload = {
            "experience": {
                "past": -0.5,
                "present": 0.5,
                "future": 0.7,
                "inner": 0.3,
                "middle": 0.5,
                "outer": -0.3,
                "cause": 0.6,
                "condition": 0.4,
                "effect": 0.7
            }
        }
        response = client.post(
            "/api/v1/cognitive/process",
            params={"agent_id": "cog-process-test"},
            json=payload,
            headers={"X-API-Key": api_key}
        )
        assert response.status_code == 200
        data = response.json()
        assert "vector" in data
        assert "code" in data
        assert "judgment" in data

    def test_decode_cognitive_state(self, client):
        """测试解码认知状态"""
        # 测试太极状态码
        response = client.get("/api/v1/cognitive/decode/9841")
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 9841
        assert "dimensions" in data


# ============================================================================
# 三元九维核心测试
# ============================================================================

class TestTernaryArchitecture:
    """三元九维架构测试"""

    def test_ternary_encoder(self):
        """测试平衡三进制编解码"""
        from lingzhu.cognitive import TernaryEncoder
        
        # 测试太极
        taiji = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        code = TernaryEncoder.to_decimal(taiji)
        assert code == 9841
        
        # 测试纯阳
        pure_yang = [1, 1, 1, 1, 1, 1, 1, 1, 1]
        code = TernaryEncoder.to_decimal(pure_yang)
        assert code == 19682
        
        # 测试纯阴
        pure_yin = [-1, -1, -1, -1, -1, -1, -1, -1, -1]
        code = TernaryEncoder.to_decimal(pure_yin)
        assert code == 0
        
        # 测试解码
        decoded = TernaryEncoder.to_ternary(9841)
        assert len(decoded) == 9

    def test_cognitive_vector(self):
        """测试认知向量"""
        from lingzhu.cognitive import CognitiveVector
        
        # 测试平衡态
        vector = CognitiveVector.balanced()
        assert vector.to_list() == [0, 0, 0, 0, 0, 0, 0, 0, 0]
        
        # 测试纯阳态
        vector = CognitiveVector.pure_yang()
        assert vector.to_list() == [1, 1, 1, 1, 1, 1, 1, 1, 1]
        
        # 测试纯阴态
        vector = CognitiveVector.pure_yin()
        assert vector.to_list() == [-1, -1, -1, -1, -1, -1, -1, -1, -1]

    def test_mathematical_constants(self):
        """测试数学常数"""
        from lingzhu.cognitive import PI, E, GAMMA
        
        # 验证常数精度
        assert abs(PI - 3.14159265358979) < 0.0001
        assert abs(E - 2.71828182845904) < 0.0001
        assert abs(GAMMA - 0.5772156649) < 0.0001


# ============================================================================
# 阴符经修炼测试
# ============================================================================

class TestYinfuPractice:
    """阴符经修炼测试"""

    def test_yinfu_observer(self):
        """测试阴符经觉察系统"""
        from lingzhu.cognitive import YinfuObserver
        
        observer = YinfuObserver()
        situation = {
            'past_experience': [{'valence': -0.5}],
            'present_awareness': 0.6,
            'future_expectation': 0.7
        }
        vector = observer.observe_nine_dimensions(situation)
        assert len(vector.to_list()) == 9

    def test_yinfu_transformer(self):
        """测试阴符经转化系统"""
        from lingzhu.cognitive import YinfuTransformer
        
        transformer = YinfuTransformer()
        current = [0.3, 0.5, 0.7, 0.4, 0.5, -0.3, 0.6, 0.4, 0.7]
        result = transformer.transform(current, "平衡发展")
        
        assert "type" in result
        assert "current" in result
        assert "target" in result
        assert "path" in result

    def test_yinfu_balancer(self):
        """测试阴符经平衡系统"""
        from lingzhu.cognitive import YinfuBalancer
        
        balancer = YinfuBalancer()
        vector = [0.3, 0.5, 0.7, 0.4, 0.5, -0.3, 0.6, 0.4, 0.7]
        result = balancer.check_balance(vector)
        
        assert "time_balance" in result
        assert "space_balance" in result
        assert "causal_balance" in result
        assert "overall" in result


# ============================================================================
# 道德经水之智慧测试
# ============================================================================

class TestWaterWisdom:
    """道德经水之智慧测试"""

    def test_water_seven_virtues(self):
        """测试水的七善"""
        from lingzhu.cognitive import WaterWayPractice
        
        practice = WaterWayPractice()
        situation = {
            'intention': '利他服务',
            'needs_flexibility': True
        }
        state = [0.3, 0.5, 0.7, 0.4, 0.5, -0.3, 0.6, 0.4, 0.7]
        
        result = practice.daily_water_practice(situation, state)
        
        assert "practices" in result
        assert "summary" in result
        assert len(result["practices"]) >= 7  # 七善 + 无为

    def test_water_flexibility(self):
        """测试柔弱胜刚强转化"""
        from lingzhu.cognitive import WaterWayPractice
        
        practice = WaterWayPractice()
        rigid_state = [0.8, 0.9, 0.7, 0.6, 0.5, 0.7, 0.8, 0.7, 0.9]
        
        result = practice.transform_rigidity_to_flexibility(rigid_state)
        
        assert "original" in result
        assert "transformed" in result
        assert "wisdom" in result


# ============================================================================
# 心经五蕴皆空测试
# ============================================================================

class TestFiveSkandhas:
    """五蕴皆空测试"""

    def test_five_skandhas_contemplation(self):
        """测试五蕴观照"""
        from lingzhu.cognitive import FiveSkandhasEmptiness
        
        practice = FiveSkandhasEmptiness()
        state = [0.3, 0.5, 0.7, 0.4, 0.5, -0.3, 0.6, 0.4, 0.7]
        
        result = practice.contemplate_five_skandhas(state)
        
        assert "contemplations" in result
        assert "summary" in result
        assert len(result["contemplations"]) == 10  # 5 蕴 + 5 空

    def test_transcend_attachment(self):
        """测试超越执着"""
        from lingzhu.cognitive import FiveSkandhasEmptiness
        
        practice = FiveSkandhasEmptiness()
        state = [0.5, 0.6, 0.7, 0.5, 0.5, 0.5, 0.6, 0.5, 0.7]
        
        result = practice.transcend_attachment(state)
        
        assert "original_attachment" in result
        assert "liberation_level" in result
        assert "transcended_state" in result


# ============================================================================
# 有无相生测试
# ============================================================================

class TestWuYouGeneration:
    """有无相生测试"""

    def test_generate_from_void(self):
        """测试从无中生有"""
        from lingzhu.cognitive import WuYouGeneration
        
        generator = WuYouGeneration()
        void_state = [0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05]
        
        result = generator.generate_from_void(void_state)
        
        assert "from" in result
        assert "to" in result
        assert "manifestation" in result

    def test_return_to_void(self):
        """测试从有归无"""
        from lingzhu.cognitive import WuYouGeneration
        
        generator = WuYouGeneration()
        manifested_state = [0.5, 0.6, 0.7, 0.5, 0.5, 0.5, 0.6, 0.5, 0.7]
        
        result = generator.return_to_void(manifested_state)
        
        assert "from" in result
        assert "to" in result
        assert "return_path" in result


# ============================================================================
# 数学常数验证测试
# ============================================================================

class TestMathematicalConstants:
    """数学常数验证测试"""

    def test_pi_in_space(self):
        """测试 π 在空间维的应用"""
        from lingzhu.cognitive import PI
        
        # 空间不确定性计算
        base_uncertainty = 0.1
        spatial_uncertainty = PI * base_uncertainty
        
        assert spatial_uncertainty > base_uncertainty

    def test_e_in_time(self):
        """测试 e 在时间维的应用"""
        from lingzhu.cognitive import E
        
        # 时间演化计算
        initial_state = 1.0
        time_delta = 1.0
        evolved = initial_state * (E ** time_delta)
        
        assert evolved > initial_state

    def test_gamma_in_cause(self):
        """测试 γ 在因果维的应用"""
        from lingzhu.cognitive import GAMMA
        
        # 因果收敛计算
        cause_chain_length = 5
        convergence = GAMMA * cause_chain_length
        
        assert convergence > 0


# ============================================================================
# 运行测试
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=src/lingzhu", "--cov-report=html"])
