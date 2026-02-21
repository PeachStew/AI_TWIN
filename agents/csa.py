import pandas as pd
import numpy as np
import random

class CrowdSimulatorAgent:
    def __init__(self, num_personas=500):
        self.num_personas = num_personas
        self.personas = self._generate_personas()
        self.global_sentiment = 0.0 # -1.0(비관) ~ 1.0(낙관)
        
    def _generate_personas(self):
        personas = []
        age_groups = [20, 30, 40, 50, 60]
        risk_profiles = ['안정형', '중립형', '공격형']
        
        for i in range(self.num_personas):
            persona = {
                'user_id': f'user_{i:03d}',
                'age': random.choice(age_groups) + random.randint(0, 9),
                'risk_profile': random.choice(risk_profiles),
                'base_asset': random.uniform(10_000_000, 500_000_000), # 1천만 ~ 5억
                'preferred_sectors': random.sample(['IT', '금융', '바이오', '제조', '에너지', '소비재'], 2),
                'sentiment_sensitivity': random.uniform(0.5, 1.5) # 감도 개인차
            }
            personas.append(persona)
        return pd.DataFrame(personas)

    def update_sentiment(self, risk_sentiment):
        """Debater 피드백에 따라 시장 심리 업데이트"""
        # 점진적 반영 (Smoothing)
        self.global_sentiment = self.global_sentiment * 0.7 + risk_sentiment * 0.3

    def generate_hourly_behavior(self, current_time):
        """1시간 단위 금융 행동 생성"""
        behaviors = []
        
        # 전체 행동 발생 확률: 기본 30% + 센티먼트에 따른 변동
        base_prob = max(0.1, 0.3 + (self.global_sentiment * 0.1))
        
        for idx, persona in self.personas.iterrows():
            # 페르소나별 리스크 프로필과 센티먼트 감도 반영
            sentiment_adj = self.global_sentiment * persona['sentiment_sensitivity']
            
            # 랜덤한 확률로 행동 발생
            if random.random() < base_prob:
                # 비관적일 때는 출금/매도 확률 증가, 낙관적일 때는 입금/매수 확률 증가
                if sentiment_adj < -0.3:
                    behavior_types = ['Bank', 'Card', 'Securities', 'Securities', 'Life'] # 매도(Securities) 비중 높임 (간이)
                else:
                    behavior_types = ['Bank', 'Card', 'Securities', 'Life']
                
                behavior_type = random.choice(behavior_types)
                
                detail = ""
                amount = 0
                
                if behavior_type == 'Bank':
                    if sentiment_adj < -0.5:
                        action = random.choice(['예금출금', '예금출금', '대출상환']) # 불안 시 출금 증가
                    else:
                        action = random.choice(['예금입금', '예금출금', '대출상환'])
                    amount = random.uniform(10_000, 1_000_000)
                    detail = f"{action}: {int(amount)}원"
                elif behavior_type == 'Card':
                    category = random.choice(['식비', '교통', '쇼핑', '온라인배달', '의료'])
                    # 소비 위축 반영
                    amount = random.uniform(5_000, 200_000) * (1.0 + sentiment_adj * 0.2)
                    detail = f"{category} 결제: {int(max(0, amount))}원"
                elif behavior_type == 'Securities':
                    if sentiment_adj < -0.3:
                        action = '매도' if random.random() < 0.7 else '매수'
                    elif sentiment_adj > 0.3:
                        action = '매수' if random.random() < 0.7 else '매도'
                    else:
                        action = random.choice(['매수', '매도'])
                        
                    sector = random.choice(persona['preferred_sectors'])
                    amount = random.uniform(100_000, 5_000_000)
                    detail = f"{sector} 섹터 {action}: {int(amount)}원"
                elif behavior_type == 'Life':
                    action = random.choice(['보험료납입', '사고접수', '해지상담'])
                    detail = f"보험 {action}"
                
                behaviors.append({
                    'timestamp': current_time,
                    'user_id': persona['user_id'],
                    'type': behavior_type,
                    'detail': detail,
                    'amount': amount,
                    'risk_profile': persona['risk_profile']
                })
        return pd.DataFrame(behaviors)

if __name__ == "__main__":
    csa = CrowdSimulatorAgent()
    print("Personas Sample:")
    print(csa.personas.head())
    behaviors = csa.generate_hourly_behavior("2024-05-23 09:00")
    print("\nBehaviors Sample:")
    print(behaviors.head())
