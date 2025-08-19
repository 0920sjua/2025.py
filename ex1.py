import streamlit as st
import time
import pandas as pd
import datetime

# -------------------------------
# 세션 상태 초기화
# -------------------------------
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "elapsed" not in st.session_state:
    st.session_state.elapsed = 0
if "running" not in st.session_state:
    st.session_state.running = False
if "logs" not in st.session_state:
    st.session_state.logs = []
if "current_subject" not in st.session_state:
    st.session_state.current_subject = None

# -------------------------------
# 동기부여 문구
# -------------------------------
motivations = [
    "🚀 지금의 땀이 내일의 너를 만든다!",
    "🔥 넌 할 수 있어, 끝까지 가보자!",
    "📖 작은 습관이 큰 성공을 만든다!",
    "⏳ 시간은 금, 낭비하지 말자!",
    "🌟 노력은 배신하지 않는다.",
    "💡 오늘의 1시간이 내일의 10시간을 바꾼다!",
    "🦁 강한 자가 아니라 끝까지 하는 자가 이긴다.",
    "🎯 목표는 분명히, 노력은 꾸준히!",
    "🚴 넘어져도 다시 일어서면 된다.",
    "🌱 씨앗은 바로 자라지 않지만 반드시 자란다."
]

# -------------------------------
# UI
# -------------------------------
st.title("📚 공부 타이머 + 기록 앱")

# D-Day 입력
exam_date = st.date_input("시험 날짜를 선택하세요:", datetime.date(2025, 11, 15))
days_left = (exam_date - datetime.date.today()).days
st.metric("시험까지 남은 D-Day", f"{days_left}일")

st.markdown("## ⏱ 공부 타이머")

# -------------------------------
# 과목 선택
# -------------------------------
subjects = ["국어", "영어", "수학", "생활과 윤리", "정치와 법", "한국지리"]
subject = st.selectbox("공부할 과목을 선택하세요:", subjects)

# -------------------------------
# 타이머 버튼
# -------------------------------
col1, col2 = st.columns(2)
with col1:
    if st.button("▶️ 시작", use_container_width=True):
        if not st.session_state.running:
            st.session_state.start_time = time.time()
            st.session_state.running = True
            st.session_state.current_subject = subject  # 현재 과목 기록
with col2:
    if st.button("⏸ 멈춤", use_container_width=True):
        if st.session_state.running:
            st.session_state.elapsed += time.time() - st.session_state.start_time
            st.session_state.running = False
            # 로그 저장
            today = datetime.date.today().isoformat()
            st.session_state.logs.append({
                "날짜": today,
                "과목": st.session_state.current_subject,
                "순공부시간(초)": int(st.session_state.elapsed)
            })
            st.session_state.elapsed = 0
            st.session_state.current_subject = None

# -------------------------------
# 실시간 타이머
# -------------------------------
timer_placeholder = st.empty()
motivation_placeholder = st.empty()

if st.session_state.running:
    while st.session_state.running:
        elapsed = st.session_state.elapsed + (time.time() - st.session_state.start_time)
        h, m, s = int(elapsed // 3600), int((elapsed % 3600) // 60), int(elapsed % 60)
        timer_placeholder.metric("공부 시간", f"{h:02}:{m:02}:{s:02} ({st.session_state.current_subject})")

        # 10분마다 동기부여 문구 바꾸기
        if int(elapsed) % 600 == 0 and int(elapsed) > 0:
            idx = (int(elapsed) // 600) % len(motivations)
            motivation_placeholder.subheader(motivations[idx])

        time.sleep(1)
else:
    elapsed = st.session_state.elapsed
    h, m, s = int(elapsed // 3600), int((elapsed % 3600) // 60), int(elapsed % 60)
    if st.session_state.current_subject:
        timer_placeholder.metric("공부 시간", f"{h:02}:{m:02}:{s:02} ({st.session_state.current_subject})")
    else:
        timer_placeholder.metric("공부 시간", f"{h:02}:{m:02}:{s:02}")

# -------------------------------
# 공부 기록 (과목별 + 일별)
# -------------------------------
st.markdown("## 🗓 공부 기록 (과목별, 일별)")
if st.session_state.logs:
    df = pd.DataFrame(st.session_state.logs)
    df["순공부시간(h)"] = (df["순공부시간(초)"] / 3600).round(2)
    st.dataframe(df[["날짜", "과목", "순공부시간(h)"]], use_container_width=True)
else:
    st.info("아직 공부 기록이 없습니다.")
