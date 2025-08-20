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

# ---------------- 동기부여 문구 ----------------
motivations = {
    "국어": [
        "글쓰기는 사고를 명료하게 한다. - 윌리엄 제임스",
        "독서는 마음의 양식이다. - 프랜시스 베이컨",
        "배운 것을 글로 표현하면 진정한 이해가 된다. - 루소",
        "언어는 사고의 집이다. - 루트비히 비트겐슈타인"
        # ... 필요하면 더 추가
    ],
    "영어": [
        "미래는 자신의 꿈을 믿는 자의 것이다. - 엘리너 루즈벨트",
        "끝내기 전까지는 항상 불가능해 보인다. - 넬슨 만델라"
        # ...
    ],
    # 수학, 생활과 윤리, 정치와 법, 한국지리 동일하게 추가
}

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

# ---------------- 타이머 표시 ----------------
timer_placeholder = st.empty()
motivation_placeholder = st.empty()
record_placeholder = st.empty()

def update_motivation():
    # 10분마다 동기부여 바꾸기
    if time.time() - st.session_state.last_motivation_time > 600 or st.session_state.last_motivation == "":
        all_subjects = sum(motivations.values(), [])
        st.session_state.last_motivation = random.choice(all_subjects)
        st.session_state.last_motivation_time = time.time()
    motivation_placeholder.markdown(f"## 💡 {st.session_state.last_motivation}")

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
        study_subject = st.selectbox("과목 선택", ["국어", "영어", "수학", "생활과 윤리", "정치와 법", "한국지리"], key=f"subject_{len(st.session_state.records)}")
        st.session_state.records.append({
            "날짜": date.today().strftime("%Y-%m-%d"),
            "과목": study_subject,
            "순공부시간(h)": round(st.session_state.elapsed / 3600, 2)
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

# ---------------- 실시간 업데이트 루프 ----------------
if st.session_state.running:
    while st.session_state.running:
        update_timer()
        update_motivation()
        time.sleep(1)
