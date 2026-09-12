#!/usr/bin/env python3
"""
Generate in-browser vector database (embeddings.bin & embeddings_meta.json)
for all skills, commands, and agents.

Uses 'sentence-transformers/all-MiniLM-L6-v2' via ONNX/fastembed (384 dimensions, normalized).
In-browser Transformers.js loads 'Xenova/all-MiniLM-L6-v2' to produce identical embeddings.
"""

import json
import time
import numpy as np
from pathlib import Path
from fastembed import TextEmbedding

BASE_DIR = Path(__file__).resolve().parent
INDEX_FILE = BASE_DIR / "assets_index.json"
CACHE_FILE = BASE_DIR / "translations_cache.json"
BIN_OUTPUT = BASE_DIR / "embeddings.bin"
META_OUTPUT = BASE_DIR / "embeddings_meta.json"


def build_embeddings():
    if not INDEX_FILE.exists():
        print("❌ assets_index.json 파일이 없습니다.")
        return

    print("📖 assets_index.json 로드 중...")
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 번역 캐시 로드
    trans_cache = {}
    if CACHE_FILE.exists():
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as cf:
                trans_cache = json.load(cf)
        except Exception:
            pass

    # 커스텀 RAG 스킬 추가 확인
    custom_rag = BASE_DIR / "rag-search-optimizer" / "SKILL.md"
    if custom_rag.exists() and "rag-search-optimizer" not in data.get("skills", {}):
        data.setdefault("skills", {})["rag-search-optimizer"] = {
            "name": "rag-search-optimizer",
            "type": "skill",
            "description": "RAG(Retrieval-Augmented Generation) 시스템의 검색 정확도 향상, 하이브리드 검색, 리랭킹, 청킹 전략, Contextual Retrieval 등 검색 파이프라인 최적화",
            "description_ko": "RAG(Retrieval-Augmented Generation) 시스템의 검색 정확도 향상, 하이브리드 검색, 리랭킹, 청킹 전략, Contextual Retrieval 등 검색 파이프라인 최적화",
            "source_repo": "local/custom",
            "source_name": "local-custom",
            "path": "rag-search-optimizer"
        }

    # 전체 에셋 순회 및 텍스트 구성
    items_to_embed = []
    item_ids = []

    for section in ["skills", "commands", "agents"]:
        for key, item in data.get(section, {}).items():
            name = item.get("name", key)
            item_type = item.get("type", section[:-1])
            desc_en = item.get("description", "")
            desc_ko = item.get("description_ko") or trans_cache.get(desc_en) or desc_en

            # 이름 + 타입 + 영문 설명 + 한글 설명 결합하여 시맨틱 풍부도 극대화
            text_parts = [name, f"[{item_type}]"]
            if desc_en:
                text_parts.append(desc_en[:400])
            if desc_ko and desc_ko != desc_en:
                text_parts.append(desc_ko[:400])

            combined_text = " - ".join(text_parts).strip()
            items_to_embed.append(combined_text)
            item_ids.append(key)

    total_count = len(items_to_embed)
    print(f"🚀 총 {total_count}개 에셋 벡터 임베딩 생성 시작...")
    print("   🤖 모델: sentence-transformers/all-MiniLM-L6-v2 (384차원)")

    t0 = time.time()
    model = TextEmbedding("sentence-transformers/all-MiniLM-L6-v2")

    # 배치 단위 임베딩 생성 (배치 크기 128)
    vectors = []
    batch_size = 128
    processed = 0

    for i in range(0, total_count, batch_size):
        batch = items_to_embed[i:i + batch_size]
        batch_vecs = list(model.embed(batch))
        vectors.extend(batch_vecs)
        processed += len(batch)
        if processed % 512 == 0 or processed == total_count:
            elapsed = time.time() - t0
            speed = processed / elapsed if elapsed > 0 else 0
            print(f"   ⏳ 진행률: {processed}/{total_count} ({(processed/total_count*100):.1f}%) - {speed:.1f}개/초")

    # NumPy float32 2D 배열 변환
    vectors_array = np.array(vectors, dtype=np.float32)
    dim = vectors_array.shape[1]

    # 정규화 재확인 (L2 norm = 1.0)
    norms = np.linalg.norm(vectors_array, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    vectors_array = vectors_array / norms

    # 1. 바이너리 파일 저장 (Float32Array)
    vectors_array.tofile(str(BIN_OUTPUT))
    bin_size_mb = BIN_OUTPUT.stat().st_size / (1024 * 1024)

    # 2. 메타데이터 JSON 저장
    meta = {
        "count": total_count,
        "dim": dim,
        "model": "Xenova/all-MiniLM-L6-v2",
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "ids": item_ids
    }
    with open(META_OUTPUT, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False)

    total_time = time.time() - t0
    print("\n" + "=" * 80)
    print("🎉 브라우저 벡터 데이터베이스 빌드 완료!")
    print(f"   📦 총 벡터 수: {total_count}개")
    print(f"   📐 벡터 차원: {dim}D (float32)")
    print(f"   💾 바이너리 파일: {BIN_OUTPUT} ({bin_size_mb:.2f} MB)")
    print(f"   📄 메타데이터 파일: {META_OUTPUT}")
    print(f"   ⏱️ 총 소요 시간: {total_time:.1f}초 (초당 {total_count/total_time:.1f}개 처리)")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    build_embeddings()
