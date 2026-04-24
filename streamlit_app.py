import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

# 페이지 설정
st.set_page_config(page_title="High-Speed EEG AI", layout="wide")

# CSS (뇌 부위 애니메이션)
st.markdown("""
    <style>
    .brain-container { position: relative; width: 260px; height: 200px; background: #111; border-radius: 50% 50% 40% 40%; margin: auto; border: 1px solid #333; }
    .lobe { position: absolute; border: 1px solid #222; display: flex; align-items: center; justify-content: center; font-size: 10px; transition: 0.2s; color: #444; background: #1a1a1a; }
    .frontal { top: 15px; left: 65px; width: 130px; height: 60px; border-radius: 40% 40% 0 0; }
    .temporal { top: 85px; left: 40px; width: 85px; height: 55px; border-radius: 20%; }
    .parietal { top: 75px; left: 135px; width: 85px; height: 55px; border-radius: 20%; }
    .occipital { top: 140px; left: 80px; width: 100px; height: 50px; border-radius: 0 0 50% 50%; }
    .active-glow { color: white !important; font-weight: bold; box-shadow: 0 0 15px; transform: scale(1.03); }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ 초고속 실시간 AI 뇌파 진단 시스템")

# 데이터 세션 초기화 (더 촘촘한 파형을 위해 데이터 포인트 200개로 확장)
if 'eeg_buffer' not in st.session_state:
    st.session_state.eeg_buffer = np.zeros(200)
if 'target_freq' not in st.session_state:
    st.session_state.target_freq = 12.0

# 사이드바 컨트롤
if st.sidebar.button("🚨 무작위 증상 강제 발생"):
    st.session_state.target_freq = np.random.uniform(2.0, 45.0)
speed_factor = st.sidebar.slider("흐름 속도 조절", 1, 10, 5)

run = st.sidebar.toggle("AI 시스템 가동", value=True)

view = st.empty()

# 성능을 위해 루프 최적화
while run:
    # 1. 고속 데이터 생성 (타임스탬프 기반으로 끊김 없는 파형 생성)
    curr_time = time.time()
    # 한 번의 루프에서 여러 개의 포인트를 추가하여 시각적 속도 상향
    new_points = [np.sin((curr_time + i*0.01) * st.session_state.target_freq) + np.random.normal(0, 0.2) for i in range(speed_factor)]
    
    st.session_state.eeg_buffer = np.append(st.session_state.eeg_buffer[len(new_points):], new_points)
    
    # 2. 주파수 추론 알고리즘 (빠른 감지를 위해 최근 데이터 기준)
    zero_crosses = np.where(np.diff(np.sign(st.session_state.eeg_buffer[-100:])))[0]
    est_freq = len(zero_crosses) * (100 / (len(st.session_state.eeg_buffer) * 0.1)) # 보정된 Hz 계산
    
    # AI 진단 로직
    color, status, active_parts = "#1f77b4", "분석 중", []
    if est_freq < 5:
        color, status, active_parts = "#7D3CFF", "Delta (깊은 수면)", ["frontal", "parietal", "temporal", "occipital"]
    elif est_freq < 13:
        color, status, active_parts = "#1f77b4", "Alpha (안정)", ["occipital"]
    elif est_freq < 30:
        color, status, active_parts = "#FFA500", "Beta (활동/긴장)", ["frontal"]
    else:
        color, status, active_parts = "#FF4B4B", "Gamma (위험/발작)", ["frontal", "temporal"]

    # 3. 렌더링
    with view.container():
        c1, c2 = st.columns([2, 1])
        with c1:
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(st.session_state.eeg_buffer, color=color, linewidth=1.5)
            ax.set_ylim(-3, 3)
            ax.set_facecolor('#0E1117')
            ax.axis('off') # 속도와 가독성을 위해 축 제거
            st.pyplot(fig)
            plt.close(fig)
            st.write(f"**AI 추정 수치:** {est_freq:.1f} Hz | **진단:** {status}")

        with c2:
            def get_style(name):
                return f"active-glow; background-color: {color}bb;" if name in active_parts else ""
            
            brain_html = f"""
            <div class="brain-container">
                <div class="lobe frontal {get_style('frontal')}">전두엽</div>
                <div class="lobe temporal {get_style('temporal')}">측두엽</div>
                <div class="lobe parietal {get_style('parietal')}">두정엽</div>
                <div class="lobe occipital {get_style('occipital')}">후두엽</div>
            </div>
            """
            st.markdown(brain_html, unsafe_allow_html=True)

    # 0.01초로 대기 시간을 줄여 물리적 속도 한계까지 밀어붙임
    time.sleep(0.01)
