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
if "background" not in st.session_state:
    st.session_state.background = "흰색"
if "subject" not in st.session_state:
    st.session_state.subject = None  # 처음 과목 선택용

# ---------------- 동기부여 문구 ----------------
motivations_list = [
    "열심히 하면 반드시 보답이 온다.",
    "작은 성취가 큰 변화를 만든다.",
    "포기하지 말고 계속 나아가라.",
    "시간은 가장 소중한 자산이다.",
    "오늘의 노력은 내일의 힘이 된다."
]

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

# ---------------- 과목 선택 ----------------
if st.session_state.subject is None:
    st.session_state.subject = st.selectbox(
        "공부할 과목 선택", 
        ["국어", "영어", "수학", "생활과 윤리", "정치와 법", "한국지리"]
    )

# ---------------- 타이머 계산 ----------------
if st.session_state.running:
    elapsed = int(time.time() - st.session_state.start_time + st.session_state.elapsed)
else:
    elapsed = st.session_state.elapsed

hours, remainder = divmod(elapsed, 3600)
minutes, seconds = divmod(remainder, 60)

# ---------------- 동기부여 문구 갱신 ----------------
if time.time() - st.session_state.last_motivation_time > 600 or st.session_state.last_motivation == "":
    st.session_state.last_motivation = random.choice(motivations_list)
    st.session_state.last_motivation_time = time.time()

st.markdown(f"## 💡 {st.session_state.last_motivation}")
st.markdown(f"# ⏱️ {hours:02d}:{minutes:02d}:{seconds:02d}")

# ---------------- 버튼 컨트롤 ----------------
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
        record_date = st.date_input("기록할 날짜 선택", date.today())
        st.session_state.records.append({
            "날짜": record_date.strftime("%Y-%m-%d"),
            "과목": st.session_state.subject,
            "순공부시간(h)": round(elapsed / 3600, 2)
        })
        st.session_state.start_time = None
        st.session_state.elapsed = 0
        st.session_state.running = False

# ---------------- 기록 표시 ----------------
if st.session_state.records:
    df = pd.DataFrame(st.session_state.records)
    st.dataframe(df, use_container_width=True)

# ---------------- 자동 새로고침 (실시간 타이머) ----------------
from streamlit_autorefresh import st_autorefresh
if st.session_state.running:
    st_autorefresh(interval=1000, key="timer")  # 1초마다 안전하게 새로고침
