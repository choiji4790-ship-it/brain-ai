import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.set_page_config(page_title="Stable EEG AI", layout="wide")

# CSS: 뇌 맵핑 디자인 (가시성 확보)
st.markdown("""
    <style>
    .brain-box { position: relative; width: 260px; height: 200px; background: #111; border-radius: 50% 50% 40% 40%; margin: auto; border: 2px solid #333; }
    .lobe { position: absolute; border: 1px solid #444; display: flex; align-items: center; justify-content: center; font-size: 11px; transition: 0.5s; color: #666; background: #1a1a1a; }
    .frontal { top: 15px; left: 65px; width: 130px; height: 60px; border-radius: 40% 40% 0 0; }
    .temporal { top: 85px; left: 40px; width: 85px; height: 55px; border-radius: 20%; }
    .parietal { top: 75px; left: 135px; width: 85px; height: 55px; border-radius: 20%; }
    .occipital { top: 140px; left: 80px; width: 100px; height: 50px; border-radius: 0 0 50% 50%; }
    .active-glow { color: white !important; font-weight: bold; box-shadow: 0 0 20px; border: 2px solid white; transform: scale(1.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("🏥 안정화된 실시간 뇌파 진단 시스템 (AI 필터 적용)")

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
run = st.sidebar.toggle("모니터링 시작", value=True)

# 메인 화면 컨테이너
screen = st.empty()

while run:
    # 1. 데이터 생성 및 필터링 (부드러운 주파수 변화)
    # 실제 주파수에 노이즈를 섞되, 이전 값과 평균을 내어 '떨림'을 방지합니다.
    raw_hz = st.session_state.target_hz + np.random.normal(0, 0.3)
    st.session_state.smooth_hz = st.session_state.smooth_hz * 0.8 + raw_hz * 0.2
    
    new_point = np.sin(time.time() * st.session_state.smooth_hz) + np.random.normal(0, 0.1)
    st.session_state.eeg_hist = np.append(st.session_state.eeg_hist[1:], new_point)
    
    # 2. 진단 로직 (경계선 완화)
    current_hz = st.session_state.smooth_hz
    color, status, active = "#1f77b4", "분석 중", []
    
    if current_hz < 6: # 수면 (Delta)
        color, status, active = "#7D3CFF", "Delta (수면)", ["frontal", "parietal", "temporal", "occipital"]
    elif current_hz < 14: # 안정 (Alpha)
        color, status, active = "#1f77b4", "Alpha (안정)", ["occipital"]
    elif current_hz < 30: # 긴장 (Beta)
        color, status, active = "#FFA500", "Beta (긴장/활동)", ["frontal"]
    else: # 위험 (Gamma)
        color, status, active = "#FF4B4B", "Gamma (발작 위험)", ["frontal", "temporal"]

    # 3. 화면 렌더링 (덮어쓰기)
    with screen.container():
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader(f"🌐 실시간 뇌파 신호")
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(st.session_state.eeg_hist, color=color, linewidth=2.5)
            ax.set_ylim(-3, 3)
            ax.set_facecolor('#0E1117')
            ax.axis('off')
            st.pyplot(fig)
            plt.close(fig)
            st.metric("AI 분석 주파수", f"{current_hz:.1f} Hz", delta=status)

        with col2:
            st.subheader("🧠 활성 부위 매핑")
            def get_glow(name):
                return f"active-glow; background-color: {color};" if name in active else ""
            
            # HTML/CSS 구조 명확화
            brain_html = f"""
            <div class="brain-box">
                <div class="lobe frontal {get_glow('frontal')}">전두엽</div>
                <div class="lobe temporal {get_glow('temporal')}">측두엽</div>
                <div class="lobe parietal {get_glow('parietal')}">두정엽</div>
                <div class="lobe occipital {get_glow('occipital')}">후두엽</div>
            </div>
            """
            st.markdown(brain_html, unsafe_allow_html=True)
            st.write(f"**진단 결과:** {status}")
            st.write("---")
            st.caption("AI가 신호의 미세 떨림을 필터링하여 안정적인 진단을 제공합니다.")

    time.sleep(0.08)
