# 회원 CRUD 실습 (Spring Boot + MyBatis + Oracle)

클래스, 필드, 생성자, 메서드를 배운 뒤 DB의 한 행이 Java 객체가 되는 과정을 확인하는 작은 REST API입니다.

## 수업에서 볼 흐름

```text
HTTP 요청 → MemberController → MemberService → MemberMapper → Oracle
                                                   ↕
                                         MemberMapper.xml(SQL)
```

- `Member` 클래스: `MEMBERS` 테이블의 컬럼과 필드가 1:1 대응합니다.
- 생성자: 기본 생성자는 MyBatis/JSON 변환에, 전체 필드 생성자는 객체 생성 예시에 사용합니다.
- Controller 메서드: HTTP 요청을 받습니다.
- Service 메서드: CRUD 흐름과 트랜잭션을 담당합니다.
- Mapper 메서드/XML: Java 메서드와 SQL을 연결합니다.

## 1. Oracle 준비

1. 관리자 계정으로 `sql/create-user.sql`을 실행합니다.
2. 생성된 `member_app` 계정으로 다시 접속하여 `sql/schema.sql`을 실행합니다.

기본 접속 정보는 Oracle 21c XE 기준입니다.

```text
URL      jdbc:oracle:thin:@//localhost:1521/XEPDB1
username member_app
password member1234
```

Oracle 11g XE는 `application-11g.yml`의 `jdbc:oracle:thin:@localhost:1521:XE`를 사용합니다. 실제 환경에서는 `DB_URL`, `DB_USERNAME`, `DB_PASSWORD` 환경 변수로 값을 바꾸세요.

## 2. 실행과 테스트

Windows PowerShell:

```powershell
.\gradlew.bat test
.\gradlew.bat bootRun
```

Oracle 11g XE 프로필:

```powershell
.\gradlew.bat bootRun --args="--spring.profiles.active=11g"
```

실행 후 Swagger UI 주소:

```text
http://localhost:8095/swagger-ui.html
```

각 API를 펼치고 `Try it out`을 누르면 브라우저에서 CRUD를 실행할 수 있습니다.

## 3. CRUD 호출

조회:

```powershell
Invoke-RestMethod http://localhost:8080/api/members
Invoke-RestMethod http://localhost:8080/api/members/1
```

등록:

```powershell
$body = @{ email = "park@example.com"; name = "박학생"; phone = "010-5555-6666" } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri http://localhost:8080/api/members -ContentType "application/json" -Body $body
```

수정:

```powershell
$body = @{ email = "park@example.com"; name = "박수정"; phone = "010-7777-8888" } | ConvertTo-Json
Invoke-RestMethod -Method Put -Uri http://localhost:8080/api/members/3 -ContentType "application/json" -Body $body
```

삭제:

```powershell
Invoke-RestMethod -Method Delete http://localhost:8080/api/members/3
```

## API 표

| HTTP | URL | 기능 | SQL |
|---|---|---|---|
| GET | `/api/members` | 전체 조회 | SELECT |
| GET | `/api/members/{id}` | 단건 조회 | SELECT |
| POST | `/api/members` | 등록 | INSERT |
| PUT | `/api/members/{id}` | 수정 | UPDATE |
| DELETE | `/api/members/{id}` | 삭제 | DELETE |
