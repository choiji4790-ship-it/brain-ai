import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.set_page_config(page_title="Brain Mapping AI", layout="wide")

# [핵심] CSS로 뇌 모양과 활성 애니메이션 만들기
st.markdown("""
    <style>
    .brain-container {
        position: relative; width: 300px; height: 250px; 
        background: #1e1e1e; border-radius: 50% 50% 40% 40%;
        margin: 20px auto; border: 2px solid #444;
    }
    .lobe {
        position: absolute; border: 1px solid #333; 
        display: flex; align-items: center; justify-content: center;
        font-size: 12px; transition: 0.3s; color: #888;
    }
    /* 뇌 부위별 위치 설정 */
    .frontal { top: 20px; left: 75px; width: 150px; height: 80px; border-radius: 40% 40% 0 0; }
    .temporal { top: 110px; left: 50px; width: 100px; height: 70px; border-radius: 20%; }
    .parietal { top: 100px; left: 150px; width: 100px; height: 70px; border-radius: 20%; }
    .occipital { top: 170px; left: 100px; width: 100px; height: 60px; border-radius: 0 0 50% 50%; }
    
    /* 활성화 애니메이션 */
    .active-lobe {
        background-color: rgba(255, 75, 75, 0.8) !important;
        color: white !important; font-weight: bold;
        box-shadow: 0 0 20px #ff4b4b; transform: scale(1.05);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🧠 AI 실시간 뇌 기능 매핑 시스템")

mapping = {
    "정상 상태": {"freq": 10, "active": ["occipital"], "note": "Alpha파 (안정)", "color": "#1f77b4"},
    "간질/발작": {"freq": 35, "active": ["frontal", "temporal"], "note": "고주파 (위험!)", "color": "#FF4B4B"},
    "수면 상태": {"freq": 3, "active": ["frontal", "parietal", "temporal", "occipital"], "note": "Delta파 (수면)", "color": "#7D3CFF"},
    "극도의 불안": {"freq": 22, "active": ["frontal"], "note": "Beta파 (긴장)", "color": "#FFA500"}
}

condition = st.sidebar.selectbox("진단 모드 선택", list(mapping.keys()))
run = st.sidebar.toggle("모니터링 시스템 가동", value=True)

if 'eeg_data' not in st.session_state:
    st.session_state.eeg_data = np.zeros(100)

main_view = st.empty()

while run:
    conf = mapping[condition]
    new_val = np.sin(time.time() * conf["freq"]) + np.random.normal(0, 0.1)
    st.session_state.eeg_data = np.append(st.session_state.eeg_data[1:], new_val)
    
    with main_view.container():
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader(f"🌐 실시간 뇌파 신호: {conf['note']}")
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(st.session_state.eeg_data, color=conf['color'], linewidth=2)
            ax.set_ylim(-2.5, 2.5)
            ax.set_facecolor('#0E1117')
            ax.grid(alpha=0.1)
            st.pyplot(fig)
            plt.close(fig)

        with col2:
            st.subheader("📍 활성 부위 매핑")
            # 뇌 모양 시각화 HTML
            def get_class(lobe_name):
                return "active-lobe" if lobe_name in conf["active"] else ""

            brain_html = f"""
            <div class="brain-container">
                <div class="lobe frontal {get_class('frontal')}">전두엽</div>
                <div class="lobe temporal {get_class('temporal')}">측두엽</div>
                <div class="lobe parietal {get_class('parietal')}">두정엽</div>
                <div class="lobe occipital {get_class('occipital')}">후두엽</div>
            </div>
            """
            st.markdown(brain_html, unsafe_allow_html=True)
            st.metric("자극 빈도", f"{conf['freq']} Hz")

    time.sleep(0.1)
