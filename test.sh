#!/bin/bash

# lingzhu 测试运行脚本

set -e

echo "🧪 开始运行 lingzhu 测试套件..."
echo ""

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}⚠️  未检测到虚拟环境，创建中...${NC}"
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
fi

# 激活虚拟环境
source venv/bin/activate

# 运行基础测试
echo "📋 运行基础测试..."
echo ""
pytest tests/test_main.py -v --tb=short
echo ""

# 运行完整测试
echo "📋 运行完整测试套件..."
echo ""
pytest tests/test_comprehensive.py -v --tb=short
echo ""

# 生成覆盖率报告
echo "📊 生成覆盖率报告..."
echo ""
pytest tests/ -v --cov=src/lingzhu --cov-report=html --cov-report=term-missing

echo ""
echo "✅ 测试完成！"
echo ""
echo "📈 查看覆盖率报告："
echo "   open htmlcov/index.html"
echo ""

# 显示覆盖率摘要
echo "📊 覆盖率摘要："
coverage report --sort=cover
