import pandas as pd

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

    def get_now_candle_is_plus(self) -> bool:
        return self.opens[0] < self.closes[0]

    # previous candle

    def get_previous_close(self) -> float:
        return self.closes[1]

    def get_previous_volumes(self) -> list:
        return self.volumes[1:COUNT_OF_CANDLES + 1]

    def get_previous_candle_is_plus(self) -> bool:
        return self.opens[1] < self.closes[1]

    # etc

    def is_same_candle_now_and_previous(self) -> bool:
        return self.get_now_candle_is_plus() == self.get_previous_candle_is_plus()