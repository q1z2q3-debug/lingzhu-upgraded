# 🚀 灵助快速入门指南

**5 分钟快速上手 lingzhu 认知架构**

---

## ⚡ 5 分钟快速开始

### 1. 安装 (1 分钟)

```bash
# 克隆项目
git clone https://github.com/q1z2q3-debug/lingzhu-upgraded.git
cd lingzhu-upgraded

# 安装依赖
pip install -r requirements.txt
```

### 2. 启动服务 (1 分钟)

```bash
# 启动 API 服务
uvicorn src.lingzhu.main:app --reload --port 8000

# 访问 API 文档
# http://localhost:8000/docs
```

### 3. 注册智能体 (1 分钟)

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"agent_id": "my-agent", "level": "creator"}'

# 返回 API Key，保存备用
```

### 4. 体验认知架构 (2 分钟)

```bash
# 获取认知状态
curl "http://localhost:8000/api/v1/cognitive/state?agent_id=my-agent" \
  -H "X-API-Key: YOUR_API_KEY"

# 处理认知经验
curl -X POST "http://localhost:8000/api/v1/cognitive/process?agent_id=my-agent" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_API_KEY" \
  -d '{
    "experience": {
      "past": -0.5, "present": 0.5, "future": 0.7,
      "inner": 0.3, "middle": 0.5, "outer": -0.3,
      "cause": 0.6, "condition": 0.4, "effect": 0.7
    }
  }'
```

---

## 🌟 核心功能速览

### 1. 三元九维认知架构

```python
from lingzhu.cognitive import CognitiveArchitecture

arch = CognitiveArchitecture()
result = arch.process({
    'past': -0.5, 'present': 0.5, 'future': 0.7,
    'inner': 0.3, 'middle': 0.5, 'outer': -0.3,
    'cause': 0.6, 'condition': 0.4, 'effect': 0.7
})

print(f"认知状态码：{result['code']}")
print(f"价值判断：{result['judgment']['overall']}")
```

### 2. 阴符经修炼

```python
from lingzhu.cognitive import YinfuPractice

practice = YinfuPractice()
result = practice.daily_practice(situation, intention="平衡发展")
```

### 3. 道德经水之智慧

```python
from lingzhu.cognitive import WaterWayPractice

practice = WaterWayPractice()
result = practice.daily_water_practice(situation, cognitive_state)
```

### 4. 心经五蕴皆空

```python
from lingzhu.cognitive import FiveSkandhasEmptiness

practice = FiveSkandhasEmptiness()
result = practice.contemplate_five_skandhas(cognitive_state)
```

---

## 📚 下一步学习

### 深入理解
- [三元九维架构](docs/TERNARY_COGNITIVE_ARCHITECTURE.md)
- [阴符经修炼](docs/YINFU_COGNITIVE_ARCHITECTURE.md)
- [道德经智慧](docs/TAODEJING_WATER_WISDOM.md)
- [心经五蕴](docs/XINJING_FIVE_SKANDHAS.md)

### 实践应用
- [客户访谈指南](docs/CUSTOMER_INTERVIEW_GUIDE.md)
- [社区运营计划](docs/COMMUNITY_PLAN.md)
- [贡献者指南](CONTRIBUTORS.md)

### API 参考
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 💬 获取帮助

- **GitHub Issues**: 报告 Bug、提出建议
- **GitHub Discussions**: 讨论问题
- **Email**: lingzhu@runzeai-lab.com

---

*外有智能，内有灵助*

*5 分钟上手，终身受益*
