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
            is_buy, quantity, price = algorithm.get_entry_position(
                candles=db.eth_candles,
                usdt_balance=client_binance.get_usdt_balance(),
                leverage=config.LEVERAGE
            )
            order = client_binance.create_position(
                is_buy=is_buy,
                quantity=quantity,
                price=price
            )
            # print(order)
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
    # 최초 한번 update
    update_df(loop=False)

    # trade
    start_trade(delay=False)

    # update
    thread = threading.Thread(target=update_df)
    thread.start()


if __name__ == '__main__':
    run()
