--1. 인라인뷰 (LG_PRODUCT, PRODUCT_REVIEW를 상품별로 카운트한 인라인뷰 조인) 

SELECT A.PRODUCT_ID 
    , A.PRODUCT_NAME
    , NVL(B.리뷰개수, 0) AS 리뷰개수 
  FROM LG_PRODUCT A 
  LEFT JOIN ( 
                SELECT PRODUCT_ID 
                    , COUNT(*) AS 리뷰개수 
                  FROM PRODUCT_REVIEW
                  GROUP BY PRODUCT_ID 
                  ) B
            ON (A.PRODUCT_ID = B.PRODUCT_ID) ;
            
--2. 스칼라서브쿼리를 이용 

SELECT PRODUCT_ID 
    , PRODUCT_NAME
    , ( 
        SELECT COUNT(*) 
          FROM PRODUCT_REVIEW 
        WHERE PRODUCT_ID = LG_PRODUCT.PRODUCT_ID) AS REVIEW_COUNT 
    FROM LG_PRODUCT ; 


SELECT * 
  FROM PRODUCT_REVIEW 
WHERE PRODUCT_ID = 'P002' 

--문제2
SELECT DEPT_NAME 
    , DEPT_EN_NAME 
    , (
    SELECT COUNT(*) 
        FROM EMP
    WHERE RETIRE_YN = 'N'
     AND DEPT_NO = DEPT.DEPT_NO) AS 부서별인원수 
  FROM DEPT ;
  
--문제3 
SELECT GU_NAME
    , TOTAL_RESIDENT_POP
    , ( 
        SELECT SUM(SALES_AMT)
          FROM STG_SALES_GU_20254 S
        WHERE S.GU_NAME = R.GU_NAME
        ) AS 자치구별판매총액 
```sql
--1. 정답
SELECT PRODUCT_NAME 
     , PRICE
     , ( 
        SELECT COUNT(*)
          FROM PRODUCT_REVIEW
         WHERE PRODUCT_ID = LG_PRODUCT.PRODUCT_ID ) AS 리뷰개수
  FROM LG_PRODUCT
 ORDER BY PRICE DESC;

--2. 
SELECT DEPT_NAME 
     , DEPT_EN_NAME
     , (SELECT COUNT(*) 
          FROM EMP
         WHERE DEPT.DEPT_NO = DEPT_NO
           AND RETIRE_YN = 'N' ) AS 부서별인원수 
  FROM DEPT ;
  
SELECT * 
  FROM 회원 ; 
  
SELECT * 
  FROM 회원연락처 ; 
  
SELECT * 
  FROM 회원 
WHERE EXISTS ( 
                SELECT 'X' 
                  FROM 회원연락처 
                WHERE 회원ID = 회원.회원ID 
            ) ; 
            

SELECT PRODUCT_NAME 
    , CATEGORY_NAME
    , PRICE 
    , ROW_NUMBER() OVER (ORDER BY PRICE DESC) AS RN 
  FROM LG_PRODUCT ;

SELECT PRODUCT_NAME
    , CATEGORY_NAME
    , PRICE 
  FROM LG_PRODUCT 
ORDER BY CATEGORY_NAME , PRICE DESC ; 


--예제 2. 카테고리별로 가장 비싼 상품 보기 
SELECT * 
  FROM (
        SELECT PRODUCT_NAME 
             , CATEGORY_NAME
             , PRICE 
             , ROW_NUMBER() OVER ( PARTITION BY CATEGORY_NAME ORDER BY PRICE DESC ) AS RN 
           FROM LG_PRODUCT 
         )
WHERE RN = 2 ;

SELECT GENDER, JOB_TITLE, COUNT(*) 
  FROM EMP 
GROUP BY CUBE(GENDER, JOB_TITLE) 


SELECT PRODUCT_NAME
    , CATEGORY_NAME
    , PRICE
    , SUM(PRICE) OVER() AS 모든상품의금액합
    , SUM(PRICE) OVER(PARTITION BY CATEGORY_NAME) AS 상품별금액합 
  FROM LG_PRODUCT ; 
  
SELECT MEMBER_ID 
    , PRODUCT_ID 
    , USED_DATE 
    , USE_AMOUNT_KWH
    , SUM(USE_AMOUNT_KWH) OVER(ORDER BY USED_DATE) AS 합산KWH 
  FROM LG_ENERGY_USAGE_DAILY
  
  
---윈도우 함수 
--문제1 
SELECT CATEGORY_NAME 
    , PRODUCT_NAME 
    , PRICE
    , ROW_NUMBER() OVER ( PARTITION BY CATEGORY_NAME ORDER BY PRICE DESC ) AS RN 
  FROM LG_PRODUCT ;


--문제2 
SELECT * 
    FROM ( 
            SELECT CATEGORY_NAME
                 , PRODUCT_NAME 
                 , PRICE 
                 , ROW_NUMBER() OVER ( PARTITION BY CATEGORY_NAME ORDER BY PRICE DESC ) AS RN
                 FROM LG_PRODUCT
                ) 
WHERE RN = 1; 