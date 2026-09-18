#!/usr/bin/env python3
"""
Automated Skill Collection, Indexing, Vector DB & Web Build Orchestrator
GitHub Actions 및 로컬 환경에서 원클릭으로 최신 에셋을 수집, 벡터화, Blazor 빌드까지 수행합니다.
"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def run_cmd(cmd, cwd=None):
    cmd_str = ' '.join(cmd) if isinstance(cmd, list) else cmd
    print(f"👉 Executing: {cmd_str}")
    res = subprocess.run(cmd, cwd=cwd or BASE_DIR, shell=isinstance(cmd, str), capture_output=True, text=True)
    if res.stdout:
        print(res.stdout)
    if res.stderr and res.returncode != 0:
        print(f"⚠️ Error (code {res.returncode}):\n{res.stderr}", file=sys.stderr)
    return res


def main():
    print("=" * 80)
    print("🤖 OpenCode & OpenWork Hub Auto-Sync Engine")
    print("=" * 80)

    # 1. 원격 저장소들로부터 최신 에셋 동기화
    print("\n=== [1/4] GitHub 저장소들로부터 최신 에셋 동기화 시작 ===")
    sync_res = run_cmd([sys.executable, "skill_collector.py", "sync"])
    if sync_res.returncode != 0:
        print("❌ skill_collector.py sync 실패")
        sys.exit(sync_res.returncode)

    index_file = BASE_DIR / "assets_index.json"
    if not index_file.exists():
        print("❌ assets_index.json 파일이 존재하지 않습니다.")
        sys.exit(1)

    with open(index_file, "r", encoding="utf-8") as f:
        assets_data = json.load(f)

    total_assets = sum(len(assets_data.get(k, {})) for k in ["skills", "commands", "agents"])
    print(f"📦 현재 총 수집된 에셋 수: {total_assets}개")

    # 2. 벡터 DB 최신 여부 확인 및 임베딩 갱신
    meta_file = BASE_DIR / "embeddings_meta.json"
    prev_count = 0
    if meta_file.exists():
        try:
            with open(meta_file, "r", encoding="utf-8") as f:
                prev_meta = json.load(f)
                prev_count = prev_meta.get("count", 0)
        except Exception:
            pass

    print(f"🔍 기존 벡터 DB 에셋 수: {prev_count}개")
    needs_embedding = (total_assets != prev_count) or not (BASE_DIR / "embeddings.bin").exists()

    if needs_embedding:
        print(f"\n=== [2/4] 신규 에셋 감지 ({total_assets - prev_count}개 차이) - 384차원 AI 벡터 임베딩 생성 중 ===")
        embed_res = run_cmd([sys.executable, "build_embeddings.py"])
        if embed_res.returncode != 0:
            print("❌ build_embeddings.py 실행 실패")
            sys.exit(embed_res.returncode)
    else:
        print("\n=== [2/4] 기존 벡터 DB가 최신 상태입니다. (임베딩 갱신 생략) ===")

    # 3. 초경량 카탈로그(data/skills.json) 갱신
    print("\n=== [3/4] 초경량 카탈로그(data/skills.json) 갱신 중 ===")
    from export_html import classify_category

    cache_file = BASE_DIR / "translations_cache.json"
    trans_cache = {}
    if cache_file.exists():
        try:
            with open(cache_file, "r", encoding="utf-8") as cf:
                trans_cache = json.load(cf)
        except Exception:
            pass

    items = []
    idx = 0
    for section in ["skills", "commands", "agents"]:
        for key, item in assets_data.get(section, {}).items():
            name = item.get("name", key)
            item_type = item.get("type", section[:-1])
            desc_en = item.get("description", "")
            desc_ko = item.get("description_ko") or trans_cache.get(desc_en) or desc_en
            cat_id, cat_label = classify_category(name, desc_ko, item_type)

            candidates = []
            if item_type == "skill":
                candidates += [
                    f"collected_assets/skills/{key}/SKILL.md",
                    f"collected_assets/skills/{name}/SKILL.md",
                    f"collected_assets/skills/{key}",
                    f"collected_skills/{key}/SKILL.md",
                    f"{key}/SKILL.md",
                ]
            elif item_type == "command":
                candidates += [
                    f"collected_assets/commands/{key}.md",
                    f"collected_assets/commands/{name}.md",
                    f"collected_assets/commands/{key}.yaml",
                    f"collected_assets/commands/{name}.yaml",
                ]
            else:
                candidates += [
                    f"collected_assets/agents/{key}.md",
                    f"collected_assets/agents/{name}.md",
                    f"collected_assets/agents/{key}.yaml",
                    f"collected_assets/agents/{name}.yaml",
                    f"collected_assets/agents/{key}.json",
                    f"collected_assets/agents/{name}.json",
                ]

            doc_path = ""
            for cand in candidates:
                cand_path = BASE_DIR / cand
                if cand_path.is_file():
                    doc_path = cand
                    break

            if item_type == "skill":
                install_cmd = f"mkdir -p ~/.config/opencode/skills/{name} && curl -fsSL https://raw.githubusercontent.com/kurtkim80/skills/main/collected_assets/skills/{name}/SKILL.md -o ~/.config/opencode/skills/{name}/SKILL.md"
            elif item_type == "command":
                ext = ".yaml" if doc_path.endswith(".yaml") else ".md"
                install_cmd = f"mkdir -p ~/.config/opencode/commands && curl -fsSL https://raw.githubusercontent.com/kurtkim80/skills/main/collected_assets/commands/{name}{ext} -o ~/.config/opencode/commands/{name}{ext}"
            else:
                ext = ".yaml" if doc_path.endswith(".yaml") else (".json" if doc_path.endswith(".json") else ".md")
                install_cmd = f"mkdir -p ~/.config/opencode/agents && curl -fsSL https://raw.githubusercontent.com/kurtkim80/skills/main/collected_assets/agents/{name}{ext} -o ~/.config/opencode/agents/{name}{ext}"

            items.append({
                "idx": idx,
                "id": key,
                "name": name,
                "type": item_type,
                "catId": cat_id,
                "catLabel": cat_label,
                "desc": desc_ko,
                "source": item.get("source_repo", item.get("source_name", "community")),
                "repoUrl": item.get("source_url", ""),
                "install": install_cmd,
                "doc": doc_path,
            })
            idx += 1

    skills_json_path = BASE_DIR / "data" / "skills.json"
    skills_json_path.parent.mkdir(parents=True, exist_ok=True)
    with open(skills_json_path, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False)

    blazor_skills_json = BASE_DIR / "BlazorHub" / "wwwroot" / "data" / "skills.json"
    blazor_skills_json.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(skills_json_path, blazor_skills_json)

    if (BASE_DIR / "embeddings.bin").exists():
        shutil.copyfile(BASE_DIR / "embeddings.bin", BASE_DIR / "BlazorHub" / "wwwroot" / "embeddings.bin")

    print(f"✅ data/skills.json 갱신 완료 ({skills_json_path.stat().st_size / (1024*1024):.2f} MB)")

    # 4. Git 변경사항 확인 후 필요 시 Blazor 빌드
    status_res = run_cmd(["git", "status", "--porcelain"])
    changed = False
    for line in status_res.stdout.splitlines():
        # Blazor 빌드에 영향을 주는 파일 변경 여부 확인
        if any(p in line for p in ["collected_assets", "data/skills.json", "embeddings.bin", "BlazorHub/Pages", "BlazorHub/Services"]):
            changed = True
            break

    if not changed:
        print("\n✨ 신규 또는 변경된 에셋이 없습니다. Blazor 재빌드를 건너뜁니다.")
        return

    print("\n=== [4/4] 변경사항 감지 - Blazor WebAssembly 배포 빌드 시작 ===")
    blazor_dir = BASE_DIR / "BlazorHub"
    pub_res = run_cmd(["dotnet", "publish", "-c", "Release", "-o", "publish"], cwd=blazor_dir)
    if pub_res.returncode != 0:
        print("❌ dotnet publish 실패")
        sys.exit(pub_res.returncode)

    pub_wwwroot = blazor_dir / "publish" / "wwwroot"
    if not pub_wwwroot.exists():
        print("❌ publish/wwwroot 디렉토리가 생성되지 않았습니다.")
        sys.exit(1)

    for item_name in ["_framework", "data", "js", "css", "BlazorHub.styles.css", "index.html"]:
        src = pub_wwwroot / item_name
        dst = BASE_DIR / item_name
        if src.is_dir():
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
        elif src.is_file():
            shutil.copyfile(src, dst)

    shutil.copyfile(BASE_DIR / "index.html", BASE_DIR / "404.html")
    (BASE_DIR / ".nojekyll").touch()

    # 불필요한 압축 파일 제거
    for ext in ["*.br", "*.gz"]:
        for p in BASE_DIR.glob(f"_framework/**/{ext}"):
            p.unlink(missing_ok=True)
        for p in BASE_DIR.glob(f"data/**/{ext}"):
            p.unlink(missing_ok=True)
        for p in BASE_DIR.glob(f"css/**/{ext}"):
            p.unlink(missing_ok=True)

    shutil.rmtree(blazor_dir / "publish", ignore_errors=True)
    print("\n🎉 자동 수집 및 배포 빌드 완료!")


if __name__ == "__main__":
    main()
