import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

# 1. 페이지 설정
st.set_page_config(page_title="Professional EEG AI", layout="wide")

# 2. CSS 스타일 (뇌 부위 애니메이션)
st.markdown("""
    <style>
    .main { background-color: #0E1117; }
    .brain-container { position: relative; width: 260px; height: 200px; background: #111; border-radius: 50% 50% 40% 40%; margin: auto; border: 1px solid #333; }
    .lobe { position: absolute; border: 1px solid #222; display: flex; align-items: center; justify-content: center; font-size: 11px; transition: 0.3s; color: #444; background: #1a1a1a; }
    .frontal { top: 15px; left: 65px; width: 130px; height: 60px; border-radius: 40% 40% 0 0; }
    .temporal { top: 85px; left: 40px; width: 85px; height: 55px; border-radius: 20%; }
    .parietal { top: 75px; left: 135px; width: 85px; height: 55px; border-radius: 20%; }
    .occipital { top: 140px; left: 80px; width: 100px; height: 50px; border-radius: 0 0 50% 50%; }
    .active-glow { color: white !important; font-weight: bold; box-shadow: 0 0 15px; transform: scale(1.03); }
    </style>
    """, unsafe_allow_html=True)

st.title("🏥 실시간 자율 진단 뇌파 시스템")

# 세션 데이터 초기화
if 'eeg_hist' not in st.session_state:
    st.session_state.eeg_hist = np.zeros(100)
if 'target_hz' not in st.session_state:
    st.session_state.target_hz = 12.0

# 사이드바
if st.sidebar.button("🚨 무작위 증상 발생"):
    st.session_state.target_hz = np.random.uniform(2.0, 40.0)
run = st.sidebar.toggle("시스템 가동", value=True)

# [중요] 화면 전체를 담을 단 하나의 컨테이너
screen = st.empty()

while run:
    # 데이터 생성
    new_point = np.sin(time.time() * st.session_state.target_hz) + np.random.normal(0, 0.1)
    st.session_state.eeg_hist = np.append(st.session_state.eeg_hist[1:], new_point)
    
    # AI 주파수 분석 (추정 Hz)
    est_hz = st.session_state.target_hz + np.random.normal(0, 0.5)
    
    # AI 상태 판단
    color, status, active = "#1f77b4", "분석 중", []
    if est_hz < 5: color, status, active = "#7D3CFF", "Delta (수면)", ["frontal", "parietal", "temporal", "occipital"]
    elif est_hz < 13: color, status, active = "#1f77b4", "Alpha (안정)", ["occipital"]
    elif est_hz < 25: color, status, active = "#FFA500", "Beta (긴장)", ["frontal"]
    else: color, status, active = "#FF4B4B", "Gamma (발작 위험)", ["frontal", "temporal"]

    # 화면 렌더링 (이 내부에서만 모든 것이 그려져야 함)
    with screen.container():
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("🌐 실시간 신호 분석")
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(st.session_state.eeg_hist, color=color, linewidth=2)
            ax.set_ylim(-3, 3)
            ax.set_facecolor('#0E1117')
            ax.axis('off')
            st.pyplot(fig)
            plt.close(fig)
            st.metric("AI 추정 주파수", f"{est_hz:.1f} Hz", delta=status)

        with col2:
            st.subheader("🧠 뇌 맵핑")
            def get_style(name):
                return f"active-glow; background-color: {color}cc;" if name in active else ""
            
            brain_html = f"""
            <div class="brain-container">
                <div class="lobe frontal {get_style('frontal')}">전두엽</div>
                <div class="lobe temporal {get_style('temporal')}">측두엽</div>
                <div class="lobe parietal {get_style('parietal')}">두정엽</div>
                <div class="lobe occipital {get_style('occipital')}">후두엽</div>
            </div>
            """
            st.markdown(brain_html, unsafe_allow_html=True)
            st.write(f"**현재 상태:** {status}")

    # 적절한 업데이트 속도 (0.05~0.1초 추천)
    time.sleep(0.05)
