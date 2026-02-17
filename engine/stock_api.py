import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

class StockEngine:
    def __init__(self):
        # 주요 KOSPI/KOSDAQ 종목 티커 (예시)
        self.tickers = {
            '삼성전자': '005930.KS',
            'SK하이닉스': '000660.KS',
            'LG에너지솔루션': '373220.KS',
            '삼성바이오로직스': '207940.KS',
            '현대차': '005380.KS',
            'NAVER': '035420.KS',
            '카카오': '035720.KS',
            'POSCO홀딩스': '005490.KS',
            '기아': '000270.KS',
            '셀트리온': '068270.KS'
        }
        
    def get_stock_data(self, period="1mo", interval="1h"):
        """종목별 가격 데이터 수집"""
        data = {}
        for name, ticker in self.tickers.items():
            stock = yf.Ticker(ticker)
            hist = stock.history(period=period, interval=interval)
            data[name] = hist['Close']
        return pd.DataFrame(data)

    def get_current_prices(self):
        """최근 종가 수집"""
        prices = {}
        for name, ticker in self.tickers.items():
            stock = yf.Ticker(ticker)
            # 최신 1일치 데이터의 마지막 값
            hist = stock.history(period="1d")
            if not hist.empty:
                prices[name] = hist['Close'].iloc[-1]
            else:
                prices[name] = 0.0
        return prices

if __name__ == "__main__":
    engine = StockEngine()
    print("Fetching current prices...")
    print(engine.get_current_prices())
