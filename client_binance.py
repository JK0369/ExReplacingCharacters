from typing import List

from binance.client import Client
from binance.enums import ORDER_TYPE_LIMIT

from datetime import datetime, timedelta
import pandas as pd
import config
import order_info
import position
import trade_history

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

# 진입한 포지션을 포함한 확정된 USDT (현재 이익중이거나 손실중인 usdt는 미포함)
def get_total_usdt_balance() -> float:
    return float(get_account_banlance(symbol='USDT')['balance'])

# 현재 진입한 포지션들의 USDT (진입하지 않은 usdt는 제외)
def get_entered_usdt() -> float:
    account_info = client.futures_account()

    # USDT 잔고를 저장할 변수 초기화
    usdt_balance = 0.0

    # 포지션 정보를 확인하고 USDT 잔고 누적
    for position in account_info['positions']:
        if position['symbol'] == config.TARGET_SYMBOL:
            usdt_balance += float(position['initialMargin'])

    return usdt_balance

def get_account_banlance(symbol: str) -> dict:
    account_infos = _get_account_banlances()
    for asset in account_infos:
        if asset['asset'] == symbol:
            return asset
    return {}


def _get_account_banlances() -> list:
    return client.futures_account_balance()


def cancel_all_position_and_create_position(should_buy: bool, quantity: float, price: float) -> order_info.OrderInfo:
    _cancel_all_position()

    order_params = {
        'symbol': config.TARGET_SYMBOL,
        'side': 'BUY' if should_buy else 'SELL', # 매수 혹은 매도
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

def _cancel_all_position():
    # 지정가 주문 조회
    open_orders = client.futures_get_open_orders()

    # 체결되지 않은 주문 취소
    for order in open_orders:
        if order['status'] == 'NEW': # 'NEW': 체결되지 않은 주문
            result = client.futures_cancel_order(symbol=order['symbol'], orderId=order['orderId'])

def get_position_info() -> position.Info | None:
    # 포지션 정보 가져오기
    position_info = client.futures_position_information(symbol=config.TARGET_SYMBOL)
    if not position_info:
        return None
    info = position_info[0]
    return position.Info.from_api_response(info)

def get_position_history_list() -> list[trade_history.Trade]:
    position_trades = client.futures_account_trades(symbol=config.TARGET_SYMBOL)
    ordered_position_trades = position_trades[::-1]
    trades = [trade_history.Trade(entry) for entry in ordered_position_trades]
    return trades