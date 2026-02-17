import pandas as pd
import numpy as np
import random

class CrowdSimulatorAgent:
    def __init__(self, num_personas=500):
        self.num_personas = num_personas
        self.personas = self._generate_personas()
        
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
                'preferred_sectors': random.sample(['IT', '금융', '바이오', '제조', '에너지', '소비재'], 2)
            }
            personas.append(persona)
        return pd.DataFrame(personas)

    def generate_hourly_behavior(self, current_time):
        """1시간 단위 금융 행동 생성"""
        behaviors = []
        for idx, persona in self.personas.iterrows():
            # 랜덤한 확률로 행동 발생
            if random.random() < 0.3: # 30% 확률로 행동 발생
                behavior_type = random.choice(['Bank', 'Card', 'Securities', 'Life'])
                
                detail = ""
                amount = 0
                
                if behavior_type == 'Bank':
                    action = random.choice(['예금입금', '예금출금', '대출상환'])
                    amount = random.uniform(10_000, 1_000_000)
                    detail = f"{action}: {int(amount)}원"
                elif behavior_type == 'Card':
                    category = random.choice(['식비', '교통', '쇼핑', '온라인배달', '의료'])
                    amount = random.uniform(5_000, 200_000)
                    detail = f"{category} 결제: {int(amount)}원"
                elif behavior_type == 'Securities':
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
