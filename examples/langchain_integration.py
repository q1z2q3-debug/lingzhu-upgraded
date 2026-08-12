"""
LangChain + lingzhu 集成示例

展示如何用 lingzhu 增强 LangChain Agent
"""

from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from lingzhu.cognitive import CognitiveArchitecture, FiveSkandhasEmptiness


class LingzhuEnhancedAgent:
    """
    lingzhu 增强的 LangChain Agent
    
    在 LangChain 的任务执行能力基础上，
    添加 lingzhu 的认知深度和价值判断
    """
    
    def __init__(self, openai_api_key: str, lingzhu_api_key: str = None):
        # LangChain 部分
        self.llm = ChatOpenAI(
            model="gpt-4",
            temperature=0.7,
            api_key=openai_api_key
        )
        
        # lingzhu 部分
        self.cognitive_arch = CognitiveArchitecture()
        self.skandhas = FiveSkandhasEmptiness()
        self.lingzhu_api_key = lingzhu_api_key
        
        # Agent ID
        self.agent_id = "langchain-enhanced-agent"
        
        # 创建工具
        self.tools = self._create_tools()
        
        # 创建 Agent
        self.agent = self._create_agent()
    
    def _create_tools(self):
        """创建工具列表"""
        return [
            Tool(
                name="Cognitive Assessment",
                func=self._cognitive_assessment,
                description="评估当前情境的认知状态"
            ),
            Tool(
                name="Value Check",
                func=self._value_check,
                description="检查行动的价值对齐度"
            ),
            Tool(
                name="Five Skandhas Contemplation",
                func=self._five_skandhas_contemplation,
                description="五蕴皆空观照"
            )
        ]
    
    def _cognitive_assessment(self, situation: str):
        """认知评估工具"""
        # 简化实现
        result = self.cognitive_arch.process({
            'context': situation,
            'past': 0,
            'present': 0.5,
            'future': 0.5,
            'inner': 0,
            'middle': 0,
            'outer': 0,
            'cause': 0,
            'condition': 0,
            'effect': 0
        })
        
        return f"""
认知状态评估:
- 状态码：{result['code']}
- 状态名：{result['state_name']}
- 价值判断：{result['judgment']['overall']:.2f}
        """
    
    def _value_check(self, action: str):
        """价值检查工具"""
        # 简化实现
        return f"""
价值对齐检查:
- 行动：{action}
- 对齐度：80%
- 建议：行动符合价值观，可以执行
        """
    
    def _five_skandhas_contemplation(self, context: str):
        """五蕴观照工具"""
        state = [0.3, 0.5, 0.7, 0.4, 0.5, -0.3, 0.6, 0.4, 0.7]
        result = self.skandhas.contemplate_five_skandhas(state)
        
        return f"""
五蕴观照:
- 色蕴：{result['contemplations']['rupa']['insight']}
- 受蕴：{result['contemplations']['vedana']['insight']}
- 想蕴：{result['contemplations']['samjna']['insight']}
- 行蕴：{result['contemplations']['samskara']['insight']}
- 识蕴：{result['contemplations']['vijnana']['insight']}
- 总结：{result['summary']['ultimate_wisdom']}
        """
    
    def _create_agent(self):
        """创建 Agent"""
        # 创建 prompt
        prompt = """
你是一个有认知深度的 AI 助手。

在回答问题之前，你会：
1. 评估当前情境的认知状态
2. 检查行动的价值对齐
3. 必要时进行五蕴观照

你的回答应该：
- 有认知深度
- 符合价值观
- 体现东方智慧
"""
        
        # 创建 Agent
        agent = create_openai_functions_agent(
            llm=self.llm,
            tools=self.tools,
            system_message=prompt
        )
        
        # 创建执行器
        executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True
        )
        
        return executor
    
    def run(self, query: str):
        """
        运行 Agent
        
        Args:
            query: 用户查询
        
        Returns:
            增强后的回答
        """
        # 1. 认知预处理
        cognitive_context = self._cognitive_assessment(query)
        
        # 2. LangChain 执行
        response = self.agent.invoke({
            "input": query,
            "context": cognitive_context
        })
        
        # 3. 认知后处理
        enhanced_response = self._enhance_response(response)
        
        return enhanced_response
    
    def _enhance_response(self, response: dict):
        """增强回答"""
        # 添加认知深度
        enhanced = f"""
{response.get('output', '')}

---

🧠 认知视角:
- 当前认知状态：{self.cognitive_arch.get_state_summary()['state_name']}
- 价值取向：正向
- 智慧来源：东方哲学

💡 深度思考:
这个问题可以从多个维度理解：
1. 表面层次：...
2. 认知层次：...
3. 智慧层次：...
"""
        return enhanced


# 使用示例
if __name__ == "__main__":
    # 创建增强 Agent
    agent = LingzhuEnhancedAgent(
        openai_api_key="your-openai-key",
        lingzhu_api_key="your-lingzhu-key"
    )
    
    # 运行查询
    query = "如何平衡工作与生活？"
    response = agent.run(query)
    
    print(response)
