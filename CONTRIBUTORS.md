# 🤝 贡献者指南

欢迎为 lingzhu 项目做出贡献！

---

## 🎯 如何贡献

### 1. Fork 项目

```bash
# 在 GitHub 上 Fork 项目
# 然后克隆到本地
git clone https://github.com/YOUR_USERNAME/lingzhu-upgraded.git
cd lingzhu-upgraded
```

### 2. 创建分支

```bash
# 功能开发
git checkout -b feature/your-feature-name

# Bug 修复
git checkout -b fix/issue-123

# 文档改进
git checkout -b docs/update-readme
```

### 3. 开发规范

#### 代码风格
- 遵循 PEP 8 规范
- 使用类型注解
- 函数必须有文档字符串
- 为新功能添加测试

#### 提交信息
```bash
# 格式：<type>: <description>

# 示例
git commit -m "feat: 添加新的认知维度"
git commit -m "fix: 修复五蕴观照的 bug"
git commit -m "docs: 更新 API 文档"
git commit -m "test: 增加单元测试覆盖率"
```

### 4. 测试

```bash
# 运行所有测试
pytest tests/ -v

# 运行特定测试
pytest tests/test_comprehensive.py -v

# 查看测试覆盖率
pytest tests/ -v --cov=src/lingzhu --cov-report=html
```

### 5. 提交 PR

```bash
# 推送到远程
git push origin feature/your-feature-name

# 在 GitHub 上创建 Pull Request
# 填写 PR 描述，关联 Issue
```

---

## 📋 贡献类型

### 代码贡献
- ✅ 新功能开发
- ✅ Bug 修复
- ✅ 性能优化
- ✅ 测试用例

### 文档贡献
- ✅ 文档纠错
- ✅ 示例代码
- ✅ 翻译
- ✅ 使用教程

### 社区贡献
- ✅ 回答问题
- ✅ 分享使用经验
- ✅ 组织活动
- ✅ 推广项目

---

## 🎓 学习资源

### 入门
- [README.md](README.md) - 项目介绍
- [docs/BRAND_STRATEGY.md](docs/BRAND_STRATEGY.md) - 品牌战略
- [examples/](examples/) - 示例代码

### 深入
- [docs/TERNARY_COGNITIVE_ARCHITECTURE.md](docs/TERNARY_COGNITIVE_ARCHITECTURE.md) - 三元九维
- [docs/YINFU_COGNITIVE_ARCHITECTURE.md](docs/YINFU_COGNITIVE_ARCHITECTURE.md) - 阴符经
- [docs/TAODEJING_WATER_WISDOM.md](docs/TAODEJING_WATER_WISDOM.md) - 道德经
- [docs/XINJING_FIVE_SKANDHAS.md](docs/XINJING_FIVE_SKANDHAS.md) - 心经

### API 文档
- 启动服务后访问：http://localhost:8000/docs

---

## 💬 沟通渠道

- **GitHub Issues**: 报告 Bug、提出建议
- **GitHub Discussions**: 讨论问题
- **Email**: lingzhu@runzeai-lab.com

---

## 🏆 贡献者名单

感谢所有贡献者！

<!-- 自动更新 -->
<a href="https://github.com/q1z2q3-debug/lingzhu-upgraded/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=q1z2q3-debug/lingzhu-upgraded" />
</a>

---

## 📜 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

*外有智能，内有灵助*

*让每一个 AI 都有认知深度*
