import streamlit as st
import datetime
import pandas as pd
import random
from streamlit_autorefresh import st_autorefresh

# -------------------------------
# 초기 세션 상태 설정
# -------------------------------
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

# -------------------------------
# 동기부여 문구 (30개)
# -------------------------------
motivations = [
    "작은 발걸음이 큰 변화를 만든다!",
    "오늘의 노력은 내일의 자신감을 만든다!",
    "포기하지 않는 사람이 결국 해낸다!",
    "천천히 가도 멈추지 말자!",
    "노력은 배신하지 않는다!",
    "지금 하는 공부가 미래의 나를 만든다!",
    "오늘 흘린 땀은 내일의 영광!",
    "할 수 있다, 반드시 해내자!",
    "어제보다 나은 오늘을 만들자!",
    "끝까지 해보자!",
    "시작이 반이다!",
    "작심삼일도 백 번이면 300일!",
    "실패는 성공의 발판!",
    "집중은 최고의 무기다!",
    "할 수 있다는 믿음이 반이다!",
    "노력의 즐거움을 느껴라!",
    "지금 이 순간이 기회다!",
    "꾸준함이 곧 실력이다!",
    "포기하지 않으면 반드시 도착한다!",
    "공부는 배신하지 않는다!",
    "오늘을 버티면 내일은 더 쉽다!",
    "마지막까지 해보자!",
    "땀은 거짓말하지 않는다!",
    "작은 습관이 큰 성과를 만든다!",
    "할 수 있다, 넌 강하다!",
    "오늘 공부가 미래를 바꾼다!",
    "끝날 때까지 끝난 게 아니다!",
    "잠깐의 고통, 영원한 자유!",
    "나 자신을 믿어라!",
    "네가 해낼 때까지 끝난 게 아니다!"
]

# -------------------------------
# 제목 = 동기부여 문구 (10분마다 변경)
# -------------------------------
minutes_passed = datetime.datetime.now().minute
motivation_index = (minutes_passed // 10) % len(motivations)
motivation_text = motivations[motivation_index]
st.markdown(f"# 💡 {motivation_text}")

# -------------------------------
# D-Day 설정
# -------------------------------
exam_date = datetime.date(2025, 11, 13)  # 수능 가정일
today = datetime.date.today()
d_day = (exam_date - today).days
st.markdown(f"📅 수능까지 D-{d_day}")

# -------------------------------
# 과목 선택
# -------------------------------
subject = st.selectbox("공부 과목 선택", ["국어", "영어", "수학", "생활과 윤리", "정치와 법", "한국지리"])

# -------------------------------
# 실시간 타이머 (자동 새로고침)
# -------------------------------
st_autorefresh(interval=1000, key="timer_refresh")  # 1초마다 새로고침

if st.button("▶ 시작", key="start"):
    if not st.session_state.running:
        st.session_state.start_time = datetime.datetime.now()
        st.session_state.running = True

if st.button("⏸ 멈춤", key="stop"):
    if st.session_state.running:
        st.session_state.elapsed += (datetime.datetime.now() - st.session_state.start_time).seconds
        st.session_state.running = False

# 경과 시간 계산
if st.session_state.running:
    elapsed = st.session_state.elapsed + (datetime.datetime.now() - st.session_state.start_time).seconds
else:
    elapsed = st.session_state.elapsed

hours, remainder = divmod(elapsed, 3600)
minutes, seconds = divmod(remainder, 60)
st.markdown(f"### ⏱ {hours:02d}:{minutes:02d}:{seconds:02d}")

# -------------------------------
# 기록 버튼 (작게 만들기)
# -------------------------------
if st.button("💾 오늘 공부 기록 저장", key="save_record"):
    st.session_state.records.append({
        "날짜": today,
        "과목": subject,
        "순공부시간(h)": round(elapsed / 3600, 2)
    })
    st.session_state.elapsed = 0
    st.session_state.running = False

# -------------------------------
# 기록 표시 (캘린더형 테이블)
# -------------------------------
if st.session_state.records:
    df = pd.DataFrame(st.session_state.records)
    st.dataframe(df, use_container_width=True)
