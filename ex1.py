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
if "selected_subject" not in st.session_state:
    st.session_state.selected_subject = st.selectbox("공부할 과목 선택", ["국어", "영어", "수학", "생활과 윤리", "정치와 법", "한국지리"])

# ---------------- 동기부여 문구 ----------------
motivations = {
    "국어": ["글쓰기 중요 문구1", "글쓰기 중요 문구2"],
    "영어": ["영어 중요 문구1", "영어 중요 문구2"],
    "수학": ["수학 중요 문구1", "수학 중요 문구2"],
    "생활과 윤리": ["윤리 중요 문구1", "윤리 중요 문구2"],
    "정치와 법": ["정치 중요 문구1", "정치 중요 문구2"],
    "한국지리": ["지리 중요 문구1", "지리 중요 문구2"]
}

# 10분마다 문구 변경
if time.time() - st.session_state.last_motivation_time > 600:
    st.session_state.last_motivation = random.choice(motivations[st.session_state.selected_subject])
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
        record_date = st.date_input("기록 날짜 선택", date.today())
        st.session_state.records.append({
            "날짜": record_date.strftime("%Y-%m-%d"),
            "과목": st.session_state.selected_subject,
            "순공부시간(h)": round(elapsed / 3600, 2)
        })
        st.session_state.start_time = None
        st.session_state.elapsed = 0
        st.session_state.running = False

# ---------------- 기록 표시 ----------------
if st.session_state.records:
    df = pd.DataFrame(st.session_state.records)
    st.dataframe(df, use_container_width=True)

# ---------------- 실시간 갱신 ----------------
from streamlit_autorefresh import st_autorefresh
st_autorefresh(interval=1000, key="timer_refresh")
