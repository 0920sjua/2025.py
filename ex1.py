import streamlit as st
import datetime, time, random
import pandas as pd

# ---------------- 세션 상태 초기화 ----------------
if "running" not in st.session_state:
    st.session_state.running = False
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "elapsed" not in st.session_state:
    st.session_state.elapsed = 0
if "records" not in st.session_state:
    st.session_state.records = []

# ---------------- 배경화면 설정 ----------------
bg_choice = st.sidebar.selectbox(
    "배경 선택",
    ["흰", "빨", "주", "노", "검", "무지개", "내 사진 업로드"]
)

if bg_choice == "흰":
    st.markdown("<style>body{background-color:white;}</style>", unsafe_allow_html=True)
elif bg_choice == "빨":
    st.markdown("<style>body{background-color:red;}</style>", unsafe_allow_html=True)
elif bg_choice == "주":
    st.markdown("<style>body{background-color:orange;}</style>", unsafe_allow_html=True)
elif bg_choice == "노":
    st.markdown("<style>body{background-color:yellow;}</style>", unsafe_allow_html=True)
elif bg_choice == "검":
    st.markdown("<style>body{background-color:black;color:white;}</style>", unsafe_allow_html=True)
elif bg_choice == "무지개":
    rainbow_css = """
    <style>
    body {
        background: linear-gradient(90deg, red, orange, yellow, green, blue, indigo, violet);
        color: white;
    }
    </style>
    """
    st.markdown(rainbow_css, unsafe_allow_html=True)
elif bg_choice == "내 사진 업로드":
    uploaded = st.sidebar.file_uploader("배경으로 쓸 이미지를 올리세요", type=["png", "jpg", "jpeg"])
    if uploaded:
        img_data = uploaded.getvalue()
        st.markdown(
            f"""
            <style>
            body {{
                background-image: url("data:image/png;base64,{img_data.decode('latin1')}");
                background-size: cover;
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )

# ---------------- D-Day ----------------
target_date = st.sidebar.date_input("📅 목표 날짜")
today = datetime.date.today()
d_day = (target_date - today).days
st.sidebar.markdown(f"**⏳ D-{d_day}**")

# ---------------- 동기부여 문구 ----------------
motivations = [
    "조금만 더! 네가 해낼 수 있어.",
    "포기하지 말자, 끝까지 간다!",
    "작은 성취가 큰 성공을 만든다.",
    "오늘의 노력이 내일의 자산이다.",
    "남들과 비교 말고 어제의 나와 겨뤄라.",
    "집중하면 불가능은 없다.",
    "한 문제 더! 미래의 나를 위해.",
    "실패는 성장의 과정이다.",
    "할 수 있다! 넌 이미 절반 왔다.",
    "꾸준함이 곧 실력이다.",
] * 3  # 30개 정도 복사

idx = (int(datetime.datetime.now().timestamp()) // 600) % len(motivations)  # 10분마다 변경
st.title(motivations[idx])

# ---------------- 과목 선택 ----------------
subject = st.selectbox("📘 오늘 공부 과목", ["국어", "영어", "수학", "생활과 윤리", "정치와 법", "한국지리"])

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

# 타이머 실시간 표시
if st.session_state.running:
    while st.session_state.running:
        elapsed = st.session_state.elapsed + (datetime.datetime.now() - st.session_state.start_time).seconds
        h, r = divmod(elapsed, 3600)
        m, s = divmod(r, 60)
        timer_placeholder.markdown(f"## ⏱ {h:02d}:{m:02d}:{s:02d}")
        time.sleep(1)
        st.experimental_rerun()
else:
    elapsed = st.session_state.elapsed
    h, r = divmod(elapsed, 3600)
    m, s = divmod(r, 60)
    timer_placeholder.markdown(f"## ⏱ {h:02d}:{m:02d}:{s:02d}")

# ---------------- 공부 기록 표시 ----------------
if st.session_state.records:
    df = pd.DataFrame(st.session_state.records)
    st.dataframe(df, use_container_width=True)
