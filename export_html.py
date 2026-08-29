#!/usr/bin/env python3
"""
OpenCode & OpenWork Asset Dashboard Generator
애플(Apple.com) 스타일의 프리미엄 미니멀리즘 디자인 대시보드를 생성합니다.
- SF Pro / Apple Human Interface Guidelines 스타일 타이포그래피 & 라운딩
- 글래스모피즘(Glassmorphism) 블러 내비게이션 바 & 세그먼트 컨트롤 탭
- 13개 세부 카테고리 & 다크/라이트 테마 원클릭 전환
- macOS 스타일 코드 프리뷰어 (트래픽 라이트 인디케이터 포함)
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INDEX_FILE = BASE_DIR / "assets_index.json"
COLLECTED_DIR = BASE_DIR / "collected_assets"
HTML_OUTPUT = BASE_DIR / "index.html"

# 세부 카테고리 정의 (ID, 라벨, UI pill 색상)
CATEGORY_DEFS = [
    ("all", "전체", "pill-blue"),
    ("rag_search", "🔍 RAG & 시맨틱 검색", "pill-blue"),
    ("llm_ai", "🧠 LLM & AI 개발", "pill-purple"),
    ("frontend", "🎨 프론트엔드 & UI/UX", "pill-teal"),
    ("backend", "⚙️ 백엔드 & API", "pill-green"),
    ("database", "🗄️ DB & 데이터", "pill-amber"),
    ("devops", "☁️ DevOps & 클라우드", "pill-blue"),
    ("security", "🛡️ 보안 & 취약점", "pill-red"),
    ("testing", "🧪 테스트 & QA", "pill-green"),
    ("architecture", "🏗️ 아키텍처 & 리뷰", "pill-purple"),
    ("mobile_sys", "📱 모바일 & 시스템", "pill-teal"),
    ("general_dev", "💻 일반 언어 & 도구", "pill-blue"),
    ("workflow", "⚡ 워크플로우 커맨드", "pill-purple"),
    ("agent", "🤖 자율 에이전트", "pill-green"),
]


def classify_category(name: str, desc: str, asset_type: str) -> tuple:
    text = (name + " " + desc).lower()

    if asset_type == "command":
        return "workflow", "⚡ 워크플로우 커맨드"

    if asset_type == "agent":
        return "agent", "🤖 자율 에이전트"

    # 1. RAG & 시맨틱 검색
    if any(k in text for k in ["rag", "embedding", "vector", "retrieval", "semantic search", "hybrid search", "similarity search", "index-tuning", "chunking", "re-ranking", "rerank", "contextual retrieval"]):
        return "rag_search", "🔍 RAG & 시맨틱 검색"

    # 2. LLM & AI 엔지니어링 / 프롬프트
    if any(k in text for k in ["fine-tuning", "fine_tuning", "finetune", "prompt-engineer", "prompt", "llm", "nlp", "mcp-", "mcp developer", "agent-creator", "skill-creator", "model-selection", "langchain", "llamaindex", "ai-engineer", "token-optim", "few-shot"]):
        return "llm_ai", "🧠 LLM & AI 개발"

    # 3. 보안 & 취약점 분석
    if any(k in text for k in ["security", "auth", "vulnerability", "xss", "injection", "privilege", "exploit", "metasploit", "penetration", "secret", "crypto", "compliance", "guardian", "cors", "csrf", "oauth", "jwt", "sanitization"]):
        return "security", "🛡️ 보안 & 취약점"

    # 4. 테스팅, 검증 & QA
    if any(k in text for k in ["test", "testing", "tdd", "pytest", "jest", "mock", "benchmark", "qa", "verification", "fuzzing", "coverage", "e2e", "cypress", "playwright"]):
        return "testing", "🧪 테스트 & QA"

    # 5. 프론트엔드 & UI/UX
    if any(k in text for k in ["react", "next.js", "nextjs", "vue", "nuxt", "svelte", "tailwind", "css", "html", "ui", "ux", "frontend", "front-end", "web-design", "astro", "solidjs", "accessibility", "wcag", "canvas", "svg", "animation"]):
        return "frontend", "🎨 프론트엔드 & UI/UX"

    # 6. 백엔드 & API 개발
    if any(k in text for k in ["fastapi", "django", "flask", "express", "nestjs", "spring", "spring boot", "springboot", "api-design", "graphql", "rest", "backend", "grpc", "websocket", "http", "routing", "controller", "middleware"]):
        return "backend", "⚙️ 백엔드 & API"

    # 7. 데이터베이스 & 데이터 엔지니어링
    if any(k in text for k in ["sql", "postgres", "postgresql", "mysql", "mongodb", "redis", "sqlite", "database", "orm", "prisma", "query", "recsys", "data-tables", "storage-blob", "etl", "analytics", "data warehouse", "schema", "migration"]):
        return "database", "🗄️ DB & 데이터"

    # 8. DevOps, 클라우드 & 인프라
    if any(k in text for k in ["docker", "kubernetes", "k8s", "terraform", "aws", "azure", "gcp", "cloudflare", "ci-cd", "cicd", "devops", "sre", "infra", "chaos", "prometheus", "monitoring", "deployment", "serverless", "helm", "ansible"]):
        return "devops", "☁️ DevOps & 클라우드"

    # 9. 모바일 & 시스템 프로그래밍
    if any(k in text for k in ["ios", "swift", "swiftui", "android", "kotlin", "flutter", "react-native", "embedded", "c++", "cpp", "rust", "linux", "windows", "wasm", "webassembly", "kernel", "driver"]):
        return "mobile_sys", "📱 모바일 & 시스템"

    # 10. 아키텍처 & 코드 리뷰
    if any(k in text for k in ["review", "reviewer", "architect", "refactor", "pattern", "clean code", "spec", "document", "documentation", "audit", "optimization", "analysis", "solid", "dry", "kiss", "design pattern"]):
        return "architecture", "🏗️ 아키텍처 & 리뷰"

    # 11. 일반 언어 & 유틸리티 (기타)
    return "general_dev", "💻 일반 언어 & 도구"


def esc(s: str) -> str:
    """HTML에서 안전하게 사용할 수 있도록 특수문자 이스케이프"""
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;")
             .replace('"', "&quot;")
             .replace("'", "&#39;"))


def generate_dashboard():
    if not INDEX_FILE.exists():
        print("❌ assets_index.json 없음. 먼저 `python3 skill_collector.py sync`를 실행하세요.")
        return

    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 커스텀 RAG 스킬 포함
    custom_rag = BASE_DIR / "rag-search-optimizer" / "SKILL.md"
    if custom_rag.exists() and "rag-search-optimizer" not in data.get("skills", {}):
        data.setdefault("skills", {})["rag-search-optimizer"] = {
            "name": "rag-search-optimizer",
            "type": "skill",
            "description": "RAG(Retrieval-Augmented Generation) 시스템의 검색 정확도 향상, 하이브리드 검색, 리랭킹, 청킹 전략, Contextual Retrieval 등 검색 파이프라인 최적화",
            "source_repo": "local/custom",
            "source_name": "local-custom",
            "path": "rag-search-optimizer"
        }

    raw_cards = []
    cat_counts = {}

    for item_type, items in [("skill", data.get("skills", {})),
                             ("command", data.get("commands", {})),
                             ("agent", data.get("agents", {}))]:
        for key, item in items.items():
            name = item.get("name", key)
            desc = item.get("description", "")
            src = item.get("source_name", "local")
            rel = item.get("path", "")

            content = ""
            fp = BASE_DIR / rel
            if fp.is_dir():
                sm = fp / "SKILL.md"
                if sm.exists():
                    content = sm.read_text(encoding="utf-8", errors="ignore")[:8000]
            elif fp.is_file():
                content = fp.read_text(encoding="utf-8", errors="ignore")[:8000]

            cat_id, cat_label = classify_category(name, desc, item_type)
            cat_counts[cat_id] = cat_counts.get(cat_id, 0) + 1

            repo_url = item.get("source_repo", "")
            if repo_url.endswith(".git"):
                repo_url = repo_url[:-4]

            raw_cards.append({
                "id": key,
                "name": name,
                "type": item_type,
                "cat_id": cat_id,
                "cat_label": cat_label,
                "desc": desc,
                "source": src,
                "repo_url": repo_url,
                "content": content,
                "install": f"python3 skill_collector.py install {key} --target global",
            })

    # </script> 가 content 안에 있으면 브라우저가 스크립트 태그를 조기 종료함
    # → </ 를 <\/ 로 이스케이프하여 안전하게 주입
    js_data = json.dumps(raw_cards, ensure_ascii=False)
    js_data = js_data.replace("</", "<\\/")

    total = len(raw_cards)

    # 퀵 필터 알약(Pills) 동적 생성 (전체 제외)
    pills_html = ""
    for cid, clabel, ccolor in CATEGORY_DEFS:
        if cid == "all":
            continue
        count = cat_counts.get(cid, 0)
        if count > 0:
            pills_html += f'<button class="pill {ccolor}" onclick="setTab(\'{cid}\')">{clabel} <span class="pill-count">{count}</span></button>\n'

    # 상단 탭(Tabs) 동적 생성
    tabs_html = f'<button class="tab-btn active" data-cat="all" onclick="setTab(\'all\')">전체 <span class="tab-count">{total}</span></button>\n'
    for cid, clabel, _ in CATEGORY_DEFS:
        if cid == "all":
            continue
        count = cat_counts.get(cid, 0)
        if count > 0:
            tabs_html += f'<button class="tab-btn" data-cat="{cid}" onclick="setTab(\'{cid}\')">{clabel} <span class="tab-count">{count}</span></button>\n'

    html = f"""<!DOCTYPE html>
<html lang="ko" data-theme="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>OpenCode &amp; OpenWork Hub</title>
<style>
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

/* ── Apple Dark Theme (Default) ─────────────────────────── */
:root {{
  --bg: #000000;
  --bg-secondary: #121212;
  --card-bg: #1c1c1e;
  --card-hover: #2c2c2e;
  --nav-bg: rgba(0, 0, 0, 0.8);
  --border: rgba(255, 255, 255, 0.1);
  --border-subtle: rgba(255, 255, 255, 0.06);
  --text: #f5f5f7;
  --text-muted: #86868b;
  --text-secondary: #a1a1a6;
  --apple-blue: #2997ff;
  --apple-blue-hover: #0077ed;
  --apple-blue-dim: rgba(41, 151, 255, 0.12);
  --apple-blue-border: rgba(41, 151, 255, 0.3);
  --purple: #bf5af2;
  --purple-dim: rgba(191, 90, 242, 0.12);
  --green: #30d158;
  --green-dim: rgba(48, 209, 88, 0.12);
  --amber: #ffd60a;
  --amber-dim: rgba(255, 214, 10, 0.12);
  --red: #ff453a;
  --red-dim: rgba(255, 69, 58, 0.12);
  --teal: #64d2ff;
  --teal-dim: rgba(100, 210, 255, 0.12);
  --card-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
  --card-shadow-hover: 0 16px 36px rgba(0, 0, 0, 0.6);
  --segment-bg: rgba(120, 120, 128, 0.24);
  --segment-active: #2c2c2e;
  --modal-overlay: rgba(0, 0, 0, 0.7);
  --code-bg: #141416;
}}

/* ── Apple Light Theme ──────────────────────────────────── */
[data-theme="light"] {{
  --bg: #f5f5f7;
  --bg-secondary: #ffffff;
  --card-bg: #ffffff;
  --card-hover: #ffffff;
  --nav-bg: rgba(245, 245, 247, 0.8);
  --border: rgba(0, 0, 0, 0.08);
  --border-subtle: rgba(0, 0, 0, 0.04);
  --text: #1d1d1f;
  --text-muted: #86868b;
  --text-secondary: #515154;
  --apple-blue: #0071e3;
  --apple-blue-hover: #0077ed;
  --apple-blue-dim: rgba(0, 113, 227, 0.08);
  --apple-blue-border: rgba(0, 113, 227, 0.2);
  --purple: #9b51e0;
  --purple-dim: rgba(155, 81, 224, 0.08);
  --green: #28cd41;
  --green-dim: rgba(40, 205, 65, 0.08);
  --amber: #f5a623;
  --amber-dim: rgba(245, 166, 35, 0.08);
  --red: #ff3b30;
  --red-dim: rgba(255, 59, 48, 0.08);
  --teal: #00a0dc;
  --teal-dim: rgba(0, 160, 220, 0.08);
  --card-shadow: 0 4px 18px rgba(0, 0, 0, 0.04);
  --card-shadow-hover: 0 16px 36px rgba(0, 0, 0, 0.08);
  --segment-bg: rgba(118, 118, 128, 0.12);
  --segment-active: #ffffff;
  --modal-overlay: rgba(0, 0, 0, 0.4);
  --code-bg: #1d1d1f;
}}

html {{ scroll-behavior: smooth; }}
body {{
  background: var(--bg);
  color: var(--text);
  font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Helvetica Neue", Arial, sans-serif;
  font-size: 14px;
  line-height: 1.5;
  min-height: 100vh;
  letter-spacing: -0.015em;
  -webkit-font-smoothing: antialiased;
  transition: background-color .3s ease, color .3s ease;
}}

/* ── Scrollbar ─────────────────────────────────────────── */
::-webkit-scrollbar {{ width: 6px; height: 6px; }}
::-webkit-scrollbar-track {{ background: transparent; }}
::-webkit-scrollbar-thumb {{ background: var(--border); border-radius: 980px; }}

/* ── Apple Global Navigation ────────────────────────────── */
.header {{
  position: sticky; top: 0; z-index: 100;
  background: var(--nav-bg);
  backdrop-filter: saturate(180%) blur(20px);
  -webkit-backdrop-filter: saturate(180%) blur(20px);
  border-bottom: 1px solid var(--border);
  padding: 0 28px;
  height: 52px;
  display: flex; align-items: center; justify-content: space-between; gap: 20px;
  transition: all .3s ease;
}}
.header-logo {{
  display: flex; align-items: center; gap: 10px;
  text-decoration: none; color: var(--text);
  font-weight: 600; font-size: 15px; letter-spacing: -0.02em;
}}
.logo-badge {{
  width: 28px; height: 28px; border-radius: 7px;
  background: linear-gradient(135deg, #0071e3, #64d2ff);
  display: flex; align-items: center; justify-content: center;
  font-size: 14px; color: white;
  box-shadow: 0 2px 8px rgba(0, 113, 227, 0.4);
}}
.logo-title {{ font-weight: 600; }}
.logo-subtitle {{ font-size: 11px; color: var(--text-muted); font-weight: 400; }}

/* ── Search Bar (Apple Pill Style) ─────────────────────── */
.search-wrap {{ flex: 1; max-width: 420px; position: relative; }}
.search-input {{
  width: 100%;
  background: var(--segment-bg);
  border: 1px solid transparent;
  color: var(--text);
  border-radius: 980px;
  padding: 7px 14px 7px 34px;
  font-size: 13px;
  outline: none;
  font-family: inherit;
  letter-spacing: -0.01em;
  transition: all .2s ease;
}}
.search-input::placeholder {{ color: var(--text-muted); }}
.search-input:focus {{
  background: var(--card-bg);
  border-color: var(--apple-blue);
  box-shadow: 0 0 0 3px var(--apple-blue-dim);
}}
.search-icon {{
  position: absolute; left: 11px; top: 50%; transform: translateY(-50%);
  color: var(--text-muted); font-size: 13px; pointer-events: none;
}}

/* ── Header Actions (Apple Capsule Buttons) ─────────────── */
.header-actions {{ display: flex; gap: 10px; align-items: center; }}
.btn-apple {{
  background: var(--segment-bg);
  border: 1px solid transparent;
  color: var(--text);
  border-radius: 980px;
  padding: 6px 14px;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-family: inherit;
  transition: all .2s ease;
  user-select: none;
}}
.btn-apple:hover {{
  background: var(--card-hover);
  border-color: var(--border);
}}
.btn-primary {{
  background: var(--apple-blue);
  color: #ffffff;
  border-radius: 980px;
  padding: 6px 14px;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  border: none;
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-family: inherit;
  transition: background-color .2s ease, transform .1s ease;
}}
.btn-primary:hover {{
  background: var(--apple-blue-hover);
  transform: scale(1.02);
}}
.header-stat {{ text-align: right; flex-shrink: 0; }}
.header-stat small {{ display: block; font-size: 10px; color: var(--text-muted); font-weight: 500; }}
.header-stat strong {{ font-size: 15px; font-weight: 700; color: var(--apple-blue); }}

/* ── Hero Section (Apple Keynote Style) ─────────────────── */
.hero {{
  padding: 56px 28px 24px;
  text-align: center;
  background: radial-gradient(circle at 50% 0%, var(--apple-blue-dim) 0%, transparent 60%);
}}
.hero-eyebrow {{
  font-size: 13px;
  font-weight: 600;
  color: var(--apple-blue);
  letter-spacing: 0.08em;
  text-transform: uppercase;
  margin-bottom: 8px;
}}
.hero h1 {{
  font-size: 40px;
  font-weight: 700;
  letter-spacing: -0.035em;
  line-height: 1.15;
  margin-bottom: 12px;
  color: var(--text);
}}
.hero p {{
  font-size: 17px;
  color: var(--text-secondary);
  max-width: 640px;
  margin: 0 auto 28px;
  line-height: 1.5;
  letter-spacing: -0.015em;
}}

/* ── Quick Pills (Capsule Tags) ──────────────────────────── */
.stat-pills {{
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
  max-width: 1440px;
  margin: 0 auto 28px;
}}
.pill {{
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 18px;
  border-radius: 980px;
  font-size: 13px;
  font-weight: 500;
  white-space: nowrap;
  word-break: keep-all;
  cursor: pointer;
  border: 1px solid transparent;
  background: var(--card-bg);
  color: var(--text);
  box-shadow: var(--card-shadow);
  transition: all .2s ease;
  font-family: inherit;
}}
.pill:hover {{
  transform: translateY(-2px);
  border-color: var(--apple-blue-border);
}}
.pill-count {{
  font-size: 11px;
  font-weight: 600;
  opacity: 0.7;
}}
.pill-blue   {{ background: var(--apple-blue-dim); color: var(--apple-blue); border-color: var(--apple-blue-border); }}
.pill-purple {{ background: var(--purple-dim); color: var(--purple); border-color: rgba(191, 90, 242, 0.25); }}
.pill-green  {{ background: var(--green-dim); color: var(--green); border-color: rgba(48, 209, 88, 0.25); }}
.pill-amber  {{ background: var(--amber-dim); color: var(--amber); border-color: rgba(255, 214, 10, 0.25); }}
.pill-teal   {{ background: var(--teal-dim); color: var(--teal); border-color: rgba(100, 210, 255, 0.25); }}
.pill-red    {{ background: var(--red-dim); color: var(--red); border-color: rgba(255, 69, 58, 0.25); }}

/* ── Segmented Tabs Bar (Apple macOS / iOS Style) ───────── */
.tabs-container {{
  max-width: 1520px;
  margin: 0 auto;
  padding: 0 28px;
}}
.tabs {{
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 8px;
  padding: 8px 12px;
  background: var(--segment-bg);
  border-radius: 18px;
}}
.tab-btn {{
  flex-shrink: 0;
  padding: 8px 18px;
  border-radius: 980px;
  border: none;
  background: transparent;
  color: var(--text-muted);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  font-family: inherit;
  letter-spacing: -0.01em;
  transition: all .2s cubic-bezier(0.16, 1, 0.3, 1);
  white-space: nowrap;
  word-break: keep-all;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}}
.tab-btn:hover {{ color: var(--text); }}
.tab-btn.active {{
  background: var(--segment-active);
  color: var(--text);
  font-weight: 600;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.12);
}}
.tab-count {{
  font-size: 11px;
  opacity: 0.65;
  font-weight: 600;
}}

/* ── Main Layout ─────────────────────────────────────────── */
.main {{
  max-width: 1520px;
  margin: 0 auto;
  padding: 32px 28px 80px;
}}
.results-bar {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
}}
.results-bar p {{
  font-size: 13px;
  color: var(--text-muted);
  font-weight: 500;
}}
.results-bar span {{
  color: var(--text);
  font-weight: 700;
}}

/* ── Card Grid (Apple Product Bento Style) ───────────────── */
.grid {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
}}
.card {{
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 22px;
  cursor: pointer;
  transition: transform .25s cubic-bezier(0.16, 1, 0.3, 1), box-shadow .25s ease, border-color .25s ease;
  display: flex;
  flex-direction: column;
  gap: 12px;
  box-shadow: var(--card-shadow);
  position: relative;
  overflow: hidden;
}}
.card:hover {{
  transform: translateY(-4px) scale(1.008);
  box-shadow: var(--card-shadow-hover);
  border-color: var(--apple-blue-border);
}}
.card.rag-highlight {{
  border-color: var(--apple-blue-border);
  background: linear-gradient(180deg, var(--card-bg) 0%, var(--apple-blue-dim) 100%);
}}

.card-badges {{
  display: flex;
  align-items: center;
  gap: 8px;
}}
.badge {{
  display: inline-block;
  padding: 3px 10px;
  border-radius: 980px;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.02em;
}}
.badge-skill   {{ background: var(--apple-blue-dim); color: var(--apple-blue); }}
.badge-command {{ background: var(--purple-dim); color: var(--purple); }}
.badge-src {{
  color: var(--text-muted);
  font-size: 11px;
  font-weight: 400;
  margin-left: auto;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 140px;
}}
.badge-src-link {{
  color: var(--text-muted);
  font-size: 11px;
  font-weight: 500;
  margin-left: auto;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 160px;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 3px 10px;
  border-radius: 980px;
  background: var(--segment-bg);
  transition: all .2s ease;
}}
.badge-src-link:hover {{
  color: var(--apple-blue);
  background: var(--apple-blue-dim);
  border-color: var(--apple-blue-border);
  transform: translateY(-1px);
}}

.card-cat {{
  font-size: 11px;
  color: var(--apple-blue);
  font-weight: 600;
  letter-spacing: 0.02em;
}}
.card-name {{
  font-size: 17px;
  font-weight: 700;
  color: var(--text);
  line-height: 1.25;
  letter-spacing: -0.02em;
}}
.card-desc {{
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.6;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  flex: 1;
}}

.card-footer {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 14px;
  border-top: 1px solid var(--border-subtle);
}}
.card-footer-label {{
  font-size: 12px;
  color: var(--apple-blue);
  font-weight: 500;
}}
.btn-install {{
  background: var(--apple-blue-dim);
  border: 1px solid transparent;
  color: var(--apple-blue);
  border-radius: 980px;
  padding: 5px 12px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
  font-family: inherit;
  transition: all .2s ease;
}}
.btn-install:hover {{
  background: var(--apple-blue);
  color: #ffffff;
}}

/* ── Empty State ─────────────────────────────────────────── */
.empty {{ text-align: center; padding: 100px 20px; display: none; }}
.empty-icon {{ font-size: 54px; margin-bottom: 16px; }}
.empty h3 {{ font-size: 20px; font-weight: 700; margin-bottom: 6px; letter-spacing: -0.02em; }}
.empty p {{ font-size: 14px; color: var(--text-muted); }}

/* ── Modal (Apple iOS/macOS Sheet Style) ─────────────────── */
.modal-overlay {{
  position: fixed; inset: 0; z-index: 200;
  background: var(--modal-overlay);
  backdrop-filter: blur(24px) saturate(180%);
  -webkit-backdrop-filter: blur(24px) saturate(180%);
  display: none; align-items: center; justify-content: center;
  padding: 20px;
}}
.modal-overlay.open {{ display: flex; }}
.modal {{
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: 24px;
  max-width: 880px; width: 100%; max-height: 88vh;
  display: flex; flex-direction: column;
  box-shadow: 0 24px 64px rgba(0, 0, 0, 0.35);
  animation: apple-modal-in .25s cubic-bezier(0.16, 1, 0.3, 1);
  overflow: hidden;
}}
@keyframes apple-modal-in {{
  from {{ opacity: 0; transform: scale(0.95) translateY(12px); }}
  to   {{ opacity: 1; transform: scale(1) translateY(0); }}
}}

.modal-head {{
  padding: 24px 28px 18px;
  border-bottom: 1px solid var(--border);
  display: flex; align-items: flex-start; justify-content: space-between; gap: 16px;
}}
.modal-head-info {{ flex: 1; min-width: 0; }}
.modal-badges {{ display: flex; align-items: center; gap: 8px; margin-bottom: 8px; flex-wrap: wrap; }}
.modal-name {{ font-size: 22px; font-weight: 700; line-height: 1.25; letter-spacing: -0.025em; }}
.modal-desc {{ font-size: 13px; color: var(--text-secondary); line-height: 1.6; margin-top: 6px; }}
.btn-close {{
  background: var(--segment-bg);
  border: none;
  color: var(--text-muted);
  border-radius: 50%;
  width: 32px; height: 32px; flex-shrink: 0;
  font-size: 14px; cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  transition: all .2s ease;
}}
.btn-close:hover {{ background: var(--red); color: #fff; }}

.modal-install {{
  padding: 12px 28px;
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border);
  display: flex; align-items: center; justify-content: space-between; gap: 16px;
}}
.modal-install code {{
  font-family: "SF Mono", "Cascadia Code", "JetBrains Mono", Menlo, Consolas, monospace;
  font-size: 12px; color: var(--apple-blue); font-weight: 600; flex: 1;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}}
.btn-copy {{
  background: var(--apple-blue);
  border: none;
  color: #fff;
  border-radius: 980px;
  padding: 6px 14px;
  font-size: 12px; font-weight: 600;
  cursor: pointer; flex-shrink: 0;
  transition: opacity .2s ease, transform .1s ease;
}}
.btn-copy:hover {{ opacity: .9; transform: scale(1.02); }}
.btn-copy.copied {{ background: var(--green); }}

.modal-body {{
  flex: 1; overflow-y: auto; padding: 24px 28px;
}}
.modal-body-label {{
  font-size: 11px; font-weight: 700;
  text-transform: uppercase; letter-spacing: .08em;
  color: var(--text-muted); margin-bottom: 12px;
}}

/* ── macOS Xcode / Terminal styled Code Previewer ────────── */
.mac-terminal {{
  background: var(--code-bg);
  border: 1px solid var(--border);
  border-radius: 14px;
  overflow: hidden;
}}
.mac-terminal-bar {{
  background: rgba(0, 0, 0, 0.2);
  padding: 8px 14px;
  display: flex;
  align-items: center;
  gap: 6px;
  border-bottom: 1px solid var(--border-subtle);
}}
.mac-dot {{
  width: 11px; height: 11px; border-radius: 50%;
}}
.dot-red    {{ background: #ff5f56; }}
.dot-yellow {{ background: #ffbd2e; }}
.dot-green  {{ background: #27c93f; }}
.mac-terminal-title {{
  font-size: 11px; color: #86868b; margin-left: 8px; font-family: "SF Mono", monospace;
}}
.modal-content-pre {{
  padding: 16px;
  font-family: "SF Mono", "Cascadia Code", "JetBrains Mono", Menlo, Consolas, monospace;
  font-size: 12px; color: #e6edf3; line-height: 1.7;
  white-space: pre-wrap; word-break: break-word; overflow-x: auto;
}}

.modal-foot {{
  padding: 14px 28px;
  border-top: 1px solid var(--border);
  display: flex; align-items: center; justify-content: space-between;
  background: var(--bg-secondary);
}}
.modal-foot small {{ font-size: 11px; color: var(--text-muted); }}

/* ── Footer ──────────────────────────────────────────────── */
.footer {{
  border-top: 1px solid var(--border);
  background: var(--bg-secondary);
  padding: 32px 28px 48px;
  margin-top: 40px;
  text-align: center;
}}
.footer-inner {{
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}}
.footer-inner p {{
  font-size: 12px;
  color: var(--text-muted);
  letter-spacing: -0.01em;
}}
.footer-link {{
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 500;
  color: var(--apple-blue);
  text-decoration: none;
  transition: opacity .2s;
}}
.footer-link:hover {{
  text-decoration: underline;
  opacity: 0.85;
}}

/* ── Toast ───────────────────────────────────────────────── */
.toast {{
  position: fixed; bottom: 28px; right: 28px; z-index: 300;
  background: var(--green); color: #fff;
  border-radius: 980px; padding: 10px 18px;
  font-size: 13px; font-weight: 600;
  display: none; align-items: center; gap: 8px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25);
  animation: apple-toast-in .25s ease-out;
}}
.toast.show {{ display: flex; }}
@keyframes apple-toast-in {{
  from {{ opacity: 0; transform: translateY(16px) scale(0.95); }}
  to   {{ opacity: 1; transform: translateY(0) scale(1); }}
}}

/* ── Responsive ──────────────────────────────────────────── */
@media (max-width: 680px) {{
  .header {{ padding: 0 16px; }}
  .hero {{ padding: 36px 16px 20px; }}
  .hero h1 {{ font-size: 28px; }}
  .hero p {{ font-size: 15px; }}
  .main {{ padding: 20px 16px 60px; }}
  .grid {{ grid-template-columns: 1fr; }}
  .search-wrap {{ display: none; }}
  .logo-subtitle {{ display: none; }}
  .tabs-container {{ padding: 0 16px; }}
  .btn-github span {{ display: none; }}
}}
</style>
</head>
<body>

<!-- Apple Global Navigation -->
<header class="header">
  <a href="#" class="header-logo">
    <div class="logo-badge"></div>
    <div>
      <div class="logo-title">OpenCode &amp; OpenWork Hub</div>
    </div>
  </a>

  <div class="search-wrap">
    <span class="search-icon">🔍</span>
    <input class="search-input" id="searchInput" type="text"
           placeholder="스킬, 에이전트, 커맨드 검색 (단축키 /)" />
  </div>

  <div class="header-actions">
    <a href="https://github.com/kurtkim80/skills" target="_blank" rel="noopener noreferrer" class="btn-apple btn-github" title="GitHub 저장소 바로가기" style="text-decoration: none;">
      <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor" style="vertical-align: middle;">
        <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/>
      </svg>
      <span>GitHub</span>
    </a>
    <button id="themeToggleBtn" onclick="toggleTheme()" class="btn-apple" title="다크/라이트 테마 전환">🌙 다크</button>
    <button id="syncBtn" onclick="triggerSync()" class="btn-primary">🔄 Sync</button>
    <div class="header-stat">
      <small>TOTAL</small>
      <strong>{total}</strong>
    </div>
  </div>
</header>

<!-- Hero Section -->
<section class="hero">
  <div class="hero-eyebrow">Next-Generation AI Agent Toolkit</div>
  <h1>OpenCode &amp; OpenWork Hub</h1>
  <p>인터넷과 GitHub의 최고 성능 AI 코딩 에이전트 스킬, 커맨드, 페르소나를 한 곳에서 탐색하고 원클릭으로 설치하세요.</p>

  <div class="stat-pills">
    {pills_html}
  </div>
</section>

<!-- Segmented Tabs Navigation -->
<div class="tabs-container">
  <div class="tabs" id="tabs">
    {tabs_html}
  </div>
</div>

<!-- Main Content Area -->
<main class="main">
  <div class="results-bar">
    <p id="resultsLabel">전체 <span id="resultsCount">{total}</span>개 에셋</p>
  </div>
  <div class="grid" id="grid"></div>
  <div class="empty" id="emptyState">
    <div class="empty-icon">🔍</div>
    <h3>검색 결과가 없습니다</h3>
    <p>다른 검색어나 카테고리를 선택해 보세요.</p>
  </div>
</main>

<!-- Footer -->
<footer class="footer">
  <div class="footer-inner">
    <p>OpenCode &amp; OpenWork Skills Dashboard · Apple HIG Design System</p>
    <a href="https://github.com/kurtkim80/skills" target="_blank" rel="noopener noreferrer" class="footer-link">
      <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor">
        <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/>
      </svg>
      <span>github.com/kurtkim80/skills 바로가기 ↗</span>
    </a>
  </div>
</footer>

<!-- Modal (iOS/macOS Sheet) -->
<div class="modal-overlay" id="modal" onclick="onOverlayClick(event)">
  <div class="modal" id="modalBox">
    <div class="modal-head">
      <div class="modal-head-info">
        <div class="modal-badges" id="modalBadges"></div>
        <div class="modal-name" id="modalName"></div>
        <div class="modal-desc" id="modalDesc"></div>
      </div>
      <button class="btn-close" onclick="closeModal()">✕</button>
    </div>
    <div class="modal-install">
      <code id="modalInstall"></code>
      <button class="btn-copy" id="copyBtn" onclick="copyInstall()">📋 복사</button>
    </div>
    <div class="modal-body">
      <div class="modal-body-label">SPECIFICATION &amp; INSTRUCTIONS</div>
      <div class="mac-terminal">
        <div class="mac-terminal-bar">
          <span class="mac-dot dot-red"></span>
          <span class="mac-dot dot-yellow"></span>
          <span class="mac-dot dot-green"></span>
          <span class="mac-terminal-title">SKILL.md preview</span>
        </div>
        <pre class="modal-content-pre" id="modalContent"></pre>
      </div>
    </div>
    <div class="modal-foot">
      <small>ESC 키 또는 바깥 영역을 클릭하여 닫기</small>
      <button class="btn-apple" onclick="closeModal()">닫기</button>
    </div>
  </div>
</div>

<!-- Toast -->
<div class="toast" id="toast">✅ <span id="toastMsg"></span></div>

<script>
const DATA = {js_data};

const typeBadgeClass = {{ skill: 'badge-skill', command: 'badge-command', agent: 'badge-agent' }};
const typeLabel = {{ skill: '🌟 SKILL', command: '⚡ COMMAND', agent: '🤖 AGENT' }};

let curCat = 'all';
let curSearch = '';
let curCard = null;

/* ── Theme Switcher ────────────────────────────────────── */
function initTheme() {{
  const saved = localStorage.getItem('opencode_theme') || 'dark';
  setTheme(saved);
}}

function toggleTheme() {{
  const cur = document.documentElement.getAttribute('data-theme') || 'dark';
  const next = cur === 'dark' ? 'light' : 'dark';
  setTheme(next);
}}

function setTheme(theme) {{
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem('opencode_theme', theme);
  const btn = document.getElementById('themeToggleBtn');
  if (btn) {{
    btn.innerHTML = theme === 'light' ? '☀️ 라이트' : '🌙 다크';
  }}
}}

/* ── Render ────────────────────────────────────────────── */
function render() {{
  const q = curSearch.toLowerCase();
  const filtered = DATA.filter(c => {{
    const matchCat = curCat === 'all' || c.cat_id === curCat;
    const matchQ = !q ||
      c.name.toLowerCase().includes(q) ||
      c.desc.toLowerCase().includes(q);
    return matchCat && matchQ;
  }});

  document.getElementById('resultsCount').textContent = filtered.length;
  const grid = document.getElementById('grid');
  const empty = document.getElementById('emptyState');

  if (filtered.length === 0) {{
    grid.innerHTML = '';
    empty.style.display = 'block';
    return;
  }}
  empty.style.display = 'none';

  grid.innerHTML = filtered.map(c => {{
    const isRAG = c.cat_id === 'rag_search';
    const bClass = typeBadgeClass[c.type] || 'badge-skill';
    const bLabel = typeLabel[c.type] || 'SKILL';
    const descText = c.desc || '상세 지침 및 사양을 보려면 카드를 클릭하세요.';
    const srcShort = c.source.length > 22 ? c.source.slice(0,22)+'…' : c.source;
    const repoBtn = c.repo_url ?
      `<a href="${{escAttr(c.repo_url)}}" target="_blank" rel="noopener noreferrer" class="badge-src-link" onclick="event.stopPropagation()" title="원본 GitHub 저장소 바로가기: ${{escAttr(c.source)}}">
        🐙 ${{escHtml(srcShort)}} ↗
      </a>` :
      `<span class="badge-src" title="${{escAttr(c.source)}}">${{escHtml(srcShort)}}</span>`;

    return `<div class="card${{isRAG ? ' rag-highlight' : ''}}" onclick="openModal('${{escAttr(c.id)}}')">
      <div class="card-badges">
        <span class="badge ${{bClass}}">${{bLabel}}</span>
        ${{repoBtn}}
      </div>
      <div class="card-cat">${{escHtml(c.cat_label)}}</div>
      <div class="card-name">${{escHtml(c.name)}}</div>
      <div class="card-desc">${{escHtml(descText)}}</div>
      <div class="card-footer">
        <span class="card-footer-label">세부 사양 보기 →</span>
        <button class="btn-install" title="설치 명령어 복사" onclick="event.stopPropagation();copyCmd('${{escAttr(c.install)}}')">
          📋 설치
        </button>
      </div>
    </div>`;
  }}).join('');
}}

/* ── Tabs ──────────────────────────────────────────────── */
function setTab(cat) {{
  curCat = cat;
  document.querySelectorAll('.tab-btn').forEach(btn => {{
    btn.classList.toggle('active', btn.getAttribute('data-cat') === cat);
  }});
  render();
}}

/* ── Search ────────────────────────────────────────────── */
function onSearch(val) {{
  curSearch = val;
  document.getElementById('searchInput').value = val;
  render();
}}
document.getElementById('searchInput').addEventListener('input', e => onSearch(e.target.value));

/* ── Keyboard shortcuts ────────────────────────────────── */
document.addEventListener('keydown', e => {{
  const inp = document.getElementById('searchInput');
  if (e.key === '/' && document.activeElement !== inp) {{
    e.preventDefault(); inp.focus();
  }}
  if (e.key === 'Escape') closeModal();
}});

/* ── Modal ─────────────────────────────────────────────── */
function openModal(id) {{
  const c = DATA.find(x => x.id === id);
  if (!c) return;
  curCard = c;

  const bClass = typeBadgeClass[c.type] || 'badge-skill';
  const bLabel = typeLabel[c.type] || 'SKILL';
  const modalRepoBtn = c.repo_url ?
    `<a href="${{escAttr(c.repo_url)}}" target="_blank" rel="noopener noreferrer" class="btn-apple" style="padding: 3px 10px; font-size: 11px; text-decoration: none; display: inline-flex; align-items: center; gap: 4px; margin-left: 4px;" title="원본 GitHub 저장소 새 탭으로 열기">
      🐙 원본 GitHub: ${{escHtml(c.source)}} ↗
    </a>` :
    `<span style="font-size:11px;color:var(--text-muted);margin-left:4px">출처: ${{escHtml(c.source)}}</span>`;

  document.getElementById('modalBadges').innerHTML =
    `<span class="badge ${{bClass}}">${{bLabel}}</span>` +
    `<span class="badge" style="background:var(--segment-bg);color:var(--text-secondary)">${{escHtml(c.cat_label)}}</span>` +
    modalRepoBtn;

  document.getElementById('modalName').textContent = c.name;
  document.getElementById('modalDesc').textContent = c.desc || '';
  document.getElementById('modalInstall').textContent = c.install;
  document.getElementById('modalContent').textContent = c.content || '// 상세 내용 없음';

  const btn = document.getElementById('copyBtn');
  btn.textContent = '📋 복사';
  btn.classList.remove('copied');

  document.getElementById('modal').classList.add('open');
  document.body.style.overflow = 'hidden';
}}

function closeModal() {{
  document.getElementById('modal').classList.remove('open');
  document.body.style.overflow = '';
}}

function onOverlayClick(e) {{
  if (e.target.id === 'modal') closeModal();
}}

/* ── Copy helpers ──────────────────────────────────────── */
function copyCmd(cmd) {{
  navigator.clipboard.writeText(cmd).then(() => {{
    showToast('설치 명령어 복사 완료!');
  }}).catch(() => {{
    const ta = document.createElement('textarea');
    ta.value = cmd;
    document.body.appendChild(ta);
    ta.select();
    document.execCommand('copy');
    document.body.removeChild(ta);
    showToast('설치 명령어 복사 완료!');
  }});
}}

function copyInstall() {{
  if (!curCard) return;
  copyCmd(curCard.install);
  const btn = document.getElementById('copyBtn');
  btn.textContent = '✅ 복사됨';
  btn.classList.add('copied');
  setTimeout(() => {{ btn.textContent = '📋 복사'; btn.classList.remove('copied'); }}, 2000);
}}

function showToast(msg) {{
  const t = document.getElementById('toast');
  document.getElementById('toastMsg').textContent = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 2400);
}}

/* ── API triggers ──────────────────────────────────────── */
async function triggerSync() {{
  const btn = document.getElementById('syncBtn');
  const origText = btn.innerHTML;
  btn.innerHTML = '⏳ 수집 중...';
  btn.disabled = true;
  btn.style.opacity = '0.7';
  try {{
    const res = await fetch('/api/sync', {{ method: 'POST' }});
    if (res.ok) {{
      showToast('수집 및 동기화 완료! 페이지를 새로고침합니다.');
      setTimeout(() => window.location.reload(), 1500);
    }} else {{
      showToast('수집 실패. 서버 로그를 확인하세요.');
      btn.innerHTML = origText;
      btn.disabled = false;
      btn.style.opacity = '1';
    }}
  }} catch (e) {{
    showToast('❌ 로컬 서버(server.py) 모드에서만 수집 버튼을 사용할 수 있습니다.');
    btn.innerHTML = origText;
    btn.disabled = false;
    btn.style.opacity = '1';
  }}
}}

/* ── HTML escape helpers ───────────────────────────────── */
function escHtml(s) {{
  return String(s)
    .replace(/&/g,'&amp;').replace(/</g,'&lt;')
    .replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;');
}}
function escAttr(s) {{
  return String(s).replace(/'/g,"\\'").replace(/"/g,'&quot;');
}}

/* ── Init ─────────────────────────────────────────────── */
initTheme();
render();
</script>
</body>
</html>
"""

    with open(HTML_OUTPUT, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ 애플 스타일 대시보드 생성 완료: {HTML_OUTPUT}")
    print(f"   총 {len(raw_cards)}개 에셋 포함")


if __name__ == "__main__":
    generate_dashboard()
