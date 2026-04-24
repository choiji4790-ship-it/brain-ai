import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.set_page_config(page_title="Autonomous Brain AI", layout="wide")

# CSS 스타일 (뇌 부위 애니메이션)
st.markdown("""
    <style>
    .brain-container { position: relative; width: 280px; height: 220px; background: #111; border-radius: 50% 50% 40% 40%; margin: auto; border: 1px solid #333; }
    .lobe { position: absolute; border: 1px solid #222; display: flex; align-items: center; justify-content: center; font-size: 11px; transition: 0.5s; color: #444; background: #1a1a1a; }
    .frontal { top: 15px; left: 70px; width: 140px; height: 70px; border-radius: 40% 40% 0 0; }
    .temporal { top: 95px; left: 45px; width: 90px; height: 60px; border-radius: 20%; }
    .parietal { top: 85px; left: 145px; width: 90px; height: 60px; border-radius: 20%; }
    .occipital { top: 155px; left: 90px; width: 100px; height: 50px; border-radius: 0 0 50% 50%; }
    .active-glow { color: white !important; font-weight: bold; box-shadow: 0 0 20px; transform: scale(1.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("🔬 자율형 AI 뇌파 정밀 진단 시스템")
st.write("사용자가 선택하지 않습니다. AI가 흐르는 신호를 분석해 환자의 상태를 실시간 역추적합니다.")

# 세션 상태 초기화
if 'eeg_buffer' not in st.session_state:
    st.session_state.eeg_buffer = np.zeros(100)
if 'target_freq' not in st.session_state:
    st.session_state.target_freq = 10.0 # 초기 주파수

# 사이드바: AI 통제
if st.sidebar.button("🚨 무작위 증상 발생 (환자 환경 변화)"):
    st.session_state.target_freq = np.random.uniform(1.0, 45.0)

run = st.sidebar.toggle("AI 분석 가동", value=True)

view = st.empty()

while run:
    # 1. 미지의 신호 생성 (서서히 목표 주파수로 변화 - 자연스러움 추구)
    st.session_state.target_freq += np.random.uniform(-0.5, 0.5) # 미세한 변화
    st.session_state.target_freq = np.clip(st.session_state.target_freq, 1, 50)
    
    new_sample = np.sin(time.time() * st.session_state.target_freq) + np.random.normal(0, 0.3)
    st.session_state.eeg_buffer = np.append(st.session_state.eeg_buffer[1:], new_sample)
    
    # 2. AI 주파수 추론 (단순 연산이 아닌 데이터 패턴 분석)
    # 실제 주파수 계산 (Zero-crossing rate 활용)
    zero_crosses = np.where(np.diff(np.sign(st.session_state.eeg_buffer)))[0]
    est_freq = len(zero_crosses) / 2 # 대략적인 Hz 추정
    
    # AI의 진단 로직
    color, status, active_parts, note = "#ffffff", "알 수 없음", [], "신호 분석 중..."
    if est_freq < 4:
        color, status, active_parts, note = "#7D3CFF", "깊은 수면 (Delta)", ["frontal", "parietal", "temporal", "occipital"], "환자가 의식이 없는 깊은 수면 상태입니다."
    elif est_freq < 8:
        color, status, active_parts, note = "#00FFAA", "이완/졸음 (Theta)", ["parietal"], "가벼운 졸음이나 명상 상태가 감지됩니다."
    elif est_freq < 13:
        color, status, active_parts, note = "#1f77b4", "안정 (Alpha)", ["occipital"], "안정적인 휴식 상태입니다."
    elif est_freq < 30:
        color, status, active_parts, note = "#FFA500", "집중/불안 (Beta)", ["frontal"], "고도의 집중 혹은 불안 반응이 전두엽에서 포착됩니다."
    else:
        color, status, active_parts, note = "#FF4B4B", "이상 과활성 (Gamma/발작)", ["frontal", "temporal"], "뇌의 이상 고주파 발생! 간질성 발작이 의심됩니다."

    # 3. 화면 렌더링
    with view.container():
        c1, c2 = st.columns([2, 1])
        with c1:
            st.subheader(f"📊 실시간 뇌파 신호 분석")
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(st.session_state.eeg_buffer, color=color, linewidth=2)
            ax.set_ylim(-3, 3)
            ax.set_facecolor('#0E1117')
            ax.grid(alpha=0.1)
            st.pyplot(fig)
            plt.close(fig)
            st.info(f"**AI 추정 주파수:** {est_freq:.1f} Hz | **상태:** {status}")

        with c2:
            st.subheader("🧠 실시간 뇌 맵핑")
            def get_style(name):
                return f"active-glow; background-color: {color}88;" if name in active_parts else ""
            
            brain_html = f"""
            <div class="brain-container">
                <div class="lobe frontal {get_style('frontal')}">전두엽</div>
                <div class="lobe temporal {get_style('temporal')}">측두엽</div>
                <div class="lobe parietal {get_style('parietal')}">두정엽</div>
                <div class="lobe occipital {get_style('occipital')}">후두엽</div>
            </div>
            """
            st.markdown(brain_html, unsafe_allow_html=True)
            st.write(f"**진단 노트:** {note}")

    time.sleep(0.05)
