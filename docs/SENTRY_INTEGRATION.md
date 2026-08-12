# 🔍 Sentry 监控集成指南

**目标**: 集成生产级监控告警系统

---

## 📋 集成步骤

### 1. 创建 Sentry 账号

```bash
# 访问 https://sentry.io
# 注册免费账号
# 创建新项目 (选择 Python + FastAPI)
```

### 2. 安装依赖

```bash
pip install sentry-sdk[fastapi]
```

### 3. 配置 Sentry

```python
# src/lingzhu/main.py 添加:

import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn="YOUR_SENTRY_DSN",
    integrations=[
        FastApiIntegration(),
    ],
    traces_sample_rate=1.0,  # 采样率
    environment=settings.ENVIRONMENT,
    release=f"lingzhu@{settings.APP_VERSION}"
)
```

### 4. 添加环境变量

```bash
# .env 添加:
SENTRY_DSN=https://xxx@xxx.ingest.sentry.io/xxx
SENTRY_ENVIRONMENT=development  # 生产环境改为 production
```

---

## 📊 监控指标

### 错误监控
- ✅ 所有未捕获异常
- ✅ HTTP 5xx 错误
- ✅ 数据库错误
- ✅ 认证失败

### 性能监控
- ⏱️ API 响应时间
- ⏱️ 数据库查询时间
- ⏱️ 认知架构处理时间
- ⏱️ 外部 API 调用时间

### 用户行为
- 👤 活跃用户数
- 👤 错误率 per 用户
- 👤 功能使用频率

---

## 🚨 告警配置

### 错误告警
- **阈值**: >5 个错误/小时
- **渠道**: Email + Slack
- **升级**: >20 个错误/小时 → 电话

### 性能告警
- **阈值**: P95 >2 秒
- **渠道**: Email
- **升级**: P95 >5 秒 → Slack

---

## 📈 仪表板

### 推荐创建
1. **错误概览**: 错误类型分布
2. **性能趋势**: 响应时间趋势
3. **用户影响**: 受影响用户数
4. **版本对比**: 不同版本错误率

---

## 💡 最佳实践

### Do's ✅
- 记录有意义的上下文
- 区分错误严重级别
- 设置合理的告警阈值
- 定期审查 Sentry 数据

### Don'ts ❌
- 不要记录敏感信息
- 不要过度告警
- 不要忽略警告
- 不要在生产环境用高采样率

---

*外有智能，内有灵助*

*生产级监控，保障稳定运行*
