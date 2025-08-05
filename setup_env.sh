#!/bin/bash

# ========================
# 环境初始化脚本
# 作用: 创建虚拟环境并安装所有依赖
# ========================

# 1. 检查 Python3
if ! command -v python3 &> /dev/null
then
    echo "❌ Python3 未安装，请先安装 Python3"
    exit 1
fi

# 2. 创建虚拟环境
echo "🔧 创建 Python 虚拟环境..."
python3 -m venv venv

# 3. 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 4. 升级 pip
echo "🔧 升级 pip..."
pip install --upgrade pip

# 5. 生成 requirements.txt
echo "🔧 创建 requirements.txt..."
cat <<EOF > requirements.txt
javalang
GitPython
langchain
langchain-openai
pydantic
openai
EOF

# 6. 安装依赖
echo "🔧 安装 Python 包..."
pip install -r requirements.txt

# 7. 提示设置 OpenAI Key
echo ""
echo "=============================="
echo "✅ 环境准备完成!"
echo "请设置 OpenAI API Key:"
echo "export OPENAI_API_KEY=\"你的API密钥\""
echo "=============================="
