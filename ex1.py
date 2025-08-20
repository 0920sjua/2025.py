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
        "언어는 사고의 집이다. - 루트비히 비트겐슈타인",
        "문학은 인간을 이해하는 창이다. - 헤르만 헤세",
        "좋은 글은 마음을 움직인다. - 마르쿠스 툴리우스 키케로",
        "언어를 배우는 것은 세계를 배우는 것이다. - 알베르트 아인슈타인",
        "읽는 것은 사고의 훈련이다. - 레프 톨스토이",
        "문학은 삶의 거울이다. - 프랑수아 드 라 로슈푸코",
        "글을 쓰며 자신을 발견하라. - 루쉰",
        "표현 없는 생각은 의미가 없다. - 토마스 아퀴나스",
        "글은 생각을 담는 그릇이다. - 사마셰프",
        "좋은 독서는 사색을 키운다. - 존 듀이",
        "문장을 다듬는 것은 마음을 다듬는 것이다. - 프랭클린",
        "언어는 생각을 조직하는 도구다. - 에드워드 사피어",
        "읽고 쓰는 습관이 삶을 바꾼다. - 샤를 보들레르",
        "언어는 힘이다. - 조지 오웰",
        "좋은 책은 마음의 스승이다. - 세네카",
        "독서는 지혜를 준다. - 솔로몬",
        "글쓰기는 자기 수련이다. - 빅토르 위고",
        "문학은 세상을 이해하게 한다. - 에밀리 디킨슨",
        "생각을 기록하면 명확해진다. - 벤저민 프랭클린",
        "언어는 마음을 표현하는 도구다. - 카를 융",
        "글쓰기와 사색은 불가분이다. - 랠프 왈도 에머슨",
        "독서를 통해 타인을 이해하라. - 헨리 제임스",
        "좋은 글은 사람을 설득한다. - 아리스토텔레스",
        "문장은 생각의 집이다. - 레프 톨스토이",
        "글쓰기는 문제 해결의 훈련이다. - 알베르트 아인슈타인",
        "언어를 다루는 능력이 사고를 키운다. - 윌리엄 워즈워스",
        "독서는 사고의 깊이를 만든다. - 마이클 조던"
    ],
    "영어": [
        "미래는 자신의 꿈을 믿는 자의 것이다. - 엘리너 루즈벨트",
        "끝내기 전까지는 항상 불가능해 보인다. - 넬슨 만델라",
        "성공이 끝이 아니며, 실패가 치명적이지도 않다. - 윈스턴 처칠",
        "행복은 우리 자신에게 달려 있다. - 아리스토텔레스",
        "앞으로 나아가는 비밀은 시작하는 것이다. - 마크 트웨인",
        "오늘 하는 일이 내일을 바꾼다. - 랄프 마스턴",
        "어려움 속에 기회가 있다. - 알베르트 아인슈타인",
        "아는 것이 힘이다. - 프랜시스 베이컨",
        "크게 꿈꾸고 실패를 두려워하지 마라. - 노먼 보언",
        "펜은 칼보다 강하다. - 에드워드 불워-리튼",
        "교육은 가장 강력한 무기다. - 넬슨 만델라",
        "시간은 우리가 가장 원하면서 가장 잘못 사용하는 것이다. - 윌리엄 펜",
        "행동은 모든 성공의 열쇠다. - 파블로 피카소",
        "가진 것으로, 있는 자리에서, 할 수 있는 일을 하라. - 시어도어 루스벨트",
        "용기는 압박 속의 우아함이다. - 어니스트 헤밍웨이",
        "상처를 지혜로 바꿔라. - 오프라 윈프리",
        "책 없는 방은 영혼 없는 육체와 같다. - 키케로",
        "말은 가장 고갈되지 않는 마법의 원천이다. - 조앤 롤링",
        "산을 옮기는 사람도 작은 돌을 옮기는 것부터 시작한다. - 공자",
        "역경은 평범한 사람을 특별한 운명으로 이끈다. - C. S. 루이스",
        "배움은 결코 마음을 지치게 하지 않는다. - 레오나르도 다빈치",
        "훈련은 목표와 성취 사이의 다리다. - 짐 론",
        "미래를 예측하는 최고의 방법은 그것을 발명하는 것이다. - 앨런 케이",
        "계획 없는 목표는 단지 소망일 뿐이다. - 앙투안 드 생텍쥐페리",
        "잃어버린 시간은 다시 찾을 수 없다. - 벤저민 프랭클린",
        "실패는 진행 중인 성공이다. - 알베르트 아인슈타인",
        "천 리 길도 한 걸음부터 시작된다. - 노자",
        "성공은 그것을 찾느라 바쁘지 않은 이에게 온다. - 헨리 데이비드 소로",
        "위대한 일은 안락한 구역에서 나오지 않는다. - 조지 애데어",
        "스스로를 밀어붙여라. 다른 누구도 대신해주지 않는다. - 익명"
    ],
    "수학": [
        "수학은 문제 해결의 힘을 길러준다. - 피타고라스",
        "패턴을 이해하면 세상이 명확해진다. - 아르키메데스",
        "작은 계산이 큰 변화를 만든다. - 아이작 뉴턴",
        "논리는 사고의 기초다. - 레온하르트 오일러",
        "실수는 성장의 기회다. - 카를 프리드리히 가우스",
        "수학적 사고는 삶을 조직한다. - 앨런 튜링",
        "증명은 진리로 가는 길이다. - 피에르-시몽 라플라스",
        "문제를 나누면 해결이 쉽다. - 존 폰 노이만",
        "모든 숫자는 의미를 가진다. - 블레즈 파스칼",
        "연습은 완벽을 만든다. - 히포크라테스",
        "패턴은 세상을 읽는 언어다. - 프랑수아 비에트",
        "추상화는 사고를 자유롭게 한다. - 다비드 힐베르트",
        "함수는 관계를 이해하는 도구다. - 레온하르트 오일러",
        "논리적 사고는 문제 해결을 빠르게 한다. - 조지 불",
        "수학은 모험이다. - 앙리 푸앵카레",
        "계산은 사고의 훈련이다. - 존 네이피어",
        "문제를 푸는 즐거움이 성장이다. - 카를 프리드리히 가우스",
        "정확함은 자유를 준다. - 리차드 파인만",
        "증명 없는 지식은 신뢰할 수 없다. - 알베르트 아인슈타인",
        "패턴을 찾아라. 세상이 보인다. - 피타고라스",
        "수학은 세상을 이해하는 창이다. - 레오나르도 다빈치",
        "논리적 사고는 삶을 계획하게 한다. - 칼 프리드리히 가우스",
        "작은 성취가 큰 자신감을 만든다. - 에밀리 뒤 샤토브리앙",
        "수학은 사고의 운동이다. - 프랑수아 비에트",
        "끊임없는 연습이 능력을 만든다. - 존 폰 노이만",
        "증명 과정에서 지혜가 자란다. - 힐베르트",
        "문제를 나누면 두렵지 않다. - 아르키메데스",
        "패턴 속에 질서가 있다. - 피타고라스",
        "계산은 사고의 거울이다. - 앨런 튜링"
    ]
}

# ---------------- 과목 선택 ----------------
subject = st.sidebar.selectbox("오늘의 공부 과목 선택", list(motivations.keys()))

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
st.markdown(f"<style>.stApp {{background: {bg_color};}}</style>", unsafe_allow_html=True)

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

# ---------------- 동기부여 문구 (10분마다 갱신) ----------------
if time.time() - st.session_state.last_motivation_time > 600 or st.session_state.last_motivation == "":
    st.session_state.last_motivation = random.choice(motivations[subject])
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
        st.session_state.records.append({
            "날짜": date.today().strftime("%Y-%m-%d"),
            "과목": subject,
            "순공부시간(h)": round(elapsed / 3600, 2)
        })

# ---------------- 기록 표시 ----------------
if st.session_state.records:
    df = pd.DataFrame(st.session_state.records)
    st.dataframe(df, use_container_width=True)

# ---------------- 자동 새로고침 ----------------
if st.session_state.running:
    time.sleep(1)
    st.experimental_rerun()
