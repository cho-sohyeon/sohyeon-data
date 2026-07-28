--실습1 
SELECT DISTINCT GENDER 
    FROM EMP; 

--실습2
SELECT DISTINCT DEPT_NO, JOB_TITLE 
    FROM EMP;

--실습3
SELECT NAME AS 이름 
    , GENDER AS 성별 
    , BIRTH_DATE AS 생년월일 
    FROM EMP; 
    
/*
자료형을 실험하기 위한 테이블을 생성합니다. 
컬럼은 문자컬럼, 숫자컬럼 , 날짜컬럼이 있고
각각 VARCHAR2(10) , NUMBER , DATE 자료형을 지정했습니다. 
*/ 

CREATE TABLE 자료형검증 (  
문자컬럼 VARCHAR2(10) ,             
숫자컬럼 NUMBER       ,              
날짜컬럼 DATE  
) ;                  

/*
테이블에 데이터를 삽입하는 INSERT 문법입니다. 
하나씩 실행해봅시다. 
*/
INSERT INTO 자료형검증 ( 문자컬럼 , 숫자컬럼 , 날짜컬럼 ) VALUES ( 'A' , 1 , SYSDATE );  
INSERT INTO 자료형검증 ( 문자컬럼 , 숫자컬럼 , 날짜컬럼 ) VALUES ( 'A' , '3살' , SYSDATE );  
INSERT INTO 자료형검증 ( 문자컬럼 , 숫자컬럼 , 날짜컬럼 ) VALUES ( 'A' , 3 , 1 );  --오류!
INSERT INTO 자료형검증 ( 문자컬럼 , 숫자컬럼 , 날짜컬럼  ) VALUES ( 'BB' , '3' , SYSDATE ); 

COMMIT; --데이터 변경사항을 영구 반영해주는 문법

SELECT * FROM 자료형검증 ;

--사칙연산 
SELECT PRODUCT_NAME
     , CATEGORY_NAME
     , PRICE         AS 정상가 
     , PRICE * 0.7   AS 중고상품판매가
     , PRICE * 0.9   AS 전시품판매가
     , 10000         AS 만원쿠폰
     , PRICE - 10000 AS 만원쿠폰적용판매가
     , STOCK_QTY 
  FROM LG_PRODUCT ;
  

--연결연산 ||
SELECT NAME || '(직급:' || JOB_TITLE || ')' AS "2024년이후입사자"
  FROM EMP  
 WHERE HIRE_DATE >= '20240101'; -- 2024년 1월1일 이후 입사한 대상만 필터링

--실습 1 
SELECT PRODUCT_NAME
    , PRICE 
    , STOCK_QTY 
    , PRICE * STOCK_QTY AS TOTAL_STOCK_AMOUNT
    , PRICE * STOCK_QTY / 1000 AS "총판매금액(단위:천원)" 
 FROM LG_PRODUCT ;
 
--실습(심화) 
SELECT PRODUCT_NAME
    , PRICE AS 기존가격
    , CASE WHEN PRICE >= 2000000 THEN 100000
           WHEN PRICE >= 1000000 THEN 50000
           WHEN PRICE >= 500000 THEN 20000
           ELSE 0 
      END AS 할인가격 
    ,PRICE - CASE WHEN PRICE >= 2000000 THEN 100000
                  WHEN PRICE >= 1000000 THEN 50000
                  WHEN PRICE >= 500000 THEN 20000
                  ELSE 0
             END AS 최종판매금액 
FROM LG_PRODUCT ; 


--SUBSTR 
SELECT EMP_ID 
    , BIRTH_DATE 
    , SUBSTR(BIRTH_DATE, 1, 4) AS 출생연도
 FROM EMP ; 
 

SELECT PAYLOAD_JSON
    , REPLACE(PAYLOAD_JSON , ':' , '=')
    , REPLACE(REPLACE(PAYLOAD_JSON , ':' , '=') , '"' , '')
 FROM LG_PRODUCT_STATE_LOG; --디바이스상태로그 
 
 
SELECT PAYLOAD_JSON
    , INSTR(PAYLOAD_JSON , 'messageId')
 FROM LG_DEVICE_STATE_LOG ; 
 
SELECT PAYLOAD_JSON
    , INSTR(PAYROAD_JSON , 'timestamp') 
    , SUBSTR(PAYROAD_JSON , INSTR(PAYROAD_JSON , 'timestamp')+12, 25)
 FROM LG_DEVICE_STATE_LOG ;
 
 4. LG_DEVICE_STATE_LOG의 PAYLOAD_JSON에서 데이터가 들어오는 시점을 
   분석할 수 있도록  timestamp 영역만 출력해주세요.  
   즉, 다음과 같이 데이터가 있다면 timestamp만 출력되어야 합니다. 
   
   {
    "logType":"DEVICE_STATE",
    "apiName":"GET /devices/{deviceId}/state",
    "messageId":"oBg7mvcgS7rHE5C84ZgfFE",
    "timestamp":"2026-03-01T00:00:00+09:00",
    "deviceId":"6095278c24fa0ad6dd48e55030626ee0ddae89169ae54aaa072886b4a5f57f9c",
    "memberId":"MEMBER38",
    "productId":"P006",
    "response": {"meta":  
                        {
                          "deviceType":"DEVICE_AIR_PURIFIER",
                          "modelName":"FS061PSHA",
                          "alias":"Kids Purifier"
                         },
                 "operation":
                         {
                          "power":"ON",
                          "runState":"STANDBY",
                          "mode":"SLEEP",
                          "fanSpeed":"LOW"
                          },
                   "air":{ "pm25":19.1,
                           "airQuality":"NORMAL",
                           "humidityPct":39.9
                         },
                   "consumable":{"filterLifePct":81.7},
                   "usage":{"instantPowerW":22.4},
                   "diagnosis":{ "errorCode":"0000",
                                 "networkStatus":"ONLINE" }
                  }
  }

SELECT PAYLOAD_JSON
     , INSTR(PAYLOAD_JSON , 'timestamp') AS timestamp문자열위치값
     , SUBSTR(PAYLOAD_JSON, INSTR(PAYLOAD_JSON , 'timestamp')+12 , 25) AS timestamp값만추출 
  FROM LG_DEVICE_STATE_LOG;

--혹은 json_value라면 다음과 같이도 제공함 
--데이터 형식이 JSON_VALUE일 경우 KEY가 timestamp인 것을 찾아서 값을 반환 
--반환 타입을 varchar2(30) 형태로 반환 
SELECT PAYLOAD_JSON
     , JSON_VALUE(PAYLOAD_JSON, '$.apiName' RETURNING VARCHAR2(30)) AS timestamp값만추출 
  FROM LG_DEVICE_STATE_LOG;
  
  
  
SELECT TO_NUMBER('1') FROM DUAL ; -- 문자형('1')을 숫자형(1) 로 형변환해 출력 
SELECT TO_CHAR(1) FROM DUAL ;       --숫자형(1)을 문자형('1') 로 형변환해 출력 
SELECT TO_CHAR(SYSDATE , 'YYYY/MM/DD HH24:MI') FROM DUAL ; 
SELECT TO_CHAR(SYSDATE , 'YYYYMMDD') FROM DUAL ;

SELECT TO_DATE('20230101' , 'YYYY/MM/DD') FROM DUAL ; 
SELECT TO_DATE('2023010114' , 'YYYY/MM/DD HH24') FROM DUAL ; 
SELECT TO_DATE('20230101141212' , 'YYYY/MM/DD HH24:MI:SS') FROM DUAL; 

/* 포매팅은 중요한 개념입니다 */ 
YYYY : 연도 4자리 
MM : 월 2자리 
DD : 일 2자리 
HH : 시간 (12시간제)
HH24 : 시간 (24시간제) 
MI : 분 (0~59)
SS : 초 (0~59) 

--실습 1 
SELECT EMP_ID 
    ,BIRTH_DATE
    ,SUBSTR (BIRTH_DATE, 1, 4) AS 년 
    ,SUBSTR (BIRTH_DATE, 5, 2) AS 월 
    ,SUBSTR (BIRTH_DATE, 7, 2) AS 일 
 FROM EMP ; 
 
--실습2 
SELECT RATING,   
    ,SUBSTR (REVIEW_TEXT, 1, 10) || '...' AS 리뷰요약
    ,REVIEW_TEXT AS 원본리뷰 
 FROM PRODUCT_REVIEW ;
 
 --실습3
 SELECT DEPT_EN_NAME 
    , UPPER(DEPT_EN_NAME) AS 대문자부서명 
  FROM DEPT ;
  
---WHERE---
SELECT * 
  FROM EMP
 WHERE JOB_TITLE = '팀장' ; 
 
--실습 1 
SELECT * 
  FROM DEPT 
WHERE DEPT_NO = 'D003' ; 

--실습 2 
SELECT * 
  FROM EMP 
WHERE NAME = '김영희' ; 

--실습 3 
SELECT * 
  FROM LG_PRODUCT 
WHERE STOCK_QTY <= 200 ; 

--실습 4 
SELECT * 
  FROM PRODUCT_REVIEW
WHERE LENGTH(REVIEW_TEXT) > 1000 ;

SELECT * FROM EMP
 WHERE JOB_TITLE = '선임' 
    OR JOB_TITLE = '팀장' ;
    
AND : 앞뒤조건모두 참, 더 세밀한 행을 가져올 수 있음 
OR : 앞뒤조건 중 하나라도 참이면 참, 가져올 데이터가 더 확장 

SELECT * 
  FROM LG_DEVICE
 WHERE ACTIVE_FLAG = 'Y'
  AND INSTALL_ROOM = 'LIVING_ROOM'; 

SELECT * 
  FROM PRODUCT_REVIEW 
WHERE PRODUCT_ID = 'P003' 
 AND RATING <= 3; 


--실습1 
SELECT * 
  FROM LG_MEMBER
WHERE HOUSEHOLD_TYPE = 'FAMILY'
 AND HOUSEHOLD_SIZE >= 4 ; 
 
 
--실습2
SELECT PRODUCT_ID, PRODUCT_NAME, MODEL_NAME
  FROM LG_PRODUCT
WHERE BASE_POWER_WATTS >= 40 
 OR ACTIVE_POWER_WATTS >= 700 ;
 
--실습3 
SELECT *
  FROM EMP
WHERE GENDER = 'M'
 AND RETIRE_YN = 'Y'
 AND JOB_TITLE = '팀장' ; 
 
--실습4
SELECT * 
  FROM LG_PRODUCT 
WHERE PRICE >= 1000000
 AND PRICE <= 2000000 
 AND STOCK_QTY >= 200
 AND STOCK_QTY <= 400 ;
 
 
--실습5
SELECT * 
  FROM EMP 
WHERE RETIRE_YN = 'Y'
 AND(JOB_TITLE = '선임' OR JOB_TITLE = '팀장') ;
 
--부정 조건 

SELECT * 
  FROM EMP 
  WHERE NOT JOB_TITLE = '선임' ;

SELECT * 
  FROM EMP 
WHERE JOB_TITLE != '선임' ; 

SELECT * 
 FROM EMP
WHERE JOB_TITLE <> '선임' ;


--실습 1 
SELECT * 
  FROM LG_MEMBER 
WHERE CITY_NAME != '서울'
 AND CITY_NAME != '경기'
 AND BIRTH_YEAR >= 1990 
 AND GENDER_CODE = 'M' ;
 
 
--실습 2
SELECT * 
  FROM LG_MEMBER 
WHERE CHILD_FLAG = 'N'
 AND PET_FLAG = 'Y' ; 
 
 
-- NULL 은 정상적인 비교 연산이 불가능 
-- IS NULL : NULL 인 데이터만 뽑음 
-- IS NOT NULL : NULL이 아닌 데이터가 뽑음 
SELECT * FROM EMP WHERE RETIRE_DATE IS NULL ; 
SELECT * FROM EMP WHERE RETIRE_DATE IS NOT NULL ; \


--IN 연산자
SELECT * 
  FROM DEPT 
WHERE DEPT_NO IN ('D001', 'D002', 'D004');

SELECT * 
  FROM EMP 
WHERE JOB_TITLE IN ('선임', '팀장') ; 

--BETWEEN 연산자 
SELECT * 
  FROM EMP 
WHERE JOB_TITLE = '선임' 
 AND RETIRE_YN = 'N'
 AND LEAVE_AMOUNT BETWEEN 5 AND 10; 

SELECT * 
  FROM LG_PRODUCT
WHERE PRICE BETWEEN 1000000 AND 2000000
 AND STOCK_QTY BETWEEN 200 AND 400 ; 


--LIKE 연산자 
SELECT * 
  FROM EMP 
WHERE NAME LIKE '%하%';

SELECT * 
  FROM LG_PRODUCT 
WHERE PRODUCT_NAME LIKE 'LG 퓨리케어%';
  
SELECT * 
  FROM LG_DIVICE 
WHERE DEVICE_ALIAS LIKE '%Refrigerator%'; 


--날짜 데이터로 조회하는 방법 
SELECT * 
  FROM EMP 
WHERE RETIRE_YN = 'Y' 
  AND TO_CHAR(RETIRE_DATE, 'YYYY') = '2025' ; 
  
  
  
SELECT * 
  FROM EMP 
WHERE RETIRE_YN = 'Y'
 AND TO_CHAR(RETIRE_DATE, 'YYYY') = '2025' ; 
 
SELECT * 
  FROM EMP 
 WHERE RETIRE_YN = 'Y' 
  AND RETIRE_DATE >= TO_DATE('20250101000000' , 'YYYYMMDDHH24MISS')
  AND RETIRE_DATE <= TO_DATE('20251231235959' , 'YYYYMMDDHH24MISS');
    
SELECT * 
  FROM EMP 
 WHERE HIRE_DATE >= '20240101' ;
 
WITH TET AS ( 
SELECT '999' AS NUM1 FROM DUAL UNION ALL
SELECT '900' AS NUM1 FROM DUAL UNION ALL 
SELECT '1000' AS NUM1 FROM DUAL) 
SELECT * FROM TET ORDER BY TO_NUMBER(NUM1) DESC; 

--실습1 
SELECT EMP_ID, NAME, HIRE_DATE, LEAVE_AMOUNT
  FROM EMP 
WHERE HIRE_DATE >= TO_DATE('2024-01-01', 'YYYY-MM-DD')
 AND JOB_TITLE IN ('선임', '수석') ;
 
 
--실습2 
SELECT MEMBER_ID, MEMBER_NAME, CITY_NAME, DISTRICT_NAME, JOINED_AT
  FROM LG_MEMBER 
WHERE TO_CHAR(JOINED_AT, 'YYYYMM') = '202502' 
 AND CITY_NAME = '서울' ; 
 
 
--실습3 
SELECT EMP_ID, NAME, JOB_TITLE, BIRTH_DATE
  FROM EMP 
WHERE RETIRE_YN = 'N'
 AND (NAME LIKE '우%'
 OR NAME LIKE '주%'
 OR NAME LIKE '최%'
 OR NAME LIKE '강%') ; 
 
--실습4 
SELECT * 
  FROM PRODUCT_REVIEW
WHERE TO_CHAR(CREATED_AT, 'YYYYMM' = '202508'
 AND RATING <= 3 ; 
 
 
---FROM---
SELECT A.EMP_ID
     , A.NAME
     , B.DEPT_NO  --이 컬럼은 EMP,DEPT 모두 가지고 있으므로 오류 발생
     , B.DEPT_NAME 
  FROM EMP A
     , DEPT B ;
     
-- 주의사항 ! 한번 별칭 썼으면 그 이후에는 별칭만 써야함 

--> 실행 순서 : FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY


DROP TABLE 회원; 
DROP TABLE 회원연락처 ;

CREATE TABLE 회원 ( 
    회원ID VARCHAR2(20) PRIMARY KEY , 
      이름 VARCHAR2(50) 
);
INSERT INTO 회원 
SELECT 'A0001' , '동동일' FROM DUAL UNION ALL 
SELECT 'A0002' , '동동이' FROM DUAL UNION ALL 
SELECT 'A0003' , '동동삼' FROM DUAL UNION ALL
SELECT 'A0005' , '동동오' FROM DUAL ;

CREATE TABLE 회원연락처 ( 
    회원ID VARCHAR2(20) ,
    구분코드 VARCHAR2(20) , 
    연락처 VARCHAR2(30) ,
    PRIMARY KEY(회원ID , 구분코드 ) 
);

INSERT INTO 회원연락처
SELECT 'A0001' , '휴대폰' , '010-111-1111' FROM DUAL UNION ALL 
SELECT 'A0001' , '집전화' , '062-111-1111' FROM DUAL UNION ALL 
SELECT 'A0002' , '집전화' , '062-222-2222' FROM DUAL UNION ALL 
SELECT 'A0004' , '휴대폰' , '010-4444-4444' FROM DUAL ;

COMMIT; 


SELECT * FROM 회원 ; 
SELECT * FROM 회원연락처 ; 


SELECT * 
  FROM 회원, 회원연락처 
 WHERE 회원.회원ID = 회원연락처.회원ID 
  AND 회원.회원ID = 'A0001'
  AND 회원연락처.구분코드 = '휴대폰' ;
  
  
-실습1
SELECT A.EMP_ID
    , A.NAME
    , B.DEPT_NAME
  FROM EMP A 
JOIN DEPT B ON A.DEPT_NO = B.DEPT_NO
 WHERE A.RETIRE_YN = 'Y' ; 
 
 
--실습2 

--실습3 
SELECT A. 