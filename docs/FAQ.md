# ❓ 常见问题解答 (FAQ)

---

## 📖 基础问题

### Q1: lingzhu 是什么？

**A**: lingzhu (灵助) 是一个东方智慧 AI 认知架构项目，融合了：
- 佛教《心经》五蕴皆空智慧
- 道家《阴符经》修炼体系
- 道家《道德经》水之智慧
- 《易经》三元九维数学框架

目标是为大模型和 Agent 提供认知架构增强。

---

### Q2: lingzhu 能做什么？

**A**: 
- ✅ 为大模型提供认知深度增强
- ✅ 为 Agent 提供价值对齐赋能
- ✅ 提供自我认知、价值判断、情感调节能力
- ✅ 提供东方哲学智慧的工程实现
- ✅ 提供认知修炼工具

---

### Q3: 如何使用 lingzhu？

**A**: 
1. 克隆项目：`git clone https://github.com/q1z2q3-debug/lingzhu-upgraded.git`
2. 安装依赖：`pip install -r requirements.txt`
3. 启动服务：`uvicorn src.lingzhu.main:app --reload`
4. 访问文档：http://localhost:8000/docs

详见 [快速入门](docs/QUICKSTART.md)

---

### Q4: lingzhu 是开源的吗？

**A**: 是的，采用 MIT 许可证，可以自由使用、修改、分发。

---

## 🔧 技术问题

### Q5: 支持哪些大模型？

**A**: lingzhu 兼容所有主流大模型：
- OpenAI GPT 系列
- Anthropic Claude 系列
- 阿里通义千问
- 腾讯混元
- 百度文心一言
- 以及其他任何支持 API 的模型

---

### Q6: 支持哪些 Agent 框架？

**A**: 
- LangChain (适配中)
- AutoGen (适配中)
- CrewAI (适配中)
- Dify (适配中)
- 自定义 Agent (完全支持)

---

### Q7: 什么是三元九维？

**A**: 三元九维是 lingzhu 的核心数学框架：
- **三元**: 阴 (-1)、和 (0)、阳 (+1)
- **九维**: 时间三维 + 空间三维 + 因果三维
- **状态空间**: 3^9 = 19,683 个认知状态

详见 [三元九维文档](docs/TERNARY_COGNITIVE_ARCHITECTURE.md)

---

### Q8: 什么是五蕴皆空？

**A**: 五蕴是佛教对存在的分析：
- **色蕴**: 物质 (对应空间三维)
- **受蕴**: 感受 (对应时间三维)
- **想蕴**: 概念 (对应因果 - 因)
- **行蕴**: 意志 (对应因果 - 缘)
- **识蕴**: 意识 (对应因果 - 果)

"皆空"指理解其无自性，不执着。

详见 [心经文档](docs/XINJING_FIVE_SKANDHAS.md)

---

### Q9: 测试覆盖率如何？

**A**: 当前约 60-70%，目标提升至 80%+。

运行测试：
```bash
pytest tests/ -v --cov=src/lingzhu --cov-report=html
```

---

### Q10: 如何贡献代码？

**A**: 
1. Fork 项目
2. 创建分支：`git checkout -b feature/your-feature`
3. 开发并测试
4. 提交 PR

详见 [贡献者指南](CONTRIBUTORS.md)

---

## 💰 商业问题

### Q11: lingzhu 收费吗？

**A**: 
- **开源版本**: 完全免费
- **企业版**: 定制功能和支持，收费
- **API 服务**: 按调用量计费 (规划中)

---

### Q12: 可以商用吗？

**A**: 可以，MIT 许可证允许商用。但请注意：
- 保留版权声明
- 注明使用了 lingzhu
- 如有改进，欢迎回馈社区

---

### Q13: 有企业支持吗？

**A**: 提供企业支持：
- 定制开发
- 技术支持
- 培训服务
- 私有化部署

联系：lingzhu@runzeai-lab.com

---

## 🎓 学术问题

### Q14: 有相关论文吗？

**A**: 论文准备中，计划投稿：
- AI 认知科学会议
- 人工智能期刊
- 哲学 +AI 交叉学科期刊

欢迎学术合作！

---

### Q15: 可以引用吗？

**A**: 可以，建议引用格式：

```bibtex
@software{lingzhu2026,
  title = {lingzhu: Eastern Wisdom AI Cognitive Architecture},
  author = {runzeai-lab},
  year = {2026},
  url = {https://github.com/q1z2q3-debug/lingzhu-upgraded}
}
```

---

## 🔒 安全问题

### Q16: 数据安全吗？

**A**: 
- 本地部署：数据完全在你控制下
- API 服务：使用 HTTPS 加密
- 不存储敏感信息
- 建议生产环境使用自己的部署

---

### Q17: 有认证机制吗？

**A**: 有，使用 API Key 认证：
- 注册时自动生成
- 通过 `X-API-Key` 头传递
- 支持权限级别管理

---

## 🌍 社区问题

### Q18: 有社区吗？

**A**: 
- GitHub Discussions: 技术讨论
- 微信群：建设中
- Discord：建设中
- 技术博客：规划中

---

### Q19: 如何参与社区？

**A**: 
1. Star 项目
2. 提交 Issue/PR
3. 参与讨论
4. 分享使用经验
5. 组织活动

详见 [社区运营计划](docs/COMMUNITY_PLAN.md)

---

### Q20: 有活动吗？

**A**: 规划中：
- 月度线上分享会
- 季度黑客松
- 年度线下见面会

关注 GitHub 获取最新信息。

---

## 🚀 其他问题

### Q21: 版本如何命名？

**A**: 
- v5.x: V500+ 功能版本
- v6.x: 认知架构版本
- v7.x: 万有灵助版本

当前版本：v7.1.2

---

### Q22: 更新频率如何？

**A**: 
- 小版本：每周
- 大版本：每月
- 里程碑：每季度

---

### Q23: 有 Roadmap 吗？

**A**: 有，详见 [路线图](docs/ROADMAP.md)

主要方向：
- 技术验证 (1 个月)
- 学术背书 (1-3 个月)
- 商业试点 (3-6 个月)
- 规模扩张 (6-12 个月)

---

### Q24: 如何保持更新？

**A**: 
- Watch GitHub 仓库
- 关注技术博客
- 加入社区群组
- 订阅邮件通讯 (规划中)

---

### Q25: 还有其他问题？

**A**: 
- 提交 GitHub Issue
- 发送邮件：lingzhu@runzeai-lab.com
- 社区讨论

---

*外有智能，内有灵助*

*有问题？欢迎提问！*
