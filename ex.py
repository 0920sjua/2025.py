import streamlit as st
import pandas as pd
import time
import random
from datetime import datetime, date
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="공부 타이머 & 동기부여", page_icon="📚", layout="centered")

# -----------------------------
# 동기부여 메시지 (30개)
# -----------------------------
motivation_messages = [
    "🚀 지금 이 순간이 당신의 미래를 만든다!",
    "🔥 포기하지 않는 한, 실패는 없다!",
    "🌱 작은 습관이 큰 변화를 만든다.",
    "💪 오늘의 땀방울이 내일의 성취다.",
    "🎯 목표를 향해 한 걸음 더!",
    "📚 꾸준함이 최고의 무기다.",
    "🏆 노력은 배신하지 않는다.",
    "🌟 당신은 생각보다 훨씬 강하다.",
    "⏳ 완벽한 순간을 기다리지 말고 지금 시작하라.",
    "⚡ 기회는 준비된 자에게 온다.",
    "📖 오늘 배우는 것이 내일의 무기가 된다.",
    "🚴‍♂️ 천천히 가도 멈추지 않으면 된다.",
    "🧠 집중은 최고의 생산성 도구다.",
    "🌞 하루의 첫 1시간이 하루 전체를 만든다.",
    "🛠️ 꾸준함은 재능을 이긴다.",
    "🌊 파도는 멈추지 않는다. 너도 멈추지 마라.",
    "🔥 지금의 선택이 미래를 만든다.",
    "🎵 작은 진전도 진전이다.",
    "🌻 오늘 심은 씨앗은 내일 꽃이 된다.",
    "🏃‍♀️ 시작이 반이다.",
    "🧗 도전 없이는 성장도 없다.",
    "📅 오늘을 최선을 다해 살아라.",
    "🕰️ 시간이 부족한 게 아니라, 우선순위가 문제다.",
    "🪴 하루하루가 쌓여 인생이 된다.",
    "⚙️ 실패는 시도했다는 증거다.",
    "🌟 불가능은 단지 시간이 더 필요한 것뿐이다.",
    "💡 배움은 평생의 자산이다.",
    "🚪 문이 닫히면 다른 문을 찾아라.",
    "🌍 작은 변화가 세상을 바꾼다.",
    "💖 자신을 믿는 것이 시작이다."
]

# -----------------------------
# 세션 상태 초기화
# -----------------------------
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "elapsed_seconds" not in st.session_state:
    st.session_state.elapsed_seconds = 0
if "running" not in st.session_state:
    st.session_state.running = False
if "records" not in st.session_state:
    st.session_state.records = []
if "current_message" not in st.session_state:
    st.session_state.current_message = random.choice(motivation_messages)
if "d_day" not in st.session_state:
    st.session_state.d_day = None

# -----------------------------
# D-Day 선택
# -----------------------------
st.subheader("📅 시험 날짜 선택 (D-Day)")
exam_date = st.date_input("시험일을 선택하세요", value=date.today())
st.session_state.d_day = exam_date

# D-Day 계산
today = date.today()
days_left = (exam_date - today).days
if days_left > 0:
    st.markdown(f"<h3 style='text-align:center; color:red;'>🔥 D-{days_left} (시험까지 {days_left}일 남음)</h3>", unsafe_allow_html=True)
elif days_left == 0:
    st.markdown("<h3 style='text-align:center; color:green;'>🎉 오늘이 시험일입니다! 최선을 다하세요!</h3>", unsafe_allow_html=True)
else:
    st.markdown(f"<h3 style='text-align:center; color:gray;'>시험일이 이미 지났습니다 (D+{abs(days_left)})</h3>", unsafe_allow_html=True)

# -----------------------------
# 맨 처음 동기부여 메시지 크게 출력
# -----------------------------
st.markdown(
    f"<h2 style='text-align: center; color: blue;'>{st.session_state.current_message}</h2>",
    unsafe_allow_html=True
)

st.title("📚 공부 타이머 & 동기부여")

# -----------------------------
# 과목 선택
# -----------------------------
subject = st.selectbox("공부할 과목을 선택하세요", ["수학", "영어", "정법", "국어", "한지", "생윤"])

# -----------------------------
# 타이머 표시 (자동 새로고침)
# -----------------------------
st_autorefresh(interval=1000, key="timer_refresh")

if st.session_state.running:
    elapsed = time.time() - st.session_state.start_time
    total_elapsed = st.session_state.elapsed_seconds + elapsed
    hours = int(total_elapsed // 3600)
    minutes = int((total_elapsed % 3600) // 60)
    seconds = int(total_elapsed % 60)
    st.metric("⏳ 공부 시간", f"{hours:02}:{minutes:02}:{seconds:02}")

    # 10분마다 동기부여 문구 갱신
    if int(total_elapsed // 60) % 10 == 0 and int(total_elapsed) > 0:
        st.session_state.current_message = random.choice(motivation_messages)
        st.markdown(
            f"<h2 style='text-align: center; color: blue;'>{st.session_state.current_message}</h2>",
            unsafe_allow_html=True
        )

# -----------------------------
# 시작 / 멈춤 버튼
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    if st.button("▶️ 시작"):
        if not st.session_state.running:
            st.session_state.start_time = time.time()
            st.session_state.running = True

with col2:
    if st.button("⏸️ 멈춤"):
        if st.session_state.running:
            elapsed = time.time() - st.session_state.start_time
            st.session_state.elapsed_seconds += elapsed
            st.session_state.running = False

            # 기록 저장
            date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.session_state.records.append(
                {"날짜": date_str, "과목": subject, "공부시간(초)": int(st.session_state.elapsed_seconds)}
            )
            st.session_state.elapsed_seconds = 0

# -----------------------------
# 기록 보여주기
# -----------------------------
if st.session_state.records:
    st.subheader("📒 공부 기록")
    df = pd.DataFrame(st.session_state.records)
    st.table(df)
