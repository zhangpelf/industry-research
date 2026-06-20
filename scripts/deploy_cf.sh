#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "用法: $0 <项目名> <HTML文件所在目录>"
  echo ""
  echo "示例:"
  echo "  $0 xincailiao-report ./新能源汽车/"
  echo ""
  echo "前置条件:"
  echo "  npm install -g wrangler"
  echo "  wrangler login"
  exit 1
}

[[ $# -lt 2 ]] && usage

PROJECT_NAME="$1"
DEPLOY_DIR="$2"

if ! command -v wrangler &>/dev/null; then
  echo "❌ 未安装 wrangler，请先运行: npm install -g wrangler"
  exit 1
fi

if [[ ! -d "$DEPLOY_DIR" ]]; then
  echo "❌ 目录不存在: $DEPLOY_DIR"
  exit 1
fi

echo "🔍 检查项目是否存在..."
if wrangler pages project list 2>/dev/null | grep -q "$PROJECT_NAME"; then
  echo "📦 项目已存在，直接部署..."
else
  echo "📦 创建新项目: $PROJECT_NAME"
  wrangler pages project create "$PROJECT_NAME" --production-branch=main
fi

echo "🚀 部署中..."
wrangler pages deploy "$DEPLOY_DIR" --project-name="$PROJECT_NAME" --branch=main

echo ""
echo "✅ 部署完成！"
echo "🌐 访问地址: https://${PROJECT_NAME}.pages.dev"
