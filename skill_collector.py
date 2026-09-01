#!/usr/bin/env python3
"""
OpenCode & OpenWork Asset Collector (Skills, Commands, Agents)
=============================================================
GitHub 및 인터넷에서 OpenCode / OpenWork용:
1) 🌟 스킬 (Skills)
2) ⚡ 커맨드 (Commands)
3) 🤖 서브에이전트 (Agents)
를 자동으로 탐색, 수집, 색인(Index), 검색(Search), 설치(Install)하는 CLI 도구입니다.

의존성: Python 3.8+ (표준 라이브러리만 사용)
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import urllib.parse
from pathlib import Path

# 기본 경로
BASE_DIR = Path(__file__).resolve().parent
SOURCES_FILE = BASE_DIR / "sources.json"
COLLECTED_DIR = BASE_DIR / "collected_assets"
INDEX_FILE = BASE_DIR / "assets_index.json"

DEFAULT_OPENCODE_GLOBAL_PATH = Path.home() / ".config" / "opencode"
DEFAULT_OPENCODE_LOCAL_PATH = Path.cwd() / ".opencode"


def parse_frontmatter(content: str) -> dict:
    """YAML Frontmatter 또는 마크다운 헤더 파싱"""
    metadata = {}
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            yaml_block = parts[1]
            for line in yaml_block.splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if ":" in line:
                    key, val = line.split(":", 1)
                    metadata[key.strip()] = val.strip().strip("'\"")

    # Frontmatter가 없거나 설명이 부족할 경우 첫 번째 # 헤더나 본문 첫 줄 활용
    if "description" not in metadata or not metadata["description"]:
        for line in content.splitlines():
            line = line.strip()
            if line.startswith("# "):
                metadata.setdefault("title", line.lstrip("# ").strip())
            elif line and not line.startswith("---") and not line.startswith("#"):
                metadata.setdefault("description", line[:150])
                break

    return metadata


def load_sources():
    if not SOURCES_FILE.exists():
        return []
    with open(SOURCES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_sources(sources):
    with open(SOURCES_FILE, "w", encoding="utf-8") as f:
        json.dump(sources, f, indent=2, ensure_ascii=False)


def load_index():
    if not INDEX_FILE.exists():
        return {}
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_index(index_data):
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(index_data, f, indent=2, ensure_ascii=False)


def sync_assets():
    """모든 원격 저장소에서 Skills, Commands, Agents 수집 및 색인"""
    sources = load_sources()
    if not sources:
        print("❌ 등록된 소스가 없습니다. sources.json을 확인하세요.")
        return

    COLLECTED_DIR.mkdir(parents=True, exist_ok=True)
    skills_dir = COLLECTED_DIR / "skills"
    commands_dir = COLLECTED_DIR / "commands"
    agents_dir = COLLECTED_DIR / "agents"

    skills_dir.mkdir(parents=True, exist_ok=True)
    commands_dir.mkdir(parents=True, exist_ok=True)
    agents_dir.mkdir(parents=True, exist_ok=True)

    index = {"skills": {}, "commands": {}, "agents": {}}
    print(f"🚀 총 {len(sources)}개 저장소로부터 Skills, Commands, Agents 수집을 시작합니다...\n")

    for src in sources:
        repo_name = src.get("name", "unknown")
        repo_url = src.get("repo")
        branch = src.get("branch", "main")

        print(f"📦 [{repo_name}] 동기화 중: {repo_url}")

        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                cmd = ["git", "clone", "--depth", "1", "-b", branch, repo_url, tmpdir]
                res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                if res.returncode != 0:
                    cmd = ["git", "clone", "--depth", "1", repo_url, tmpdir]
                    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    if res.returncode != 0:
                        print(f"   ⚠️ 클론 실패: {res.stderr.strip()[:100]}")
                        continue

                root = Path(tmpdir)
                repo_skills = 0
                repo_commands = 0
                repo_agents = 0

                # 1. Skills 수집 (SKILL.md)
                for skill_file in root.rglob("SKILL.md"):
                    folder = skill_file.parent
                    s_name = folder.name
                    if s_name.startswith("."):
                        continue
                    try:
                        content = skill_file.read_text(encoding="utf-8", errors="ignore")
                    except Exception:
                        continue

                    meta = parse_frontmatter(content)
                    target_dir = skills_dir / s_name
                    if target_dir.exists():
                        shutil.rmtree(target_dir)
                    shutil.copytree(folder, target_dir)

                    index["skills"][s_name] = {
                        "name": meta.get("name", s_name),
                        "type": "skill",
                        "description": meta.get("description", "설명 없음"),
                        "source_repo": repo_url,
                        "source_name": repo_name,
                        "path": str(target_dir.relative_to(BASE_DIR))
                    }
                    repo_skills += 1

                # 2. Commands 수집 (commands/*.md, commands/*/COMMAND.md)
                for cmd_path in root.rglob("commands"):
                    if not cmd_path.is_dir():
                        continue
                    for f in cmd_path.glob("**/*"):
                        if f.is_file() and f.suffix in [".md", ".yaml", ".json"] and not f.name.startswith("."):
                            c_name = f.stem
                            if c_name.upper() == "COMMAND":
                                c_name = f.parent.name
                            try:
                                content = f.read_text(encoding="utf-8", errors="ignore")
                            except Exception:
                                continue

                            meta = parse_frontmatter(content)
                            target_file = commands_dir / f"{c_name}{f.suffix}"
                            shutil.copy2(f, target_file)

                            index["commands"][c_name] = {
                                "name": c_name,
                                "type": "command",
                                "description": meta.get("description", meta.get("title", f"Workflow command: {c_name}")),
                                "source_repo": repo_url,
                                "source_name": repo_name,
                                "path": str(target_file.relative_to(BASE_DIR))
                            }
                            repo_commands += 1

                # 3. Agents 수집 (agents/*.md, agents/*.json)
                for ag_path in root.rglob("agents"):
                    if not ag_path.is_dir():
                        continue
                    for f in ag_path.glob("**/*"):
                        if f.is_file() and f.suffix in [".md", ".json", ".yaml"] and not f.name.startswith("."):
                            a_name = f.stem
                            try:
                                content = f.read_text(encoding="utf-8", errors="ignore")
                            except Exception:
                                continue

                            meta = parse_frontmatter(content)
                            target_file = agents_dir / f"{a_name}{f.suffix}"
                            shutil.copy2(f, target_file)

                            index["agents"][a_name] = {
                                "name": a_name,
                                "type": "agent",
                                "description": meta.get("description", meta.get("title", f"Subagent persona: {a_name}")),
                                "source_repo": repo_url,
                                "source_name": repo_name,
                                "path": str(target_file.relative_to(BASE_DIR))
                            }
                            repo_agents += 1

                print(f"   ✅ [수집] Skills: {repo_skills}개 | Commands: {repo_commands}개 | Agents: {repo_agents}개")

    # 한국어 번역 캐시 자동 연동 및 보존
    cache_file = BASE_DIR / "translations_cache.json"
    if cache_file.exists():
        try:
            with open(cache_file, "r", encoding="utf-8") as cf:
                trans_cache = json.load(cf)
            for sec in ["skills", "commands", "agents"]:
                for k, item in index.get(sec, {}).items():
                    desc = item.get("description", "")
                    if desc in trans_cache:
                        item["description_ko"] = trans_cache[desc]
        except Exception:
            pass

    save_index(index)
    total_skills = len(index["skills"])
    total_commands = len(index["commands"])
    total_agents = len(index["agents"])

    print("\n" + "=" * 80)
    print(f"🎉 전체 수집 완료!")
    print(f"   🌟 Skills: {total_skills}개")
    print(f"   ⚡ Commands: {total_commands}개")
    print(f"   🤖 Agents: {total_agents}개")
    print(f"   📂 저장 디렉토리: {COLLECTED_DIR}")
    print("=" * 80 + "\n")

    # 자동으로 HTML 대시보드 재생성
    try:
        from export_html import generate_dashboard
        generate_dashboard()
    except Exception as e:
        pass



def list_assets(asset_type="all"):
    """수집된 에셋 목록 출력"""
    index = load_index()
    if not index or not any(index.values()):
        print("💡 수집된 에셋이 없습니다. 먼저 `python3 skill_collector.py sync`를 실행하세요.")
        return

    types_to_show = ["skills", "commands", "agents"] if asset_type == "all" else [asset_type + ("s" if not asset_type.endswith("s") else "")]

    for t in types_to_show:
        items = index.get(t, {})
        if not items:
            continue
        emoji = "🌟" if t == "skills" else ("⚡" if t == "commands" else "🤖")
        print(f"\n{emoji} [ {t.upper()} ] (총 {len(items)}개):")
        print("=" * 85)
        print(f"{'이름 (Name)':<28} | {'출처 (Source)':<20} | {'설명 (Description)'}")
        print("-" * 85)
        for name, info in sorted(items.items()):
            desc = info.get("description", "").split("\n")[0][:45]
            if len(info.get("description", "")) > 45:
                desc += "..."
            src = info.get("source_name", "local")[:18]
            print(f"{name:<28} | {src:<20} | {desc}")
        print("=" * 85)
    print()


def search_assets(query: str, asset_type="all"):
    """키워드로 Skills, Commands, Agents 통합 검색"""
    index = load_index()
    if not index:
        print("💡 수집된 에셋이 없습니다. 먼저 `python3 skill_collector.py sync`를 실행하세요.")
        return

    query_lower = query.lower()
    matches = []

    types_to_check = ["skills", "commands", "agents"] if asset_type == "all" else [asset_type + ("s" if not asset_type.endswith("s") else "")]

    for t in types_to_check:
        for name, info in index.get(t, {}).items():
            desc = info.get("description", "").lower()
            if query_lower in name.lower() or query_lower in desc:
                matches.append((t, name, info))

    if not matches:
        print(f"🔍 '{query}' 키워드에 해당하는 에셋을 찾을 수 없습니다.")
        return

    print(f"\n🔍 '{query}' 검색 결과 (총 {len(matches)}건):")
    print("=" * 85)
    for t, name, info in matches:
        emoji = "🌟 [SKILL]" if t == "skills" else ("⚡ [COMMAND]" if t == "commands" else "🤖 [AGENT]")
        print(f"{emoji} {name}  (출처: {info.get('source_name')})")
        print(f"   설명: {info.get('description')}")
        print(f"   경로: {info.get('path')}")
        print("-" * 85)
    print()


def show_info(name: str):
    """에셋 상세 내용 확인"""
    index = load_index()
    found_info = None
    asset_type = None

    for t in ["skills", "commands", "agents"]:
        if name in index.get(t, {}):
            found_info = index[t][name]
            asset_type = t
            break

    if not found_info:
        # 파일 경로 직접 탐색
        for sub in ["skills", "commands", "agents"]:
            p = COLLECTED_DIR / sub / name
            if p.exists():
                asset_type = sub
                found_info = {"path": str(p.relative_to(BASE_DIR))}
                break

    if not found_info:
        print(f"❌ 에셋 '{name}'을(를) 찾을 수 없습니다.")
        return

    path = BASE_DIR / found_info["path"]
    if path.is_dir():
        skill_md = path / "SKILL.md"
        if skill_md.exists():
            path = skill_md

    print(f"\n📄 [ {name} ({asset_type}) 상세 내용 ]:")
    print("=" * 85)
    print(path.read_text(encoding="utf-8", errors="ignore"))
    print("=" * 85 + "\n")


def install_asset(name: str, target: str = "global"):
    """스킬, 커맨드, 에이전트를 OpenCode/OpenWork 디렉토리에 설치"""
    index = load_index()
    found_info = None
    asset_type = None

    for t in ["skills", "commands", "agents"]:
        if name in index.get(t, {}):
            found_info = index[t][name]
            asset_type = t
            break

    if not found_info:
        print(f"❌ 설치할 에셋 '{name}'을(를) 찾을 수 없습니다.")
        return

    source_path = BASE_DIR / found_info["path"]
    base_target = DEFAULT_OPENCODE_GLOBAL_PATH if target == "global" else DEFAULT_OPENCODE_LOCAL_PATH
    dest_category_dir = base_target / asset_type
    dest_category_dir.mkdir(parents=True, exist_ok=True)

    if source_path.is_dir():
        dest_path = dest_category_dir / name
        if dest_path.exists():
            shutil.rmtree(dest_path)
        shutil.copytree(source_path, dest_path)
    else:
        dest_path = dest_category_dir / source_path.name
        shutil.copy2(source_path, dest_path)

    print(f"✅ {asset_type.upper()} '{name}' 설치 완료!")
    print(f"   위치: {dest_path}")
    print(f"   타입: {'전역 (Global)' if target == 'global' else '프로젝트 로컬 (Local)'}\n")


def add_source(repo_url: str, name: str = None, branch: str = "main"):
    sources = load_sources()
    if not name:
        name = repo_url.rstrip("/").split("/")[-1].replace(".git", "")

    for s in sources:
        if s.get("repo") == repo_url:
            print(f"⚠️ 이미 등록된 저장소입니다: {repo_url}")
            return

    sources.append({
        "name": name,
        "repo": repo_url,
        "branch": branch,
        "description": f"Repository source: {repo_url}"
    })
    save_sources(sources)
    print(f"✅ 소스 추가 완료: [{name}] {repo_url}")
    print("💡 `python3 skill_collector.py sync`를 실행하여 에셋을 수집하세요.")


def search_github(topic="opencode"):
    url = f"https://api.github.com/search/repositories?q={topic}+skills+agents&sort=stars&order=desc"
    req = urllib.request.Request(url, headers={"User-Agent": "OpenCode-Asset-Collector"})
    print(f"🌐 GitHub에서 '{topic}' 관련 최신 에이전트/스킬 저장소 탐색 중...")
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            items = data.get("items", [])
            print(f"\n⭐ GitHub 추천 저장소 목록 (총 {len(items)}개 발견):")
            print("=" * 85)
            for item in items[:10]:
                full_name = item.get("full_name")
                stars = item.get("stargazers_count")
                desc = item.get("description", "설명 없음")
                clone_url = item.get("clone_url")
                print(f"⭐ {stars:>4} stars | {full_name}")
                print(f"   URL: {clone_url}")
                print(f"   설명: {desc}\n")
    except Exception as e:
        print(f"❌ GitHub 탐색 실패: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="OpenCode & OpenWork Asset Collector - Skills, Commands, Agents 올인원 수집기"
    )
    subparsers = parser.add_subparsers(dest="command", help="실행할 명령")

    # sync
    subparsers.add_parser("sync", help="원격 저장소들로부터 Skills, Commands, Agents 수집 및 동기화")

    # list
    list_p = subparsers.add_parser("list", help="수집된 에셋 목록 조회")
    list_p.add_argument("--type", choices=["all", "skill", "command", "agent"], default="all", help="표시할 에셋 종류")

    # search
    search_p = subparsers.add_parser("search", help="키워드로 에셋 검색")
    search_p.add_argument("query", help="검색할 키워드 (예: rag, review, architect, docker)")
    search_p.add_argument("--type", choices=["all", "skill", "command", "agent"], default="all", help="검색 대상 에셋 종류")

    # info
    info_p = subparsers.add_parser("info", help="특정 에셋 상세 내용 출력")
    info_p.add_argument("name", help="확인할 에셋 이름")

    # install
    install_p = subparsers.add_parser("install", help="에셋을 OpenCode/OpenWork에 설치")
    install_p.add_argument("name", help="설치할 에셋 이름")
    install_p.add_argument("--target", choices=["global", "local"], default="global", help="설치 대상 위치")

    # add-source
    add_p = subparsers.add_parser("add-source", help="새로운 GitHub 저장소 추가")
    add_p.add_argument("repo_url", help="GitHub 저장소 URL")
    add_p.add_argument("--name", help="소스 식별 이름")
    add_p.add_argument("--branch", default="main", help="브랜치 이름 (기본: main)")

    # find-repos
    find_p = subparsers.add_parser("find-repos", help="GitHub에서 신규 에이전트/스킬 저장소 추천 검색")
    find_p.add_argument("--topic", default="opencode", help="검색 키워드/토픽 (기본: opencode)")

    # html
    subparsers.add_parser("html", help="수집된 에셋들을 인터랙티브 HTML 대시보드로 내보내기")

    args = parser.parse_args()

    if args.command == "sync":
        sync_assets()
    elif args.command == "html":
        from export_html import generate_dashboard
        generate_dashboard()
    elif args.command == "list":

        list_assets(args.type)
    elif args.command == "search":
        search_assets(args.query, args.type)
    elif args.command == "info":
        show_info(args.name)
    elif args.command == "install":
        install_asset(args.name, args.target)
    elif args.command == "add-source":
        add_source(args.repo_url, args.name, args.branch)
    elif args.command == "find-repos":
        search_github(args.topic)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
