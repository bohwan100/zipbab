# 🤖 집밥봇 (ZipbabBot) - 자동화 식단 및 장바구니 구축 시스템

> **1인 가구 자취생을 위한 한 달 20~30만 원 예산 맞춤 식단 & 쿠팡 4주 분할 스마트 장바구니 올인원 솔루션**

---

## 📂 프로젝트 구조 (Clean Architecture)

```text
📁 zipbab/ (antigravity 폴더)
│
├── 🌐 [Core Web & Deployment] (GitHub Pages & Render 배포 보장 루트 파일)
│   ├── index.html                   # 🏠 메인 포털 랜딩 페이지 (CDN 배포)
│   ├── survey.html                  # 📋 고객 맞춤 8대 항목 설문지 페이지
│   ├── clients.html                 # 👥 고객 관리자 매니저 대시보드 (최종본 📌 0순위 고정)
│   ├── server.py                    # ⚡ Render 백엔드 API 서버 (포트 10000, 설문/고객 생성/삭제)
│   ├── github_sync.py               # 🔄 GitHub Pages 실시간 자동 커밋 & 영구 배포 모듈
│   ├── Procfile                     # 🚀 Render 웹 프로세스 구동 명령 (web: python3 server.py)
│   ├── render.yaml                  # ⚙️ Render 인프라 설정
│   ├── requirements.txt             # 📦 Python 필수 라이브러리 목록
│   ├── AGENTS.md                    # 📜 에이전트 작업 원칙 및 기배포 고객 20개 동결 규칙
│   └── restore_golden_state.py      # ⏪ 황금 스냅샷 (2026-10-06 클린본) 즉시 복원 도구
│
├── 📁 clients/                      # 👤 배포된 21개 고객 전용 포털 & 식단 (동결 보호)
│   ├── 최종본_100세_2/               # 📌 상시 검증 전용 마스터 포털 (107종 레시피 풀 & 원팬 10분컷)
│   ├── 김태영_23/                   # 👤 고객 맞춤 포털 (한식/일식/양식)
│   └── ... (기타 19개 고객 폴더 완전 동결)
│
├── 📁 generator/                    # 🧠 핵심 개인화 생성 엔진
│   ├── recipe_engine.py             # 🍳 107개 레시피 풀, 식약처 19대 알레르기 NLP, 30일 식단 편성 엔진
│   ├── build_client.py              # 🏗️ 고객 설문 기반 4개 HTML/JSON 자동 빌더
│   ├── storage_engine.py            # ❄️ 구매 식재료 100% 동적 보관 백과 생성기
│   ├── pantry_master.json           # 🧂 기본 양념 5종 및 팬트리 공제 데이터베이스
│   └── google_form_script.js        # 📝 설문 폼 연동 스크립트
│
├── 📁 templates/                    # 🎨 고객 포털 생성용 정규 Jinja/HTML 템플릿
│   ├── portal.html                  # 🏠 고객 메인 포털 템플릿 (index.html로 생성)
│   ├── recipes.html                 # 🍳 30일 식단표 & 셰프 조리법 템플릿
│   ├── cart.html                    # 🛒 쿠팡 4주 분할 장바구니 템플릿
│   └── storage.html                 # ❄️ 식재료 보관법 백과 템플릿
│
├── 📁 assets/                       # 🖼️ 정적 미디어 및 자산
│   ├── qr/                          # 📱 설문/포털 QR 코드 이미지 보관소
│   └── extension/                   # 🧩 장바구니 원클릭 담기 크롬 익스텐션 배포본
│
├── 📁 tools/                        # 🛠️ 쿠팡 파트너스 및 보조 자동화 도구
│   ├── coupang_engine.py            # 쿠팡 장바구니 자동화 엔진
│   ├── coupang_partners.py          # 쿠팡 파트너스 API 딥링크 생성기
│   └── automation/                  # 쿠팡 로그인 헬퍼, 애플스크립트, 노션 업로더 등
│
├── 📁 snapshots/                    # 🛡️ 황금 상태 스냅샷 보관소 (golden-v1.0-clean)
│   └── golden_state/
│
├── 📁 scratch/                      # 🧪 개발 검증 및 테스트 작업 공간
│   ├── generate_clients_dashboard.py # 👥 관리자 대시보드(clients.html) 동적 생성기 (server.py 연동)
│   └── rebuild_requested_clients.py  # 🔄 지목 고객 단독 재빌드 스크립트
│
└── 📁 archive/                      # 📦 구버전 프로토타입 및 과거 프로젝트 아카이브
    ├── legacy_html/                 # 과거 정적 프로토타입 (card_news_viewer.html 등)
    └── legacy_marketing/            # 스레드 바이럴 마케팅 레거시 파일
```

---

## ⚡ 핵심 기능 및 기술 아키텍처

### 1. 107종 마스터 레시피 & 자취생 원팬 10분컷 조리법
* **4대 요리 완벽 밸런스**: 한식 33종, 일식 25종, 중식 24종, 양식 25종 (총 107종).
* **요리 초보 맞춤화**: 복잡한 조리 단계 및 조리도구 최소화, '원팬(One-pan) 10~15분 컷'으로 조리법 및 꿀팁 100% 최적화.
* **셰프 인물명 배제**: 특정 셰프/인물 명칭을 제거하고 '셰프 스타일 만능 레시피'로 표준화.

### 2. 식약처 19대 식품 알레르기 NLP 온톨로지 엔진
* 정규식 단어 경계(`\b` / `re.search`) 정밀 매칭 적용으로 오작동(False Positive) 원천 방지 (예: '소고기' 제외 시 '소시지' 오인 제외 방지 등).
* 어류/패류/갑각류/난류/견과류 등 유의어 자동 확장 필터링.

### 3. 팬트리 공제 & 쿠팡 파트너스 수익 최적화 로켓프레시
* **팬트리 공제**: 집에 이미 보유한 양념(진간장, 식용유, 설탕, 고춧가루, 쌀 등)을 자동 식별하여 장바구니에서 0원 처리.
* **파트너스 정규 링크**: 리뷰 최상위, 로켓배송, 1인용 소용량 단품 위주의 깔끔한 `link.coupang.com` 연결.

### 4. 20개 기배포 고객 파일 동결(Freeze) 보호 원칙
* 시스템 업데이트 및 레시피 풀 확장은 **[1] 새로 제출되는 신규 고객**과 **[2] 상시 검증용 `최종본 !!!`(`clients/최종본_100세_2`)**에만 적용.
* 기배포 20개 고객 파일은 사용자가 명시적으로 지목하여 수정을 요청했을 때만 단독 수정.

---

## 🚀 로컬 실행 및 사용 가이드

### 1. 로컬 개발 서버 실행
```bash
python3 server.py
```
* 서버 실행 후 브라우저 접속:
  - 설문지: `http://localhost:10000/survey.html`
  - 관리자 대시보드: `http://localhost:10000/clients.html`

### 2. 관리자 대시보드 갱신
```bash
python3 scratch/generate_clients_dashboard.py
```

### 3. 황금 스냅샷 즉시 복원 (필요 시)
```bash
python3 restore_golden_state.py
```
