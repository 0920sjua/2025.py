import streamlit as st
import time
import random
import pandas as pd
from datetime import datetime, date

# -------------------------------
# 세션 상태 초기화
# -------------------------------
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "elapsed_seconds" not in st.session_state:
    st.session_state.elapsed_seconds = 0
if "running" not in st.session_state:
    st.session_state.running = False
if "current_message" not in st.session_state:
    st.session_state.current_message = "🔥 오늘도 시작이 반이다! 집중하자!"
if "records" not in st.session_state:
    st.session_state.records = []

# -------------------------------
# 동기부여 문구 30개
# -------------------------------
motivation_messages = [
    "🔥 오늘도 시작이 반이다! 집중하자!",
    "🚀 지금의 노력이 미래를 바꾼다!",
    "🌱 작은 습관이 큰 성과를 만든다!",
    "💪 포기하지 않는 자가 승리한다!",
    "✨ 네가 하고 있는 건 의미 있는 일이다!",
    "📖 꾸준함은 재능을 이긴다!",
    "🏃 달리다 보면 어느새 도착해 있다!",
    "🌟 최고의 경쟁자는 어제의 나!",
    "🕰️ 시간은 금이다. 헛되이 쓰지 말자!",
    "🚴 노력은 배신하지 않는다!",
    "🔥 집중하면 할 수 있다!",
    "🌄 오늘의 땀은 내일의 빛!",
    "🎯 목표는 가까워지고 있다!",
    "🥇 작은 성공이 큰 성공을 만든다!",
    "🌌 네 가능성은 무한하다!",
    "🧩 하나씩 해내면 된다!",
    "🌊 흐르는 물처럼 꾸준히 하자!",
    "🌻 오늘도 성장하고 있다!",
    "💡 공부는 최고의 투자다!",
    "🚀 시작이 늦어도 도착은 빠를 수 있다!",
    "🔥 끝까지 해내는 사람이 되자!",
    "🌈 힘든 순간이 지나면 무지개가 뜬다!",
    "📌 흔들려도 포기하지 말자!",
    "🕹️ 네 인생의 플레이어는 너 자신!",
    "🏔️ 큰 산도 한 걸음씩 오르면 정복된다!",
    "🌞 아침의 노력이 하루를 결정한다!",
    "🚴 넘어져도 다시 일어나면 된다!",
    "✨ 네 꿈은 이룰 가치가 있다!",
    "🎶 오늘의 집중이 내일의 노래가 된다!",
    "🌍 노력은 결코 헛되지 않는다!"
]

# -------------------------------
# 제목 및 초기 문구
# -------------------------------
st.title("⏳ 공부 타이머 & 기록 앱")
st.markdown(f"<h2 style='text-align: center; color: blue;'>{st.session_state.current_message}</h2>", unsafe_allow_html=True)

# -------------------------------
# 디데이 설정
# -------------------------------
target_date = st.date_input("📅 목표 날짜를 선택하세요", value=date(2025, 12, 31))
days_left = (target_date - date.today()).days
if days_left >= 0:
    st.success(f"🎯 목표일까지 {days_left}일 남았습니다!")
else:
    st.warning("목표 날짜가 지났습니다!")

# -------------------------------
# 교재 선택
# -------------------------------
subjects = ["수학", "영어", "정법", "국어", "한지", "생윤"]
selected_subject = st.selectbox("📘 오늘 공부할 교재를 선택하세요", subjects)

# -------------------------------
# 타이머 표시 (자동 새로고침)
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
        st.markdown(
            f"<h2 style='text-align: center; color: blue;'>{st.session_state.current_message}</h2>",
            unsafe_allow_html=True
        )

# -------------------------------
# 버튼
# -------------------------------
col1, col2 = st.columns(2)

with col1:
    if st.button("▶ 시작"):
        if not st.session_state.running:
            st.session_state.running = True
            st.session_state.start_time = time.time()
            st.rerun()   # ✅ 여기 수정

with col2:
    if st.button("⏸ 멈춤"):
        if st.session_state.running:
            elapsed = time.time() - st.session_state.start_time
            st.session_state.elapsed_seconds += elapsed
            st.session_state.running = False

            # 기록 저장
            total_minutes = int(st.session_state.elapsed_seconds // 60)
            today_str = datetime.today().strftime("%Y-%m-%d")
            st.session_state.records.append({
                "날짜": today_str,
                "과목": selected_subject,
                "공부 시간(분)": total_minutes
            })
            st.success(f"✅ {selected_subject} 공부 기록이 저장되었습니다!")

# -------------------------------
# 기록 테이블
# -------------------------------
if st.session_state.records:
    df = pd.DataFrame(st.session_state.records)
    st.subheader("📊 공부 기록")
    st.dataframe(df)
