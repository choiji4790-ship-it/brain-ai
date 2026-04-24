import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

# 페이지 설정 및 레이아웃 고정
st.set_page_config(page_title="Professional EEG Monitor", layout="wide")

# CSS 스타일 (박스 디자인)
st.markdown("""
    <style>
    .brain-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
    .part { padding: 15px; border-radius: 8px; text-align: center; color: white; font-weight: bold; }
    .active { background-color: #FF4B4B; box-shadow: 0 0 15px #FF4B4B; border: 2px solid white; }
    .inactive { background-color: #262730; border: 1px solid #4B4B4B; color: #808495; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏥 전문 의료용 실시간 뇌파 모니터")

# 진단 데이터 설정
mapping = {
    "정상 상태": {"freq": 10, "active": ["후두엽"], "color": "#1f77b4", "note": "Alpha파 (안정)"},
    "간질/발작": {"freq": 35, "active": ["전두엽", "측두엽"], "color": "#FF4B4B", "note": "고주파 (위험!)"},
    "수면 상태": {"freq": 3, "active": ["전두엽", "두정엽", "측두엽", "후두엽"], "color": "#7D3CFF", "note": "Delta파 (수면)"},
    "극도의 불안": {"freq": 22, "active": ["전두엽"], "color": "#FFA500", "note": "Beta파 (긴장)"}
}

# 사이드바
condition = st.sidebar.selectbox("진단 모드 선택", list(mapping.keys()))
run = st.sidebar.toggle("모니터링 시작", value=True)

# 데이터 기록용 세션 상태
if 'eeg_hist' not in st.session_state:
    st.session_state.eeg_hist = np.zeros(100)

# [핵심] 화면 전체를 덮어씌울 하나의 커다란 빈 바구니 생성
main_container = st.empty()

while run:
    conf = mapping[condition]
    
    # 새로운 데이터 포인트 생성 (부드러운 흐름을 위해 sin값 사용)
    new_val = np.sin(time.time() * conf["freq"]) + np.random.normal(0, 0.1)
    st.session_state.eeg_hist = np.append(st.session_state.eeg_hist[1:], new_val)
    
    # 바구니(main_container) 안에 모든 내용을 집어넣음 (이전 내용을 덮어씀)
    with main_container.container():
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader(f"🌐 실시간 뇌파 신호 ({conf['note']})")
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(st.session_state.eeg_hist, color=conf["color"], linewidth=2)
            ax.set_ylim(-2.5, 2.5)
            ax.set_facecolor('#0E1117')
            ax.grid(color='#4B4B4B', linestyle='--', alpha=0.3)
            st.pyplot(fig)
            plt.close(fig) # 메모리 폭발 방지
            
        with col2:
            st.subheader("🧠 뇌 활성 영역")
            all_parts = ["전두엽", "측두엽", "두정엽", "후두엽"]
            html_code = '<div class="brain-grid">'
            for p in all_parts:
                st_class = "active" if p in conf["active"] else "inactive"
                html_code += f'<div class="part {st_class}">{p}</div>'
            html_code += '</div>'
            st.markdown(html_code, unsafe_allow_html=True)
            
            st.write("---")
            st.metric("자극 주파수", f"{conf['freq']} Hz")
            st.info(f"**AI 진단:** {condition} 패턴 분석 완료")

    # 업데이트 속도 조절 (너무 빠르면 서버가 못 따라가니 0.1 정도로)
    time.sleep(0.1)
