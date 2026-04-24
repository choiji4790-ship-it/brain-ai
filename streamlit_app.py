import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.set_page_config(page_title="Advanced Medical EEG", layout="wide")

# CSS를 활용해 뇌 부위 시각화 스타일 정의
st.markdown("""
    <style>
    .brain-part { padding: 20px; border-radius: 10px; text-align: center; color: white; font-weight: bold; }
    .active { background-color: #ff4b4b; box-shadow: 0px 0px 15px #ff4b4b; }
    .inactive { background-color: #31333F; border: 1px solid #4B4B4B; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏥 차세대 AI 의료 뇌파 시뮬레이션")

# 사이드바 설정
condition = st.sidebar.selectbox("진단 모드 선택", ["정상 상태", "간질/발작", "수면 상태", "극도의 불안"])
is_running = st.sidebar.toggle("실시간 분석 가동", value=True)

# 뇌 부위 데이터 매핑
mapping = {
    "정상 상태": {"freq": 10, "part": "후두엽", "color": "#1f77b4", "status": "안정"},
    "간질/발작": {"freq": 40, "part": "전두엽", "color": "#ff4b4b", "status": "위험"},
    "수면 상태": {"freq": 3, "part": "뇌 전체", "color": "#7d3cff", "status": "서파"},
    "극도의 불안": {"freq": 25, "part": "전두엽/측두엽", "color": "#ffa500", "status": "과활성"}
}

# 실시간 데이터 저장을 위한 리스트
if 'data_history' not in st.session_state:
    st.session_state.data_history = np.zeros(100)

# 화면 레이아웃
c1, c2 = st.columns([2, 1])

placeholder = st.empty()

while is_running:
    with placeholder.container():
        # 데이터 생성 (흐르는 효과를 위해 마지막 값을 밀어내고 새 값 추가)
        info = mapping[condition]
        new_val = np.sin(time.time() * info["freq"]) + np.random.normal(0, 0.2)
        st.session_state.data_history = np.append(st.session_state.data_history[1:], new_val)
        
        with c1:
            st.subheader(f"🌐 실시간 뇌파 스트리밍 ({info['part']})")
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(st.session_state.data_history, color=info["color"], linewidth=2)
            ax.set_ylim(-3, 3)
            ax.axis('off') # 의료기기 느낌을 위해 축 숨기기
            st.pyplot(fig)
            
        with c2:
            st.subheader("🧠 뇌 활성 부위 모니터")
            # 뇌 부위 시각화 (간단한 HTML/CSS 활용)
            parts = ["전두엽", "측두엽", "두정엽", "후두엽"]
            for p in parts:
                active_class = "active" if p in info["part"] or info["part"] == "뇌 전체" else "inactive"
                st.markdown(f'<div class="brain-part {active_class}">{p}</div>', unsafe_allow_html=True)
                st.write("") # 간격
            
            st.metric("현재 자극 주파수", f"{info['freq']} Hz", delta=info["status"])

        time.sleep(0.05) # 빠른 업데이트 속도
