import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 웹 페이지 설정
st.set_page_config(page_title="Brainwave AI Monitor", page_icon="🧠")
st.title("🧠 16살의 뇌파 AI 모니터")
st.write("실시간 뇌파를 분석하여 집중도를 측정하는 AI 시스템 시뮬레이션입니다.")

# 슬라이더 설정
focus_level = st.slider("테스트용 집중도 설정 (높을수록 집중)", 0.0, 5.0, 2.5)

# 가상 뇌파 생성
t = np.linspace(0, 1, 500)
signal = focus_level * np.sin(2 * np.pi * 20 * t) + np.random.normal(0, 0.5, 500)

# 그래프 출력
fig, ax = plt.subplots()
ax.plot(t, signal, color='#1f77b4')
ax.set_title("Simulated EEG Brainwaves")
st.pyplot(fig)

# 결과 분석 로직
score = min(100, np.abs(signal).mean() * 40)
st.subheader(f"현재 집중도 점수: {score:.2f}/100")

if score > 70:
    st.success("🔥 현재 매우 높은 집중 상태입니다!")
elif score > 40:
    st.info("☕ 보통의 집중도입니다. 조금 더 힘내세요!")
else:
    st.warning("⚠️ 휴식이 필요해 보여요. 잠시 눈을 붙여보세요.")

