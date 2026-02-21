import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class OrchestratorAgent:
    def __init__(self, stock_engine, csa_agent):
        self.stock_engine = stock_engine
        self.csa_agent = csa_agent
        self.current_sim_time = datetime(2024, 5, 23, 9, 0)
        self.etf_portfolio = {} # {종목명: 가중치}
        self.history = []

    def step_hour(self, extra_signals=None):
        """1시간 진행"""
        print(f"--- Simulating Hour: {self.current_sim_time} ---")
        
        # 1. CSA로부터 행동 데이터 수집
        behaviors = self.csa_agent.generate_hourly_behavior(self.current_sim_time.strftime("%Y-%m-%d %H:%M"))
        
        # 2. 행동 데이터 분석 및 시장 시그널 생성
        signals = self._analyze_behaviors(behaviors)
        
        # 3. 포트폴리오 최적화 (재균형) - DA의 추가 시그널 반영
        self._optimize_portfolio(signals, extra_signals)
        
        # 4. 결과 저장
        self.history.append({
            'time': self.current_sim_time,
            'portfolio': self.etf_portfolio.copy(),
            'behaviors_count': len(behaviors)
        })
        
        # 5. 시간 업데이트
        self.current_sim_time += timedelta(hours=1)
        return behaviors

    def _analyze_behaviors(self, behaviors):
        """행동 데이터를 섹터별 시그널로 변환"""
        if behaviors.empty:
            return {}
            
        # 간단한 로직: 카드 결제 카테고리/증권 매수 섹터를 기반으로 점수 산출
        sector_scores = {
            'IT': 0.0, '금융': 0.0, '바이오': 0.0, '제조': 0.0, '에너지': 0.0, '소비재': 0.0, '플랫폼': 0.0
        }
        
        for _, row in behaviors.iterrows():
            if row['type'] == 'Card':
                if '온라인배달' in row['detail']:
                    sector_scores['플랫폼'] += 1
                elif '쇼핑' in row['detail']:
                    sector_scores['소비재'] += 1
            elif row['type'] == 'Securities':
                for sector in sector_scores.keys():
                    if sector in row['detail']:
                        if '매수' in row['detail']:
                            sector_scores[sector] += 2
                        else:
                            sector_scores[sector] -= 1
                            
        return sector_scores

    def _optimize_portfolio(self, signals, extra_signals=None):
        """시그널을 바탕으로 ETF 종목 선정 및 비중 조절"""
        # extra_signals는 DA의 제안: {'sector_recs': {'IT': 0.05, ...}}
        sector_recs = extra_signals.get('sector_recs', {}) if extra_signals else {}

        stock_list = list(self.stock_engine.tickers.keys())
        
        # 종목별 섹터 매핑 (예시)
        stock_sectors = {
            '삼성전자': 'IT', 'SK하이닉스': 'IT', 'LG에너지솔루션': '에너지',
            '삼성바이오로직스': '바이오', '현대차': '제조', 'NAVER': '플랫폼',
            '카카오': '플랫폼', 'POSCO홀딩스': '제조', '기아': '제조', '셀트리온': '바이오'
        }
        
        weights = {}
        for stock in stock_list:
            sector = stock_sectors.get(stock, '기타')
            score = signals.get(sector, 0)
            
            # 기본 비중 10% + 시그널에 따른 가감 + DA 제안 반영
            da_adj = sector_recs.get(sector, 0)
            weight = max(0.05, 0.10 + (score * 0.01) + da_adj)
            weights[stock] = weight
            
        # 가중치 정규화 (합계 1.0)
        total_weight = sum(weights.values())
        self.etf_portfolio = {k: v / total_weight for k, v in weights.items()}

if __name__ == "__main__":
    from agents.csa import CrowdSimulatorAgent
    from engine.stock_api import StockEngine
    
    se = StockEngine()
    csa = CrowdSimulatorAgent()
    oa = OrchestratorAgent(se, csa)
    
    for _ in range(3):
        oa.step_hour()
        print("Current ETF Portfolio:", oa.etf_portfolio)
