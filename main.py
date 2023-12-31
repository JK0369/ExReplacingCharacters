import datetime
import threading

import position
import time

import algorithm
import candle

import client_binance
import config
import db
import entry
import utils
import sys

def update_df(loop: bool = True):
    while True:
        if loop:
            time.sleep(1)

        # dataframe[{"timestamp", "open", "high", "low", "close", "volume"}]
        btc_candle_df = client_binance.get_candle_df(symbol=config.BTC_SYMBOL)
        db.btc_candles = candle.Candles(btc_candle_df)

        if config.TARGET_SYMBOL == config.BTC_SYMBOL:
            db.target_candles = candle.Candles(btc_candle_df)
        else:
            target_candle_df = client_binance.get_candle_df(symbol=config.TARGET_SYMBOL)
            db.target_candles = candle.Candles(target_candle_df)

        if not loop:
            break


def start_trade(delay: bool = True):
    if delay:
        time.sleep(1)

    print('\n<---------------', utils.get_now_formatted_ymd_time(), "--------------->")

    has_position = client_binance.has_position(symbol=config.TARGET_SYMBOL)

    if not has_position:
        should_entry_position = algorithm.should_entry_position(
            btc_candles=db.btc_candles,
            target_candles=db.target_candles
        )
        if should_entry_position:
            price = algorithm.get_limit_price(candles=db.target_candles,
                                              should_long=not db.target_candles.get_now_candle_is_plus())
            quantity = algorithm.get_entry_quantity(entered_usdt=client_binance.get_entered_usdt(),
                                                    total_usdt=client_binance.get_total_usdt_balance(),
                                                    cur_target_coin_price=db.target_candles.get_now_close())

            order = client_binance.cancel_all_position_and_create_position(
                should_buy=algorithm.get_should_entry_long_position(db.target_candles),
                quantity=quantity,
                price=price
            )
            print('order>', order)
        else:
            print('waiting...')
    else:
        # 조회할때 필요한 정보
        position_info = client_binance.get_position_info()
        total_usdt_balance = client_binance.get_total_usdt_balance()
        trade_history_list = client_binance.get_position_history_list()
        entered_usdt = client_binance.get_entered_usdt()
        total_usdt = client_binance.get_total_usdt_balance()

        entry_category = algorithm.get_entry_category(position_info, trade_history_list, db.target_candles,
                                                      total_usdt_balance, entered_usdt, total_usdt)

        # 거래할때 필요한 정보
        price = algorithm.get_limit_price(candles=db.target_candles,
                                          should_long=position_info.position_type == position.PositionType.SHORT)

        if entry_category == entry.Category.익절 or entry_category == entry.Category.손절:
            print('익절 or 손절')
            client_binance.cancel_all_position_and_create_position(should_buy=False, quantity=entered_usdt, price=price)

        elif entry_category == entry.Category.반털:
            print('반털')
            client_binance.cancel_all_position_and_create_position(should_buy=False, quantity=entered_usdt / 2,
                                                                   price=price)
        elif entry_category == entry.Category.물타기:
            print('물타기')
            quantity = algorithm.get_entry_quantity(entered_usdt, total_usdt, db.target_candles.get_now_close())
            client_binance.cancel_all_position_and_create_position(should_buy=True, quantity=quantity, price=price)

        else:
            print('대기')

    start_trade()


def test():
    update_df(loop=False)


def run():
    # test()

    # 재귀 제한 풀기
    sys.setrecursionlimit(10000^10000^100000)  #  재귀 깊이 제한 풀기

    # 최초 한번 update
    update_df(loop=False)

    # trade
    start_trade(delay=False)

    # update
    thread = threading.Thread(target=update_df)
    thread.start()


if __name__ == '__main__':
    run()
