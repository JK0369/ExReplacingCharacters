import time
import pandas as pd
import numpy as np
import scipy.stats as stats
from datetime import datetime, timedelta
import threading
import candle

import client_binance
import db


def update_df_every_seconds():
    while True:
        time.sleep(1)

        # dataframe[{"timestamp", "open", "high", "low", "close", "volume"}]
        bitcoin_candle_df = client_binance.get_candle_df(symbol='BTCUSDT')
        etherium_candle_df = client_binance.get_candle_df(symbol='ETHUSDT')

        db.bitcoin_candles = candle.Candles(bitcoin_candle_df)
        db.etherium_candles = candle.Candles(etherium_candle_df)


def run():
    thread = threading.Thread(target=update_df_every_seconds)
    thread.start()


if __name__ == '__main__':
    run()
