import streamlit as st
import time
import datetime
import pandas as pd
import random   # ⬅️ 여기에서 import

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
if "last_motivation" not in st.session_state:
    st.session_state.last_motivation = ""
if "last_motivation_time" not in st.session_state:
    st.session_state.last_motivation_time = 0

# -------------------------------
# 동기부여 문구
# -------------------------------
motivations = [
    "🔥 지금 이 순간이 미래를 바꾼다!",
    "🚀 시작이 반이다, 지금 바로 집중하자!",
    "💡 한 문제 한 문제 쌓이면 큰 힘이 된다.",
    "🏆 넌 반드시 해낼 수 있어!",
    "📚 꾸준함이 최고의 무기다.",
    "✨ 오늘의 땀이 내일의 영광이 된다.",
    "🌱 작은 성장이 모여 큰 성공을 만든다.",
    "🕰️ 시간은 기다려주지 않는다. 지금 해라!",
    "💪 포기하지 말고 끝까지 가자!",
    "🎯 목표를 향해 한 걸음 더!",
    "🔥 집중하면 남들과 다른 결과가 나온다.",
    "🚀 넌 이미 절반은 해냈다.",
    "💡 오늘의 공부가 내일의 나를 만든다.",
    "🏆 위대한 일은 작은 습관에서 시작된다.",
    "📚 눈 앞의 공부가 미래의 길을 연다.",
    "✨ 네가 하는 노력은 절대 배신하지 않는다.",
    "🌱 매일 조금씩, 하지만 멈추지 않고.",
    "🕰️ 지금 공부 안 하면, 나중에 더 힘들다.",
    "💪 힘들수록 성장하는 순간이다.",
    "🎯 남들과 비교하지 말고 어제의 나와 경쟁하라.",
    "🔥 한 문제라도 더 풀자!",
    "🚀 집중력은 최고의 무기다.",
    "💡 오늘 외운 것은 내일의 자신감을 만든다.",
    "🏆 넌 충분히 잘하고 있어, 계속해!",
    "📚 노력은 배신하지 않는다.",
    "✨ 천재는 노력하는 사람을 이길 수 없다.",
    "🌱 오늘의 1시간이 내일의 자유다.",
    "🕰️ 미루면 미룰수록 늦어진다.",
    "💪 포기하지 않는 자가 결국 이긴다.",
    "🎯 지금 하는 공부가 미래를 결정한다."
]

# -------------------------------
# 타이머 동작
# -------------------------------
def start_timer():
    if not st.session_state.running:
        st.session_state.start_time = time.time() - st.session_state.elapsed
        st.session_state.running = True

def stop_timer(subject):
    if st.session_state.running:
        st.session_state.running = False
        st.session_state.elapsed = time.time() - st.session_state.start_time

        # 공부 기록 저장
        today = datetime.date.today().strftime("%Y-%m-%d")
        st.session_state.logs.append({
            "날짜": today,
            "과목": subject,
            "순공부시간(초)": round(st.session_state.elapsed)
        })

def reset_timer():
    st.session_state.start_time = None
    st.session_state.elapsed = 0
    st.session_state.running = False

# -------------------------------
# 앱 화면 구성
# -------------------------------

# 👉 앱 제목을 "동기부여 문구"로만 표시
st.title("💡 동기부여 문구")

# D-day 설정
exam_date = st.date_input("📅 시험 날짜를 선택하세요")
days_left = (exam_date - datetime.date.today()).days
if days_left >= 0:
    st.write(f"🎯 시험까지 D-{days_left}")
else:
    st.write("시험이 이미 지났습니다!")

# 과목 선택
subject = st.selectbox("📚 과목 선택", ["국어", "영어", "수학", "생활과 윤리", "정치와 법", "한국지리"])

# 타이머 표시
if st.session_state.running:
    st.session_state.elapsed = time.time() - st.session_state.start_time

elapsed_time = int(st.session_state.elapsed)
hours, remainder = divmod(elapsed_time, 3600)
minutes, seconds = divmod(remainder, 60)

st.metric("⏱️ 현재 공부 시간", f"{hours:02}:{minutes:02}:{seconds:02}")

# 동기부여 문구 (10분마다 변경)
if elapsed_time // 600 > st.session_state.last_motivation_time:
    st.session_state.last_motivation = random.choice(motivations)
    st.session_state.last_motivation_time = elapsed_time // 600

st.markdown(f"## {st.session_state.last_motivation if st.session_state.last_motivation else random.choice(motivations)}")

# 버튼
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("▶️ 시작"):
        start_timer()
with col2:
    if st.button("⏸ 멈춤"):
        stop_timer(subject)
with col3:
    if st.button("🔄 리셋"):
        reset_timer()

# -------------------------------
# 공부 기록 (캘린더 느낌으로)
# -------------------------------
if st.session_state.logs:
    df = pd.DataFrame(st.session_state.logs)

    if "순공부시간(초)" in df.columns and "순공부시간(h)" not in df.columns:
        df["순공부시간(h)"] = (df["순공부시간(초)"] / 3600).round(2)

    show_cols = [c for c in ["날짜", "과목", "순공부시간(h)"] if c in df.columns]
    st.dataframe(df[show_cols], use_container_width=True)
