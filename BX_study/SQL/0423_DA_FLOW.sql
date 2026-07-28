CREATE TABLE raw_unmanned_store (
    seq_no      VARCHAR2(20),
    gu_name     VARCHAR2(50),
    store_name  VARCHAR2(300),
    biz_type    VARCHAR2(100)
);

CREATE TABLE raw_flow_gu (
    base_yq_code          VARCHAR2(20),
    gu_code               VARCHAR2(20),
    gu_name               VARCHAR2(50),
    total_flow_pop        VARCHAR2(50),
    male_flow_pop         VARCHAR2(50),
    female_flow_pop       VARCHAR2(50),
    age10_flow_pop        VARCHAR2(50),
    age20_flow_pop        VARCHAR2(50),
    age30_flow_pop        VARCHAR2(50),
    age40_flow_pop        VARCHAR2(50),
    age50_flow_pop        VARCHAR2(50),
    age60_over_flow_pop   VARCHAR2(50),
    time_00_06_flow_pop   VARCHAR2(50),
    time_06_11_flow_pop   VARCHAR2(50),
    time_11_14_flow_pop   VARCHAR2(50),
    time_14_17_flow_pop   VARCHAR2(50),
    time_17_21_flow_pop   VARCHAR2(50),
    time_21_24_flow_pop   VARCHAR2(50),
    mon_flow_pop          VARCHAR2(50),
    tue_flow_pop          VARCHAR2(50),
    wed_flow_pop          VARCHAR2(50),
    thu_flow_pop          VARCHAR2(50),
    fri_flow_pop          VARCHAR2(50),
    sat_flow_pop          VARCHAR2(50),
    sun_flow_pop          VARCHAR2(50)
);

CREATE TABLE raw_resident_gu (
    base_yq_code                    VARCHAR2(20),
    gu_code                         VARCHAR2(20),
    gu_name                         VARCHAR2(50),
    total_resident_pop              VARCHAR2(50),
    male_resident_pop               VARCHAR2(50),
    female_resident_pop             VARCHAR2(50),
    age10_resident_pop              VARCHAR2(50),
    age20_resident_pop              VARCHAR2(50),
    age30_resident_pop              VARCHAR2(50),
    age40_resident_pop              VARCHAR2(50),
    age50_resident_pop              VARCHAR2(50),
    age60_over_resident_pop         VARCHAR2(50),
    male_age10_resident_pop         VARCHAR2(50),
    male_age20_resident_pop         VARCHAR2(50),
    male_age30_resident_pop         VARCHAR2(50),
    male_age40_resident_pop         VARCHAR2(50),
    male_age50_resident_pop         VARCHAR2(50),
    male_age60_over_resident_pop    VARCHAR2(50),
    female_age10_resident_pop       VARCHAR2(50),
    female_age20_resident_pop       VARCHAR2(50),
    female_age30_resident_pop       VARCHAR2(50),
    female_age40_resident_pop       VARCHAR2(50),
    female_age50_resident_pop       VARCHAR2(50),
    female_age60_over_resident_pop  VARCHAR2(50),
    total_household_cnt             VARCHAR2(50),
    apt_household_cnt               VARCHAR2(50),
    non_apt_household_cnt           VARCHAR2(50)
);

CREATE TABLE raw_income_consume_gu (
    base_yq_code                VARCHAR2(20),
    dong_code                   VARCHAR2(20),
    dong_name                   VARCHAR2(50),
    avg_month_income_amt        VARCHAR2(50),
    income_bracket_code         VARCHAR2(20),
    total_spend_amt             VARCHAR2(50),
    grocery_spend_amt           VARCHAR2(50),
    clothing_shoes_spend_amt    VARCHAR2(50),
    living_goods_spend_amt      VARCHAR2(50),
    medical_spend_amt           VARCHAR2(50),
    transport_spend_amt         VARCHAR2(50),
    education_spend_amt         VARCHAR2(50),
    entertainment_spend_amt     VARCHAR2(50),
    leisure_culture_spend_amt   VARCHAR2(50),
    other_spend_amt             VARCHAR2(50),
    food_spend_amt              VARCHAR2(50)
);

CREATE TABLE raw_store_gu (
    base_yq_code          VARCHAR2(20),
    gu_code               VARCHAR2(20),
    gu_name               VARCHAR2(50),
    svc_code              VARCHAR2(30),
    svc_name              VARCHAR2(100),
    store_cnt             VARCHAR2(50),
    similar_store_cnt     VARCHAR2(50),
    open_rate             VARCHAR2(50),
    open_store_cnt        VARCHAR2(50),
    close_rate            VARCHAR2(50),
    close_store_cnt       VARCHAR2(50),
    franchise_store_cnt   VARCHAR2(50)
);

CREATE TABLE raw_sales_gu (
    base_yq_code              VARCHAR2(20),
    gu_code                   VARCHAR2(20),
    gu_name                   VARCHAR2(50),
    svc_code                  VARCHAR2(30),
    svc_name                  VARCHAR2(100),

    sales_amt                 VARCHAR2(50),
    sales_cnt                 VARCHAR2(50),
    weekday_sales_amt         VARCHAR2(50),
    weekend_sales_amt         VARCHAR2(50),

    mon_sales_amt             VARCHAR2(50),
    tue_sales_amt             VARCHAR2(50),
    wed_sales_amt             VARCHAR2(50),
    thu_sales_amt             VARCHAR2(50),
    fri_sales_amt             VARCHAR2(50),
    sat_sales_amt             VARCHAR2(50),
    sun_sales_amt             VARCHAR2(50),

    time_00_06_sales_amt      VARCHAR2(50),
    time_06_11_sales_amt      VARCHAR2(50),
    time_11_14_sales_amt      VARCHAR2(50),
    time_14_17_sales_amt      VARCHAR2(50),
    time_17_21_sales_amt      VARCHAR2(50),
    time_21_24_sales_amt      VARCHAR2(50),

    male_sales_amt            VARCHAR2(50),
    female_sales_amt          VARCHAR2(50),
    age10_sales_amt           VARCHAR2(50),
    age20_sales_amt           VARCHAR2(50),
    age30_sales_amt           VARCHAR2(50),
    age40_sales_amt           VARCHAR2(50),
    age50_sales_amt           VARCHAR2(50),
    age60_over_sales_amt      VARCHAR2(50),

    weekday_sales_cnt         VARCHAR2(50),
    weekend_sales_cnt         VARCHAR2(50),

    mon_sales_cnt             VARCHAR2(50),
    tue_sales_cnt             VARCHAR2(50),
    wed_sales_cnt             VARCHAR2(50),
    thu_sales_cnt             VARCHAR2(50),
    fri_sales_cnt             VARCHAR2(50),
    sat_sales_cnt             VARCHAR2(50),
    sun_sales_cnt             VARCHAR2(50),

    time_00_06_sales_cnt      VARCHAR2(50),
    time_06_11_sales_cnt      VARCHAR2(50),
    time_11_14_sales_cnt      VARCHAR2(50),
    time_14_17_sales_cnt      VARCHAR2(50),
    time_17_21_sales_cnt      VARCHAR2(50),
    time_21_24_sales_cnt      VARCHAR2(50),

    male_sales_cnt            VARCHAR2(50),
    female_sales_cnt          VARCHAR2(50),
    age10_sales_cnt           VARCHAR2(50),
    age20_sales_cnt           VARCHAR2(50),
    age30_sales_cnt           VARCHAR2(50),
    age40_sales_cnt           VARCHAR2(50),
    age50_sales_cnt           VARCHAR2(50),
    age60_over_sales_cnt      VARCHAR2(50)
);

--------------------------------------------------------------------------------
-- RAW TABLE COMMENTS
--------------------------------------------------------------------------------

COMMENT ON TABLE raw_unmanned_store IS '서울시 무인점포 현황 원본 CSV를 적재한 RAW 테이블';
COMMENT ON COLUMN raw_unmanned_store.seq_no IS '원본 연번';
COMMENT ON COLUMN raw_unmanned_store.gu_name IS '원본 자치구명';
COMMENT ON COLUMN raw_unmanned_store.store_name IS '원본 업소명';
COMMENT ON COLUMN raw_unmanned_store.biz_type IS '원본 업종명';

COMMENT ON TABLE raw_flow_gu IS '서울시 상권분석서비스 길단위인구-자치구 원본 CSV를 적재한 RAW 테이블';
COMMENT ON COLUMN raw_flow_gu.base_yq_code IS '기준 년분기 코드';
COMMENT ON COLUMN raw_flow_gu.gu_code IS '자치구 코드';
COMMENT ON COLUMN raw_flow_gu.gu_name IS '자치구명';
COMMENT ON COLUMN raw_flow_gu.total_flow_pop IS '총 유동인구 수';
COMMENT ON COLUMN raw_flow_gu.male_flow_pop IS '남성 유동인구 수';
COMMENT ON COLUMN raw_flow_gu.female_flow_pop IS '여성 유동인구 수';
COMMENT ON COLUMN raw_flow_gu.age10_flow_pop IS '10대 유동인구 수';
COMMENT ON COLUMN raw_flow_gu.age20_flow_pop IS '20대 유동인구 수';
COMMENT ON COLUMN raw_flow_gu.age30_flow_pop IS '30대 유동인구 수';
COMMENT ON COLUMN raw_flow_gu.age40_flow_pop IS '40대 유동인구 수';
COMMENT ON COLUMN raw_flow_gu.age50_flow_pop IS '50대 유동인구 수';
COMMENT ON COLUMN raw_flow_gu.age60_over_flow_pop IS '60대 이상 유동인구 수';
COMMENT ON COLUMN raw_flow_gu.time_00_06_flow_pop IS '00시~06시 유동인구 수';
COMMENT ON COLUMN raw_flow_gu.time_06_11_flow_pop IS '06시~11시 유동인구 수';
COMMENT ON COLUMN raw_flow_gu.time_11_14_flow_pop IS '11시~14시 유동인구 수';
COMMENT ON COLUMN raw_flow_gu.time_14_17_flow_pop IS '14시~17시 유동인구 수';
COMMENT ON COLUMN raw_flow_gu.time_17_21_flow_pop IS '17시~21시 유동인구 수';
COMMENT ON COLUMN raw_flow_gu.time_21_24_flow_pop IS '21시~24시 유동인구 수';
COMMENT ON COLUMN raw_flow_gu.mon_flow_pop IS '월요일 유동인구 수';
COMMENT ON COLUMN raw_flow_gu.tue_flow_pop IS '화요일 유동인구 수';
COMMENT ON COLUMN raw_flow_gu.wed_flow_pop IS '수요일 유동인구 수';
COMMENT ON COLUMN raw_flow_gu.thu_flow_pop IS '목요일 유동인구 수';
COMMENT ON COLUMN raw_flow_gu.fri_flow_pop IS '금요일 유동인구 수';
COMMENT ON COLUMN raw_flow_gu.sat_flow_pop IS '토요일 유동인구 수';
COMMENT ON COLUMN raw_flow_gu.sun_flow_pop IS '일요일 유동인구 수';

COMMENT ON TABLE raw_resident_gu IS '서울시 상권분석서비스 상주인구-자치구 원본 CSV를 적재한 RAW 테이블';
COMMENT ON COLUMN raw_resident_gu.base_yq_code IS '기준 년분기 코드';
COMMENT ON COLUMN raw_resident_gu.gu_code IS '자치구 코드';
COMMENT ON COLUMN raw_resident_gu.gu_name IS '자치구명';
COMMENT ON COLUMN raw_resident_gu.total_resident_pop IS '총 상주인구 수';
COMMENT ON COLUMN raw_resident_gu.male_resident_pop IS '남성 상주인구 수';
COMMENT ON COLUMN raw_resident_gu.female_resident_pop IS '여성 상주인구 수';
COMMENT ON COLUMN raw_resident_gu.age10_resident_pop IS '10대 상주인구 수';
COMMENT ON COLUMN raw_resident_gu.age20_resident_pop IS '20대 상주인구 수';
COMMENT ON COLUMN raw_resident_gu.age30_resident_pop IS '30대 상주인구 수';
COMMENT ON COLUMN raw_resident_gu.age40_resident_pop IS '40대 상주인구 수';
COMMENT ON COLUMN raw_resident_gu.age50_resident_pop IS '50대 상주인구 수';
COMMENT ON COLUMN raw_resident_gu.age60_over_resident_pop IS '60대 이상 상주인구 수';
COMMENT ON COLUMN raw_resident_gu.male_age10_resident_pop IS '남성 10대 상주인구 수';
COMMENT ON COLUMN raw_resident_gu.male_age20_resident_pop IS '남성 20대 상주인구 수';
COMMENT ON COLUMN raw_resident_gu.male_age30_resident_pop IS '남성 30대 상주인구 수';
COMMENT ON COLUMN raw_resident_gu.male_age40_resident_pop IS '남성 40대 상주인구 수';
COMMENT ON COLUMN raw_resident_gu.male_age50_resident_pop IS '남성 50대 상주인구 수';
COMMENT ON COLUMN raw_resident_gu.male_age60_over_resident_pop IS '남성 60대 이상 상주인구 수';
COMMENT ON COLUMN raw_resident_gu.female_age10_resident_pop IS '여성 10대 상주인구 수';
COMMENT ON COLUMN raw_resident_gu.female_age20_resident_pop IS '여성 20대 상주인구 수';
COMMENT ON COLUMN raw_resident_gu.female_age30_resident_pop IS '여성 30대 상주인구 수';
COMMENT ON COLUMN raw_resident_gu.female_age40_resident_pop IS '여성 40대 상주인구 수';
COMMENT ON COLUMN raw_resident_gu.female_age50_resident_pop IS '여성 50대 상주인구 수';
COMMENT ON COLUMN raw_resident_gu.female_age60_over_resident_pop IS '여성 60대 이상 상주인구 수';
COMMENT ON COLUMN raw_resident_gu.total_household_cnt IS '총 가구 수';
COMMENT ON COLUMN raw_resident_gu.apt_household_cnt IS '아파트 가구 수';
COMMENT ON COLUMN raw_resident_gu.non_apt_household_cnt IS '비아파트 가구 수';

COMMENT ON TABLE raw_income_consume_gu IS '서울시 상권분석서비스 소득소비-자치구 원본 CSV를 적재한 RAW 테이블';
COMMENT ON COLUMN raw_income_consume_gu.base_yq_code IS '기준 년분기 코드';
COMMENT ON COLUMN raw_income_consume_gu.dong_code IS '원본 행정동 코드';
COMMENT ON COLUMN raw_income_consume_gu.dong_name IS '원본 행정동명';
COMMENT ON COLUMN raw_income_consume_gu.avg_month_income_amt IS '월 평균 소득 금액';
COMMENT ON COLUMN raw_income_consume_gu.income_bracket_code IS '소득 구간 코드';
COMMENT ON COLUMN raw_income_consume_gu.total_spend_amt IS '지출 총금액';
COMMENT ON COLUMN raw_income_consume_gu.grocery_spend_amt IS '식료품 지출 금액';
COMMENT ON COLUMN raw_income_consume_gu.clothing_shoes_spend_amt IS '의류 신발 지출 금액';
COMMENT ON COLUMN raw_income_consume_gu.living_goods_spend_amt IS '생활용품 지출 금액';
COMMENT ON COLUMN raw_income_consume_gu.medical_spend_amt IS '의료비 지출 금액';
COMMENT ON COLUMN raw_income_consume_gu.transport_spend_amt IS '교통비 지출 금액';
COMMENT ON COLUMN raw_income_consume_gu.education_spend_amt IS '교육비 지출 금액';
COMMENT ON COLUMN raw_income_consume_gu.entertainment_spend_amt IS '유흥비 지출 금액';
COMMENT ON COLUMN raw_income_consume_gu.leisure_culture_spend_amt IS '여가 문화 지출 금액';
COMMENT ON COLUMN raw_income_consume_gu.other_spend_amt IS '기타 지출 금액';
COMMENT ON COLUMN raw_income_consume_gu.food_spend_amt IS '음식 지출 금액';

COMMENT ON TABLE raw_store_gu IS '서울시 상권분석서비스 점포-자치구 원본 CSV를 적재한 RAW 테이블';
COMMENT ON COLUMN raw_store_gu.base_yq_code IS '기준 년분기 코드';
COMMENT ON COLUMN raw_store_gu.gu_code IS '자치구 코드';
COMMENT ON COLUMN raw_store_gu.gu_name IS '자치구명';
COMMENT ON COLUMN raw_store_gu.svc_code IS '서비스 업종 코드';
COMMENT ON COLUMN raw_store_gu.svc_name IS '서비스 업종명';
COMMENT ON COLUMN raw_store_gu.store_cnt IS '점포 수';
COMMENT ON COLUMN raw_store_gu.similar_store_cnt IS '유사 업종 점포 수';
COMMENT ON COLUMN raw_store_gu.open_rate IS '개업률';
COMMENT ON COLUMN raw_store_gu.open_store_cnt IS '개업 점포 수';
COMMENT ON COLUMN raw_store_gu.close_rate IS '폐업률';
COMMENT ON COLUMN raw_store_gu.close_store_cnt IS '폐업 점포 수';
COMMENT ON COLUMN raw_store_gu.franchise_store_cnt IS '프랜차이즈 점포 수';

COMMENT ON TABLE raw_sales_gu IS '서울시 상권분석서비스 추정매출-자치구 원본 CSV를 적재한 RAW 테이블';
COMMENT ON COLUMN raw_sales_gu.base_yq_code IS '기준 년분기 코드';
COMMENT ON COLUMN raw_sales_gu.gu_code IS '자치구 코드';
COMMENT ON COLUMN raw_sales_gu.gu_name IS '자치구명';
COMMENT ON COLUMN raw_sales_gu.svc_code IS '서비스 업종 코드';
COMMENT ON COLUMN raw_sales_gu.svc_name IS '서비스 업종명';
COMMENT ON COLUMN raw_sales_gu.sales_amt IS '당월 매출 금액';
COMMENT ON COLUMN raw_sales_gu.sales_cnt IS '당월 매출 건수';
COMMENT ON COLUMN raw_sales_gu.weekday_sales_amt IS '주중 매출 금액';
COMMENT ON COLUMN raw_sales_gu.weekend_sales_amt IS '주말 매출 금액';
COMMENT ON COLUMN raw_sales_gu.mon_sales_amt IS '월요일 매출 금액';
COMMENT ON COLUMN raw_sales_gu.tue_sales_amt IS '화요일 매출 금액';
COMMENT ON COLUMN raw_sales_gu.wed_sales_amt IS '수요일 매출 금액';
COMMENT ON COLUMN raw_sales_gu.thu_sales_amt IS '목요일 매출 금액';
COMMENT ON COLUMN raw_sales_gu.fri_sales_amt IS '금요일 매출 금액';
COMMENT ON COLUMN raw_sales_gu.sat_sales_amt IS '토요일 매출 금액';
COMMENT ON COLUMN raw_sales_gu.sun_sales_amt IS '일요일 매출 금액';
COMMENT ON COLUMN raw_sales_gu.time_00_06_sales_amt IS '00시~06시 매출 금액';
COMMENT ON COLUMN raw_sales_gu.time_06_11_sales_amt IS '06시~11시 매출 금액';
COMMENT ON COLUMN raw_sales_gu.time_11_14_sales_amt IS '11시~14시 매출 금액';
COMMENT ON COLUMN raw_sales_gu.time_14_17_sales_amt IS '14시~17시 매출 금액';
COMMENT ON COLUMN raw_sales_gu.time_17_21_sales_amt IS '17시~21시 매출 금액';
COMMENT ON COLUMN raw_sales_gu.time_21_24_sales_amt IS '21시~24시 매출 금액';
COMMENT ON COLUMN raw_sales_gu.male_sales_amt IS '남성 매출 금액';
COMMENT ON COLUMN raw_sales_gu.female_sales_amt IS '여성 매출 금액';
COMMENT ON COLUMN raw_sales_gu.age10_sales_amt IS '10대 매출 금액';
COMMENT ON COLUMN raw_sales_gu.age20_sales_amt IS '20대 매출 금액';
COMMENT ON COLUMN raw_sales_gu.age30_sales_amt IS '30대 매출 금액';
COMMENT ON COLUMN raw_sales_gu.age40_sales_amt IS '40대 매출 금액';
COMMENT ON COLUMN raw_sales_gu.age50_sales_amt IS '50대 매출 금액';
COMMENT ON COLUMN raw_sales_gu.age60_over_sales_amt IS '60대 이상 매출 금액';
COMMENT ON COLUMN raw_sales_gu.weekday_sales_cnt IS '주중 매출 건수';
COMMENT ON COLUMN raw_sales_gu.weekend_sales_cnt IS '주말 매출 건수';
COMMENT ON COLUMN raw_sales_gu.mon_sales_cnt IS '월요일 매출 건수';
COMMENT ON COLUMN raw_sales_gu.tue_sales_cnt IS '화요일 매출 건수';
COMMENT ON COLUMN raw_sales_gu.wed_sales_cnt IS '수요일 매출 건수';
COMMENT ON COLUMN raw_sales_gu.thu_sales_cnt IS '목요일 매출 건수';
COMMENT ON COLUMN raw_sales_gu.fri_sales_cnt IS '금요일 매출 건수';
COMMENT ON COLUMN raw_sales_gu.sat_sales_cnt IS '토요일 매출 건수';
COMMENT ON COLUMN raw_sales_gu.sun_sales_cnt IS '일요일 매출 건수';
COMMENT ON COLUMN raw_sales_gu.time_00_06_sales_cnt IS '00시~06시 매출 건수';
COMMENT ON COLUMN raw_sales_gu.time_06_11_sales_cnt IS '06시~11시 매출 건수';
COMMENT ON COLUMN raw_sales_gu.time_11_14_sales_cnt IS '11시~14시 매출 건수';
COMMENT ON COLUMN raw_sales_gu.time_14_17_sales_cnt IS '14시~17시 매출 건수';
COMMENT ON COLUMN raw_sales_gu.time_17_21_sales_cnt IS '17시~21시 매출 건수';
COMMENT ON COLUMN raw_sales_gu.time_21_24_sales_cnt IS '21시~24시 매출 건수';
COMMENT ON COLUMN raw_sales_gu.male_sales_cnt IS '남성 매출 건수';
COMMENT ON COLUMN raw_sales_gu.female_sales_cnt IS '여성 매출 건수';
COMMENT ON COLUMN raw_sales_gu.age10_sales_cnt IS '10대 매출 건수';
COMMENT ON COLUMN raw_sales_gu.age20_sales_cnt IS '20대 매출 건수';
COMMENT ON COLUMN raw_sales_gu.age30_sales_cnt IS '30대 매출 건수';
COMMENT ON COLUMN raw_sales_gu.age40_sales_cnt IS '40대 매출 건수';
COMMENT ON COLUMN raw_sales_gu.age50_sales_cnt IS '50대 매출 건수';
COMMENT ON COLUMN raw_sales_gu.age60_over_sales_cnt IS '60대 이상 매출 건수';


SELECT * FROM raw_unmanned_store ; 
SELECT * FROM raw_flow_gu ; 
SELECT * FROM raw_resident_gu ; 
SELECT * FROM raw_income_consume_gu ; 
SELECT * FROM raw_store_gu ; 
SELECT * FROM raw_sales_gu ; 

CREATE TABLE STG_UNMANNED_STORE_ONLY_PICTURE AS 
SELECT GU_NAME, STORE_NAME
  FROM RAW_UNMANNED_STORE
WHERE BIZ_TYPE = '무인사진관'  ; 

SELECT * FROM STG_UNMANNED_STORE_ONLY_PICTURE ;

CREATE TABLE STG_UNMANNED_STORE AS 
SELECT * 
  FROM RAW_UNMANNED_STORE ; 
  
SELECT * FROM STG_UNMANNED_STORE ;

UPDATE STG_UNMANNED_STORE 
  SET GU_NAME = GU_NAME || '구' ; 
  
  
SELECT * FROM RAW_FLOW_GU ; --유동인구 

CREATE TABLE stg_flow_gu_20254 AS
SELECT
    TO_NUMBER(base_yq_code) AS base_yq_code,
    gu_code                 AS gu_code,
    gu_name                 AS gu_name,

    TO_NUMBER(NULLIF(REPLACE(TRIM(total_flow_pop), ',', ''), ''))        AS total_flow_pop,
    TO_NUMBER(NULLIF(REPLACE(TRIM(male_flow_pop), ',', ''), ''))         AS male_flow_pop,
    TO_NUMBER(NULLIF(REPLACE(TRIM(female_flow_pop), ',', ''), ''))       AS female_flow_pop,
    TO_NUMBER(NULLIF(REPLACE(TRIM(age10_flow_pop), ',', ''), ''))        AS age10_flow_pop,
    TO_NUMBER(NULLIF(REPLACE(TRIM(age20_flow_pop), ',', ''), ''))        AS age20_flow_pop,
    TO_NUMBER(NULLIF(REPLACE(TRIM(age30_flow_pop), ',', ''), ''))        AS age30_flow_pop,
    TO_NUMBER(NULLIF(REPLACE(TRIM(age40_flow_pop), ',', ''), ''))        AS age40_flow_pop,
    TO_NUMBER(NULLIF(REPLACE(TRIM(age50_flow_pop), ',', ''), ''))        AS age50_flow_pop,
    TO_NUMBER(NULLIF(REPLACE(TRIM(age60_over_flow_pop), ',', ''), ''))   AS age60_over_flow_pop,

    TO_NUMBER(NULLIF(REPLACE(TRIM(time_00_06_flow_pop), ',', ''), ''))   AS time_00_06_flow_pop,
    TO_NUMBER(NULLIF(REPLACE(TRIM(time_06_11_flow_pop), ',', ''), ''))   AS time_06_11_flow_pop,
    TO_NUMBER(NULLIF(REPLACE(TRIM(time_11_14_flow_pop), ',', ''), ''))   AS time_11_14_flow_pop,
    TO_NUMBER(NULLIF(REPLACE(TRIM(time_14_17_flow_pop), ',', ''), ''))   AS time_14_17_flow_pop,
    TO_NUMBER(NULLIF(REPLACE(TRIM(time_17_21_flow_pop), ',', ''), ''))   AS time_17_21_flow_pop,
    TO_NUMBER(NULLIF(REPLACE(TRIM(time_21_24_flow_pop), ',', ''), ''))   AS time_21_24_flow_pop,

    TO_NUMBER(NULLIF(REPLACE(TRIM(mon_flow_pop), ',', ''), ''))          AS mon_flow_pop,
    TO_NUMBER(NULLIF(REPLACE(TRIM(tue_flow_pop), ',', ''), ''))          AS tue_flow_pop,
    TO_NUMBER(NULLIF(REPLACE(TRIM(wed_flow_pop), ',', ''), ''))          AS wed_flow_pop,
    TO_NUMBER(NULLIF(REPLACE(TRIM(thu_flow_pop), ',', ''), ''))          AS thu_flow_pop,
    TO_NUMBER(NULLIF(REPLACE(TRIM(fri_flow_pop), ',', ''), ''))          AS fri_flow_pop,
    TO_NUMBER(NULLIF(REPLACE(TRIM(sat_flow_pop), ',', ''), ''))          AS sat_flow_pop,
    TO_NUMBER(NULLIF(REPLACE(TRIM(sun_flow_pop), ',', ''), ''))          AS sun_flow_pop
FROM raw_flow_gu
WHERE base_yq_code = '20254';


CREATE TABLE stg_resident_gu_20254 AS
SELECT
    TO_NUMBER(base_yq_code) AS base_yq_code,
    gu_code                 AS gu_code,
    gu_name                 AS gu_name,

    TO_NUMBER(NULLIF(REPLACE(TRIM(total_resident_pop), ',', ''), ''))             AS total_resident_pop,
    TO_NUMBER(NULLIF(REPLACE(TRIM(male_resident_pop), ',', ''), ''))              AS male_resident_pop,
    TO_NUMBER(NULLIF(REPLACE(TRIM(female_resident_pop), ',', ''), ''))            AS female_resident_pop,
    TO_NUMBER(NULLIF(REPLACE(TRIM(age10_resident_pop), ',', ''), ''))             AS age10_resident_pop,
    TO_NUMBER(NULLIF(REPLACE(TRIM(age20_resident_pop), ',', ''), ''))             AS age20_resident_pop,
    TO_NUMBER(NULLIF(REPLACE(TRIM(age30_resident_pop), ',', ''), ''))             AS age30_resident_pop,
    TO_NUMBER(NULLIF(REPLACE(TRIM(age40_resident_pop), ',', ''), ''))             AS age40_resident_pop,
    TO_NUMBER(NULLIF(REPLACE(TRIM(age50_resident_pop), ',', ''), ''))             AS age50_resident_pop,
    TO_NUMBER(NULLIF(REPLACE(TRIM(age60_over_resident_pop), ',', ''), ''))        AS age60_over_resident_pop,

    TO_NUMBER(NULLIF(REPLACE(TRIM(male_age10_resident_pop), ',', ''), ''))        AS male_age10_resident_pop,
    TO_NUMBER(NULLIF(REPLACE(TRIM(male_age20_resident_pop), ',', ''), ''))        AS male_age20_resident_pop,
    TO_NUMBER(NULLIF(REPLACE(TRIM(male_age30_resident_pop), ',', ''), ''))        AS male_age30_resident_pop,
    TO_NUMBER(NULLIF(REPLACE(TRIM(male_age40_resident_pop), ',', ''), ''))        AS male_age40_resident_pop,
    TO_NUMBER(NULLIF(REPLACE(TRIM(male_age50_resident_pop), ',', ''), ''))        AS male_age50_resident_pop,
    TO_NUMBER(NULLIF(REPLACE(TRIM(male_age60_over_resident_pop), ',', ''), ''))   AS male_age60_over_resident_pop,

    TO_NUMBER(NULLIF(REPLACE(TRIM(female_age10_resident_pop), ',', ''), ''))      AS female_age10_resident_pop,
    TO_NUMBER(NULLIF(REPLACE(TRIM(female_age20_resident_pop), ',', ''), ''))      AS female_age20_resident_pop,
    TO_NUMBER(NULLIF(REPLACE(TRIM(female_age30_resident_pop), ',', ''), ''))      AS female_age30_resident_pop,
    TO_NUMBER(NULLIF(REPLACE(TRIM(female_age40_resident_pop), ',', ''), ''))      AS female_age40_resident_pop,
    TO_NUMBER(NULLIF(REPLACE(TRIM(female_age50_resident_pop), ',', ''), ''))      AS female_age50_resident_pop,
    TO_NUMBER(NULLIF(REPLACE(TRIM(female_age60_over_resident_pop), ',', ''), '')) AS female_age60_over_resident_pop,

    TO_NUMBER(NULLIF(REPLACE(TRIM(total_household_cnt), ',', ''), ''))            AS total_household_cnt,
    TO_NUMBER(NULLIF(REPLACE(TRIM(apt_household_cnt), ',', ''), ''))              AS apt_household_cnt,
    TO_NUMBER(NULLIF(REPLACE(TRIM(non_apt_household_cnt), ',', ''), ''))          AS non_apt_household_cnt
FROM raw_resident_gu
WHERE base_yq_code = '20254';

CREATE TABLE stg_income_consume_gu_20254 AS
SELECT
    TO_NUMBER(base_yq_code) AS base_yq_code,
    dong_code               AS gu_code,
    dong_name               AS gu_name,
    income_bracket_code     AS income_bracket_code,

    TO_NUMBER(NULLIF(REPLACE(TRIM(avg_month_income_amt), ',', ''), ''))      AS avg_month_income_amt,
    TO_NUMBER(NULLIF(REPLACE(TRIM(total_spend_amt), ',', ''), ''))           AS total_spend_amt,
    TO_NUMBER(NULLIF(REPLACE(TRIM(grocery_spend_amt), ',', ''), ''))         AS grocery_spend_amt,
    TO_NUMBER(NULLIF(REPLACE(TRIM(clothing_shoes_spend_amt), ',', ''), ''))  AS clothing_shoes_spend_amt,
    TO_NUMBER(NULLIF(REPLACE(TRIM(living_goods_spend_amt), ',', ''), ''))    AS living_goods_spend_amt,
    TO_NUMBER(NULLIF(REPLACE(TRIM(medical_spend_amt), ',', ''), ''))         AS medical_spend_amt,
    TO_NUMBER(NULLIF(REPLACE(TRIM(transport_spend_amt), ',', ''), ''))       AS transport_spend_amt,
    TO_NUMBER(NULLIF(REPLACE(TRIM(education_spend_amt), ',', ''), ''))       AS education_spend_amt,
    TO_NUMBER(NULLIF(REPLACE(TRIM(entertainment_spend_amt), ',', ''), ''))   AS entertainment_spend_amt,
    TO_NUMBER(NULLIF(REPLACE(TRIM(leisure_culture_spend_amt), ',', ''), '')) AS leisure_culture_spend_amt,
    TO_NUMBER(NULLIF(REPLACE(TRIM(other_spend_amt), ',', ''), ''))           AS other_spend_amt,
    TO_NUMBER(NULLIF(REPLACE(TRIM(food_spend_amt), ',', ''), ''))            AS food_spend_amt
FROM raw_income_consume_gu
WHERE base_yq_code = '20254';

CREATE TABLE stg_store_gu_20254 AS
SELECT
    TO_NUMBER(base_yq_code) AS base_yq_code,
    gu_code                 AS gu_code,
    gu_name                 AS gu_name,
    svc_code                AS svc_code,
    svc_name                AS svc_name,

    TO_NUMBER(NULLIF(REPLACE(TRIM(store_cnt), ',', ''), ''))            AS store_cnt,
    TO_NUMBER(NULLIF(REPLACE(TRIM(similar_store_cnt), ',', ''), ''))    AS similar_store_cnt,
    TO_NUMBER(NULLIF(REPLACE(TRIM(open_rate), ',', ''), ''))            AS open_rate,
    TO_NUMBER(NULLIF(REPLACE(TRIM(open_store_cnt), ',', ''), ''))       AS open_store_cnt,
    TO_NUMBER(NULLIF(REPLACE(TRIM(close_rate), ',', ''), ''))           AS close_rate,
    TO_NUMBER(NULLIF(REPLACE(TRIM(close_store_cnt), ',', ''), ''))      AS close_store_cnt,
    TO_NUMBER(NULLIF(REPLACE(TRIM(franchise_store_cnt), ',', ''), ''))  AS franchise_store_cnt
FROM raw_store_gu
WHERE base_yq_code = '20254';

CREATE TABLE stg_sales_gu_20254 AS
SELECT
    TO_NUMBER(base_yq_code) AS base_yq_code,
    gu_code                 AS gu_code,
    gu_name                 AS gu_name,
    svc_code                AS svc_code,
    svc_name                AS svc_name,

    TO_NUMBER(NULLIF(REPLACE(TRIM(sales_amt), ',', ''), ''))            AS sales_amt,
    TO_NUMBER(NULLIF(REPLACE(TRIM(sales_cnt), ',', ''), ''))            AS sales_cnt,
    TO_NUMBER(NULLIF(REPLACE(TRIM(weekday_sales_amt), ',', ''), ''))    AS weekday_sales_amt,
    TO_NUMBER(NULLIF(REPLACE(TRIM(weekend_sales_amt), ',', ''), ''))    AS weekend_sales_amt,

    TO_NUMBER(NULLIF(REPLACE(TRIM(mon_sales_amt), ',', ''), ''))        AS mon_sales_amt,
    TO_NUMBER(NULLIF(REPLACE(TRIM(tue_sales_amt), ',', ''), ''))        AS tue_sales_amt,
    TO_NUMBER(NULLIF(REPLACE(TRIM(wed_sales_amt), ',', ''), ''))        AS wed_sales_amt,
    TO_NUMBER(NULLIF(REPLACE(TRIM(thu_sales_amt), ',', ''), ''))        AS thu_sales_amt,
    TO_NUMBER(NULLIF(REPLACE(TRIM(fri_sales_amt), ',', ''), ''))        AS fri_sales_amt,
    TO_NUMBER(NULLIF(REPLACE(TRIM(sat_sales_amt), ',', ''), ''))        AS sat_sales_amt,
    TO_NUMBER(NULLIF(REPLACE(TRIM(sun_sales_amt), ',', ''), ''))        AS sun_sales_amt,

    TO_NUMBER(NULLIF(REPLACE(TRIM(time_00_06_sales_amt), ',', ''), '')) AS time_00_06_sales_amt,
    TO_NUMBER(NULLIF(REPLACE(TRIM(time_06_11_sales_amt), ',', ''), '')) AS time_06_11_sales_amt,
    TO_NUMBER(NULLIF(REPLACE(TRIM(time_11_14_sales_amt), ',', ''), '')) AS time_11_14_sales_amt,
    TO_NUMBER(NULLIF(REPLACE(TRIM(time_14_17_sales_amt), ',', ''), '')) AS time_14_17_sales_amt,
    TO_NUMBER(NULLIF(REPLACE(TRIM(time_17_21_sales_amt), ',', ''), '')) AS time_17_21_sales_amt,
    TO_NUMBER(NULLIF(REPLACE(TRIM(time_21_24_sales_amt), ',', ''), '')) AS time_21_24_sales_amt,

    TO_NUMBER(NULLIF(REPLACE(TRIM(male_sales_amt), ',', ''), ''))       AS male_sales_amt,
    TO_NUMBER(NULLIF(REPLACE(TRIM(female_sales_amt), ',', ''), ''))     AS female_sales_amt,
    TO_NUMBER(NULLIF(REPLACE(TRIM(age10_sales_amt), ',', ''), ''))      AS age10_sales_amt,
    TO_NUMBER(NULLIF(REPLACE(TRIM(age20_sales_amt), ',', ''), ''))      AS age20_sales_amt,
    TO_NUMBER(NULLIF(REPLACE(TRIM(age30_sales_amt), ',', ''), ''))      AS age30_sales_amt,
    TO_NUMBER(NULLIF(REPLACE(TRIM(age40_sales_amt), ',', ''), ''))      AS age40_sales_amt,
    TO_NUMBER(NULLIF(REPLACE(TRIM(age50_sales_amt), ',', ''), ''))      AS age50_sales_amt,
    TO_NUMBER(NULLIF(REPLACE(TRIM(age60_over_sales_amt), ',', ''), '')) AS age60_over_sales_amt,

    TO_NUMBER(NULLIF(REPLACE(TRIM(weekday_sales_cnt), ',', ''), ''))    AS weekday_sales_cnt,
    TO_NUMBER(NULLIF(REPLACE(TRIM(weekend_sales_cnt), ',', ''), ''))    AS weekend_sales_cnt,

    TO_NUMBER(NULLIF(REPLACE(TRIM(mon_sales_cnt), ',', ''), ''))        AS mon_sales_cnt,
    TO_NUMBER(NULLIF(REPLACE(TRIM(tue_sales_cnt), ',', ''), ''))        AS tue_sales_cnt,
    TO_NUMBER(NULLIF(REPLACE(TRIM(wed_sales_cnt), ',', ''), ''))        AS wed_sales_cnt,
    TO_NUMBER(NULLIF(REPLACE(TRIM(thu_sales_cnt), ',', ''), ''))        AS thu_sales_cnt,
    TO_NUMBER(NULLIF(REPLACE(TRIM(fri_sales_cnt), ',', ''), ''))        AS fri_sales_cnt,
    TO_NUMBER(NULLIF(REPLACE(TRIM(sat_sales_cnt), ',', ''), ''))        AS sat_sales_cnt,
    TO_NUMBER(NULLIF(REPLACE(TRIM(sun_sales_cnt), ',', ''), ''))        AS sun_sales_cnt,

    TO_NUMBER(NULLIF(REPLACE(TRIM(time_00_06_sales_cnt), ',', ''), '')) AS time_00_06_sales_cnt,
    TO_NUMBER(NULLIF(REPLACE(TRIM(time_06_11_sales_cnt), ',', ''), '')) AS time_06_11_sales_cnt,
    TO_NUMBER(NULLIF(REPLACE(TRIM(time_11_14_sales_cnt), ',', ''), '')) AS time_11_14_sales_cnt,
    TO_NUMBER(NULLIF(REPLACE(TRIM(time_14_17_sales_cnt), ',', ''), '')) AS time_14_17_sales_cnt,
    TO_NUMBER(NULLIF(REPLACE(TRIM(time_17_21_sales_cnt), ',', ''), '')) AS time_17_21_sales_cnt,
    TO_NUMBER(NULLIF(REPLACE(TRIM(time_21_24_sales_cnt), ',', ''), '')) AS time_21_24_sales_cnt,

    TO_NUMBER(NULLIF(REPLACE(TRIM(male_sales_cnt), ',', ''), ''))       AS male_sales_cnt,
    TO_NUMBER(NULLIF(REPLACE(TRIM(female_sales_cnt), ',', ''), ''))     AS female_sales_cnt,
    TO_NUMBER(NULLIF(REPLACE(TRIM(age10_sales_cnt), ',', ''), ''))      AS age10_sales_cnt,
    TO_NUMBER(NULLIF(REPLACE(TRIM(age20_sales_cnt), ',', ''), ''))      AS age20_sales_cnt,
    TO_NUMBER(NULLIF(REPLACE(TRIM(age30_sales_cnt), ',', ''), ''))      AS age30_sales_cnt,
    TO_NUMBER(NULLIF(REPLACE(TRIM(age40_sales_cnt), ',', ''), ''))      AS age40_sales_cnt,
    TO_NUMBER(NULLIF(REPLACE(TRIM(age50_sales_cnt), ',', ''), ''))      AS age50_sales_cnt,
    TO_NUMBER(NULLIF(REPLACE(TRIM(age60_over_sales_cnt), ',', ''), '')) AS age60_over_sales_cnt
FROM raw_sales_gu
WHERE base_yq_code = '20254';



--------------------------------------------------------------------------------
-- STG TABLE COMMENTS
--------------------------------------------------------------------------------

COMMENT ON TABLE stg_unmanned_store IS '서울시 무인점포 현황 원본을 전처리한 STG 테이블';
COMMENT ON COLUMN stg_unmanned_store.store_seq IS '무인점포 원본 연번';
COMMENT ON COLUMN stg_unmanned_store.gu_name IS '표준화된 자치구명';
COMMENT ON COLUMN stg_unmanned_store.store_name IS '업소명';
COMMENT ON COLUMN stg_unmanned_store.biz_type IS '무인점포 업종명';

COMMENT ON TABLE stg_flow_gu_20254 IS '2025년 4분기 자치구별 유동인구 전처리 STG 테이블';
COMMENT ON COLUMN stg_flow_gu_20254.yq IS '기준 년분기 코드';
COMMENT ON COLUMN stg_flow_gu_20254.gu_code IS '자치구 코드';
COMMENT ON COLUMN stg_flow_gu_20254.gu_name IS '자치구명';
COMMENT ON COLUMN stg_flow_gu_20254.total_flow_pop IS '총 유동인구 수';
COMMENT ON COLUMN stg_flow_gu_20254.male_flow_pop IS '남성 유동인구 수';
COMMENT ON COLUMN stg_flow_gu_20254.female_flow_pop IS '여성 유동인구 수';
COMMENT ON COLUMN stg_flow_gu_20254.age10_flow_pop IS '10대 유동인구 수';
COMMENT ON COLUMN stg_flow_gu_20254.age20_flow_pop IS '20대 유동인구 수';
COMMENT ON COLUMN stg_flow_gu_20254.age30_flow_pop IS '30대 유동인구 수';
COMMENT ON COLUMN stg_flow_gu_20254.age40_flow_pop IS '40대 유동인구 수';
COMMENT ON COLUMN stg_flow_gu_20254.age50_flow_pop IS '50대 유동인구 수';
COMMENT ON COLUMN stg_flow_gu_20254.age60_over_flow_pop IS '60대 이상 유동인구 수';
COMMENT ON COLUMN stg_flow_gu_20254.time_00_06_flow_pop IS '00시~06시 유동인구 수';
COMMENT ON COLUMN stg_flow_gu_20254.time_06_11_flow_pop IS '06시~11시 유동인구 수';
COMMENT ON COLUMN stg_flow_gu_20254.time_11_14_flow_pop IS '11시~14시 유동인구 수';
COMMENT ON COLUMN stg_flow_gu_20254.time_14_17_flow_pop IS '14시~17시 유동인구 수';
COMMENT ON COLUMN stg_flow_gu_20254.time_17_21_flow_pop IS '17시~21시 유동인구 수';
COMMENT ON COLUMN stg_flow_gu_20254.time_21_24_flow_pop IS '21시~24시 유동인구 수';
COMMENT ON COLUMN stg_flow_gu_20254.mon_flow_pop IS '월요일 유동인구 수';
COMMENT ON COLUMN stg_flow_gu_20254.tue_flow_pop IS '화요일 유동인구 수';
COMMENT ON COLUMN stg_flow_gu_20254.wed_flow_pop IS '수요일 유동인구 수';
COMMENT ON COLUMN stg_flow_gu_20254.thu_flow_pop IS '목요일 유동인구 수';
COMMENT ON COLUMN stg_flow_gu_20254.fri_flow_pop IS '금요일 유동인구 수';
COMMENT ON COLUMN stg_flow_gu_20254.sat_flow_pop IS '토요일 유동인구 수';
COMMENT ON COLUMN stg_flow_gu_20254.sun_flow_pop IS '일요일 유동인구 수';

COMMENT ON TABLE stg_resident_gu_20254 IS '2025년 4분기 자치구별 상주인구 전처리 STG 테이블';
COMMENT ON COLUMN stg_resident_gu_20254.yq IS '기준 년분기 코드';
COMMENT ON COLUMN stg_resident_gu_20254.gu_code IS '자치구 코드';
COMMENT ON COLUMN stg_resident_gu_20254.gu_name IS '자치구명';
COMMENT ON COLUMN stg_resident_gu_20254.total_resident_pop IS '총 상주인구 수';
COMMENT ON COLUMN stg_resident_gu_20254.male_resident_pop IS '남성 상주인구 수';
COMMENT ON COLUMN stg_resident_gu_20254.female_resident_pop IS '여성 상주인구 수';
COMMENT ON COLUMN stg_resident_gu_20254.age10_resident_pop IS '10대 상주인구 수';
COMMENT ON COLUMN stg_resident_gu_20254.age20_resident_pop IS '20대 상주인구 수';
COMMENT ON COLUMN stg_resident_gu_20254.age30_resident_pop IS '30대 상주인구 수';
COMMENT ON COLUMN stg_resident_gu_20254.age40_resident_pop IS '40대 상주인구 수';
COMMENT ON COLUMN stg_resident_gu_20254.age50_resident_pop IS '50대 상주인구 수';
COMMENT ON COLUMN stg_resident_gu_20254.age60_over_resident_pop IS '60대 이상 상주인구 수';
COMMENT ON COLUMN stg_resident_gu_20254.male_age10_resident_pop IS '남성 10대 상주인구 수';
COMMENT ON COLUMN stg_resident_gu_20254.male_age20_resident_pop IS '남성 20대 상주인구 수';
COMMENT ON COLUMN stg_resident_gu_20254.male_age30_resident_pop IS '남성 30대 상주인구 수';
COMMENT ON COLUMN stg_resident_gu_20254.male_age40_resident_pop IS '남성 40대 상주인구 수';
COMMENT ON COLUMN stg_resident_gu_20254.male_age50_resident_pop IS '남성 50대 상주인구 수';
COMMENT ON COLUMN stg_resident_gu_20254.male_age60_over_resident_pop IS '남성 60대 이상 상주인구 수';
COMMENT ON COLUMN stg_resident_gu_20254.female_age10_resident_pop IS '여성 10대 상주인구 수';
COMMENT ON COLUMN stg_resident_gu_20254.female_age20_resident_pop IS '여성 20대 상주인구 수';
COMMENT ON COLUMN stg_resident_gu_20254.female_age30_resident_pop IS '여성 30대 상주인구 수';
COMMENT ON COLUMN stg_resident_gu_20254.female_age40_resident_pop IS '여성 40대 상주인구 수';
COMMENT ON COLUMN stg_resident_gu_20254.female_age50_resident_pop IS '여성 50대 상주인구 수';
COMMENT ON COLUMN stg_resident_gu_20254.female_age60_over_resident_pop IS '여성 60대 이상 상주인구 수';
COMMENT ON COLUMN stg_resident_gu_20254.total_household_cnt IS '총 가구 수';
COMMENT ON COLUMN stg_resident_gu_20254.apt_household_cnt IS '아파트 가구 수';
COMMENT ON COLUMN stg_resident_gu_20254.non_apt_household_cnt IS '비아파트 가구 수';

COMMENT ON TABLE stg_income_consume_gu_20254 IS '2025년 4분기 자치구별 소득소비 전처리 STG 테이블';
COMMENT ON COLUMN stg_income_consume_gu_20254.yq IS '기준 년분기 코드';
COMMENT ON COLUMN stg_income_consume_gu_20254.gu_code IS '자치구 코드';
COMMENT ON COLUMN stg_income_consume_gu_20254.gu_name IS '자치구명';
COMMENT ON COLUMN stg_income_consume_gu_20254.income_bracket_code IS '소득 구간 코드';
COMMENT ON COLUMN stg_income_consume_gu_20254.avg_month_income_amt IS '월 평균 소득 금액';
COMMENT ON COLUMN stg_income_consume_gu_20254.total_spend_amt IS '지출 총금액';
COMMENT ON COLUMN stg_income_consume_gu_20254.grocery_spend_amt IS '식료품 지출 금액';
COMMENT ON COLUMN stg_income_consume_gu_20254.clothing_shoes_spend_amt IS '의류 신발 지출 금액';
COMMENT ON COLUMN stg_income_consume_gu_20254.living_goods_spend_amt IS '생활용품 지출 금액';
COMMENT ON COLUMN stg_income_consume_gu_20254.medical_spend_amt IS '의료비 지출 금액';
COMMENT ON COLUMN stg_income_consume_gu_20254.transport_spend_amt IS '교통비 지출 금액';
COMMENT ON COLUMN stg_income_consume_gu_20254.education_spend_amt IS '교육비 지출 금액';
COMMENT ON COLUMN stg_income_consume_gu_20254.entertainment_spend_amt IS '유흥비 지출 금액';
COMMENT ON COLUMN stg_income_consume_gu_20254.leisure_culture_spend_amt IS '여가 문화 지출 금액';
COMMENT ON COLUMN stg_income_consume_gu_20254.other_spend_amt IS '기타 지출 금액';
COMMENT ON COLUMN stg_income_consume_gu_20254.food_spend_amt IS '음식 지출 금액';

COMMENT ON TABLE stg_store_gu_20254 IS '2025년 4분기 자치구별 서비스업종 점포 전처리 STG 테이블';
COMMENT ON COLUMN stg_store_gu_20254.yq IS '기준 년분기 코드';
COMMENT ON COLUMN stg_store_gu_20254.gu_code IS '자치구 코드';
COMMENT ON COLUMN stg_store_gu_20254.gu_name IS '자치구명';
COMMENT ON COLUMN stg_store_gu_20254.svc_code IS '서비스 업종 코드';
COMMENT ON COLUMN stg_store_gu_20254.svc_name IS '서비스 업종명';
COMMENT ON COLUMN stg_store_gu_20254.store_cnt IS '점포 수';
COMMENT ON COLUMN stg_store_gu_20254.similar_store_cnt IS '유사 업종 점포 수';
COMMENT ON COLUMN stg_store_gu_20254.open_rate IS '개업률';
COMMENT ON COLUMN stg_store_gu_20254.open_store_cnt IS '개업 점포 수';
COMMENT ON COLUMN stg_store_gu_20254.close_rate IS '폐업률';
COMMENT ON COLUMN stg_store_gu_20254.close_store_cnt IS '폐업 점포 수';
COMMENT ON COLUMN stg_store_gu_20254.franchise_store_cnt IS '프랜차이즈 점포 수';

COMMENT ON TABLE stg_sales_gu_20254 IS '2025년 4분기 자치구별 서비스업종 추정매출 전처리 STG 테이블';
COMMENT ON COLUMN stg_sales_gu_20254.yq IS '기준 년분기 코드';
COMMENT ON COLUMN stg_sales_gu_20254.gu_code IS '자치구 코드';
COMMENT ON COLUMN stg_sales_gu_20254.gu_name IS '자치구명';
COMMENT ON COLUMN stg_sales_gu_20254.svc_code IS '서비스 업종 코드';
COMMENT ON COLUMN stg_sales_gu_20254.svc_name IS '서비스 업종명';
COMMENT ON COLUMN stg_sales_gu_20254.sales_amt IS '당월 매출 금액';
COMMENT ON COLUMN stg_sales_gu_20254.sales_cnt IS '당월 매출 건수';
COMMENT ON COLUMN stg_sales_gu_20254.weekday_sales_amt IS '주중 매출 금액';
COMMENT ON COLUMN stg_sales_gu_20254.weekend_sales_amt IS '주말 매출 금액';
COMMENT ON COLUMN stg_sales_gu_20254.mon_sales_amt IS '월요일 매출 금액';
COMMENT ON COLUMN stg_sales_gu_20254.tue_sales_amt IS '화요일 매출 금액';
COMMENT ON COLUMN stg_sales_gu_20254.wed_sales_amt IS '수요일 매출 금액';
COMMENT ON COLUMN stg_sales_gu_20254.thu_sales_amt IS '목요일 매출 금액';
COMMENT ON COLUMN stg_sales_gu_20254.fri_sales_amt IS '금요일 매출 금액';
COMMENT ON COLUMN stg_sales_gu_20254.sat_sales_amt IS '토요일 매출 금액';
COMMENT ON COLUMN stg_sales_gu_20254.sun_sales_amt IS '일요일 매출 금액';
COMMENT ON COLUMN stg_sales_gu_20254.time_00_06_sales_amt IS '00시~06시 매출 금액';
COMMENT ON COLUMN stg_sales_gu_20254.time_06_11_sales_amt IS '06시~11시 매출 금액';
COMMENT ON COLUMN stg_sales_gu_20254.time_11_14_sales_amt IS '11시~14시 매출 금액';
COMMENT ON COLUMN stg_sales_gu_20254.time_14_17_sales_amt IS '14시~17시 매출 금액';
COMMENT ON COLUMN stg_sales_gu_20254.time_17_21_sales_amt IS '17시~21시 매출 금액';
COMMENT ON COLUMN stg_sales_gu_20254.time_21_24_sales_amt IS '21시~24시 매출 금액';
COMMENT ON COLUMN stg_sales_gu_20254.male_sales_amt IS '남성 매출 금액';
COMMENT ON COLUMN stg_sales_gu_20254.female_sales_amt IS '여성 매출 금액';
COMMENT ON COLUMN stg_sales_gu_20254.age10_sales_amt IS '10대 매출 금액';
COMMENT ON COLUMN stg_sales_gu_20254.age20_sales_amt IS '20대 매출 금액';
COMMENT ON COLUMN stg_sales_gu_20254.age30_sales_amt IS '30대 매출 금액';
COMMENT ON COLUMN stg_sales_gu_20254.age40_sales_amt IS '40대 매출 금액';
COMMENT ON COLUMN stg_sales_gu_20254.age50_sales_amt IS '50대 매출 금액';
COMMENT ON COLUMN stg_sales_gu_20254.age60_over_sales_amt IS '60대 이상 매출 금액';
COMMENT ON COLUMN stg_sales_gu_20254.weekday_sales_cnt IS '주중 매출 건수';
COMMENT ON COLUMN stg_sales_gu_20254.weekend_sales_cnt IS '주말 매출 건수';
COMMENT ON COLUMN stg_sales_gu_20254.mon_sales_cnt IS '월요일 매출 건수';
COMMENT ON COLUMN stg_sales_gu_20254.tue_sales_cnt IS '화요일 매출 건수';
COMMENT ON COLUMN stg_sales_gu_20254.wed_sales_cnt IS '수요일 매출 건수';
COMMENT ON COLUMN stg_sales_gu_20254.thu_sales_cnt IS '목요일 매출 건수';
COMMENT ON COLUMN stg_sales_gu_20254.fri_sales_cnt IS '금요일 매출 건수';
COMMENT ON COLUMN stg_sales_gu_20254.sat_sales_cnt IS '토요일 매출 건수';
COMMENT ON COLUMN stg_sales_gu_20254.sun_sales_cnt IS '일요일 매출 건수';
COMMENT ON COLUMN stg_sales_gu_20254.time_00_06_sales_cnt IS '00시~06시 매출 건수';
COMMENT ON COLUMN stg_sales_gu_20254.time_06_11_sales_cnt IS '06시~11시 매출 건수';
COMMENT ON COLUMN stg_sales_gu_20254.time_11_14_sales_cnt IS '11시~14시 매출 건수';
COMMENT ON COLUMN stg_sales_gu_20254.time_14_17_sales_cnt IS '14시~17시 매출 건수';
COMMENT ON COLUMN stg_sales_gu_20254.time_17_21_sales_cnt IS '17시~21시 매출 건수';
COMMENT ON COLUMN stg_sales_gu_20254.time_21_24_sales_cnt IS '21시~24시 매출 건수';
COMMENT ON COLUMN stg_sales_gu_20254.male_sales_cnt IS '남성 매출 건수';
COMMENT ON COLUMN stg_sales_gu_20254.female_sales_cnt IS '여성 매출 건수';
COMMENT ON COLUMN stg_sales_gu_20254.age10_sales_cnt IS '10대 매출 건수';
COMMENT ON COLUMN stg_sales_gu_20254.age20_sales_cnt IS '20대 매출 건수';
COMMENT ON COLUMN stg_sales_gu_20254.age30_sales_cnt IS '30대 매출 건수';
COMMENT ON COLUMN stg_sales_gu_20254.age40_sales_cnt IS '40대 매출 건수';
COMMENT ON COLUMN stg_sales_gu_20254.age50_sales_cnt IS '50대 매출 건수';
COMMENT ON COLUMN stg_sales_gu_20254.age60_over_sales_cnt IS '60대 이상 매출 건수';

SELECT * FROM stg_unmanned_store;
SELECT * FROM stg_flow_gu_20254;
SELECT * FROM stg_resident_gu_20254;
SELECT * FROM stg_income_consume_gu_20254;
SELECT * FROM stg_store_gu_20254;
SELECT * FROM stg_sales_gu_20254 ;

--실습1 
SELECT GU_NAME 
    , COUNT(*) AS 무인점포수 
  FROM STG_UNMANNED_STORE
GROUP BY GU_NAME 
ORDER BY 무인점포수 DESC ;

SELECT CASE WHEN BIZ_TYPE LIKE '무인판매점%' THEN '무인판매점' 
                ELSE BIZ_TYPE 
            END , COUNT(*) 
  FROM STG_UNMANNED_STORE 
 GROUP BY CASE WHEN BIZ_TYPE LIKE '무인판매점%' THEN '무인판매점' 
                ELSE BIZ_TYPE 
            END ; 


--실습2
SELECT GU_NAME 
    , COUNT(*) AS 무인점포수 
  FROM STG_UNMANNED_STORE  
GROUP BY GU_NAME
HAVING COUNT(*) >= 300;

--실습3 
SELECT BIZ_TYPE 
    , COUNT(*) AS 업종별점포수 
  FROM STG_UNMANNED_STORE 
GROUP BY BIZ_TYPE ;
  
--실습4 
SELECT CASE WHEN BIZ_TYPE LIKE '무인판매점%' THEN '무인판매점'
        ELSE BIZ_TYPE
        END AS BIZ_TYPE , COUNT(*) AS 업종별점포수 
    FROM STG_UNMANNED_STORE
    GROUP BY CASE WHEN BIZ_TYPE LIKE '무인판매점%' THEN '무인판매점'
            ELSE BIZ_TYPE 
        END; 
        
--실습5 
SELECT GU_NAME, COUNT(*) AS 점포수 
  FROM STG_UNMANNED_STORE 
 GROUP BY GU_NAME ; 
    
SELECT GU_NAME , SUM(SALES_AMT) AS 자치구별총판매액 
  FROM STG_SALES_GU_20254 
 GROUP BY GU_NAME ;

SELECT A.GU_NAME 
    , A.무인점포수 
    , B.자치구별총판매액 
  FROM ( 
        SELECT GU_NAME, COUNT(*) AS 무인점포수 
          FROM STG_UNMANNED_STORE 
        GROUP BY GU_NAME
) A
INNER JOIN 
( 
        SELECT GU_NAME, SUM(SALES_AMT) AS 자치구별총판매액 
          FROM STG_SALES_GU_20254
        GROUP BY GU_NAME 
) B 
ON (A.GU_NAME = B.GU_NAME) ;


--실습6

--실습7
--ORACLE 11G 버전 (가장 안정화된, 공공기관에서 이 버전 사용) 
SELECT * 
  FROM (
        SELECT GU_NAME 
            , TOTAL_FLOW_POP 
          FROM STG_FLOW_GU_20254 
        ORDER BY TOTAL_FLOW_POP DESC 
        )
WHERE ROWNUM <= 5 ; 

--ORACLE 12C 이후 버전 
SELECT GU_NAME 
    , TOTAL_FLOW_POP
  FROM STG_FLOW_GU_20254
ORDER BY TOTAL_FLOW_POP DESC 
FETCH FIRST 5 ROWS ONLY ; 

--실습8 
SELECT GU_NAME 
    , ROUND(AGE10_FLOW_POP / TOTAL_FLOW_POP , 2 ) AS "10대비율" 
    , ROUND(AGE20_FLOW_POP / TOTAL_FLOW_POP , 2 ) AS "20대비율" 
    , ROUND(AGE30_FLOW_POP / TOTAL_FLOW_POP , 2 ) AS "30대비율" 
    , ROUND(AGE40_FLOW_POP / TOTAL_FLOW_POP , 2 ) AS "40대비율" 
    , ROUND(AGE50_FLOW_POP / TOTAL_FLOW_POP , 2 ) AS "50대비율" 
    , ROUND(AGE60_OVER_FLOW_POP / TOTAL_FLOW_POP , 2 ) AS "60대이상비율"
    , TOTAL_FLOW_POP AS 전체유동인구수 
  FROM STG_FLOW_GU_20254; 
  
SELECT  * FROM STG_FLOW_GU_20254 ; 


---5단계: MART 생성하기 
-- 필요 시 기존 테이블 삭제
-- DROP TABLE MART_UNMANNED_STORE_GU_20254 PURGE;

SELECT *
  FROM STG_FLOW_GU_20254;

CREATE TABLE MART_UNMANNED_STORE_GU_20254 AS
SELECT
    F.BASE_YQ_CODE,
    F.GU_CODE,
    F.GU_NAME,

    NVL(U.TOTAL_UNMANNED_STORE_CNT, 0)    AS TOTAL_UNMANNED_STORE_CNT,
    NVL(U.PHOTO_STORE_CNT, 0)             AS PHOTO_STORE_CNT,
    NVL(U.LAUNDRY_STORE_CNT, 0)           AS LAUNDRY_STORE_CNT,
    NVL(U.STUDY_STORE_CNT, 0)             AS STUDY_STORE_CNT,
    NVL(U.ICECREAM_STORE_CNT, 0)          AS ICECREAM_STORE_CNT,
    NVL(U.CAFE_STORE_CNT, 0)              AS CAFE_STORE_CNT,
    NVL(U.MEALKIT_STORE_CNT, 0)           AS MEALKIT_STORE_CNT,

    F.TOTAL_FLOW_POP                      AS TOTAL_FLOW_POP,
    F.TIME_17_21_FLOW_POP                 AS EVENING_FLOW_POP,
    (F.AGE20_FLOW_POP + F.AGE30_FLOW_POP) AS AGE20_30_FLOW_POP,

    R.TOTAL_RESIDENT_POP                  AS TOTAL_RESIDENT_POP,
    R.TOTAL_HOUSEHOLD_CNT                 AS TOTAL_HOUSEHOLD_CNT,
    R.APT_HOUSEHOLD_CNT                   AS APT_HOUSEHOLD_CNT,

    I.AVG_MONTH_INCOME_AMT                AS AVG_MONTH_INCOME_AMT,
    I.TOTAL_SPEND_AMT                     AS TOTAL_SPEND_AMT,
    I.FOOD_SPEND_AMT                      AS FOOD_SPEND_AMT,
    I.LEISURE_CULTURE_SPEND_AMT           AS LEISURE_CULTURE_SPEND_AMT,

    NVL(S.DISTRICT_TOTAL_STORE_CNT, 0)    AS DISTRICT_TOTAL_STORE_CNT,
    NVL(S.DISTRICT_OPEN_STORE_CNT, 0)     AS DISTRICT_OPEN_STORE_CNT,
    NVL(S.DISTRICT_CLOSE_STORE_CNT, 0)    AS DISTRICT_CLOSE_STORE_CNT,

    NVL(SA.DISTRICT_TOTAL_SALES_AMT, 0)   AS DISTRICT_TOTAL_SALES_AMT,
    NVL(SA.DISTRICT_TOTAL_SALES_CNT, 0)   AS DISTRICT_TOTAL_SALES_CNT

FROM STG_FLOW_GU_20254 F

LEFT JOIN (
    SELECT
        GU_NAME,
        COUNT(*) AS TOTAL_UNMANNED_STORE_CNT,
        SUM(CASE WHEN BIZ_TYPE = '무인사진관' THEN 1 ELSE 0 END) AS PHOTO_STORE_CNT,
        SUM(CASE WHEN BIZ_TYPE = '무인빨래방' THEN 1 ELSE 0 END) AS LAUNDRY_STORE_CNT,
        SUM(CASE WHEN BIZ_TYPE = '무인스터디카페' THEN 1 ELSE 0 END) AS STUDY_STORE_CNT,
        SUM(CASE WHEN BIZ_TYPE = '무인판매점(아이스크림)' THEN 1 ELSE 0 END) AS ICECREAM_STORE_CNT,
        SUM(CASE WHEN BIZ_TYPE = '무인판매점(카페)' THEN 1 ELSE 0 END) AS CAFE_STORE_CNT,
        SUM(CASE WHEN BIZ_TYPE = '무인판매점(밀키트)' THEN 1 ELSE 0 END) AS MEALKIT_STORE_CNT
    FROM STG_UNMANNED_STORE
    GROUP BY GU_NAME
) U
    ON F.GU_NAME = U.GU_NAME

LEFT JOIN STG_RESIDENT_GU_20254 R
    ON F.GU_NAME = R.GU_NAME

LEFT JOIN STG_INCOME_CONSUME_GU_20254 I
    ON F.GU_NAME = I.GU_NAME

LEFT JOIN (
    SELECT
        GU_NAME,
        SUM(STORE_CNT)       AS DISTRICT_TOTAL_STORE_CNT,
        SUM(OPEN_STORE_CNT)  AS DISTRICT_OPEN_STORE_CNT,
        SUM(CLOSE_STORE_CNT) AS DISTRICT_CLOSE_STORE_CNT
    FROM STG_STORE_GU_20254
    GROUP BY GU_NAME
) S
    ON F.GU_NAME = S.GU_NAME

LEFT JOIN (
    SELECT
        GU_NAME,
        SUM(SALES_AMT) AS DISTRICT_TOTAL_SALES_AMT,
        SUM(SALES_CNT) AS DISTRICT_TOTAL_SALES_CNT
    FROM STG_SALES_GU_20254
    GROUP BY GU_NAME
) SA
    ON F.GU_NAME = SA.GU_NAME;


SELECT * FROM MART_UNMANNED_STORE_GU_20254 ;

COMMENT ON TABLE MART_UNMANNED_STORE_GU_20254 IS '2025년 4분기 자치구별 무인점포 분포와 상권 환경을 결합한 MART 테이블';

COMMENT ON COLUMN MART_UNMANNED_STORE_GU_20254.BASE_YQ_CODE IS '기준 년분기 코드';
COMMENT ON COLUMN MART_UNMANNED_STORE_GU_20254.GU_CODE IS '자치구 코드';
COMMENT ON COLUMN MART_UNMANNED_STORE_GU_20254.GU_NAME IS '자치구명';

COMMENT ON COLUMN MART_UNMANNED_STORE_GU_20254.TOTAL_UNMANNED_STORE_CNT IS '총 무인점포 수';
COMMENT ON COLUMN MART_UNMANNED_STORE_GU_20254.PHOTO_STORE_CNT IS '무인사진관 수';
COMMENT ON COLUMN MART_UNMANNED_STORE_GU_20254.LAUNDRY_STORE_CNT IS '무인빨래방 수';
COMMENT ON COLUMN MART_UNMANNED_STORE_GU_20254.STUDY_STORE_CNT IS '무인스터디카페 수';
COMMENT ON COLUMN MART_UNMANNED_STORE_GU_20254.ICECREAM_STORE_CNT IS '무인판매점(아이스크림) 수';
COMMENT ON COLUMN MART_UNMANNED_STORE_GU_20254.CAFE_STORE_CNT IS '무인판매점(카페) 수';
COMMENT ON COLUMN MART_UNMANNED_STORE_GU_20254.MEALKIT_STORE_CNT IS '무인판매점(밀키트) 수';

COMMENT ON COLUMN MART_UNMANNED_STORE_GU_20254.TOTAL_FLOW_POP IS '총 유동인구 수';
COMMENT ON COLUMN MART_UNMANNED_STORE_GU_20254.EVENING_FLOW_POP IS '17시~21시 유동인구 수';
COMMENT ON COLUMN MART_UNMANNED_STORE_GU_20254.AGE20_30_FLOW_POP IS '20대와 30대 유동인구 합계';

COMMENT ON COLUMN MART_UNMANNED_STORE_GU_20254.TOTAL_RESIDENT_POP IS '총 상주인구 수';
COMMENT ON COLUMN MART_UNMANNED_STORE_GU_20254.TOTAL_HOUSEHOLD_CNT IS '총 가구 수';
COMMENT ON COLUMN MART_UNMANNED_STORE_GU_20254.APT_HOUSEHOLD_CNT IS '아파트 가구 수';

COMMENT ON COLUMN MART_UNMANNED_STORE_GU_20254.AVG_MONTH_INCOME_AMT IS '월 평균 소득 금액';
COMMENT ON COLUMN MART_UNMANNED_STORE_GU_20254.TOTAL_SPEND_AMT IS '총 소비금액';
COMMENT ON COLUMN MART_UNMANNED_STORE_GU_20254.FOOD_SPEND_AMT IS '음식 지출 금액';
COMMENT ON COLUMN MART_UNMANNED_STORE_GU_20254.LEISURE_CULTURE_SPEND_AMT IS '여가문화 지출 금액';

COMMENT ON COLUMN MART_UNMANNED_STORE_GU_20254.DISTRICT_TOTAL_STORE_CNT IS '자치구 전체 점포 수';
COMMENT ON COLUMN MART_UNMANNED_STORE_GU_20254.DISTRICT_OPEN_STORE_CNT IS '자치구 전체 개업 점포 수';
COMMENT ON COLUMN MART_UNMANNED_STORE_GU_20254.DISTRICT_CLOSE_STORE_CNT IS '자치구 전체 폐업 점포 수';

COMMENT ON COLUMN MART_UNMANNED_STORE_GU_20254.DISTRICT_TOTAL_SALES_AMT IS '자치구 전체 상권 매출 금액';
COMMENT ON COLUMN MART_UNMANNED_STORE_GU_20254.DISTRICT_TOTAL_SALES_CNT IS '자치구 전체 상권 매출 건수';


--최종 실행
SELECT *
  FROM MART_UNMANNED_STORE_GU_20254;
  
  
  
  
---TOP-N---