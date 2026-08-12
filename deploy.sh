#!/bin/bash

# lingzhu 快速部署脚本

set -e

echo "🚀 开始部署 lingzhu..."

# 检查 Python 版本
echo "📋 检查 Python 版本..."
python3 --version || {
    echo "❌ 需要 Python 3.10+"
    exit 1
}

# 创建虚拟环境
echo "📦 创建虚拟环境..."
python3 -m venv venv
source venv/bin/activate

# 安装依赖
echo "📥 安装依赖..."
pip install --upgrade pip
pip install -r requirements.txt

# 创建数据目录
echo "📁 创建数据目录..."
mkdir -p data

# 复制环境配置
if [ ! -f .env ]; then
    echo "📝 创建环境配置..."
    cp .env.example .env
    echo "⚠️  请编辑 .env 文件配置环境变量"
fi

# 初始化数据库
echo "🗄️  初始化数据库..."
python3 -c "
from lingzhu.db.database import init_db
import asyncio
asyncio.run(init_db())
print('✅ 数据库初始化完成')
"

# 启动服务
echo "🚀 启动服务..."
echo "访问 API 文档：http://localhost:8000/docs"
echo "访问 Web UI: http://localhost:8000/webui/index.html"
echo ""
echo "按 Ctrl+C 停止服务"
echo ""

uvicorn src.lingzhu.main:app --host 0.0.0.0 --port 8000
