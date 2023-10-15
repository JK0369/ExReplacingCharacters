from binance.client import Client
from binance.enums import ORDER_TYPE_LIMIT

from datetime import datetime, timedelta
import pandas as pd
import config
import order_info

client = Client(config.API_KEY, config.API_SECRET_KEY)


# return: dataframe [{"timestamp", "open", "high", "low", "close", "volume"}]
def get_candle_df(symbol: str) -> pd.DataFrame:
    # 24시간 데이터 획득

    time_format = '%Y-%m-%d %H:%M:%S'
    start_date_time = datetime.now()
    end_date_time = start_date_time - timedelta(hours=24)

    start_time = start_date_time.strftime(time_format)
    end_time = end_date_time.strftime(time_format)

    klines = client.futures_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_5MINUTE, startTime=start_time,
                                   endTime=end_time)
    temp_df = pd.DataFrame(klines, columns=["timestamp", "open", "high", "low", "close", "volume", "close_time",
                                            "quote_asset_volume", "number_of_trades", "taker_buy_base_asset_volume",
                                            "taker_buy_quote_asset_volume", "ignore"])

    converted_datetime = [datetime.fromtimestamp(int(x / 1000)) for x in temp_df['timestamp']]
    temp_df['timestamp'] = pd.to_datetime(converted_datetime)

    cliped_df = temp_df[["timestamp", "open", "high", "low", "close", "volume"]]
    candle_df = cliped_df.sort_values(by='timestamp', ascending=False, ignore_index=True)
    return candle_df


def has_position(symbol: str) -> bool:
    account_info = client.get_account()

    # 포지션 정보 가져오기
    for balance in account_info['balances']:
        if balance['asset'] == symbol:
            # 포지션 있는 경우
            if float(balance['free']) > 0:
                return True

    # 포지션 없는 경우
    return False


def get_usdt_balance() -> float:
    return float(get_account_banlance(symbol='USDT')['balance'])


def get_account_banlance(symbol: str) -> dict:
    account_infos = _get_account_banlances()
    for asset in account_infos:
        if asset['asset'] == symbol:
            return asset
    return {}


def _get_account_banlances() -> list:
    return client.futures_account_balance()


# [
#     {
#         "accountAlias": "FzoCSgAuXqSgXqSg",
#         "asset": "BTC",
#         "balance": "0.00000000",
#         "crossWalletBalance": "0.00000000",
#         "crossUnPnl": "0.00000000",
#         "availableBalance": "0.00000000",
#         "maxWithdrawAmount": "0.00000000",
#         "marginAvailable": true,
#         "updateTime": 0
#     },
#     {
#         "accountAlias": "FzoCSgAuXqSgXqSg",
#         "asset": "XRP",
#         "balance": "0.00000000",
#         "crossWalletBalance": "0.00000000",
#         "crossUnPnl": "0.00000000",
#         "availableBalance": "0.00000000",
#         "maxWithdrawAmount": "0.00000000",
#         "marginAvailable": true,
#         "updateTime": 0
#     },
#     ...

def create_position(is_buy: bool, quantity: float, price: float) -> order_info.OrderInfo:
    order_params = {
        'symbol': config.TARGET_SYMBOL,
        'side': 'BUY',  # 매수 주문인 경우 'BUY', 매도 주문인 경우 'SELL'
        'type': ORDER_TYPE_LIMIT,  # 지정 가격 주문 사용
        'price': round(price, 2),  # 주문 가격 설정
        'quantity': round(quantity, 2),  # 주문 수량 설정
        'leverage': config.LEVERAGE,  # 레버리지 설정 (20배 레버리지)
        'timeinforce': 'GTC'
    }

    result = client.futures_create_order(**order_params)

    # timeinForce
    # "GTC" (Good 'Til Canceled): 주문을 취소할 때까지 계속 유지됩니다.
    # "IOC" (Immediate or Cancel): 주문을 즉시 실행하거나 부분적으로만 실행하고 나머지는 취소합니다.
    # "FOK" (Fill or Kill): 주문을 즉시 전량 실행하거나 전혀 실행하지 않습니다.

    return order_info.OrderInfo(result)

### order는 dict 타입
# order = {
#     'symbol': 'BTCUSDT',
#     'orderId': 12345678,
#     'clientOrderId': 'YOUR_UNIQUE_ORDER_ID',
#     'transactTime': 1633950107311,  # 주문 실행 시간 (타임스탬프)
#     'price': 60000.0,
#     'origQty': 1.0,
#     'executedQty': 1.0,  # 주문이 실행된 수량
#     'cummulativeQuoteQty': 60000.0,
#     'status': 'FILLED',
#     'timeInForce': 'GTC',
#     'type': 'LIMIT',
#     'side': 'BUY',
#     'fills': [
#         {
#             'price': 60000.0,
#             'qty': 1.0,
#             'commission': '0.001',
#             'commissionAsset': 'BTC',
#         }
#     ]
# }
###
