import pandas as pd
import candle
import numpy as np

btc_candles: candle.Candles
target_candles: candle.Candles
fee_ratio = 0.05 # 보수적으로 0.05%