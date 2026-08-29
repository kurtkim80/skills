# OpenCode & OpenWork Asset Collector (Skills, Commands, Agents)

인터넷(GitHub)의 OpenCode / OpenWork 커뮤니티 저장소들로부터 **스킬(Skills)**, **커맨드(Commands)**, **에이전트(Agents)**를 자동으로 탐색, 수집, 검색, 설치하는 올인원 CLI 도구입니다.

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
