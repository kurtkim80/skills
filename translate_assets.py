#!/usr/bin/env python3
"""
Translate asset descriptions in assets_index.json into Korean.
Saves Korean translations to assets_index.json (as description_ko) and translations_cache.json.
"""

import json
import ssl
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INDEX_FILE = BASE_DIR / "assets_index.json"
CACHE_FILE = BASE_DIR / "translations_cache.json"

ctx = ssl._create_unverified_context()


def translate_text(text: str) -> str:
    if not text or not text.strip():
        return ""

    # 이미 한글이 많은 경우 그대로 반환
    korean_chars = len([c for c in text if "\uac00" <= c <= "\ud7a3"])
    if korean_chars > len(text) * 0.3:
        return text

    clean_text = text.strip()
    # 긴 텍스트는 앞 1500자까지 번역 (상세 설명 기준)
    query_text = clean_text[:1500]

    for client in ["dict-chrome-ex", "gtx"]:
        try:
            url = f"https://translate.googleapis.com/translate_a/single?client={client}&sl=en&tl=ko&dt=t&q=" + urllib.parse.quote(query_text)
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                },
            )
            with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                translated = "".join([s[0] for s in data[0] if s and s[0]])
                if translated.strip():
                    return translated.strip()
        except Exception:
            time.sleep(0.3)
            continue

    # Fallback to MyMemory
    try:
        url = f"https://api.mymemory.translated.net/get?q={urllib.parse.quote(query_text[:450])}&langpair=en|ko"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, context=ctx, timeout=8) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["responseData"]["translatedText"]
    except Exception:
        pass

    return text


def main():
    if not INDEX_FILE.exists():
        print("❌ assets_index.json 파일이 없습니다.")
        return

    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 캐시 로드
    cache = {}
    if CACHE_FILE.exists():
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                cache = json.load(f)
            print(f"📦 기존 번역 캐시 로드: {len(cache)}개 항목")
        except Exception as e:
            print(f"⚠️ 캐시 로드 실패: {e}")

    # 번역할 작업 목록 수집
    tasks = []
    for section in ["skills", "commands", "agents"]:
        for key, item in data.get(section, {}).items():
            desc = item.get("description", "")
            if desc and desc.strip():
                tasks.append((section, key, desc))

    total = len(tasks)
    print(f"🚀 총 {total}개 에셋 상세설명 한국어 번역 시작...")

    to_translate = []
    for section, key, desc in tasks:
        if desc in cache and cache[desc].strip():
            # 캐시에 이미 있음
            data[section][key]["description_ko"] = cache[desc]
        else:
            to_translate.append((section, key, desc))

    print(f"   - 이미 번역됨: {total - len(to_translate)}개")
    print(f"   - 신규 번역 대상: {len(to_translate)}개")

    if to_translate:
        completed = 0
        batch_size = 50

        # 병렬 번역 실행 (동시 8개 워커)
        with ThreadPoolExecutor(max_workers=8) as executor:
            future_to_item = {
                executor.submit(translate_text, desc): (section, key, desc)
                for section, key, desc in to_translate
            }

            for future in as_completed(future_to_item):
                section, key, desc = future_to_item[future]
                try:
                    result = future.result()
                    if result and result.strip():
                        cache[desc] = result
                        data[section][key]["description_ko"] = result
                    else:
                        cache[desc] = desc
                        data[section][key]["description_ko"] = desc
                except Exception as e:
                    cache[desc] = desc
                    data[section][key]["description_ko"] = desc

                completed += 1
                if completed % 50 == 0 or completed == len(to_translate):
                    print(f"   ⏳ 번역 진행률: {completed}/{len(to_translate)} ({(completed/len(to_translate)*100):.1f}%)")
                    # 중간 캐시 및 인덱스 저장
                    with open(CACHE_FILE, "w", encoding="utf-8") as f:
                        json.dump(cache, f, ensure_ascii=False, indent=2)
                    with open(INDEX_FILE, "w", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)

    # 최종 저장
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("✅ 모든 상세 설명 한국어 번역 및 저장 완료!")
    print(f"   - 저장 위치: {INDEX_FILE}")
    print(f"   - 캐시 위치: {CACHE_FILE}")


if __name__ == "__main__":
    main()
