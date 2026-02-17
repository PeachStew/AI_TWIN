import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time

from agents.csa import CrowdSimulatorAgent
from agents.oa import OrchestratorAgent
from agents.da import DebaterAgent
from engine.stock_api import StockEngine

# 페이지 설정
st.set_page_config(page_title="Shinhan Active ETF S-MAES", layout="wide")

# 세션 상태 초기화
if 'initialized' not in st.session_state:
    st.session_state.stock_engine = StockEngine()
    st.session_state.csa = CrowdSimulatorAgent()
    st.session_state.oa = OrchestratorAgent(st.session_state.stock_engine, st.session_state.csa)
    st.session_state.da = DebaterAgent()
    st.session_state.all_behaviors = pd.DataFrame()
    st.session_state.performance_history = pd.DataFrame(columns=['Time', 'Return'])
    st.session_state.initialized = True

# 사이드바: 컨트롤 인터페이스
st.sidebar.title("🎮 제어 센터")
st.sidebar.markdown(f"**현재 가상 시간:** {st.session_state.oa.current_sim_time.strftime('%Y-%m-%d %H:%M')}")

def run_simulation(steps=1):
    for _ in range(steps):
        behaviors = st.session_state.oa.step_hour()
        if not behaviors.empty:
            st.session_state.all_behaviors = pd.concat([st.session_state.all_behaviors, behaviors]).tail(1000)
        
        # 가상 수익률 시뮬레이션 (간단하게 랜덤+시그널 기반)
        last_return = st.session_state.performance_history['Return'].iloc[-1] if not st.session_state.performance_history.empty else 0.0
        new_return = last_return + (np.random.normal(0.001, 0.005))
        new_row = pd.DataFrame({'Time': [st.session_state.oa.current_sim_time], 'Return': [new_return]})
        st.session_state.performance_history = pd.concat([st.session_state.performance_history, new_row])
        
        # Debater 분석
        st.session_state.da.analyze_strategy(
            st.session_state.oa.current_sim_time, 
            st.session_state.oa.etf_portfolio, 
            behaviors
        )

col1, col2, col3 = st.sidebar.columns(3)
if col1.button("1H"):
    run_simulation(1)
if col2.button("1D"):
    run_simulation(24)
if col3.button("1M"):
    run_simulation(24 * 30)

auto_run = st.sidebar.toggle("실시간 자동 업데이트")
if auto_run:
    run_simulation(1)
    time.sleep(1)
    st.rerun()

# 메인 화면
st.title("🏦 Shinhan Active ETF Real-time Intelligence")
st.markdown("---")

# 상단 지표
m1, m2, m3 = st.columns(3)
m1.metric("총 운용 자산 (AUM)", "₩ 1.2T", "+1.2%")
curr_return = st.session_state.performance_history['Return'].iloc[-1] if not st.session_state.performance_history.empty else 0.0
m2.metric("현재 수익률", f"{curr_return:.2%}", f"{(curr_return*100):.2f}%")
m3.metric("가상 고객 수", f"{st.session_state.csa.num_personas}명", "Active")

# 중간 실시간 차트
c1, c2 = st.columns([2, 1])

with c1:
    st.subheader("📈 ETF 누적 수익률 추이")
    if not st.session_state.performance_history.empty:
        fig = px.line(st.session_state.performance_history, x='Time', y='Return', template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("시뮬레이션을 시작해주세요.")

with c2:
    st.subheader("🍩 현재 ETF 구성비")
    portfolio = st.session_state.oa.etf_portfolio
    if portfolio:
        df_p = pd.DataFrame(list(portfolio.items()), columns=['종목', '비중'])
        fig = px.pie(df_p, values='비중', names='종목', hole=0.4, template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("포트폴리오 데이터가 없습니다.")

# 하단 분석 리포트
st.markdown("---")
b1, b2 = st.columns(2)

with b1:
    st.subheader("🔍 Orchestrator's Analysis")
    if not st.session_state.all_behaviors.empty:
        st.write("최근 고객 행동 로그 (Top 10)")
        st.dataframe(st.session_state.all_behaviors.sort_values('timestamp', ascending=False).head(10), use_container_width=True)
    else:
        st.write("대기 중...")

with b2:
    st.subheader("⚖️ Debater's Critique")
    if st.session_state.da.critiques:
        latest_critique = st.session_state.da.critiques[-1]
        st.info(latest_critique)
    else:
        st.write("전략 분석 중...")

# CSS 포인트 컬러 적용
st.markdown("""
<style>
    .stMetric { background-color: #1e1e1e; padding: 10px; border-radius: 10px; border: 1px solid #333; }
    h1, h2, h3 { color: #0046FF; }
</style>
""", unsafe_allow_html=True)
