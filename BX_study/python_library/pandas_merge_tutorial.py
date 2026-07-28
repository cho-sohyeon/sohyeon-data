import pandas as pd

# 1. 데이터 준비 (비유: 두 종류의 종이 문서)
# [왼쪽 테이블] 우리 반 전체 학생 명단
df_students = pd.DataFrame({
    'ID': [1, 2, 3, 4],
    '이름': ['김철수', '이영희', '박민수', '최지우']
})

# [오른쪽 테이블] 오늘 수업 출석 체크 기록
# (참고: 5번 '게스트'는 명단에는 없지만 오늘 청강하러 온 학생입니다)
df_attendance = pd.DataFrame({
    'ID': [1, 2, 5],
    '출석시간': ['09:00', '09:05', '09:10']
})

print("--- [기초 데이터] ---")
print("1. 전체 학생 명단 (Left):")
print(df_students)
print("\n2. 오늘 출석 기록 (Right):")
print(df_attendance)
print("-" * 30)

# 2. 이너 조인 (Inner Join)
# 비유: "명단에도 있고, 실제로 출석도 한 학생들만 모아보자!" (교집합)
inner_merged = pd.merge(df_students, df_attendance, on='ID', how='inner')

# 3. 레프트 조인 (Left Join)
# 비유: "우리 반 학생들은 다 보여주고, 출석한 애들은 옆에 시간 적어줘. 안 온 애들은 비워두고(NaN)."
left_merged = pd.merge(df_students, df_attendance, on='ID', how='left')

# 4. 라이트 조인 (Right Join)
# 비유: "누가 됐든 출석 기록에 있는 사람 위주로 보여줘. 명단에 없는 게스트라도!"
right_merged = pd.merge(df_students, df_attendance, on='ID', how='right')

# 결과 출력
print("\n[결과 1] 이너 조인 (Inner): 명단에도 있고 출석도 한 학생")
print(inner_merged)

print("\n[결과 2] 레프트 조인 (Left): 우리 반 명단 위주 (안 온 사람은 빈칸)")
print(left_merged)

print("\n[결과 3] 라이트 조인 (Right): 출석 기록 위주 (게스트 포함)")
print(right_merged)

print("\n" + "=" * 30)
print("--- 각 조인 결과의 행(Row) 수 ---")
print(f"이너 조인: {len(inner_merged)}행 (진짜 출석자 2명)")
print(f"레프트 조인: {len(left_merged)}행 (전체 학생 4명)")
print(f"라이트 조인: {len(right_merged)}행 (출석 기록 3명)")
print("=" * 30)
