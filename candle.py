import pandas as pd

import config

COUNT_OF_CANDLES = 70 # 캔들 70개 기준

class Candles:
    # public method

    # _ohlcv_dataframe: [{"timestamp": 1, "open": 2, "high": 3, "low": 4, "close": 5, "volume": 6}]
    def __init__(self, ohlcv_dataframe: pd.DataFrame):
        self.ohlcv_dataframe = ohlcv_dataframe
        self.opens = [float(x) for x in self.ohlcv_dataframe['open']]
        self.highs = [float(x) for x in self.ohlcv_dataframe['high']]
        self.lows = [float(x) for x in self.ohlcv_dataframe['low']]
        self.closes = [float(x) for x in self.ohlcv_dataframe['close']]
        self.volumes = [float(x) for x in self.ohlcv_dataframe['volume']]

    def update_ohlcv_dataframe(self, new_ohlcv_dataframe: pd.DataFrame):
        self.ohlcv_dataframe = new_ohlcv_dataframe

    # now candle

    def get_now_volume(self) -> float:
        return self.volumes[0]

    def get_now_open(self) -> float:
        return self.opens[0]

    def get_now_close(self) -> float:
        return self.closes[0]

    def get_now_high(self) -> float:
        return self.highs[0]

    def get_now_low(self) -> float:
        return self.lows[0]

    def get_now_candle_is_plus(self) -> bool:
        return self.opens[0] < self.closes[0]

    def get_now_candle_length(self) -> float:
        return self.get_now_high() - self.get_now_low()

    def get_is_now_candle_꼬리_생김(self):
        if self.get_now_candle_is_plus():
            return self.get_now_candle_length() * config.전체_캔들_길이_중_꼬리_길이_기준 <= (
                        self.get_now_high() - self.get_now_close())
        else:
            return self.get_now_candle_length() * config.전체_캔들_길이_중_꼬리_길이_기준 <= (
                        self.get_now_close() - self.get_now_low())

    # previous candle

    def get_previous_candles(self):
        return self[1:COUNT_OF_CANDLES + 1]

    def get_previous_close(self) -> float:
        return self.closes[1]

    def get_previous_volumes(self) -> list:
        return self.volumes[1:COUNT_OF_CANDLES + 1]

    def get_previous_candle_is_plus(self) -> bool:
        return self.opens[1] < self.closes[1]

    def get_variable_ratio(self, cnt: int) -> float:
        count = COUNT_OF_CANDLES - 1 if COUNT_OF_CANDLES < cnt or cnt == 0 else cnt
        sum_value = 0

        for i in range(1, count+1):
            # 변동률: (high - low) / low * 100
            sum_value += abs(self.highs[i] - self.lows[i]) / self.lows[i] * 100

        return sum_value / count * config.LEVERAGE

    # etc

    def is_same_candle_now_and_previous(self) -> bool:
        return self.get_now_candle_is_plus() == self.get_previous_candle_is_plus()

    def is_5분봉_3틱(self) -> bool:
        # 3개의 봉 부호가 같은지
        opens = self.opens[0:2]
        closes = self.closes[0:2]
        diffs = [o-c for o, c in zip(opens, closes)]
        all_minus = all(0 < x for x in diffs)
        all_plus = all(x < 0 for x in diffs)
        equal_candles_부호 = all_minus or all_plus

        if not equal_candles_부호:
            return False

        # 3개의 고점 or 저점이 증가하는지
        ## 현재의 봉이 양수인 경우
        if self.get_now_candle_is_plus():
            ### high 기준으로 증가하는지 체크
            return self.highs[2] < self.highs[1] < self.highs[0]
        else:
            ## 현재의 봉이 음수인 경우
            ### low 기준으로 낮아지는지 체크
            return self.lows[2] > self.lows[1] > self.lows[0]

    def _is_now_candle_변동률이_수익구간(self) -> bool:
        variable_ratio = abs((self.get_now_open() - self.get_now_close()) / self.get_now_open())
        return config.LEVERAGE * config.FEE <= variable_ratio
