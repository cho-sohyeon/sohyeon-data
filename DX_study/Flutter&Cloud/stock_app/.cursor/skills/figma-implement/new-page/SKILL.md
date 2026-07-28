---
name: new-page
description: stock_app 에 새 화면을 추가할 때 파일 생성, 라우팅 등록, 기본 위젯 셋업까지 한 번에 안내합니다. 새 화면을 머리에 그린 직후에 호출하세요.
---

# New Page

`lib/` 폴더에 새 화면을 추가하는 표준 절차입니다.

## 1. 파일 생성
- `lib/{snake_case_name}_page.dart` 파일을 만든다.
- StatefulWidget 을 기본으로, 로딩·에러·데이터 세 상태를 모두 가질 수 있게 시작한다.

## 2. 라우팅 등록
- `lib/main.dart` 의 `_onGenerateRoute` switch 안에 새 case 를 추가한다.
- 라우트 이름은 `/{kebab-case-name}` 형태.

## 3. 기본 위젯 셋업
- Scaffold + AppBar + body 패턴.
- 색상 규칙은 `.cursor/rules/flutter-guidelines.mdc` Rule 을 따른다.
- 외부 데이터가 필요하면 `lib/api/` 의 함수를 호출한다.

## 4. 확인
- 라우트 이동이 동작하는지 한 번 클릭으로 확인.
- 로딩, 에러, 데이터 세 상태가 모두 그려지는지 확인.

## 입력 형식
사용자가 알려주는 정보:
- 페이지 이름 (한글)
- 라우트 경로
- 어떤 API 데이터를 보여줄지

위 정보를 받으면 1~4 단계를 차례로 수행한다.