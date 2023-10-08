from binance.client import Client
from datetime import datetime, timedelta
import pandas as pd

# API docu: https://python-binance.readthedocs.io/en/latest/
API_KEY = 'oveppFoaNIMmD0dwpgUXq8g4AmlRUME0FY446xAzN1wqykU9wckRQBTHhIqO0tPw'
API_SECRET_KEY = 'K2spwteWI9LUCUvkPMT6Shq8bobBHhnZRwp3hTDt9Vxpz1fEpQ68SbNMmQxenpcu'

client = Client(API_KEY, API_SECRET_KEY)

# return: dataframe [{"timestamp", "open", "high", "low", "close", "volume"}]
def get_candle_df(symbol):
    # 24시간 데이터 획득

    time_format = '%Y-%m-%d %H:%M:%S'
    start_date_time = datetime.now()
    end_date_time = start_date_time - timedelta(hours=24)

    start_time = start_date_time.strftime(time_format)
    end_time = end_date_time.strftime(time_format)

    klines = client.futures_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_5MINUTE, startTime=start_time, endTime=end_time)
    temp_df = pd.DataFrame(klines, columns=["timestamp", "open", "high", "low", "close", "volume", "close_time",
                                            "quote_asset_volume", "number_of_trades", "taker_buy_base_asset_volume",
                                            "taker_buy_quote_asset_volume", "ignore"])

    converted_datetime = [datetime.fromtimestamp(int(x / 1000)) for x in temp_df['timestamp']]
    temp_df['timestamp'] = pd.to_datetime(converted_datetime)

    # TODO: volume값이 다름

    cliped_df = temp_df[["timestamp", "open", "high", "low", "close", "volume"]]
    candle_df = cliped_df.sort_values(by='timestamp', ascending=False, ignore_index=True)
    return candle_df