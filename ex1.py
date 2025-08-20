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
if "subject" not in st.session_state:
    st.session_state.subject = None

# ---------------- 동기부여 문구 ----------------
motivations = {
    "국어": ["글쓰기는 사고를 명료하게 한다. - 윌리엄 제임스", "독서는 마음의 양식이다. - 프랜시스 베이컨"],
    "영어": ["미래는 자신의 꿈을 믿는 자의 것이다. - 엘리너 루즈벨트", "끝내기 전까지는 항상 불가능해 보인다. - 넬슨 만델라"],
    "수학": ["수학은 문제 해결의 힘을 길러준다. - 피타고라스", "패턴을 이해하면 세상이 명확해진다. - 아르키메데스"]
}

# ---------------- 배경 선택 ----------------
backgrounds = {
    "흰색": "white", "빨강": "red", "주황": "orange", "노랑": "yellow",
    "검정": "black", "무지개": "linear-gradient(to right, red, orange, yellow, green, blue, indigo, violet)"
}
bg_choice = st.sidebar.selectbox("배경 선택", list(backgrounds.keys()))
bg_color = backgrounds[bg_choice]
st.markdown(f"<style>.stApp {{background: {bg_color};}}</style>", unsafe_allow_html=True)

# ---------------- 시험 날짜 (D-Day) ----------------
target_date = st.sidebar.date_input("시험 날짜 선택", date(2025, 11, 15))
days_left = (target_date - date.today()).days
st.sidebar.markdown(f"📅 시험까지 **{days_left}일 남음**")

# ---------------- 과목 선택 ----------------
if st.session_state.subject is None:
    st.session_state.subject = st.selectbox("공부할 과목 선택", list(motivations.keys()))

# ---------------- 플레이스홀더 ----------------
timer_placeholder = st.empty()
motivation_placeholder = st.empty()
record_placeholder = st.empty()

# ---------------- 동기부여 업데이트 ----------------
def update_motivation():
    if time.time() - st.session_state.last_motivation_time > 600 or st.session_state.last_motivation == "":
        st.session_state.last_motivation = random.choice(motivations[st.session_state.subject])
        st.session_state.last_motivation_time = time.time()
    motivation_placeholder.markdown(f"## 💡 {st.session_state.last_motivation}")

# ---------------- 타이머 업데이트 ----------------
def update_timer():
    if st.session_state.running and st.session_state.start_time:
        elapsed = int(time.time() - st.session_state.start_time + st.session_state.elapsed)
    else:
        elapsed = st.session_state.elapsed
    hours, remainder = divmod(elapsed, 3600)
    minutes, seconds = divmod(remainder, 60)
    timer_placeholder.markdown(f"# ⏱️ {hours:02d}:{minutes:02d}:{seconds:02d}")

update_motivation()
update_timer()

# ---------------- 버튼 ----------------
col1, col2, col3 = st.columns(3)

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
    if st.button("💾 기록"):
        # 기록 날짜 선택
        record_date = st.date_input("기록할 날짜 선택", date.today())
        elapsed_time = st.session_state.elapsed
        st.session_state.records.append({
            "날짜": record_date.strftime("%Y-%m-%d"),
            "과목": st.session_state.subject,
            "순공부시간(h)": round(elapsed_time / 3600, 2)
        })
        # 기록 후 타이머 초기화
        st.session_state.start_time = None
        st.session_state.elapsed = 0
        st.session_state.running = False
        # 기록 바로 표시
        if st.session_state.records:
            df = pd.DataFrame(st.session_state.records)
            record_placeholder.dataframe(df, use_container_width=True)

# ---------------- 기록 표시 ----------------
if st.session_state.records:
    df = pd.DataFrame(st.session_state.records)
    record_placeholder.dataframe(df, use_container_width=True)

# ---------------- 실시간 업데이트 ----------------
if st.session_state.running:
    while st.session_state.running:
        update_timer()
        update_motivation()
        time.sleep(1)
