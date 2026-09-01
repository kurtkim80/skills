#!/usr/bin/env python3
"""
수집된 전체 에셋(스킬, 커맨드, 에이전트)을 카테고리별로 분류하여
[카테고리, 이름, 설명, 링크] 4개 항목을 포함한 텍스트 파일(skills_by_category.txt)로 내보냅니다.
"""

import json
from pathlib import Path
from collections import defaultdict
from export_html import CATEGORY_DEFS, classify_category

BASE_DIR = Path(__file__).resolve().parent
INDEX_FILE = BASE_DIR / "assets_index.json"
TXT_OUTPUT = BASE_DIR / "skills_by_category.txt"


def export_to_txt():
    if not INDEX_FILE.exists():
        print("❌ assets_index.json 파일이 없습니다.")
        return

    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 카테고리별 아이템 수집
    categorized = defaultdict(list)
    total_count = 0

    for item_type, items in [("skill", data.get("skills", {})),
                             ("command", data.get("commands", {})),
                             ("agent", data.get("agents", {}))]:
        for key, item in items.items():
            name = item.get("name", key)
            desc_en = item.get("description", "")
            desc_ko = item.get("description_ko", desc_en)
            desc_final = desc_ko.strip() if desc_ko else desc_en.strip()
            
            repo_url = item.get("source_repo", "")
            if repo_url.endswith(".git"):
                repo_url = repo_url[:-4]
            
            rel_path = item.get("path", "")
            # 상세 링크 (GitHub 원본 저장소 또는 특정 경로)
            link = repo_url if repo_url else f"https://github.com/kurtkim80/skills/tree/main/{rel_path}"

            cat_id, cat_label = classify_category(name, desc_en, item_type)
            
            categorized[cat_id].append({
                "name": name,
                "type": item_type,
                "cat_label": cat_label,
                "desc": desc_final,
                "link": link
            })
            total_count += 1

    lines = []
    lines.append("=" * 90)
    lines.append("       OpenCode & OpenWork AI 에이전트 스킬 / 커맨드 / 에이전트 카탈로그")
    lines.append(f"       총 에셋 수: {total_count}개 | 분류: 13개 카테고리 | 100% 한국어 상세 설명 포함")
    lines.append("=" * 90)
    lines.append("")

    # 목차 생성
    lines.append("📌 [ 카테고리별 목차 ]")
    for cid, clabel, _ in CATEGORY_DEFS:
        if cid == "all":
            continue
        items_in_cat = categorized.get(cid, [])
        lines.append(f"  • {clabel}: {len(items_in_cat)}개")
    lines.append("")
    lines.append("=" * 90)
    lines.append("")

    # 카테고리별 본문 생성
    for cid, clabel, _ in CATEGORY_DEFS:
        if cid == "all":
            continue

        items_in_cat = categorized.get(cid, [])
        if not items_in_cat:
            continue

        # 이름순 정렬
        items_in_cat.sort(key=lambda x: x["name"].lower())

        lines.append("")
        lines.append("■" * 45)
        lines.append(f"【 카테고리: {clabel} 】 (총 {len(items_in_cat)}개)")
        lines.append("■" * 45)
        lines.append("")

        for idx, item in enumerate(items_in_cat, 1):
            type_tag = f"[{item['type'].upper()}]"
            lines.append(f"{idx:03d}. 이름: {item['name']} {type_tag}")
            lines.append(f"     카테고리: {item['cat_label']}")
            lines.append(f"     설명: {item['desc']}")
            lines.append(f"     링크: {item['link']}")
            lines.append("-" * 90)

    output_text = "\n".join(lines)
    with open(TXT_OUTPUT, "w", encoding="utf-8") as f:
        f.write(output_text)

    print(f"✅ 카테고리별 TXT 파일 생성 완료: {TXT_OUTPUT}")
    print(f"   총 {total_count}개 에셋 포함, 총 {len(lines)}줄")


if __name__ == "__main__":
    export_to_txt()
