import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

# 페이지 설정
st.set_page_config(page_title="Advanced EEG Monitor", layout="wide")

# 스타일 설정
st.markdown("""
    <style>
    .brain-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
    .part { padding: 15px; border-radius: 8px; text-align: center; color: white; font-size: 1.2em; font-weight: bold; }
    .active { background-color: #FF4B4B; box-shadow: 0 0 15px #FF4B4B; border: 2px solid white; }
    .inactive { background-color: #262730; border: 1px solid #4B4B4B; color: #808495; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏥 실시간 의료용 뇌파 모니터링 시스템")

# 상태 매핑
mapping = {
    "정상 상태": {"freq": 10, "active": ["후두엽"], "color": "#1f77b4", "note": "Alpha파 발생 중 (안정)"},
    "간질/발작": {"freq": 35, "active": ["전두엽", "측두엽"], "color": "#FF4B4B", "note": "이상 고주파 감지 (위험!)"},
    "수면 상태": {"freq": 3, "active": ["전두엽", "두정엽", "측두엽", "후두엽"], "color": "#7D3CFF", "note": "Delta파 발생 중 (깊은 수면)"},
    "극도의 불안": {"freq": 22, "active": ["전두엽"], "color": "#FFA500", "note": "Beta파 과활성화 (긴장)"}
}

# 사이드바
condition = st.sidebar.selectbox("진단 모드 선택", list(mapping.keys()))
run = st.sidebar.toggle("시스템 가동", value=True)

# 데이터 초기화
if 'eeg_data' not in st.session_state:
    st.session_state.eeg_data = np.zeros(100)

# 화면 레이아웃 설정
col1, col2 = st.columns([2, 1])

with col1:
    chart_placeholder = st.empty()
with col2:
    status_placeholder = st.empty()

# 무한 루프
while run:
    conf = mapping[condition]
    
    # 1. 새로운 데이터 생성 및 업데이트
    new_point = np.sin(time.time() * conf["freq"]) + np.random.normal(0, 0.1)
    st.session_state.eeg_data = np.append(st.session_state.eeg_data[1:], new_point)
    
    # 2. 그래프 그리기
    with chart_placeholder.container():
        st.subheader(f"🌐 실시간 뇌파 신호 ({conf['note']})")
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(st.session_state.eeg_data, color=conf["color"], linewidth=2)
        ax.set_ylim(-2.5, 2.5)
        ax.set_facecolor('#0E1117')
        ax.grid(color='#4B4B4B', linestyle='--', alpha=0.5)
        st.pyplot(fig)
        plt.close(fig) # 메모리 관리

    # 3. 뇌 부위 및 정보 업데이트
    with status_placeholder.container():
        st.subheader("🧠 뇌 활성 영역")
        all_parts = ["전두엽", "측두엽", "두정엽", "후두엽"]
        
        # 2x2 그리드 레이아웃
        html_code = '<div class="brain-grid">'
        for p in all_parts:
            status_class = "active" if p in conf["active"] else "inactive"
            html_code += f'<div class="part {status_class}">{p}</div>'
        html_code += '</div>'
        st.markdown(html_code, unsafe_allow_html=True)
        
        st.write("---")
        st.metric("자극 빈도", f"{conf['freq']} Hz")
        st.info(f"**AI 진단:** {condition}에 따른 뇌파 패턴 분석 중...")

    time.sleep(0.01) # 업데이트 속도를 아주 빠르게 설정
