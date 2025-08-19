import streamlit as st
import pandas as pd
import datetime
import time
import random

# -------------------------------
# 기본 설정
# -------------------------------
st.set_page_config(page_title="공부 타이머", page_icon="⏳", layout="centered")

motivation_messages = [
    "🔥 지금 이 순간이 기회다!",
    "💪 끝까지 가면 반드시 이긴다!",
    "🚀 오늘의 1시간이 미래를 바꾼다!",
    "📚 공부는 배신하지 않는다!",
    "🏆 포기하지 않으면 반드시 해낸다!",
    "🌱 작은 습관이 큰 변화를 만든다!",
    "🎯 목표는 멀어도 한 걸음씩!",
    "⚡ 지금의 너를 이겨라!",
    "🔑 성실이 최고의 재능이다!",
    "✨ 오늘의 노력은 내일의 자신감!",
    "🔥 조금만 더 하면 목표에 가까워진다!",
    "💪 집중은 최고의 무기다!",
    "🚀 남과 비교하지 말고 어제의 나와 비교하자!",
    "🌱 실패는 성장의 일부다!",
    "🏆 꾸준함이 승리한다!",
    "📚 오늘 공부는 내일의 자산!",
    "⚡ 지금 집중하면 불가능은 없다!",
    "🎯 시작이 반이다!",
    "🔑 끝까지 집중!",
    "✨ 노력 없이는 결과도 없다!",
    "🔥 오늘도 성장 중!",
    "💪 불가능은 없다!",
    "🚀 좋은 습관은 최고의 친구다!",
    "🌱 네가 포기하지 않는 한 끝난 게 아니다!",
    "🏆 하루하루 쌓아가자!",
    "📚 끝까지 가면 이긴다!",
    "⚡ 조금 힘들면 성장 중이라는 증거다!",
    "🎯 오늘의 1시간이 1년을 바꾼다!",
    "🔑 지금의 노력은 내일의 행복!",
    "✨ 너는 할 수 있다!"
]

subjects = ["수학", "영어", "정법", "국어", "한지", "생윤"]

# -------------------------------
# 공부 기록 불러오기/저장
# -------------------------------
def load_records():
    try:
        return pd.read_csv("study_records.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=["날짜", "과목", "공부시간(분)"])

def save_record(subject, minutes):
    df = load_records()
    today = datetime.date.today().strftime("%Y-%m-%d")
    new_row = pd.DataFrame([[today, subject, minutes]], columns=df.columns)
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv("study_records.csv", index=False)

# -------------------------------
# 세션 상태 초기화
# -------------------------------
if "running" not in st.session_state:
    st.session_state.running = False
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "elapsed_seconds" not in st.session_state:
    st.session_state.elapsed_seconds = 0
if "current_message" not in st.session_state:
    st.session_state.current_message = random.choice(motivation_messages)

# -------------------------------
# UI 표시
# -------------------------------
st.markdown(f"<h1 style='text-align: center; color: red;'>{st.session_state.current_message}</h1>", unsafe_allow_html=True)

subject = st.selectbox("공부할 과목을 선택하세요", subjects)

col1, col2 = st.columns(2)
if col1.button("▶ 시작"):
    st.session_state.running = True
    st.session_state.start_time = time.time()
if col2.button("⏹ 멈춤"):
    st.session_state.running = False
    if st.session_state.start_time:
        elapsed = time.time() - st.session_state.start_time
        st.session_state.elapsed_seconds += elapsed
        total_minutes = round(st.session_state.elapsed_seconds / 60)
        save_record(subject, total_minutes)
        st.success(f"{subject} {total_minutes}분 기록 저장 완료!")
        st.session_state.elapsed_seconds = 0

# -------------------------------
# 타이머 표시
# -------------------------------
if st.session_state.running:
    elapsed = time.time() - st.session_state.start_time
    total_elapsed = st.session_state.elapsed_seconds + elapsed
    hours = int(total_elapsed // 3600)
    minutes = int((total_elapsed % 3600) // 60)
    seconds = int(total_elapsed % 60)
    st.metric("⏳ 공부 시간", f"{hours:02}:{minutes:02}:{seconds:02}")

    # 10분마다 동기부여 문구 변경
    if int(total_elapsed // 60) % 10 == 0 and int(total_elapsed) > 0:
        st.session_state.current_message = random.choice(motivation_messages)
        st.markdown(f"<h2 style='text-align: center; color: blue;'>{st.session_state.current_message}</h2>", unsafe_allow_html=True)

# -------------------------------
# 기록 보기
# -------------------------------
st.markdown("### 📜 공부 기록")
st.dataframe(load_records())
