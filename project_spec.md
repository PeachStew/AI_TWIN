'Antigravity' 개발 팀이 즉시 개발에 착수할 수 있도록, 요청하신 내용을 바탕으로 한 **[신한금융그룹 데이터 기반 멀티 에이전트 Active ETF 시스템]** 전체 명세서(PRD)를 Markdown 형식으로 작성하였습니다.

---

# [Project Specification] Shinhan Multi-Agent Active ETF Simulator (S-MAES)

## 1. 프로젝트 개요
본 프로젝트는 신한금융그룹(은행, 카드, 증권, 라이프)의 가상 실시간 데이터를 활용하여 가상 고객 500명의 행동 패턴을 시뮬레이션하고, 이를 시장 데이터(KOSPI/KOSDAQ)와 결합하여 최적의 수익률을 지향하는 **Active ETF**를 설계 및 운용하는 시스템입니다.

---

## 2. 시스템 아키텍처 (Multi-Agent System)
시스템은 세 가지 핵심 에이전트로 구성되며, Orchestrator가 전체 워크플로우를 제어합니다.

### 2.1. Crowd Simulator Agent (CSA)
*   **역할**: 500명의 가상 페르소나 관리 및 시간별 금융 행동 생성.
*   **데이터 소스**: 가상의 신한금융 4대 부문 데이터.
    *   **Bank**: 예/적금 잔액 변화, 대출 신청 및 상환 현황.
    *   **Card**: 업종별 결제 내역 (소비 트렌드), 결제 빈도.
    *   **Securities**: 주식 매수/매도 성향, 선호 섹터, 자산 구성비.
    *   **Life**: 보험 가입/해지, 사고 보상 청구 데이터.
*   **작동 로직**: 1시간 단위로 각 유저의 상태(State)를 업데이트하고 행동 로그를 생성.

### 2.2. Orchestrator Agent (OA)
*   **역할**: 시뮬레이션 시간 제어, 데이터 취합, 최종 ETF 포트폴리오 확정.
*   **시간 제어**: "1H", "1D", "1M" 트리거에 따라 CSA에 명령 하달.
*   **포트폴리오 최적화**: 
    *   CSA로부터 전달받은 1시간 단위 ETF 제안을 누적.
    *   일간(Daily)/월간(Monthly) 단위로 가장 성과가 우수할 것으로 예상되는 'Best Active ETF'를 산출.
    *   재균형(Rebalancing) 가이드라인 제시.

### 2.3. Debater Agent (DA)
*   **역할**: 시스템의 논리적 허점 발견 및 전략 비판.
*   **분석 대상**: CSA의 행동 패턴 타당성, OA의 종목 선정 로직, 시장 왜곡 가능성.
*   **출력**: 개선 방안 리포트를 UI 하단에 실시간 업데이트.

---

## 3. 데이터 설계 및 알고리즘

### 3.1. 가상 고객 데이터 (Synthetic Data)
*   **Persona**: 연령대(20-60대), 자산 규모, 위험 선호도(안정형-공격형) 설정.
*   **Behavior-Stock Correlation**: 
    *   예: 카드 데이터 내 '배달 앱' 결제 급증 → '플랫폼/통신' 섹터 가중치 상향.
    *   예: 은행 데이터 내 '주택담보대출' 증가 → '건설/금융' 섹터 영향 분석.
*   **Time-Lag Logic**: 행동 데이터 발생 시점과 실제 주가 반영 시점 사이의 시차(Lag)를 통계적으로 계산하여 선행 지표로 활용.

### 3.2. Active ETF 구성 로직
1.  **Selection**: 유망 종목 10종 추출 (KOSPI/KOSDAQ 내 상위 종목 대상).
2.  **Weighting**: 행동 시그널 강도에 따른 가중치 배분 (최대 비중 20% 제한).
3.  **Target**: 향후 1개월 내 초과 수익률(Alpha) 극대화.

---

## 4. UI/UX 명세 (Streamlit)

### 4.1. 메인 대시보드
*   **Header**: "Shinhan Active ETF Real-time Intelligence".
*   **Status Panel**: 현재 가상 시뮬레이션 시간, 총 운용 자산(AUM), 현재 수익률.
*   **Main Visual**: 현재 Active ETF 구성비 (Donut Chart) 및 유저 행동 지표 (Heatmap).

### 4.2. 컨트롤 인터페이스 (Sidebar)
*   **[1H] 버튼**: 가상 데이터 1시간 생성 및 즉시 반영.
*   **[1D] 버튼**: 1H 프로세스 24회 반복 수행.
*   **[1M] 버튼**: 1D 프로세스 30회 반복 수행.
*   **Auto-Run Switch**: 실시간 자동 업데이트 모드 On/Off.

### 4.3. 분석 리포트 (Bottom)
*   **Orchestrator's View**: 익일/익월 최적 포트폴리오 상세 표.
*   **Debater's Critique**: 시스템 개선 제안 사항 (로그 형태).

---

## 5. 기술 스택 및 배포

| 구분 | 기술 스택 |
| :--- | :--- |
| **Language** | Python 3.9+ |
| **Framework** | Streamlit |
| **Data Science** | Pandas, NumPy, Scikit-learn |
| **Visualization** | Plotly, Altair |
| **Deployment** | Streamlit Cloud (GitHub Integration) |

---

## 6. 개발 로드맵

1.  **Phase 1**: 가상 유저 500명 페르소나 및 기본 금융 행동 생성 로직 구축.
2.  **Phase 2**: 행동 데이터-주가 간 상관관계 알고리즘 및 ETF 선정 엔진 개발.
3.  **Phase 3**: Orchestrator 시간 제어 루프 및 Streamlit UI 연동.
4.  **Phase 4**: Debater Agent 비판 로직 탑재 및 최종 배포 테스트.

---

## 7. 제약 및 예외 사항
*   본 시스템은 실제 신한금융 데이터를 사용하지 않으며, 모든 금융 데이터는 통계적 모델에 기반한 가상 생성물임.
*   주가 데이터는 Yahoo Finance API(yfinance)를 사용하여 현실성을 높임.

---
**Antigravity 개발팀 전달용**
*작성일: 2024. 05. 23*
*작성자: AI System Architect*