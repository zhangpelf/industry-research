#!/usr/bin/env python3
"""
研报 Markdown → 单文件 HTML 渲染器
用法: python3 render_report.py --input report.md --output report.html --title "标题"
"""

import argparse
import re
import hashlib
from datetime import datetime
from pathlib import Path


def md_to_html(md_text: str) -> str:
    """简易 Markdown → HTML 转换（支持标题、表格、列表、加粗、代码块）。"""
    lines = md_text.split("\n")
    html_parts: list[str] = []
    in_table = False
    in_code = False
    in_list = False
    list_type = ""

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("```"):
            if in_code:
                html_parts.append("</code></pre>")
                in_code = False
            else:
                lang = stripped[3:].strip()
                html_parts.append(f'<pre><code class="lang-{lang}">')
                in_code = True
            continue
        if in_code:
            html_parts.append(line.replace("<", "&lt;").replace(">", "&gt;"))
            continue

        if not stripped:
            if in_list:
                html_parts.append(f"</{list_type}>")
                in_list = False
            if in_table:
                html_parts.append("</tbody></table>")
                in_table = False
            continue

        h_match = re.match(r"^(#{1,6})\s+(.+)$", stripped)
        if h_match:
            level = len(h_match.group(1))
            text = h_match.group(2)
            html_parts.append(f"<h{level}>{inline(text)}</h{level}>")
            continue

        if "|" in stripped and stripped.startswith("|"):
            cells = [c.strip() for c in stripped.split("|")[1:-1]]
            if all(re.match(r"^[-:]+$", c) for c in cells):
                continue
            if not in_table:
                html_parts.append('<table><thead><tr>')
                for c in cells:
                    html_parts.append(f"<th>{inline(c)}</th>")
                html_parts.append("</tr></thead><tbody>")
                in_table = True
            else:
                html_parts.append("<tr>")
                for c in cells:
                    html_parts.append(f"<td>{inline(c)}</td>")
                html_parts.append("</tr>")
            continue

        if re.match(r"^[-*]\s+", stripped):
            text = re.sub(r"^[-*]\s+", "", stripped)
            if not in_list or list_type != "ul":
                if in_list:
                    html_parts.append(f"</{list_type}>")
                html_parts.append("<ul>")
                in_list = True
                list_type = "ul"
            html_parts.append(f"<li>{inline(text)}</li>")
            continue

        ol_match = re.match(r"^\d+[.)]\s+(.+)$", stripped)
        if ol_match:
            text = ol_match.group(1)
            if not in_list or list_type != "ol":
                if in_list:
                    html_parts.append(f"</{list_type}>")
                html_parts.append("<ol>")
                in_list = True
                list_type = "ol"
            html_parts.append(f"<li>{inline(text)}</li>")
            continue

        if stripped.startswith("> "):
            text = stripped[2:]
            html_parts.append(f"<blockquote>{inline(text)}</blockquote>")
            continue

        if re.match(r"^[-*_]{3,}$", stripped):
            html_parts.append("<hr>")
            continue

        if in_list:
            html_parts.append(f"</{list_type}>")
            in_list = False
        html_parts.append(f"<p>{inline(stripped)}</p>")

    if in_table:
        html_parts.append("</tbody></table>")
    if in_list:
        html_parts.append(f"</{list_type}>")

    return "\n".join(html_parts)


def inline(text: str) -> str:
    """行内格式：加粗、行内代码、链接。"""
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
    text = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', text)
    return text


def build_html(title: str, body_html: str, source_path: str) -> str:
    """用模板包裹 HTML body。"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    sha = hashlib.sha256(body_html.encode()).hexdigest()[:12]

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta property="og:title" content="{title}">
<meta property="og:type" content="article">
<meta property="og:locale" content="zh_CN">
<meta name="description" content="{title}">
<meta name="report-source" content="{source_path}">
<meta name="report-sha" content="{sha}">
<meta name="report-generated" content="{now}">
<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>📊</text></svg>">
<style>
  :root {{
    --bg: #f0f2f5;
    --card: #ffffff;
    --text: #1a1f2e;
    --text-secondary: #4a5568;
    --accent: #c5993e;
    --accent-light: #e8d5a8;
    --border: #dde1e7;
    --warm-brown: #5a3f2e;
  }}
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    font-family: -apple-system, "PingFang SC", "SF Pro Display", "Helvetica Neue", "Microsoft YaHei", sans-serif;
    background:
      radial-gradient(ellipse at 30% 0%, rgba(197, 153, 62, 0.18) 0%, transparent 55%),
      radial-gradient(ellipse at 70% 5%, rgba(197, 153, 62, 0.08) 0%, transparent 40%),
      radial-gradient(ellipse at 50% 100%, rgba(74, 53, 42, 0.12) 0%, transparent 50%),
      linear-gradient(165deg, #f4ede0 0%, #ede3d0 25%, #e8dcbf 50%, #f0e6d0 75%, #f4ede0 100%);
    background-attachment: fixed;
    color: var(--text);
    line-height: 1.85;
    font-size: 15px;
    -webkit-font-smoothing: antialiased;
  }}
  .hero {{
    background:
      radial-gradient(ellipse at 20% 10%, rgba(197, 153, 62, 0.25) 0%, transparent 45%),
      linear-gradient(135deg, #2a1f15 0%, #3d2e1f 25%, #4d3b28 45%, #5a4530 65%, #634e38 100%);
    color: #fdf8f0;
    padding: 80px 40px 56px;
    text-align: center;
  }}
  .hero h1 {{ font-size: clamp(28px, 4vw, 42px); font-weight: 800; letter-spacing: -0.02em; margin-bottom: 12px; }}
  .hero .meta {{ font-size: 13px; opacity: 0.7; }}
  .container {{ max-width: 960px; margin: 0 auto; padding: 40px 24px; }}
  h2 {{
    font-size: 22px; font-weight: 700; color: var(--warm-brown);
    margin: 48px 0 20px; padding-bottom: 10px;
    border-bottom: 2px solid var(--accent);
  }}
  h3 {{ font-size: 18px; font-weight: 600; color: var(--text); margin: 32px 0 12px; }}
  h4 {{ font-size: 16px; font-weight: 600; color: var(--text-secondary); margin: 24px 0 8px; }}
  p {{ margin: 12px 0; color: var(--text); }}
  strong {{ color: var(--warm-brown); }}
  table {{
    width: 100%; border-collapse: collapse; margin: 20px 0;
    background: var(--card); border-radius: 8px; overflow: hidden;
    box-shadow: 0 1px 3px rgba(58,42,30,0.08);
  }}
  th {{
    background: var(--warm-brown); color: #fff;
    padding: 12px 16px; text-align: left; font-size: 13px; font-weight: 600;
  }}
  td {{ padding: 10px 16px; border-bottom: 1px solid var(--border); font-size: 14px; }}
  tr:last-child td {{ border-bottom: none; }}
  tr:hover td {{ background: rgba(197,153,62,0.04); }}
  blockquote {{
    border-left: 3px solid var(--accent); margin: 20px 0; padding: 12px 20px;
    background: rgba(197,153,62,0.06); border-radius: 0 8px 8px 0;
    color: var(--text-secondary); font-style: italic;
  }}
  code {{
    background: rgba(197,153,62,0.1); padding: 2px 6px; border-radius: 4px;
    font-size: 13px; font-family: "SF Mono", "Fira Code", monospace;
  }}
  pre {{ background: #1a1f2e; color: #e2e8f0; padding: 20px; border-radius: 8px; overflow-x: auto; margin: 20px 0; }}
  pre code {{ background: none; padding: 0; color: inherit; }}
  ul, ol {{ margin: 12px 0 12px 24px; }}
  li {{ margin: 6px 0; }}
  hr {{ border: none; border-top: 1px solid var(--border); margin: 32px 0; }}
  a {{ color: var(--accent); text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
  @media (max-width: 640px) {{
    .hero {{ padding: 48px 20px 36px; }}
    .container {{ padding: 24px 16px; }}
    table {{ font-size: 13px; }}
    th, td {{ padding: 8px 10px; }}
  }}
  @media print {{
    body {{ background: #fff; }}
    .hero {{ background: #2a1f15; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
    table {{ page-break-inside: avoid; }}
  }}
</style>
</head>
<body>

<header class="hero">
  <h1>{title}</h1>
  <div class="meta">生成时间: {now} | 源文件: {source_path} | SHA: {sha}</div>
</header>

<main class="container">
{body_html}
</main>

<footer style="text-align:center;padding:40px 20px;color:#8895a7;font-size:12px;">
  由 research-report skill 生成 | {now}
</footer>

</body>
</html>'''


def main():
    parser = argparse.ArgumentParser(description="研报 Markdown → HTML 渲染器")
    parser.add_argument("--input", "-i", required=True, help="输入 Markdown 文件")
    parser.add_argument("--output", "-o", help="输出 HTML 文件（默认同名 .html）")
    parser.add_argument("--title", "-t", help="报告标题（默认从文件名推断）")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"错误: 文件不存在 {input_path}")
        return 1

    output_path = Path(args.output) if args.output else input_path.with_suffix(".html")
    title = args.title or input_path.stem.replace("_", " ").replace("-", " ")

    md_text = input_path.read_text(encoding="utf-8")
    body_html = md_to_html(md_text)
    full_html = build_html(title, body_html, str(input_path))

    output_path.write_text(full_html, encoding="utf-8")
    print(f"✅ 已生成: {output_path}")
    print(f"   大小: {output_path.stat().st_size / 1024:.1f} KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
