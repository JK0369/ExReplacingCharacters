import time
import threading

import algorithm
import candle

import client_binance
import config
import db


def update_df(loop: bool = True):
    while True:
        if loop:
            time.sleep(1)

        # dataframe[{"timestamp", "open", "high", "low", "close", "volume"}]
        btc_candle_df = client_binance.get_candle_df(symbol=config.BTC_SYMBOL)
        eth_candle_df = client_binance.get_candle_df(symbol=config.TARGET_SYMBOL)

        db.btc_candles = candle.Candles(btc_candle_df)
        db.eth_candles = candle.Candles(eth_candle_df)

        if not loop:
            break


def start_trade(delay: bool = True):
    if delay:
        time.sleep(1)

    has_position = client_binance.has_position(symbol=config.TARGET_SYMBOL)

    if not has_position:
        should_entry_position = algorithm.should_entry_position(
            btc_candles=db.btc_candles,
            eth_candles=db.eth_candles
        )
        if should_entry_position:
            should_entry_long_position = algorithm.get_should_entry_long_position(candles=db.eth_candles)
            price = algorithm.get_limit_price(candles=db.eth_candles, should_buy=should_entry_long_position)
            quantity = algorithm.get_entry_quantity(entered_usdt=client_binance.get_entered_usdt())

            order = client_binance.create_position(
                is_buy=should_entry_long_position,
                quantity=quantity,
                price=price
            )
            # print(order)
            # 알림넣기
        else:
            start_trade()
    else:
        if algorithm.should_sunhwan_mae():
            print()
        elif algorithm.should_take_profit():
            print()
        elif algorithm.should_stop_loss():
            print()
        else:
            start_trade()


def run():
    sam = client_binance.get_entered_usdt()

    print(sam, client_binance.get_total_usdt_balance())

    # TODO: 주석 해제 (현재는 테스트하느라 잠깐 주석처리)
    # # 최초 한번 update
    # update_df(loop=False)
    #
    # # trade
    # start_trade(delay=False)
    #
    # # update
    # thread = threading.Thread(target=update_df)
    # thread.start()


if __name__ == '__main__':
    run()
