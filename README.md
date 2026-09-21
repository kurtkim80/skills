# OpenCode & OpenWork Hub (C# Blazor WebAssembly)

인터넷(GitHub)의 AI 에이전트 커뮤니티로부터 수집한 6,186개 이상의 **스킬(Skills)**, **커맨드(Commands)**, **에이전트(Agents)**를 탐색, 자연어 AI 시맨틱 검색, 설치할 수 있는 웹 & CLI 플랫폼입니다.

👉 **실시간 라이브 웹 데모**: [https://kurtkim80.github.io/skills/](https://kurtkim80.github.io/skills/)

## ⚡ C# Blazor WebAssembly & In-Browser AI Engine
- **프론트엔드**: .NET 10 C# Blazor WebAssembly (Apple Human Interface Guidelines 스타일)
- **자연어 시맨틱 검색**: 
  - 검색창에 질문 입력 후 **Enter** 키 또는 버튼을 누를 때만 초고속 동작 (글자 입력 렉 제로)
  - 브라우저 내 경량 AI 모델(`all-MiniLM-L6-v2`)을 통해 자연어 쿼리를 384차원 벡터로 변환
  - **C# .NET SIMD 가속 (`System.Numerics.Tensors.TensorPrimitives.CosineSimilarity`)**으로 6,186개 에셋 전체를 밀리초(ms) 단위로 실시간 비교 및 유사도 랭킹 산출
- **🌐 GitHub 실시간 탐색 & DB 추가**:
  - 웹 화면 상단의 **[🌐 GitHub 탐색 & 추가]** 버튼을 통해 GitHub API로 전 세계의 최신 AI 에이전트 스킬 및 저장소를 실시간 검색
  - 검색된 저장소를 클릭 한 번(**➕ DB에 추가**)으로 내 카탈로그 DB에 즉시 등록 (브라우저 `localStorage`에 자동 영구 보관되어 메인 화면에서 바로 검색/설치 가능)
- **100% Client-Side**: 별도의 유료 API 서버 없이 브라우저 단독으로 완전히 구동되며, GitHub Pages에 정적 호스팅됩니다.

## 🤖 GitHub Actions 무인 자동 수집 파이프라인
- **스케줄 자동 실행**: 매일 한국 시간 자정(00:00 KST / 15:00 UTC)에 GitHub Actions 클라우드 러너가 자동으로 최신 스킬을 수집하고, AI 벡터를 갱신하여 GitHub Pages에 배포합니다.
- **수동 즉시 실행**: GitHub 저장소의 [Actions](https://github.com/kurtkim80/skills/actions) 탭에서 `Automated Skills Sync & Deploy` 워크플로우를 선택하고 **Run workflow** 버튼을 클릭하면 언제든 즉시 전체 수집 및 배포가 실행됩니다.
- **저장소 추가 시 자동 트리거**: `sources.json` 파일에 새로운 GitHub 저장소를 추가하여 푸시하면 워크플로우가 즉시 감지하여 자동 동기화를 시작합니다.

---

## 🌟 지원하는 에셋 종류

1. **🌟 Skills (`SKILL.md`)**: 특정 기술 분야(RAG, C#, Docker, Code Review 등)의 전문 지침과 표준 패턴
2. **⚡ Commands (`/commands/*.md`)**: 개발 라이프사이클을 단축하는 슬래시 커맨드 (기획, 구현 플랜, 테스팅, 회고 등)
3. **🤖 Agents (`/agents/*.md`)**: 특정 역할을 수행하는 페르소나 및 서브에이전트 설정

---

## 🚀 빠른 시작 가이드

### 1. 원격 저장소에서 전체 에셋 수집 / 동기화
```bash
python3 skill_collector.py sync
```
* `sources.json`에 등록된 저장소들을 Clone하여 `collected_assets/` 폴더에 분류하고 `assets_index.json` 색인을 생성합니다.

### 2. 수집된 에셋 목록 확인
```bash
# 전체 목록 조회
python3 skill_collector.py list

# 커맨드만 조회
python3 skill_collector.py list --type command

# 스킬만 조회
python3 skill_collector.py list --type skill

# 에이전트만 조회
python3 skill_collector.py list --type agent
```

### 3. 키워드로 통합 검색
```bash
# RAG 관련 검색
python3 skill_collector.py search rag

# 기획/플랜 관련 검색
python3 skill_collector.py search plan

# 코드 리뷰 관련 검색
python3 skill_collector.py search review
```

### 4. 에셋 상세 내용 확인
```bash
# 스킬 내용 확인
python3 skill_collector.py info rag-architect

# 커맨드 내용 확인
python3 skill_collector.py info create-implementation-plan
```

### 5. OpenCode / OpenWork에 설치
```bash
# 전역 설치 (~/.config/opencode/{skills|commands|agents}/)
python3 skill_collector.py install rag-architect --target global
python3 skill_collector.py install create-implementation-plan --target global

# 현재 프로젝트 로컬 설치 (.opencode/{skills|commands|agents}/)
python3 skill_collector.py install rag-architect --target local
```

### 6. 새로운 GitHub 저장소 추가
```bash
python3 skill_collector.py add-source https://github.com/someone/my-repo.git --name my-repo
python3 skill_collector.py sync
```

### 7. GitHub에서 신규 저장소 추천 탐색
```bash
python3 skill_collector.py find-repos --topic opencode
```

---

## 📁 디렉토리 구조

```
skills/
├── skill_collector.py        # 메인 CLI 실행 스크립트
├── sources.json              # 수집 대상 GitHub 저장소 설정
├── assets_index.json         # 전체 에셋 색인 및 메타데이터
├── collected_assets/         # 수집된 에셋들
│   ├── skills/               # 85개 이상의 스킬 (rag-architect, code-reviewer 등)
│   ├── commands/             # 26개 이상의 커맨드 (create-epic-plan, impl-plan 등)
│   └── agents/               # 서브에이전트 정의
└── rag-search-optimizer/     # 커스텀 Advanced RAG 최적화 스킬
```
