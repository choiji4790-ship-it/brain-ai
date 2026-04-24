import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

# 웹 페이지 설정
st.set_page_config(page_title="Real-time AI Brain Monitor", page_icon="🧠")
st.title("🧠 실시간 AI 뇌파 분석 모니터")
st.write("사용자의 뇌파를 실시간으로 시뮬레이션하고 AI가 집중 상태를 분석합니다.")

# 세션 상태 초기화 (데이터 기록용)
if 'history' not in st.session_state:
    st.session_state.history = []

# 사이드바 설정
st.sidebar.header("System Settings")
is_running = st.sidebar.checkbox("실시간 모니터링 시작", value=True)
speed = st.sidebar.slider("업데이트 속도 (초)", 0.1, 2.0, 0.5)

# 메인 화면 레이아웃 (2개로 나눔)
col1, col2 = st.columns(2)

# 실시간 데이터 생성 및 분석 루프
placeholder = st.empty()

while is_running:
    with placeholder.container():
        # 1. 가상 뇌파 데이터 생성 (랜덤하지만 연속성 있게)
        focus_level = np.random.uniform(0.5, 4.5)
        t = np.linspace(0, 1, 200)
        signal = focus_level * np.sin(2 * np.pi * 20 * t) + np.random.normal(0, 0.5, 200)
        
        # 2. AI 분석 점수 계산
        score = min(100, np.abs(signal).mean() * 45)
        st.session_state.history.append(score)
        if len(st.session_state.history) > 20: # 최근 20개만 유지
            st.session_state.history.pop(0)

        # 3. 시각화 (현재 뇌파와 변화 그래프)
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Current Brainwaves")
            fig1, ax1 = plt.subplots()
            ax1.plot(t, signal, color='#1f77b4')
            ax1.set_ylim(-10, 10)
            st.pyplot(fig1)
        
        with c2:
            st.subheader("Concentration History")
            fig2, ax2 = plt.subplots()
            ax2.plot(st.session_state.history, marker='o', color='#ff7f0e')
            ax2.set_ylim(0, 100)
            st.pyplot(fig2)

        # 4. AI 상태 진단
        if score > 75:
            st.success(f"🔥 초집중 상태 (점수: {score:.1f}/100)")
        elif score > 45:
            st.info(f"☕ 보통 상태 (점수: {score:.1f}/100)")
        else:
            st.warning(f"⚠️ 주의: 집중도 하락 (점수: {score:.1f}/100)")

        time.sleep(speed)
        # Streamlit 화면 갱신
        if not is_running:
            break
