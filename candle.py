COUNT_OF_CANDLES = 70 # 캔들 70개 기준

class Candles:
    # public method

    # _ohlcv_dataframe: [{"timestamp": 1, "open": 2, "high": 3, "low": 4, "close": 5, "volume": 6}]
    def __init__(self, ohlcv_dataframe):
        self._ohlcv_dataframe = ohlcv_dataframe
        self._opens = [float(x) for x in self._ohlcv_dataframe['open']]
        self._highs = [float(x) for x in self._ohlcv_dataframe['high']]
        self._lows = [float(x) for x in self._ohlcv_dataframe['low']]
        self._closes = [float(x) for x in self._ohlcv_dataframe['close']]
        self._volumes = [float(x) for x in self._ohlcv_dataframe['volume']]

    def update_ohlcv_dataframe(self, new_ohlcv_dataframe):
        self._ohlcv_dataframe = new_ohlcv_dataframe

    def get_now_volume(self):
        return self._volumes[0]

    def get_previous_volume(self):
        return self._volumes[1:COUNT_OF_CANDLES + 1]