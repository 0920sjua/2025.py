import streamlit as st
import datetime
import time
import pandas as pd
import random

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

# ---------------- 동기부여 문구 ----------------
motivations = [
    "작은 습관이 큰 성공을 만든다!",
    "오늘의 땀이 내일의 힘이다!",
    "포기하지 말고 한 걸음 더!",
    "성공은 준비된 자의 몫이다!",
    "시간은 금, 지금 바로 시작하자!",
    "지금 하는 공부가 미래를 바꾼다!",
    "노력 위에 꽃이 핀다!",
    "끝까지 하는 자가 승리한다!",
    "오늘의 고생이 내일의 영광이다!",
    "포기하지 않으면 실패하지 않는다!",
    "천 리 길도 한 걸음부터!",
    "땀은 배신하지 않는다!",
    "작은 성취가 큰 자신감을 만든다!",
    "내일의 나는 오늘의 나에게 달려 있다!",
    "한 문제 더! 한 줄 더!",
    "꾸준함이 최강의 무기다!",
    "오늘도 달려가자!",
    "목표를 향해 집중!",
    "스스로를 믿어라!",
    "성실이 최고의 재능이다!",
    "포기 대신 도전!",
    "어제보다 나은 오늘!",
    "노력은 결코 배신하지 않는다!",
    "작심삼일도 백 번이면 1년이다!",
    "너는 할 수 있다!",
    "조금만 더 버티자!",
    "끝까지 간 사람이 이긴다!",
    "오늘 공부가 내일의 나를 만든다!",
    "성공은 성실을 먹고 자란다!",
    "공부는 나를 위한 최고의 투자다!"
]

# ---------------- UI ----------------
today = datetime.date.today()
st.set_page_config(page_title="공부 타이머", layout="centered")

# 동기부여 문구 10분마다 변경
if "last_motivation_time" not in st.session_state:
    st.session_state.last_motivation_time = time.time()

if time.time() - st.session_state.last_motivation_time > 600:
    st.session_state.last_motivation = random.choice(motivations)
    st.session_state.last_motivation_time = time.time()
elif not st.session_state.last_motivation:
    st.session_state.last_motivation = random.choice(motivations)

st.markdown(f"# 💡 {st.session_state.last_motivation}")

# 과목 선택
subject = st.selectbox("과목 선택", ["국어", "영어", "수학", "생활과 윤리", "정치와 법", "한국지리"])

# ---------------- 실시간 타이머 ----------------
timer_placeholder = st.empty()

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("▶ 시작", key="start"):
        if not st.session_state.running:
            st.session_state.start_time = datetime.datetime.now()
            st.session_state.running = True
with col2:
    if st.button("⏸ 멈춤", key="stop"):
        if st.session_state.running:
            st.session_state.elapsed += (datetime.datetime.now() - st.session_state.start_time).seconds
            st.session_state.running = False
with col3:
    if st.button("💾 기록", key="save"):
        elapsed = st.session_state.elapsed
        h, r = divmod(elapsed, 3600)
        m, s = divmod(r, 60)
        st.session_state.records.append({
            "날짜": today.strftime("%Y-%m-%d"),
            "과목": subject,
            "순공부시간(h)": round(elapsed/3600, 2)
        })
        st.session_state.elapsed = 0
        st.session_state.running = False
        st.success("기록이 저장되었습니다!")

# ⏱ 타이머 표시 (1초마다 갱신)
if st.session_state.running:
    elapsed = st.session_state.elapsed + (datetime.datetime.now() - st.session_state.start_time).seconds
else:
    elapsed = st.session_state.elapsed

h, r = divmod(elapsed, 3600)
m, s = divmod(r, 60)
timer_placeholder.markdown(f"## ⏱ {h:02d}:{m:02d}:{s:02d}")

# ---------------- 공부 기록 ----------------
if st.session_state.records:
    df = pd.DataFrame(st.session_state.records)
    st.dataframe(df, use_container_width=True)

# ---------------- 자동 새로고침 (1초) ----------------
time.sleep(1)
st.rerun()
