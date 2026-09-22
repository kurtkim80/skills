#!/usr/bin/env python3
import json
import os
import shutil
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SOURCES_FILE = BASE_DIR / "sources.json"
COLLECTED_DIR = BASE_DIR / "collected_assets" / "skills"
DATA_SKILLS_JSON = BASE_DIR / "data" / "skills.json"
BLAZOR_SKILLS_JSON = BASE_DIR / "BlazorHub" / "wwwroot" / "data" / "skills.json"

HARNESS_REPO_DIR = Path("/tmp/harness-skills")
ECC_REPO_DIR = Path("/tmp/ecc-skills")

from export_html import classify_category

def parse_frontmatter(content: str):
    metadata = {}
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            yaml_block = parts[1]
            # simple yaml parse
            current_key = None
            for line in yaml_block.splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if ":" in line:
                    k, v = line.split(":", 1)
                    k = k.strip()
                    v = v.strip().strip("'\"")
                    if v in [">", ">-", "|", "|-"]:
                        metadata[k] = ""
                        current_key = k
                    else:
                        metadata[k] = v
                        current_key = None
                elif current_key:
                    metadata[current_key] = (metadata[current_key] + " " + line).strip()
    if "description" not in metadata or not metadata["description"]:
        for line in content.splitlines():
            line = line.strip()
            if line and not line.startswith("---") and not line.startswith("#"):
                metadata.setdefault("description", line[:150])
                break
    return metadata

def main():
    print("🚀 Importing Harness & Agent Harness Skills...")
    
    # 1. Update sources.json
    with open(SOURCES_FILE, "r", encoding="utf-8") as f:
        sources = json.load(f)
        
    existing_source_names = {s["name"] for s in sources}
    new_sources = [
        {
            "name": "harness/harness-skills",
            "repo": "https://github.com/harness/harness-skills.git",
            "branch": "main",
            "skills_subpath": "skills",
            "description": "Official Harness.io CI/CD skills — 56+ specialized skills for pipelines, debug, chaos experiments, feature flags, cost analysis, and GitOps (⭐ 1.2k)"
        },
        {
            "name": "affaan-m/ECC",
            "repo": "https://github.com/affaan-m/ECC.git",
            "branch": "main",
            "skills_subpath": "skills",
            "description": "The Agent Harness Performance Optimization System — Skills, instincts, memory, harness evaluation, verification (⭐ 264k)"
        }
    ]
    for ns in new_sources:
        if ns["name"] not in existing_source_names:
            sources.append(ns)
            print(f"Added source: {ns['name']}")
            
    with open(SOURCES_FILE, "w", encoding="utf-8") as f:
        json.dump(sources, f, indent=2, ensure_ascii=False)
        
    # 2. Read existing data/skills.json
    with open(DATA_SKILLS_JSON, "r", encoding="utf-8") as f:
        items = json.load(f)
        
    existing_ids = {item["id"].lower() for item in items}
    existing_names = {item["name"].lower() for item in items}
    max_idx = max((item["idx"] for item in items), default=0)
    
    added_count = 0
    
    # 3. Process Harness.io skills
    harness_skills_dir = HARNESS_REPO_DIR / "skills"
    if harness_skills_dir.exists():
        for sdir in sorted(harness_skills_dir.iterdir()):
            if not sdir.is_dir():
                continue
            skill_name = sdir.name
            target_id = f"harness-{skill_name}"
            if target_id.lower() in existing_ids:
                continue
                
            skill_md = sdir / "SKILL.md"
            if not skill_md.exists():
                continue
                
            content = skill_md.read_text(encoding="utf-8", errors="replace")
            meta = parse_frontmatter(content)
            desc = meta.get("description", f"Harness.io official skill for {skill_name}")
            
            # Destination folder
            dest_dir = COLLECTED_DIR / target_id
            dest_dir.mkdir(parents=True, exist_ok=True)
            # Copy all files from sdir to dest_dir
            for item_path in sdir.iterdir():
                dest_item = dest_dir / item_path.name
                if item_path.is_dir():
                    shutil.copytree(item_path, dest_item, dirs_exist_ok=True)
                else:
                    shutil.copy2(item_path, dest_item)
                    
            cat_id, cat_label = classify_category(target_id, desc, "skill")
            
            max_idx += 1
            items.append({
                "idx": max_idx,
                "id": target_id,
                "name": target_id,
                "type": "skill",
                "catId": cat_id,
                "catLabel": cat_label,
                "desc": f"[Harness 공식] {desc}",
                "source": "https://github.com/harness/harness-skills.git",
                "repoUrl": f"https://github.com/harness/harness-skills/tree/main/skills/{skill_name}",
                "install": f"mkdir -p ~/.config/opencode/skills/{target_id} && curl -fsSL https://raw.githubusercontent.com/kurtkim80/skills/main/collected_assets/skills/{target_id}/SKILL.md -o ~/.config/opencode/skills/{target_id}/SKILL.md",
                "doc": f"collected_assets/skills/{target_id}/SKILL.md"
            })
            added_count += 1
            print(f"  + Added Harness skill: {target_id} ({cat_label})")
            
    # 4. Process ECC Agent Harness & Evaluation skills
    ecc_skills_dir = ECC_REPO_DIR / "skills"
    ecc_harness_targets = [
        "agent-harness-construction",
        "autonomous-agent-harness",
        "eval-harness",
        "gan-style-harness",
        "healthcare-eval-harness",
        "agent-eval",
        "agent-self-evaluation",
        "agentic-engineering",
        "agentic-os",
        "benchmark-methodology",
        "benchmark-optimization-loop",
        "agent-introspection-debugging",
        "iterative-retrieval"
    ]
    if ecc_skills_dir.exists():
        for skill_name in ecc_harness_targets:
            sdir = ecc_skills_dir / skill_name
            if not sdir.is_dir():
                continue
            if skill_name.lower() in existing_ids:
                continue
                
            skill_md = sdir / "SKILL.md"
            if not skill_md.exists():
                continue
                
            content = skill_md.read_text(encoding="utf-8", errors="replace")
            meta = parse_frontmatter(content)
            desc = meta.get("description", f"ECC Agent harness skill for {skill_name}")
            
            dest_dir = COLLECTED_DIR / skill_name
            dest_dir.mkdir(parents=True, exist_ok=True)
            for item_path in sdir.iterdir():
                dest_item = dest_dir / item_path.name
                if item_path.is_dir():
                    shutil.copytree(item_path, dest_item, dirs_exist_ok=True)
                else:
                    shutil.copy2(item_path, dest_item)
                    
            cat_id, cat_label = classify_category(skill_name, desc, "skill")
            max_idx += 1
            items.append({
                "idx": max_idx,
                "id": skill_name,
                "name": skill_name,
                "type": "skill",
                "catId": cat_id,
                "catLabel": cat_label,
                "desc": f"[Agent Harness/ECC] {desc}",
                "source": "https://github.com/affaan-m/ECC.git",
                "repoUrl": f"https://github.com/affaan-m/ECC/tree/main/skills/{skill_name}",
                "install": f"mkdir -p ~/.config/opencode/skills/{skill_name} && curl -fsSL https://raw.githubusercontent.com/kurtkim80/skills/main/collected_assets/skills/{skill_name}/SKILL.md -o ~/.config/opencode/skills/{skill_name}/SKILL.md",
                "doc": f"collected_assets/skills/{skill_name}/SKILL.md"
            })
            added_count += 1
            print(f"  + Added ECC Harness skill: {skill_name} ({cat_label})")

    # Save to data/skills.json & BlazorHub/wwwroot/data/skills.json
    with open(DATA_SKILLS_JSON, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False)
    with open(BLAZOR_SKILLS_JSON, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False)
        
    print(f"\n🎉 Successfully added {added_count} skills! Total items in catalog: {len(items)}")

if __name__ == "__main__":
    main()
