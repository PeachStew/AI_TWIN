class DebaterAgent:
    def __init__(self):
        self.critiques = []

    def analyze_strategy(self, current_time, portfolio, behaviors):
        """현재 상태와 포트폴리오 전략 비판 및 개선 제안"""
        critique = f"### ⚖️ Debater Critique ({current_time})\n\n"
        
        # 1. 기본 건전성 체크 (종목 수, 비중)
        critique += "#### 📌 포트폴리오 건전성\n"
        critique += self._check_portfolio_health(portfolio)
        
        # 2. 행동 데이터 기반 트렌드 분석
        critique += "\n#### 📊 행동 데이터 및 트렌드 분석\n"
        critique += self._analyze_behaviors_and_trends(behaviors, portfolio)
        
        # 3. 거시적 위험 시그널 (은행/보험 데이터)
        critique += "\n#### 🌐 거시적 리스크 및 기타 제안\n"
        critique += self._check_macro_signals(behaviors)
        
        self.critiques.append(critique)
        return critique

    def _check_portfolio_health(self, portfolio):
        health_report = ""
        # 종목 수 체크
        if len(portfolio) < 5:
            health_report += "- ⚠️ **ALERT**: 포트폴리오 종목 수가 너무 적습니다. 최소 5개 이상으로 분산하여 섹터별 리스크를 관리하세요.\n"
        
        # 특정 종목 편중도 체크
        for stock, weight in portfolio.items():
            if weight > 0.20:
                 health_report += f"- ⚠️ **CAUTION**: **{stock}** 비중이 {weight:.1%}입니다. 단일 종목 20% 초과 금지 룰을 검토하세요.\n"
        
        if not health_report:
            health_report = "- ✅ 포트폴리오 기본 구성이 안정적입니다.\n"
        return health_report

    def _analyze_behaviors_and_trends(self, behaviors, portfolio):
        if behaviors.empty:
            return "- 🔍 분석 가능한 행동 데이터가 현재 없습니다.\n"
            
        report = ""
        # 섹터별 시그널 추출 (OA 로직과 유사하지만 '미반영'을 찾기 위함)
        sector_signals = {}
        for _, row in behaviors.iterrows():
            if row['type'] == 'Card' and '온라인배달' in row['detail']:
                sector_signals['플랫폼'] = sector_signals.get('플랫폼', 0) + 1
            if row['type'] == 'Securities' and '매수' in row['detail']:
                for s in ['IT', '금융', '바이오', '제조', '에너지', '소비재']:
                    if s in row['detail']:
                        sector_signals[s] = sector_signals.get(s, 0) + 1

        # 현재 포트폴리오의 섹터 분포 (간이 맵핑)
        stock_sectors = {
            '삼성전자': 'IT', 'SK하이닉스': 'IT', 'LG에너지솔루션': '에너지',
            '삼성바이오로직스': '바이오', '현대차': '제조', 'NAVER': '플랫폼',
            '카카오': '플랫폼', 'POSCO홀딩스': '제조', '기아': '제조', '셀트리온': '바이오'
        }
        active_sectors = {stock_sectors.get(s, '기타') for s, w in portfolio.items() if w > 0}

        # 미반영 트렌드 포착
        for sector, score in sector_signals.items():
            if score >= 3 and sector not in active_sectors:
                report += f"- 💡 **OPPORTUNITY**: 현재 고객 데이터에서 **{sector}** 섹터 시그널이 강하나, 포트폴리오에 반영되지 않았습니다. 추가를 검토하세요.\n"
        
        # 데이터 부족 알림
        if len(behaviors) < 15:
            report += "- ℹ️ 행동 데이터 샘플이 다소 부족하여 시그널 신뢰도가 낮을 수 있습니다.\n"
        elif not report:
            report = "- ✅ 주요 고객 트렌드가 포트폴리오에 적절히 반영되어 있습니다.\n"
            
        return report

    def _check_macro_signals(self, behaviors):
        if behaviors.empty:
            return "- 특이 사항 없음\n"
            
        report = ""
        # 은행/보험 데이터 분석
        bank_withdrawals = len(behaviors[(behaviors['type'] == 'Bank') & (behaviors['detail'].str.contains('예금출금'))])
        life_incidents = len(behaviors[(behaviors['type'] == 'Life') & (behaviors['detail'].str.contains('사고접수'))])
        
        if bank_withdrawals > 5:
            report += "- 🚨 **MACRO RISK**: 예금 출금 행동이 빈번하게 감지됩니다. 시장 유동성 저하 또는 불안 심리 확산 가능성을 주시하세요.\n"
        if life_incidents > 3:
            report += "- 🚨 **SYSTEMIC RISK**: 보험 사고 접수가 증가하고 있습니다. 관련 섹터(손해보험 등) 변동성 대비가 필요합니다.\n"
            
        if not report:
            report = "- ✅ 거시 리스크 측면에서 특이 시그널이 감지되지 않았습니다.\n"
        return report

if __name__ == "__main__":
    import pandas as pd
    da = DebaterAgent()
    sample_portfolio = {'삼성전자': 0.25, 'SK하이닉스': 0.10, '현대차': 0.10, '셀트리온': 0.10, 'LG에너지솔루션': 0.10}
    
    # 샘플 행동 데이터 생성
    sample_behaviors = pd.DataFrame([
        {'type': 'Card', 'detail': '온라인배달 결제', 'amount': 20000},
        {'type': 'Card', 'detail': '온라인배달 결제', 'amount': 15000},
        {'type': 'Card', 'detail': '온라인배달 결제', 'amount': 30000},
        {'type': 'Bank', 'detail': '예구출금', 'amount': 1000000},
        {'type': 'Bank', 'detail': '예금출금', 'amount': 1000000},
        {'type': 'Bank', 'detail': '예금출금', 'amount': 1000000},
        {'type': 'Bank', 'detail': '예금출금', 'amount': 1000000},
        {'type': 'Bank', 'detail': '예금출금', 'amount': 1000000},
        {'type': 'Bank', 'detail': '예금출금', 'amount': 1000000},
    ])
    
    print(da.analyze_strategy("2024-05-23 09:00", sample_portfolio, sample_behaviors))
