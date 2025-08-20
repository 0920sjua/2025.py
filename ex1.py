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
    st.session_state.last_motivation_time = time.time()   # ✅ None 대신 현재 시간으로 초기화
if "background" not in st.session_state:
    st.session_state.background = "흰색"

# ---------------- 동기부여 문구 ----------------
motivations = [
    "지금 이 순간이 너의 미래를 만든다!",
    "포기하지 마라, 끝까지 버텨라!",
    "오늘의 땀이 내일의 영광이다!",
    "조금만 더 힘내자!",
    "성공은 준비된 자의 것이다!",
    "작은 성취가 큰 변화를 만든다!",
    "노력 없는 꿈은 없다!",
    "오늘 할 일을 내일로 미루지 말자!",
    "너 자신을 믿어라!",
    "할 수 있다, 반드시!",
    "실패는 성공으로 가는 디딤돌이다!",
    "꾸준함이 가장 큰 무기다!",
    "너의 가능성은 무한하다!",
    "끝까지 해보자!",
    "불가능은 없다!",
    "오늘도 최선을 다하자!",
    "성장은 고통 속에서 이루어진다!",
    "노력은 배신하지 않는다!",
    "지금의 선택이 미래를 결정한다!",
    "다시 시작하자, 늦지 않았다!",
    "오늘의 고생이 내일의 행복이다!",
    "넌 이미 잘하고 있어!",
    "계속 가면 된다!",
    "포기하는 순간 끝이다!",
    "더 강해질 수 있다!",
    "실패해도 괜찮다, 다시 하면 된다!",
    "매일 조금씩 나아지자!",
    "꿈은 이루어진다!",
    "너의 미래는 빛날 것이다!",
    "오늘도 화이팅!"
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

page_bg = f"""
<style>
.stApp {{
    background: {bg_color};
}}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# ---------------- D-Day 설정 ----------------
target_date = st.sidebar.date_input("시험 날짜 선택", date(2025, 11, 15))
days_left = (target_date - date.today()).days
st.sidebar.markdown(f"📅 시험까지 **{days_left}일 남음**")

# ---------------- 실시간 타이머 ----------------
if st.session_state.running:
    elapsed = int(time.time() - st.session_state.start_time + st.session_state.elapsed)
else:
    elapsed = st.session_state.elapsed

hours, remainder = divmod(elapsed, 3600)
minutes, seconds = divmod(remainder, 60)

# ---------------- 동기부여 문구 (10분마다 변경) ----------------
if time.time() - st.session_state.last_motivation_time > 600:
    st.session_state.last_motivation = random.choice(motivations)
    st.session_state.last_motivation_time = time.time()

st.markdown(f"## 💡 {st.session_state.last_motivation}")

# ---------------- 타이머 표시 ----------------
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
        study_subject = st.selectbox("과목 선택", ["국어", "영어", "수학", "생활과 윤리", "정치와 법", "한국지리"], key=f"subject_{len(st.session_state.records)}")
        st.session_state.records.append({
            "날짜": date.today().strftime("%Y-%m-%d"),
            "과목": study_subject,
            "순공부시간(h)": round(elapsed / 3600, 2)
        })
        st.session_state.start_time = None
        st.session_state.elapsed = 0
        st.session_state.running = False

# ---------------- 기록 표시 ----------------
if st.session_state.records:
    df = pd.DataFrame(st.session_state.records)
    st.dataframe(df, use_container_width=True)

# ---------------- 자동 새로고침 (실시간 타이머 효과) ----------------
if st.session_state.running:
    time.sleep(1)
    st.rerun()
