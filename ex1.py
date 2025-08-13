import streamlit as st
import pandas as pd
from datetime import date, timedelta
import math

st.set_page_config(page_title="MBTI별 공부 계획표", page_icon="📚", layout="wide")
st.title("📚 MBTI 맞춤형 공부 계획표")

st.write("MBTI 성향에 따라 하루 공부량을 다르게 분배합니다.")

# MBTI 입력
mbti = st.text_input("당신의 MBTI를 입력하세요 (예: INFP, ESTJ)").upper()

# MBTI 가중치 (마지막 글자와 첫 글자 위주로 반영)
def get_distribution_factor(mbti_type, days):
    if not mbti_type or len(mbti_type) != 4:
        return [1/days] * days  # 균등 분배 (기본값)
    
    factor = []
    if mbti_type[3] == "J":  # 계획형
        factor = [1/days] * days
    elif mbti_type[3] == "P":  # 즉흥형
        factor = [0.05 * (i+1) for i in range(days)]
    else:
        factor = [1/days] * days

    # E/I로 초반/후반 가중치 조절
    if mbti_type[0] == "E":  # 외향형 → 초반 집중
        factor = [f * (1.2 if i < days/2 else 0.8) for i, f in enumerate(factor)]
    elif mbti_type[0] == "I":  # 내향형 → 후반 집중
        factor = [f * (0.8 if i < days/2 else 1.2) for i, f in enumerate(factor)]

    total = sum(factor)
    return [f / total for f in factor]  # 합계 1로 정규화

# 과목 입력
num_subjects = st.number_input("과목 개수", min_value=1, max_value=10, value=2)

subjects = []
for i in range(num_subjects):
    col1, col2, col3 = st.columns(3)
    with col1:
        name = st.text_input(f"{i+1}번 과목 이름", key=f"name_{i}")
    with col2:
        exam_day = st.date_input(f"{i+1}번 과목 시험 날짜", key=f"date_{i}")
    with col3:
        total_amount = st.number_input(f"{i+1}번 과목 총 공부 분량 (페이지/챕터 수)", min_value=1, key=f"amount_{i}")
    if name and exam_day and total_amount:
        subjects.append({"subject": name, "exam_date": exam_day, "total_amount": total_amount})

# 계획 생성
if st.button("계획 만들기"):
    if not subjects:
        st.error("과목명, 시험 날짜, 공부 분량을 모두 입력하세요.")
    else:
        today = date.today()
        plan_data = []

        for subj in subjects:
            days_left = (subj["exam_date"] - today).days
            if days_left <= 0:
                plan_data.append([subj["subject"], "시험일이 지났거나 오늘입니다!", ""])
            else:
                dist = get_distribution_factor(mbti, days_left)
                done = 0
                for d in range(days_left):
                    day_plan = today + timedelta(days=d)
                    amount = math.ceil(subj["total_amount"] * dist[d])
                    if amount > 0:
                        start = done + 1
                        end = min(done + amount, subj["total_amount"])
                        done = end
                        plan_text = f"{start}~{end} 페이지 공부"
                    else:
                        plan_text = "복습 또는 휴식"
                    plan_data.append([subj["subject"], day_plan, plan_text])

        df = pd.DataFrame(plan_data, columns=["과목", "날짜", "계획"])
        st.subheader("📅 MBTI 맞춤 공부 계획표")
        st.dataframe(df)

        # CSV 다운로드
        csv = df.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            label="📥 계획표 다운로드 (CSV)",
            data=csv,
            file_name="mbti_study_plan.csv",
            mime="text/csv"
        )
