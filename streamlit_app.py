import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.set_page_config(page_title="Medical Brain AI", layout="wide")

# CSS: 뇌 시각화 및 애니메이션 효과
st.markdown("""
    <style>
    .brain-svg-container { text-align: center; margin-top: 20px; }
    .lobe { fill: #262730; stroke: #444; stroke-width: 1; transition: all 0.5s ease; }
    .active { filter: drop-shadow(0 0 10px var(--glow-color)); stroke: white; stroke-width: 2; }
    .label-box { 
        padding: 10px; border-radius: 5px; text-align: center; 
        font-weight: bold; margin-top: 10px; color: white;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏥 AI 기반 실시간 뇌 기능 시각화 시스템")

# 데이터 및 주파수 필터링용 세션 상태
if 'eeg_hist' not in st.session_state:
    st.session_state.eeg_hist = np.zeros(100)
if 'smooth_hz' not in st.session_state:
    st.session_state.smooth_hz = 12.0
if 'target_hz' not in st.session_state:
    st.session_state.target_hz = 12.0

# 사이드바
if st.sidebar.button("🚨 무작위 증상 발생"):
    st.session_state.target_hz = np.random.uniform(2.0, 40.0)
run = st.sidebar.toggle("시스템 가동", value=True)

screen = st.empty()

while run:
    # 1. 데이터 생성 및 필터링
    raw_hz = st.session_state.target_hz + np.random.normal(0, 0.2)
    st.session_state.smooth_hz = st.session_state.smooth_hz * 0.85 + raw_hz * 0.15
    current_hz = st.session_state.smooth_hz
    
    new_point = np.sin(time.time() * current_hz) + np.random.normal(0, 0.1)
    st.session_state.eeg_hist = np.append(st.session_state.eeg_hist[1:], new_point)
    
    # 2. 진단 로직 및 부위 설정
    color, status, active_lobes = "#1f77b4", "분석 중", []
    if current_hz < 6:
        color, status, active_lobes = "#7D3CFF", "Delta (수면)", ["frontal", "parietal", "temporal", "occipital"]
    elif current_hz < 14:
        color, status, active_lobes = "#1f77b4", "Alpha (안정)", ["occipital"]
    elif current_hz < 30:
        color, status, active_lobes = "#FFA500", "Beta (긴장/활동)", ["frontal"]
    else:
        color, status, active_lobes = "#FF4B4B", "Gamma (발작 위험)", ["frontal", "temporal"]

    # 3. 화면 렌더링
    with screen.container():
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader(f"🌐 실시간 뇌파 신호 분석")
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(st.session_state.eeg_hist, color=color, linewidth=2.5)
            ax.set_ylim(-3, 3)
            ax.set_facecolor('#0E1117')
            ax.axis('off')
            st.pyplot(fig)
            plt.close(fig)
            st.metric("AI 추정 주파수", f"{current_hz:.1f} Hz", delta=status)

        with col2:
            st.subheader("🧠 실시간 활성 부위")
            
            # SVG 뇌 지도 생성
            def get_attr(name):
                return f'class="lobe active" style="fill: {color}; --glow-color: {color};"' if name in active_lobes else 'class="lobe"'

            brain_svg = f"""
            <div class="brain-svg-container">
                <svg viewBox="0 0 200 150" width="250">
                    <!-- 전두엽 -->
                    <path d="M20,70 Q20,20 80,20 L100,20 L100,80 L40,90 Z" {get_attr('frontal')} />
                    <!-- 두정엽 -->
                    <path d="M100,20 Q150,20 180,70 L140,90 L100,80 Z" {get_attr('parietal')} />
                    <!-- 측두엽 -->
                    <path d="M50,95 Q100,85 140,95 Q140,130 100,140 Q50,130 50,95" {get_attr('temporal')} />
                    <!-- 후두엽 -->
                    <path d="M145,95 L185,75 Q190,110 160,140 L145,95" {get_attr('occipital')} />
                </svg>
                <div class="label-box" style="background-color: {color}44; border: 1px solid {color};">
                    현재 활성: {", ".join([{"frontal":"전두엽", "temporal":"측두엽", "parietal":"두정엽", "occipital":"후두엽"}[l] for l in active_lobes])}
                </div>
            </div>
            """
            st.markdown(brain_svg, unsafe_allow_html=True)
            st.write(f"**AI 진단:** {status}")

    time.sleep(0.08)
