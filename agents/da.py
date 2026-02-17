class DebaterAgent:
    def __init__(self):
        self.critiques = []

    def analyze_strategy(self, current_time, portfolio, behaviors):
        """현재 상태와 포트폴리오 전략 비판"""
        critique = f"[{current_time}] Debater Critique:\n"
        
        # 1. 다양성 체크
        if len(portfolio) < 5:
            critique += "- WARNING: 포트폴리오 종목 수가 너무 적습니다. 분산 투자 원칙에 어긋납니다.\n"
        
        # 2. 편중도 체크
        max_weight = max(portfolio.values()) if portfolio else 0
        if max_weight > 0.20:
             critique += f"- CAUTION: 특정 종목 비중({max_weight:.1%})이 20%를 초과하여 리스크가 높습니다.\n"
             
        # 3. 행동 데이터 반영 적절성 (샘플 로직)
        if len(behaviors) < 10:
             critique += "- NOTE: 수집된 행동 데이터 샘플이 적어 시그널의 신뢰도가 낮을 수 있습니다.\n"
        else:
             critique += "- INFO: 충분한 행동 데이터가 수집되어 시장 트렌드를 반영하고 있습니다.\n"
             
        self.critiques.append(critique)
        return critique

if __name__ == "__main__":
    da = DebaterAgent()
    sample_portfolio = {'삼성전자': 0.25, 'SK하이닉스': 0.10}
    print(da.analyze_strategy("2024-05-23 09:00", sample_portfolio, []))
