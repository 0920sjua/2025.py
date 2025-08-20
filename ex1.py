import streamlit as st
import time
import pandas as pd
import random
from datetime import date

# ---------------- 세션 상태 초기화 ----------------
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "elapsed" not in st.session_state:
    st.session_state.elapsed = 0
if "running" not in st.session_state:
    st.session_state.running = False
if "records" not in st.session_state:
    st.session_state.records = []
if "last_motivation" not in st.session_state:
    st.session_state.last_motivation = ""
if "last_motivation_time" not in st.session_state:
    st.session_state.last_motivation_time = time.time()

# ---------------- 과목 선택 ----------------
subject = st.sidebar.selectbox("공부할 과목 선택", ["국어", "영어", "수학", "생활과 윤리", "정치와 법", "한국지리"])

# ---------------- 배경화면 설정 ----------------
backgrounds = {
    "흰색": "white",
    "빨강": "red",
    "주황": "orange",
    "노랑": "yellow",
    "검정": "black",
    "무지개": "linear-gradient(to right, red, orange, yellow, green, blue, indigo, violet)"
}
bg_choice = st.sidebar.selectbox("배경 선택", list(backgrounds.keys()))
bg_color = backgrounds[bg_choice]
st.markdown(f"""
<style>
.stApp {{
    background: {bg_color};
}}
</style>
""", unsafe_allow_html=True)

# ---------------- D-Day 설정 ----------------
target_date = st.sidebar.date_input("시험 날짜 선택", date(2025, 11, 15))
days_left = (target_date - date.today()).days
st.sidebar.markdown(f"📅 시험까지 **{days_left}일 남음**")

# ---------------- 동기부여 문구 ----------------
motivations = {
    "국어": ["글쓰기는 사고를 명료하게 한다. - 윌리엄 제임스", "독서는 마음의 양식이다. - 프랜시스 베이컨"],
    "영어": ["미래는 자신의 꿈을 믿는 자의 것이다. - 엘리너 루즈벨트", "끝내기 전까지는 항상 불가능해 보인다. - 넬슨 만델라"],
    "수학": ["수학은 문제 해결의 힘을 길러준다. - 피타고라스", "패턴을 이해하면 세상이 명확해진다. - 아르키메데스"],
    "생활과 윤리": ["정직은 모든 행동의 기초다. - 아리스토텔레스", "배려는 세상을 바꾼다. - 달라이 라마"],
    "정치와 법": ["법은 사회를 지킨다. - 몽테스키외", "정치는 삶의 기술이다. - 아리스토텔레스"],
    "한국지리": ["지리를 알면 세상이 보인다. - 지리학자1", "지역을 이해하면 역사가 보인다. - 지리학자2"]
}

# 10분마다 문구 변경
if time.time() - st.session_state.last_motivation_time > 600:
    st.session_state.last_motivation = random.choice(motivations[subject])
    st.session_state.last_motivation_time = time.time()

st.markdown(f"## 💡 {st.session_state.last_motivation}")

# ---------------- 타이머 계산 ----------------
if st.session_state.running:
    elapsed = int(time.time() - st.session_state.start_time + st.session_state.elapsed)
else:
    elapsed = st.session_state.elapsed

hours, remainder = divmod(elapsed, 3600)
minutes, seconds = divmod(remainder, 60)
st.markdown(f"# ⏱️ {hours:02d}:{minutes:02d}:{seconds:02d}")

# ---------------- 버튼 ----------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("▶ 시작"):
        if not st.session_state.running:
            st.session_state.start_time = time.time()
            st.session_state.running = True

with col2:
    if st.button("⏸ 정지"):
        if st.session_state.running:
            st.session_state.elapsed += int(time.time() - st.session_state.start_time)
            st.session_state.running = False

with col3:
    if st.button("⏹ 리셋"):
        st.session_state.start_time = None
        st.session_state.elapsed = 0
        st.session_state.running = False

with col4:
    if st.button("💾 기록"):
        record_date = st.date_input("기록 날짜 선택", date.today())
        st.session_state.records.append({
            "날짜": record_date.strftime("%Y-%m-%d"),
            "과목": subject,
            "순공부시간(h)": round(elapsed / 3600, 2)
        })
        st.session_state.start_time = None
        st.session_state.elapsed = 0
        st.session_state.running = False

# ---------------- 기록 표시 ----------------
if st.session_state.records:
    df = pd.DataFrame(st.session_state.records)
    st.dataframe(df, use_container_width=True)

# ---------------- 자동 새로고침 ----------------
if st.session_state.running:
    st.experimental_rerun()
