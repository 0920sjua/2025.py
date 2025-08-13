import streamlit as st
import pandas as pd
from datetime import date, timedelta
import math

st.set_page_config(page_title="시험 공부 계획표", page_icon="📚", layout="wide")
st.title("📚 시험 공부량 자동 계획표")

st.write("시험 날짜와 총 공부 분량을 입력하면 하루 공부량을 자동 계산합니다.")

# 과목 입력
num_subjects = st.number_input("과목 개수", min_value=1, max_value=10, value=3)

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
                daily_amount = math.ceil(subj["total_amount"] / days_left)
                for d in range(days_left):
                    day_plan = today + timedelta(days=d)
                    start = d * daily_amount + 1
                    end = min((d + 1) * daily_amount, subj["total_amount"])
                    plan_text = f"{start}~{end} 페이지 공부"
                    plan_data.append([subj["subject"], day_plan, plan_text])

        df = pd.DataFrame(plan_data, columns=["과목", "날짜", "계획"])
        st.subheader("📅 하루 공부량 계획표")
        st.dataframe(df)

        # CSV 다운로드
        csv = df.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            label="📥 계획표 다운로드 (CSV)",
            data=csv,
            file_name="study_plan.csv",
            mime="text/csv"
        )
