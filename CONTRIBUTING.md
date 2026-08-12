# Contributing to lingzhu

感谢您对 lingzhu（灵助）项目的关注！我们欢迎任何形式的贡献。

## 如何贡献

### 报告问题
- 使用 GitHub Issues 报告 bug 或功能请求
- 请清楚地描述问题，包括重现步骤和环境信息

### 提交代码
1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交您的更改 (`git commit -m 'feat: add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建一个 Pull Request

### 代码风格
- 遵循 PEP 8 编码规范
- 使用类型注解
- 为所有公共 API 编写文档字符串
- 为新功能添加测试

### 提交信息规范
- `feat:` 新功能
- `fix:` 修复 bug
- `docs:` 文档更新
- `refactor:` 重构
- `test:` 测试相关
- `chore:` 构建/工具链相关

## 开发环境

```bash
# 克隆仓库
git clone https://github.com/runzeai-lab/lingzhu.git
cd lingzhu

# 安装依赖
pip install -r requirements.txt

# 运行测试
pytest tests/
```

## 许可证
通过贡献代码，您同意您的贡献将在 MIT 许可证下发布。
