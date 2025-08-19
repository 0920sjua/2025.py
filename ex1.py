import streamlit as st
import pandas as pd
import datetime
import random

# -------------------------------
# 세션 상태 초기화
# -------------------------------
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "running" not in st.session_state:
    st.session_state.running = False
if "elapsed" not in st.session_state:
    st.session_state.elapsed = 0
if "logs" not in st.session_state:
    st.session_state.logs = []
if "last_motivation" not in st.session_state:
    st.session_state.last_motivation = None
if "last_motivation_time" not in st.session_state:
    st.session_state.last_motivation_time = datetime.datetime.now()

# -------------------------------
# 동기부여 문구 30개
# -------------------------------
motivations = [
    "지금 이 순간이 미래를 만든다!",
    "작은 노력이 큰 변화를 만든다.",
    "멈추지 않으면 늦어도 도착한다.",
    "오늘의 땀이 내일의 성적표다.",
    "넌 할 수 있다, 이미 절반은 했다!",
    "어제보다 나은 내가 되자.",
    "공부는 배신하지 않는다.",
    "집중하는 1시간이 놀라운 결과를 만든다.",
    "포기하지 않는 자가 결국 이긴다.",
    "작심삼일? 삼일마다 다시 시작하면 된다.",
    "끝까지 버티는 자가 승리한다.",
    "후회 없는 하루를 보내자.",
    "너의 가능성은 무한하다.",
    "오늘의 선택이 내일의 성적을 결정한다.",
    "한 페이지라도 더 보자.",
    "작은 습관이 합격을 만든다.",
    "실패는 성공으로 가는 과정이다.",
    "남과 비교 말고 어제의 나와 비교하자.",
    "넌 생각보다 강하다.",
    "합격은 노력하는 자의 것.",
    "미래의 너가 오늘의 너에게 감사할 것이다.",
    "오늘 할 일을 내일로 미루지 말자.",
    "공부는 재능보다 끈기다.",
    "시간은 칼이다, 현명하게 써라.",
    "버티는 자가 결국 웃는다.",
    "노력은 배신하지 않는다.",
    "오늘을 이겨내자.",
    "꾸준함이 가장 큰 무기다.",
    "10분 더! 그게 합격을 만든다.",
    "포기하지 않는 한 실패는 없다."
]

# -------------------------------
# 동기부여 문구 (10분마다 변경)
# -------------------------------
now = datetime.datetime.now()
if (now - st.session_state.last_motivation_time).seconds >= 600:
    st.session_state.last_motivation = random.choice(motivations)
    st.session_state.last_motivation_time = now
if st.session_state.last_motivation is None:
    st.session_state.last_motivation = random.choice(motivations)

st.markdown(f"## 💡 {st.session_state.last_motivation}")

# -------------------------------
# 과목 선택
# -------------------------------
subject = st.selectbox("📚 과목을 선택하세요", ["국어", "영어", "수학", "생활과 윤리", "정치와 법", "한국지리"])

# -------------------------------
# 타이머 버튼
# -------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("▶️ 시작", use_container_width=True):
        if not st.session_state.running:
            st.session_state.start_time = datetime.datetime.now()
            st.session_state.running = True

with col2:
    if st.button("⏹ 멈춤", use_container_width=True):
        if st.session_state.running:
            st.session_state.elapsed += (datetime.datetime.now() - st.session_state.start_time).seconds
            st.session_state.running = False

with col3:
    if st.button("📝 기록", use_container_width=True):
        today = datetime.date.today().strftime("%Y-%m-%d")
        total_hours = round(st.session_state.elapsed / 3600, 2)
        st.session_state.logs.append({"날짜": today, "과목": subject, "순공부시간(h)": total_hours})
        st.success(f"✅ {today} {subject} {total_hours}시간 기록 저장!")

# -------------------------------
# 실시간 타이머 표시
# -------------------------------
if st.session_state.running:
    elapsed = st.session_state.elapsed + (datetime.datetime.now() - st.session_state.start_time).seconds
else:
    elapsed = st.session_state.elapsed

hours, remainder = divmod(elapsed, 3600)
minutes, seconds = divmod(remainder, 60)
st.markdown(f"### ⏱ {hours:02d}:{minutes:02d}:{seconds:02d}")

# -------------------------------
# 공부 기록 (DataFrame)
# -------------------------------
if st.session_state.logs:
    df = pd.DataFrame(st.session_state.logs)
    st.dataframe(df, use_container_width=True)

# -------------------------------
# D-Day 설정
# -------------------------------
st.markdown("---")
exam_date = st.date_input("📅 시험 날짜", datetime.date(2025, 11, 13))
d_day = (exam_date - datetime.date.today()).days
if d_day > 0:
    st.markdown(f"### 🚀 D-{d_day}")
elif d_day == 0:
    st.markdown("### 🚀 오늘이 시험일입니다! 파이팅!!")
else:
    st.markdown(f"### 🚀 시험이 끝난 지 {abs(d_day)}일 지났습니다.")
