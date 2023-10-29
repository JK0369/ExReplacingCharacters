# noinspection NonAsciiCharacters

### 계정
# API docu: https://python-binance.readthedocs.io/en/latest/
API_KEY = 'oveppFoaNIMmD0dwpgUXq8g4AmlRUME0FY446xAzN1wqykU9wckRQBTHhIqO0tPw'
API_SECRET_KEY = 'K2spwteWI9LUCUvkPMT6Shq8bobBHhnZRwp3hTDt9Vxpz1fEpQ68SbNMmQxenpcu'

BTC_SYMBOL = 'BTCUSDT'
TARGET_SYMBOL = 'ETHUSDT'
LEVERAGE = 20

### 매수 기준
OVER_MULTIPLIER_VOLUME = 3

# quantity 계산: 1/45씩 진입: 1 1 1 / 2 2 2 / 4 4 4 / 8 8 8 = 45
FRACTION_RATIO = 1 / 45

# 지정가로 팔것이기 때문에, 현재 가격보다 훨씬 낮게 처리 (3배 곱해주기)
LIMIT_RATIO = 0.01

# 수익 기준 수수료
FEE = 0.08

# 평균값을 구할때의 5분봉 개수
COUNT_OF_5_MINUTE_CANDLES = 70

반털_거래량_기준_FRACTION_RATIO = FRACTION_RATIO * 5

# 0.2%이상 안움직이면 횡보라고 판단
횡보_변동폭_기준_ratio = 0.2

# 현재 캔들

# 꼬리 판단 기준
전체_캔들_길이_중_꼬리_길이_기준 = 1/7