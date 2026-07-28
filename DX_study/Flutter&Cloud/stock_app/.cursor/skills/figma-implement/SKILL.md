---
name: figma-implement
description: "Figma 디자인 노드를 보고 Flutter 코드로 옮긴다. 디자인 토큰/위젯 카탈로그가 정의도어 있으면 따르고, 없으면 Material 기본 위젯과 raw 값으로 구현한다. 사용자가 'Figma로 ~~ 화면 만들어줘', 'design 구현', '/figma-implement <figma url>' 라고 말하면 호출."
---

# figma-implement — Figma → Flutter

Figma 디자인을 Flutter 코드로 옮기는 작업의 **반복 부분만** 자동화한다. 디자인 토큰·위젯 카탈로그·디렉토리 구조는 **현장 감지**해 따르고, 없으면 기본값으로 간다.

## 입력 인자

`$ARGUMENTS` 자유 텍스트에서 다음을 추출:

1. **Figma URL** (필수, 1개 이상) — `figma.com/...`을 모두 잡는다.
2. **대상 파일 경로** (선택) — `lib/`를 포함하는 경로. 없으면 새 파일을 생성한다.

추출이 모호하면 진행 전에 사용자에게 한 문장으로 확인.

## 워크플로우

### Step 1 — Figma 디자인 가져오기

각 URL에 대해 (가능하면 병렬로):

1. Figma MCP의 `get_design_context`로 노드의 React+Tailwind 코드+힌트 받기. **참고용**.
2. `get_screenshot`로 시각 참조.
3. 노드 구조가 복잡하면 `get_metadata`.

받은 결과에서 **시각적 핵심 값들을 즉시 메모**: 색상 hex, 폰트 크기·굵기, padding/gap 픽셀, border radius, 그림자.

### Step 2 — Flutter 코드 작성

- **단일 책임 화면**: 큰 build는 `_buildHeader()`, `_buildBody()` 등으로 쪼개기.
- **재사용 위젯 우선**: Step 1에서 발견한 카탈로그 위젯이 있으면 우선 사용.
- **토큰 매핑**: 토큰이 있으면 raw hex 대신 토큰. 없으면 hex 그대로 + 자주 반복되는 색·간격은 `const`로 추출.

### Step 3 — 셀프 체크

코드 작성 후 아래 내용 빠르게 점검:

1. trailing comma (2+ args)
2. spread-if 패턴 (`if (x) ...[ ... ]`)
3. `const` 생성자 가능한 곳마다
4. `_build...` 메서드 분리
5. raw hex가 너무 흔어져 있지 않은지

더 깊은 리뷰가 필요하면 사용자가 `/multi-review`를 호출하게 둔다.

### Step 4 — 최종 보고

3줄로 끝낸다:

1. 만든/수정한 파일 (markdown link)
2. Figma에서 발견됐지만 처리하지 못한 것 (빠진 자산, 매칭 안 된 색 등)
3. 다음 추천 액션

## 하지 말 것

- **디자인 토큰 파일을 임의로 새로 만들지 말 것**. 없으면 raw 값 그대로.
- **새 디렉토리/네이밍 컨벤션을 들여오지 말 것**.
- **빠진 자산을 추측해 더미로 채우지 말 것**. 보고하고 멈춘다.
- **상태관리/라우팅을 바꾸지 말 것**. 이 스킬은 UI 구현 한정.