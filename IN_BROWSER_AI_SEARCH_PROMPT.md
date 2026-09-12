# 🧠 브라우저 내장(In-Browser) AI 시맨틱 벡터 검색 구현 가이드 & LLM 프롬프트

이 문서는 **백엔드 서버나 유료 API 없이, GitHub Pages / S3 / Vercel 등의 정적 웹 환경에서 100% 브라우저(WebAssembly) 기반으로 동작하는 AI 시맨틱 벡터 검색 시스템**의 아키텍처 정리 및 다른 웹 프로젝트에 바로 이식할 수 있는 **LLM 주입용 마스터 프롬프트**입니다.

---

## 📌 1. 아키텍처 및 핵심 원리 요약

```text
[Phase 1: 빌드 / 배포 단계 (Python)]
데이터 소스 (JSON/DB) ──▶ fastembed (all-MiniLM-L6-v2) ──▶ embeddings.bin (바이너리 float32)
                                                                 │ (정적 파일 호스팅)
                                                                 ▼
[Phase 2: 브라우저 런타임 (WebAssembly / ONNX)]
방문자 검색어 입력 ──▶ Transformers.js (all-MiniLM-L6-v2) ──▶ 질의 벡터 생성 (384D)
                                                                 │
                                                                 ▼
                 embeddings.bin과 1:1 Dot Product (코사인 유사도 연산: 2~3ms)
                                                                 │
                                                                 ▼
                 유사도 점수 내림차순 정렬 및 화면 렌더링 (Top-K 결과)
```

### 🌟 핵심 기술 사양 및 강점
1. **서버 및 DB 비용 0원**: 백엔드 API, 파이썬 서버, 클라우드 벡터 DB(Pinecone, Qdrant 등)가 일절 필요 없음.
2. **초고속 연산 (2~3ms)**: 정규화된(L2 Norm = 1.0) 단위 벡터이므로, 코사인 유사도는 단순 내적(Dot Product) 연산으로 치환됨. V8 JIT / SIMD 덕분에 6,000~10,000개 데이터 비교가 3ms 이내 완료.
3. **가벼운 네트워크 전송량**: 6,000개 데이터 기준 384차원 Float32Array 크기는 약 9MB (Gzip 압축 시 약 5~6MB).
4. **온디바이스 프라이버시**: 사용자의 모든 검색어가 외부 서버로 전송되지 않고 브라우저 메모리 안에서만 처리됨.
5. **타이핑 최적화**: 입력 중 매 글자마다 연산하지 않고, `Enter` 키를 눌렀을 때만 1회 단독 실행하여 타이핑 렉 원천 차단.

---

## 🚀 2. 다른 웹 프로젝트 적용을 위한 LLM 프롬프트 (복사하여 사용)

> **💡 사용법**: 아래 프롬프트 전체를 복사하여 **ChatGPT, Claude, Cursor, Antigravity, OpenCode** 등 AI 코딩 어시스턴트에 그대로 붙여넣고, 본인의 데이터 파일명(예: `products.json`, `articles.json`, `faq.json`)만 지정하시면 AI가 완벽한 벡터 검색 시스템을 구현해 줍니다.

```markdown
# Role & Objective
너는 브라우저 내장(In-Browser) WebAssembly 벡터 데이터베이스 및 AI 시맨틱 검색 전문 웹 개발자다.
백엔드 서버나 외부 유료 API 없이, 100% 정적 웹 호스팅(GitHub Pages, Vercel, S3 등) 환경에서 동작하는 "초경량 AI 시맨틱 벡터 검색 기능"을 내 프로젝트에 구현해줘.

# Target Data
- 입력 데이터 파일: [여기에 데이터 파일명 입력, 예: data.json 또는 items.json]
- 각 항목은 id, title, description, category, tags 등의 텍스트 필드를 가짐.

# Tech Stack & Requirements
1. **임베딩 모델 규격**:
   - 모델: `sentence-transformers/all-MiniLM-L6-v2` (384차원)
   - 사전 빌드: Python `fastembed` (또는 `sentence-transformers`)
   - 브라우저 런타임: `@xenova/transformers` (Transformers.js v2 via CDN)

2. **구현 요구사항 (2-Phase Architecture)**:

   ### Phase 1: 오프라인 벡터 빌더 스크립트 (`build_embeddings.py`)
   - 입력 데이터 파일을 읽어 검색 대상 텍스트(이름 + 카테고리 + 설명 등)를 결합
   - `fastembed.TextEmbedding("sentence-transformers/all-MiniLM-L6-v2")`로 384차원 단위 벡터 생성
   - L2 정규화(Norm = 1.0) 확인 후, 순수한 `np.float32` 2D 바이너리 버퍼로 변환하여 `embeddings.bin` 파일로 저장 (`tofile()`)
   - 각 벡터의 순서와 원본 데이터 매핑을 위한 `embeddings_meta.json` 생성

   ### Phase 2: 프론트엔드 자바스크립트 구현 (`app.js` 또는 `<script>`)
   - **엔진 초기화 (`initAiEngine`)**:
     - `fetch('embeddings.bin')`을 통해 ArrayBuffer를 받아 `new Float32Array(buf)`로 메모리에 마운트
     - Transformers.js의 `pipeline('feature-extraction', 'Xenova/all-MiniLM-L6-v2', { quantized: true })` 로드
     - 비동기 로딩 타이밍 이슈를 방지하기 위해 단일 `aiInitPromise` 패턴(Promise Caching) 적용
     - 모델 다운로드 진행률(`progress_callback`)을 UI 상단 상태바에 시각화
   - **시맨틱 검색 실행 (`runAiSearch(query)`)**:
     - 검색창에서 사용자가 글자를 쓰는 동안에는 검색을 수행하지 않고, **`Enter` 키를 눌렀을 때만** 단독 1회 실행할 것
     - 사용자의 검색어를 Transformers.js로 384차원 정규화 벡터(`qVec`)로 변환 (`{ pooling: 'mean', normalize: true }`)
     - 브라우저 메모리의 전체 벡터와 Dot Product(내적)를 순회 계산하여 유사도 점수 산출
     - 유사도 점수 내림차순으로 정렬하여 상위 Top-K 결과 렌더링
     - 검색 결과 카드에 `🧠 AI 매칭 XX%` 형태의 점수 뱃지 표시
   - **입력창 리셋**:
     - 사용자가 검색어를 백스페이스로 완전히 비웠을 때만 전체 목록으로 자동 복원할 것

3. **산출물**:
   - `build_embeddings.py` 완전한 파이썬 스크립트 코드
   - 프론트엔드 HTML / CSS / JS 코드 (또는 React / Vue 컴포넌트 형태)
   - 실행 및 배포 가이드
```

---

## 💻 3. 핵심 참조 코드 스니펫

### (1) Python 사전 빌더 (`build_embeddings.py`)
```python
import json
import numpy as np
from pathlib import Path
from fastembed import TextEmbedding

# 1. 데이터 로드
with open("data.json", "r", encoding="utf-8") as f:
    items = json.load(f)

texts = [f"{item['title']} - {item.get('description', '')}" for item in items]

# 2. 384차원 정규화 벡터 추출
model = TextEmbedding("sentence-transformers/all-MiniLM-L6-v2")
vectors = list(model.embed(texts, batch_size=128))

# 3. 바이너리 저장
vectors_array = np.array(vectors, dtype=np.float32)
norms = np.linalg.norm(vectors_array, axis=1, keepdims=True)
norms[norms == 0] = 1.0
vectors_array = vectors_array / norms
vectors_array.tofile("embeddings.bin")

# 4. 메타데이터 저장
with open("embeddings_meta.json", "w", encoding="utf-8") as f:
    json.dump({"count": len(items), "dim": 384, "ids": [x["id"] for x in items]}, f)
```

### (2) 브라우저 자바스크립트 (`index.html`)
```javascript
let aiLoaded = false;
let aiInitPromise = null;
let aiVectors = null; // Float32Array
let aiPipelineInstance = null;
const aiScores = new Map();

// 1. 엔진 초기화
function initAiEngine() {
  if (aiInitPromise) return aiInitPromise;
  aiInitPromise = (async () => {
    // embeddings.bin 로드
    const res = await fetch('embeddings.bin');
    aiVectors = new Float32Array(await res.arrayBuffer());

    // Transformers.js WASM 로드
    const { pipeline, env } = await import('https://cdn.jsdelivr.net/npm/@xenova/transformers@2.17.2');
    env.allowLocalModels = false;
    aiPipelineInstance = await pipeline('feature-extraction', 'Xenova/all-MiniLM-L6-v2', { quantized: true });
    aiLoaded = true;
    return true;
  })();
  return aiInitPromise;
}

// 2. 검색어 벡터화 및 코사인 유사도 랭킹
async function runAiSearch(query) {
  if (!aiLoaded) await initAiEngine();
  
  // 질의 벡터 추출
  const out = await aiPipelineInstance(query.trim(), { pooling: 'mean', normalize: true });
  const qVec = out.data; // Float32Array(384)

  // 6,000+개 벡터와 초고속 Dot Product
  const D = 384;
  aiScores.clear();
  for (let i = 0; i < DATA.length; i++) {
    let dot = 0;
    const off = i * D;
    for (let j = 0; j < D; j++) {
      dot += qVec[j] * aiVectors[off + j];
    }
    aiScores.set(DATA[i].id, dot);
  }

  renderResults(); // aiScores 기준 내림차순 정렬 렌더링
}

// 3. 엔터 키 이벤트 리스너
document.getElementById('searchInput').addEventListener('keydown', (e) => {
  if (e.key === 'Enter') {
    e.preventDefault();
    const val = e.target.value.trim();
    if (val) runAiSearch(val);
  }
});
```
