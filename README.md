# 🏭 industry-research

**给 AI 装上「券商研报生产线」—— 从搜索到上线，一句话搞定行业研究。**

> 从"帮我查查"到"链接发你"，全程 5 分钟，零人工介入。

---
尝鲜：[https://summit-delivers-pharmacies-viking.trycloudflare.com/](https://industry-research-szdr2v9eavarwd8fhj3oxu.streamlit.app/)
## 它能干嘛？

你说一句"帮我研究新能源汽车"，它就自己去：

| 步骤 | 做什么 | 产出 |
|------|--------|------|
| 🔍 搜研报 | 中金、中信、华泰、艾瑞……5-10篇高质量研报自动抓取 | `研报清单_按质量排序.md` |
| 📊 财务分析 | 营收、增速、毛利率、估值、国产替代确定性，三梯队评级 | `企业财务分析.md` |
| ✍️ 写报告 | 3000-5000字深度研报，产业链图谱到投资建议 | `<行业>产业投资全景报告.md` |
| 🎨 渲染网页 | 暖棕+金色投行风格，Hero大标题+卡片布局+移动端适配 | `<行业>产业投资全景报告.html` |
| 🚀 一键上线 | 推到 Cloudflare Pages，全球CDN，微信/浏览器随便打开 | `https://xxx.pages.dev` |

## 为什么不用 PPT？

**PPT 是死的，网页是活的。**

- ❌ PPT → 文件大、手机打不开、微信传不了、没有 SEO
- ✅ HTML → 链接一甩谁都能看，手机电脑都适配，带社交分享标签

## 用法

```bash
# 行业研究一句话启动
/行业研究 新能源汽车

# 带部署
/行业研究 半导体 --deploy

# 指定输出目录
/行业研究 光伏 --out ./my-reports
```

## 传统方式 vs 这个 Skill

| | 传统方式 | industry-research |
|---|---|---|
| ⏱️ 耗时 | 一整天 | 5 分钟 |
| 👥 人数 | 研究员+分析师+设计师 | 1 个人 + AI |
| 📄 格式 | PPT/PDF（死的） | HTML 网页（活的） |
| 📱 移动端 | ❌ | ✅ |
| 🔗 分享 | 传文件 | 甩链接 |
| 🎨 风格 | 各种模板 | 投行级统一配色 |

## 安装

**前置条件：**
- Python 3.x
- Node.js + Wrangler CLI（用于 Cloudflare 部署）

```bash
# 安装 Wrangler（仅部署需要）
npm install -g wrangler

# 登录 Cloudflare（仅部署需要）
wrangler login
```

**安装 Skill：**

```bash
git clone https://github.com/zhangpelf/industry-research.git ~/.claude/skills/industry-research
```

## 依赖 Skills

本 skill 依赖以下外部 skill，使用前请确保已安装：

| Skill | 用途 | 安装方式 |
|-------|------|---------|
| `impeccable` | HTML 视觉渲染（投行风格主题） | `/find-skills impeccable` |
| `websearch` | 网络搜索研报（内置，无需安装） | — |
| `anysearch` | 网络搜索研报（可选，需安装） | `/find-skills anysearch` |

> 💡 如果本地没有 `impeccable`，运行 `/find-skills impeccable` 搜索并安装。

## 文件结构

```
industry-research/
├── README.md              ← 你在这里
├── SKILL.md               ← Skill 主文件（流程定义）
└── scripts/
    └── deploy_cf.sh       ← Cloudflare Pages 一键部署脚本
```

## 输出示例

运行后你会得到：

```
新能源汽车/
├── 研报清单_按质量排序.md
├── 参考文献清单.md
├── 企业财务分析.md
├── 新能源汽车产业投资全景报告.md
└── 新能源汽车产业投资全景报告.html   ← 这个就是最终交付物
```

HTML 特性：
- 🎨 暖棕+金色投行配色
- 📱 响应式布局（手机/平板/桌面）
- 🖨️ 打印友好
- 🏷️ Open Graph 社交分享标签
- 🌐 单文件，无外部依赖

## 部署

```bash
# 一键部署到 Cloudflare Pages
bash scripts/deploy_cf.sh <项目名> <HTML文件所在目录>

# 示例
bash scripts/deploy_cf.sh xinnengyuan-auto ./新能源汽车/
# → https://xinnengyuan-auto.pages.dev
```

## 自定义

修改 `SKILL.md` 可以：
- 调整搜索关键词策略
- 修改报告结构和章节
- 更换 HTML 主题配色（修改 Step 4 的设计系统要求）
- 添加新的分析维度

## License

MIT
