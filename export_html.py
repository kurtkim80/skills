#!/usr/bin/env python3
"""
OpenCode & OpenWork Asset Dashboard Generator
CDN 없이 순수 inline CSS + JS로 동작하는 완전 오프라인 HTML 대시보드를 생성합니다.
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INDEX_FILE = BASE_DIR / "assets_index.json"
COLLECTED_DIR = BASE_DIR / "collected_assets"
HTML_OUTPUT = BASE_DIR / "index.html"


def classify_category(name: str, desc: str, asset_type: str) -> tuple:
    text = (name + " " + desc).lower()

    if asset_type == "command":
        return "workflow", "⚡ 워크플로우 커맨드"

    if asset_type == "agent":
        return "agent", "🤖 에이전트"

    if any(k in text for k in ["rag", "embedding", "vector", "retrieval", "semantic search",
                                 "fine-tuning", "fine_tuning", "finetune", "prompt-engineer",
                                 "prompt engineer", "ml-pipeline", "agent-creator", "skill-creator",
                                 "mcp-", "mcp developer", "llm", "nlp"]):
        return "ai_rag", "🤖 AI, RAG & LLM"

    if any(k in text for k in ["docker", "kubernetes", "k8s", "terraform", "devops", "sre",
                                 "cloud", "chaos", "monitoring", "embedded", "legacy", "ci-cd",
                                 "cicd", "pipeline", "infra", "deployment"]):
        return "devops", "☁️ DevOps & 인프라"

    if any(k in text for k in ["review", "reviewer", "architect", "security", "guardian",
                                 "test", "debug", "api-design", "graphql", "postgres", "sql",
                                 "database", "spec", "document", "common-ground", "microservices"]):
        return "arch_quality", "🏗️ 아키텍처, 리뷰 & 보안"

    return "dev_frameworks", "💻 언어 & 프레임워크"


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

    cards = []
    for asset_type_key, items in [("skill", data.get("skills", {})),
                                    ("command", data.get("commands", {})),
                                    ("agent", data.get("agents", {}))]:
        for key, item in items.items():
            name = item.get("name", key)
            desc = item.get("description", "")
            src_name = item.get("source_name", "local")
            rel_path = item.get("path", "")

            content = ""
            file_path = BASE_DIR / rel_path
            if file_path.is_dir():
                skill_md = file_path / "SKILL.md"
                if skill_md.exists():
                    content = skill_md.read_text(encoding="utf-8", errors="ignore")
            elif file_path.is_file():
                content = file_path.read_text(encoding="utf-8", errors="ignore")

            cat_id, cat_label = classify_category(name, desc, asset_type_key)

            cards.append({
                "id": esc(key),
                "name": esc(name),
                "type": asset_type_key,
                "cat_id": cat_id,
                "cat_label": esc(cat_label),
                "desc": esc(desc[:200]),
                "source": esc(src_name),
                "content": esc(content[:8000]),
                "install": esc(f"python3 skill_collector.py install {key} --target global"),
            })

    # 카테고리 카운트
    cat_counts = {}
    for c in cards:
        cat_counts[c["cat_id"]] = cat_counts.get(c["cat_id"], 0) + 1

    # JSON으로 카드 데이터를 JS에 주입 (이미 esc 처리됨 → JS 문자열용으로 역변환하여 다시 넣기)
    # JS embed용으로 raw 데이터를 다시 만들기 (JS JSON.parse용이므로 esc 하지 않고 json.dumps 사용)
    raw_cards = []
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

            raw_cards.append({
                "id": key,
                "name": name,
                "type": item_type,
                "cat_id": cat_id,
                "cat_label": cat_label,
                "desc": desc,
                "source": src,
                "content": content,
                "install": f"python3 skill_collector.py install {key} --target global",
            })

    # </script> 가 content 안에 있으면 브라우저가 스크립트 태그를 조기 종료함
    # → </ 를 <\/ 로 이스케이프하여 안전하게 주입
    js_data = json.dumps(raw_cards, ensure_ascii=False)
    js_data = js_data.replace("</", "<\\/")


    total = len(raw_cards)
    ai_rag_n = cat_counts.get("ai_rag", 0)
    dev_n = cat_counts.get("dev_frameworks", 0)
    arch_n = cat_counts.get("arch_quality", 0)
    devops_n = cat_counts.get("devops", 0)
    wf_n = cat_counts.get("workflow", 0)
    ag_n = cat_counts.get("agent", 0)

    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>OpenCode &amp; OpenWork Hub Dashboard</title>
<style>
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
:root {{
  --bg: #0d1117;
  --bg2: #161b22;
  --bg3: #21262d;
  --border: #30363d;
  --border2: #3d444d;
  --text: #e6edf3;
  --text2: #7d8590;
  --text3: #9198a1;
  --indigo: #6e76f1;
  --indigo-dim: rgba(110,118,241,0.15);
  --indigo-border: rgba(110,118,241,0.35);
  --purple: #a78bfa;
  --purple-dim: rgba(167,139,250,0.15);
  --green: #3fb950;
  --green-dim: rgba(63,185,80,0.15);
  --amber: #d29922;
  --amber-dim: rgba(210,153,34,0.15);
  --red: #f85149;
  --teal: #39d2c0;
  --teal-dim: rgba(57,210,192,0.12);
  --radius: 10px;
  --radius-lg: 14px;
}}
html {{ scroll-behavior: smooth; }}
body {{
  background: var(--bg);
  color: var(--text);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
  font-size: 14px;
  line-height: 1.6;
  min-height: 100vh;
}}

/* ── Scrollbar ─────────────────────────────────────────── */
::-webkit-scrollbar {{ width: 6px; height: 6px; }}
::-webkit-scrollbar-track {{ background: var(--bg); }}
::-webkit-scrollbar-thumb {{ background: var(--border2); border-radius: 3px; }}
::-webkit-scrollbar-thumb:hover {{ background: var(--text2); }}

/* ── Header ─────────────────────────────────────────────── */
.header {{
  position: sticky; top: 0; z-index: 50;
  background: rgba(13,17,23,0.92);
  backdrop-filter: blur(14px);
  border-bottom: 1px solid var(--border);
  padding: 0 24px;
  height: 64px;
  display: flex; align-items: center; justify-content: space-between; gap: 16px;
}}
.header-logo {{ display: flex; align-items: center; gap: 10px; flex-shrink: 0; }}
.logo-icon {{
  width: 38px; height: 38px; border-radius: 10px;
  background: linear-gradient(135deg, #6e76f1, #a78bfa);
  display: flex; align-items: center; justify-content: center;
  font-size: 18px;
}}
.logo-title {{ font-size: 16px; font-weight: 700; color: var(--text); }}
.logo-sub {{ font-size: 11px; color: var(--text2); }}

/* ── Search ──────────────────────────────────────────────── */
.search-wrap {{ flex: 1; max-width: 440px; position: relative; }}
.search-input {{
  width: 100%;
  background: var(--bg2);
  border: 1px solid var(--border);
  color: var(--text);
  border-radius: var(--radius);
  padding: 8px 12px 8px 36px;
  font-size: 13px;
  outline: none;
  transition: border-color .2s, box-shadow .2s;
}}
.search-input::placeholder {{ color: var(--text2); }}
.search-input:focus {{ border-color: var(--indigo); box-shadow: 0 0 0 3px var(--indigo-dim); }}
.search-icon {{
  position: absolute; left: 10px; top: 50%; transform: translateY(-50%);
  color: var(--text2); font-size: 14px; pointer-events: none;
}}
.header-stat {{ text-align: right; flex-shrink: 0; }}
.header-stat small {{ display: block; font-size: 11px; color: var(--text2); }}
.header-stat strong {{ font-size: 18px; font-weight: 800; color: var(--indigo); }}

/* ── Hero / Filter ───────────────────────────────────────── */
.hero {{
  padding: 28px 24px 0;
  background: linear-gradient(180deg, rgba(110,118,241,0.06) 0%, transparent 100%);
  border-bottom: 1px solid var(--border);
}}
.hero h1 {{ font-size: 24px; font-weight: 800; margin-bottom: 6px; }}
.hero p {{ font-size: 13px; color: var(--text2); max-width: 680px; line-height: 1.7; }}

.stat-pills {{ display: flex; flex-wrap: wrap; gap: 8px; margin: 16px 0 0; }}
.pill {{
  display: inline-flex; align-items: center; gap: 6px;
  padding: 5px 12px; border-radius: 20px;
  font-size: 12px; font-weight: 600; cursor: pointer;
  border: 1px solid transparent; transition: all .15s;
}}
.pill-indigo  {{ background: var(--indigo-dim); color: #a5b4fc; border-color: var(--indigo-border); }}
.pill-purple  {{ background: var(--purple-dim); color: var(--purple); border-color: rgba(167,139,250,.35); }}
.pill-green   {{ background: var(--green-dim); color: var(--green); border-color: rgba(63,185,80,.35); }}
.pill-amber   {{ background: var(--amber-dim); color: var(--amber); border-color: rgba(210,153,34,.35); }}
.pill-teal    {{ background: var(--teal-dim); color: var(--teal); border-color: rgba(57,210,192,.35); }}

/* ── Category Tabs ───────────────────────────────────────── */
.tabs {{ display: flex; gap: 6px; overflow-x: auto; padding: 16px 0 12px; }}
.tabs::-webkit-scrollbar {{ display: none; }}
.tab-btn {{
  flex-shrink: 0; padding: 7px 14px; border-radius: var(--radius);
  border: 1px solid var(--border);
  background: var(--bg2); color: var(--text2);
  font-size: 12px; font-weight: 600; cursor: pointer;
  transition: all .15s;
  white-space: nowrap;
}}
.tab-btn:hover {{ border-color: var(--border2); color: var(--text); }}
.tab-btn.active {{
  background: var(--indigo); border-color: var(--indigo);
  color: #fff; box-shadow: 0 0 12px rgba(110,118,241,0.4);
}}

/* ── Main Layout ─────────────────────────────────────────── */
.main {{ max-width: 1400px; margin: 0 auto; padding: 24px; }}
.results-bar {{
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 18px;
}}
.results-bar p {{ font-size: 12px; color: var(--text2); }}
.results-bar span {{ color: var(--indigo); font-weight: 700; }}

/* ── Card Grid ───────────────────────────────────────────── */
.grid {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
}}
.card {{
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 18px;
  cursor: pointer;
  transition: border-color .2s, transform .2s, box-shadow .2s;
  display: flex; flex-direction: column; gap: 10px;
}}
.card:hover {{
  border-color: var(--indigo);
  transform: translateY(-3px);
  box-shadow: 0 8px 24px rgba(110,118,241,0.18);
}}
.card.rag-highlight {{ border-color: var(--indigo-border); }}

.card-badges {{ display: flex; align-items: center; gap: 6px; }}
.badge {{
  display: inline-block; padding: 2px 8px; border-radius: 6px;
  font-size: 11px; font-weight: 700; border: 1px solid;
}}
.badge-skill   {{ background: var(--indigo-dim); color: #a5b4fc; border-color: var(--indigo-border); }}
.badge-command {{ background: var(--purple-dim); color: var(--purple); border-color: rgba(167,139,250,.35); }}
.badge-agent   {{ background: var(--green-dim); color: var(--green); border-color: rgba(63,185,80,.35); }}
.badge-src     {{ background: transparent; color: var(--text2); border-color: transparent; font-size: 10px; font-weight: 400; margin-left: auto; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 130px; }}

.card-cat {{ font-size: 11px; color: var(--indigo); font-weight: 600; }}
.card-name {{ font-size: 15px; font-weight: 700; color: var(--text); line-height: 1.3; }}
.card-desc {{
  font-size: 12px; color: var(--text2); line-height: 1.6;
  overflow: hidden; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical;
  flex: 1;
}}

.card-footer {{
  display: flex; align-items: center; justify-content: space-between;
  padding-top: 10px; border-top: 1px solid var(--border);
}}
.card-footer-label {{ font-size: 11px; color: var(--text2); }}
.btn-install {{
  background: var(--bg3); border: 1px solid var(--border2);
  color: var(--text); border-radius: 7px; padding: 4px 10px;
  font-size: 11px; font-weight: 600; cursor: pointer;
  display: flex; align-items: center; gap: 4px;
  transition: all .15s;
}}
.btn-install:hover {{ background: var(--indigo); border-color: var(--indigo); color: #fff; }}

/* ── Empty State ─────────────────────────────────────────── */
.empty {{ text-align: center; padding: 80px 20px; display: none; }}
.empty-icon {{ font-size: 48px; margin-bottom: 14px; }}
.empty h3 {{ font-size: 18px; font-weight: 700; margin-bottom: 6px; }}
.empty p {{ font-size: 13px; color: var(--text2); }}

/* ── Modal ───────────────────────────────────────────────── */
.modal-overlay {{
  position: fixed; inset: 0; z-index: 100;
  background: rgba(0,0,0,0.75);
  backdrop-filter: blur(6px);
  display: none; align-items: center; justify-content: center;
  padding: 16px;
}}
.modal-overlay.open {{ display: flex; }}
.modal {{
  background: var(--bg2); border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  max-width: 860px; width: 100%; max-height: 90vh;
  display: flex; flex-direction: column;
  animation: modal-in .18s ease-out;
}}
@keyframes modal-in {{ from {{ opacity:0; transform: scale(.96) translateY(8px); }} to {{ opacity:1; transform: scale(1) translateY(0); }} }}

.modal-head {{
  padding: 20px 22px 16px;
  border-bottom: 1px solid var(--border);
  display: flex; align-items: flex-start; justify-content: space-between; gap: 12px;
}}
.modal-head-info {{ flex: 1; min-width: 0; }}
.modal-badges {{ display: flex; align-items: center; gap: 6px; margin-bottom: 8px; flex-wrap: wrap; }}
.modal-name {{ font-size: 20px; font-weight: 800; line-height: 1.3; word-break: break-all; }}
.modal-desc {{ font-size: 12px; color: var(--text2); line-height: 1.7; margin-top: 6px; }}
.btn-close {{
  background: var(--bg3); border: 1px solid var(--border);
  color: var(--text2); border-radius: 8px;
  width: 32px; height: 32px; flex-shrink: 0;
  font-size: 16px; cursor: pointer; display: flex; align-items: center; justify-content: center;
  transition: all .15s;
}}
.btn-close:hover {{ background: var(--red); border-color: var(--red); color: #fff; }}

.modal-install {{
  padding: 10px 22px;
  background: var(--bg);
  border-bottom: 1px solid var(--border);
  display: flex; align-items: center; justify-content: space-between; gap: 12px;
}}
.modal-install code {{
  font-family: "SF Mono", "Cascadia Code", "JetBrains Mono", Consolas, monospace;
  font-size: 12px; color: #a5b4fc; flex: 1;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}}
.btn-copy {{
  background: var(--indigo); border: none;
  color: #fff; border-radius: 7px; padding: 6px 12px;
  font-size: 12px; font-weight: 600; cursor: pointer; flex-shrink: 0;
  transition: opacity .15s;
}}
.btn-copy:hover {{ opacity: .85; }}
.btn-copy.copied {{ background: var(--green); }}

.modal-body {{ flex: 1; overflow-y: auto; padding: 20px 22px; }}
.modal-body-label {{ font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: .08em; color: var(--text2); margin-bottom: 10px; }}
.modal-content-pre {{
  background: var(--bg); border: 1px solid var(--border);
  border-radius: var(--radius); padding: 16px;
  font-family: "SF Mono", "Cascadia Code", "JetBrains Mono", Consolas, monospace;
  font-size: 12px; color: var(--text); line-height: 1.7;
  white-space: pre-wrap; word-break: break-word; overflow-x: auto;
}}

.modal-foot {{
  padding: 12px 22px;
  border-top: 1px solid var(--border);
  display: flex; align-items: center; justify-content: space-between;
}}
.modal-foot small {{ font-size: 11px; color: var(--text2); }}
.btn-secondary {{
  background: var(--bg3); border: 1px solid var(--border2);
  color: var(--text); border-radius: 8px; padding: 7px 16px;
  font-size: 12px; font-weight: 600; cursor: pointer; transition: all .15s;
}}
.btn-secondary:hover {{ border-color: var(--border2); background: var(--border); }}

/* ── Toast ───────────────────────────────────────────────── */
.toast {{
  position: fixed; bottom: 24px; right: 24px; z-index: 200;
  background: #1a7f37; color: #fff;
  border-radius: var(--radius); padding: 10px 16px;
  font-size: 13px; font-weight: 600;
  display: none; align-items: center; gap: 8px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.4);
  animation: toast-in .18s ease-out;
}}
.toast.show {{ display: flex; }}
@keyframes toast-in {{ from {{ opacity:0; transform: translateY(12px); }} to {{ opacity:1; transform: translateY(0); }} }}

/* ── Responsive ──────────────────────────────────────────── */
@media (max-width: 640px) {{
  .header {{ padding: 0 14px; }}
  .hero {{ padding: 18px 14px 0; }}
  .hero h1 {{ font-size: 18px; }}
  .main {{ padding: 16px 14px; }}
  .grid {{ grid-template-columns: 1fr; }}
  .search-wrap {{ display: none; }}
  .logo-sub {{ display: none; }}
}}
</style>
</head>
<body>

<!-- Header -->
<header class="header">
  <div class="header-logo">
    <div class="logo-icon">🧩</div>
    <div>
      <div class="logo-title">OpenCode &amp; OpenWork Hub</div>
      <div class="logo-sub">Skills · Commands · Agents</div>
    </div>
  </div>

  <div class="search-wrap">
    <span class="search-icon">🔍</span>
    <input class="search-input" id="searchInput" type="text"
           placeholder="키워드 검색 (예: rag, review, docker) — 단축키 /" />
  </div>

  <div style="display: flex; gap: 12px; align-items: center;">
    <button id="syncBtn" onclick="triggerSync()" class="btn-secondary" style="background: var(--indigo); color: white; border: none; padding: 0 12px; border-radius: 6px;">🔄 수집(Sync)</button>
    <div class="header-stat">
      <small>수집된 에셋</small>
      <strong>{total}</strong>
    </div>
  </div>
</header>


<!-- Hero -->
<div class="hero">
  <div style="max-width:1400px;margin:0 auto">
    <h1>분야별 AI 에이전트 에셋 컬렉션</h1>
    <p>인터넷 &amp; GitHub에서 수집된 OpenCode / OpenWork 표준 규격의 스킬, 커맨드, 에이전트를 탐색하고 1-클릭으로 설치하세요.</p>

    <div class="stat-pills">
      <span class="pill pill-indigo" onclick="setTab('ai_rag')">🤖 AI, RAG &amp; LLM ({ai_rag_n})</span>
      <span class="pill pill-teal" onclick="setTab('dev_frameworks')">💻 언어 &amp; 프레임워크 ({dev_n})</span>
      <span class="pill pill-green" onclick="setTab('arch_quality')">🏗️ 아키텍처 &amp; 보안 ({arch_n})</span>
      <span class="pill pill-amber" onclick="setTab('devops')">☁️ DevOps &amp; 인프라 ({devops_n})</span>
      <span class="pill pill-purple" onclick="setTab('workflow')">⚡ 커맨드 ({wf_n})</span>
    </div>

    <!-- Mobile search -->
    <input class="search-input" id="searchMobile" type="text"
           placeholder="검색..."
           style="display:none;width:100%;margin:14px 0 0;" />

    <div class="tabs" id="tabs">
      <button class="tab-btn active" data-cat="all" onclick="setTab('all')">🔥 전체 ({total})</button>
      <button class="tab-btn" data-cat="ai_rag" onclick="setTab('ai_rag')">🤖 AI, RAG &amp; LLM ({ai_rag_n})</button>
      <button class="tab-btn" data-cat="dev_frameworks" onclick="setTab('dev_frameworks')">💻 언어 &amp; 프레임워크 ({dev_n})</button>
      <button class="tab-btn" data-cat="arch_quality" onclick="setTab('arch_quality')">🏗️ 아키텍처, 리뷰 &amp; 보안 ({arch_n})</button>
      <button class="tab-btn" data-cat="devops" onclick="setTab('devops')">☁️ DevOps &amp; 인프라 ({devops_n})</button>
      <button class="tab-btn" data-cat="workflow" onclick="setTab('workflow')">⚡ 워크플로우 커맨드 ({wf_n})</button>
      <button class="tab-btn" data-cat="agent" onclick="setTab('agent')">🤖 에이전트 ({ag_n})</button>
    </div>
  </div>
</div>

<!-- Main -->
<main class="main">
  <div class="results-bar">
    <p id="resultsLabel">전체 <span id="resultsCount">{total}</span>개 에셋</p>
  </div>
  <div class="grid" id="grid"></div>
  <div class="empty" id="emptyState">
    <div class="empty-icon">🔍</div>
    <h3>검색 결과 없음</h3>
    <p>다른 키워드나 카테고리를 선택해보세요.</p>
  </div>
</main>

<!-- Modal -->
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
      <div class="modal-body-label">📄 지침 &amp; 스펙 (SKILL.md / COMMAND.md 전체 내용)</div>
      <pre class="modal-content-pre" id="modalContent"></pre>
    </div>
    <div class="modal-foot">
      <small>ESC 또는 바깥 클릭으로 닫기</small>
      <button class="btn-secondary" onclick="closeModal()">닫기</button>
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
    const isRAG = c.cat_id === 'ai_rag';
    const bClass = typeBadgeClass[c.type] || 'badge-skill';
    const bLabel = typeLabel[c.type] || 'SKILL';
    const descText = c.desc || '상세 내용을 보려면 카드를 클릭하세요.';
    const srcShort = c.source.length > 22 ? c.source.slice(0,22)+'…' : c.source;
    return `<div class="card${{isRAG ? ' rag-highlight' : ''}}" onclick="openModal('${{escAttr(c.id)}}')">
      <div class="card-badges">
        <span class="badge ${{bClass}}">${{bLabel}}</span>
        <span class="badge badge-src" title="${{escAttr(c.source)}}">${{escAttr(srcShort)}}</span>
      </div>
      <div class="card-cat">${{escHtml(c.cat_label)}}</div>
      <div class="card-name">${{escHtml(c.name)}}</div>
      <div class="card-desc">${{escHtml(descText)}}</div>
      <div class="card-footer">
        <span class="card-footer-label">👁 상세 보기</span>
        <button class="btn-install" title="설치 명령 복사" onclick="event.stopPropagation();copyCmd('${{escAttr(c.install)}}')">
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
  document.getElementById('searchMobile').value = val;
  render();
}}
document.getElementById('searchInput').addEventListener('input', e => onSearch(e.target.value));
document.getElementById('searchMobile').addEventListener('input', e => onSearch(e.target.value));

/* ── Keyboard shortcuts ────────────────────────────────── */
document.addEventListener('keydown', e => {{
  const inp = document.getElementById('searchInput');
  if (e.key === '/' && document.activeElement !== inp) {{
    e.preventDefault(); inp.focus();
  }}
  if (e.key === 'Escape') closeModal();
}});

/* ── Responsive mobile search ──────────────────────────── */
if (window.innerWidth < 640) {{
  document.getElementById('searchMobile').style.display = 'block';
}}

/* ── Modal ─────────────────────────────────────────────── */
function openModal(id) {{
  const c = DATA.find(x => x.id === id);
  if (!c) return;
  curCard = c;

  const bClass = typeBadgeClass[c.type] || 'badge-skill';
  const bLabel = typeLabel[c.type] || 'SKILL';

  document.getElementById('modalBadges').innerHTML =
    `<span class="badge ${{bClass}}">${{bLabel}}</span>` +
    `<span class="badge" style="background:var(--bg3);color:var(--text2);border:1px solid var(--border)">${{escHtml(c.cat_label)}}</span>` +
    `<span style="font-size:11px;color:var(--text2);margin-left:4px">출처: ${{escHtml(c.source)}}</span>`;

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
render();
</script>
</body>
</html>
"""

    with open(HTML_OUTPUT, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ 대시보드 생성 완료: {HTML_OUTPUT}")
    print(f"   총 {len(raw_cards)}개 에셋 포함")


if __name__ == "__main__":
    generate_dashboard()
