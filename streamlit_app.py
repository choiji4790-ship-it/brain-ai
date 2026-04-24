import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.set_page_config(page_title="Medical EEG Simulator", layout="wide")
st.title("🏥 의료용 실시간 뇌파 시뮬레이션 및 진단 시스템")

# 1. 사이드바: 환자 정보 및 증상 설정
st.sidebar.header("Patient Status")
patient_name = st.sidebar.text_input("환자 성함", "Unknown")
condition = st.sidebar.selectbox("현재 증상 선택", 
    ["Normal (정상)", "Seizure (발작/간질)", "Deep Sleep (깊은 수면)", "High Stress (고도의 긴장)"])

# 증상별 주파수 및 부위 설정
cond_map = {
    "Normal (정상)": {"freq": 10, "label": "Alpha파", "region": "후두엽 (안정)", "desc": "안정적인 휴식 상태입니다."},
    "Seizure (발작/간질)": {"freq": 35, "label": "Gamma파 (이상)", "region": "전두엽/측두엽 (과활성)", "desc": "뇌의 비정상적인 전기 활동이 감지됩니다!"},
    "Deep Sleep (깊은 수면)": {"freq": 2, "label": "Delta파", "region": "뇌 전체 (서파)", "desc": "깊은 수면 단계에 진입했습니다."},
    "High Stress (고도의 긴장)": {"freq": 20, "label": "High Beta파", "region": "전두엽 (판단/불안)", "desc": "스트레스 수치가 높고 뇌가 과부하 상태입니다."}
}

# 2. 메인 화면 레이아웃
col1, col2 = st.columns([2, 1])

placeholder = st.empty()

while True:
    with placeholder.container():
        current_cond = cond_map[condition]
        t = np.linspace(0, 1, 500)
        
        # 뇌파 생성 (증상에 따라 주파수 변화)
        noise = np.random.normal(0, 0.2, 500)
        signal = np.sin(2 * np.pi * current_cond["freq"] * t) + noise
        
        with col1:
            st.subheader(f"📊 실시간 뇌파 그래프 - {current_cond['label']}")
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(t, signal, color='red' if "Seizure" in condition else 'blue')
            ax.set_ylim(-3, 3)
            ax.grid(True, alpha=0.3)
            st.pyplot(fig)
            
        with col2:
            st.subheader("🔍 AI 진단 결과")
            st.info(f"**환자명:** {patient_name}")
            st.warning(f"**활성 부위:** {current_cond['region']}")
            st.write(f"**상태 요약:** {current_cond['desc']}")
            
            # 진행 바 시각화 (자극 강도)
            intensity = current_cond["freq"] * 2.5
            st.write("뇌 활성도 강도")
            st.progress(min(100, int(intensity)))

        time.sleep(0.5)
