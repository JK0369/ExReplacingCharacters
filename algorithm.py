from typing import Iterable

import numpy as np
import scipy.stats as stats

from numpy import ndarray

import candle
import config


# public

## 사용하는쪽(포지션이 없을때): true(진입) vs false(loop)
def should_entry_position(
        btc_candles: candle.Candles,
        eth_candles: candle.Candles
) -> bool:
    # 거래량 비교: can_entry_volume
    now_volume = btc_candles.get_now_volume()
    previous_volumes = btc_candles.get_previous_volumes()
    avg_volume = _get_filtered_zscore_mean(values=previous_volumes, COUNT_OF_CANDLES=config.COUNT_OF_CANDLES)
    can_entry_volume = _can_entry_volume(now_volume=now_volume, avg_volume=avg_volume)

    # 캔들 비교: 이전 5분봉도 현재 캔들 봉과 양봉 or 음봉 동일
    same_candle_now_and_previous = btc_candles.is_same_candle_now_and_previous()

    # 최근 3개 이더리움 캔들 변동률이 수익 구간?
    is_over_profit_ratio = _is_over_profit_ratio(candles=eth_candles, count_of_candles=3)

    # TODO: 5분봉 7개 이전에도 한번 거래량이 터져있어야함 + 그 터진 거래량 시점보다 더 떨어진 경우 진입

    return can_entry_volume and same_candle_now_and_previous and is_over_profit_ratio

# (is_buy, quantity, price)
def get_entry_position(
        candles: candle.Candles,
        usdt_balance: float,
        leverage: float
) -> (bool, float, float):
    # buy인지 sell인지 구분
    is_buy = not candles.get_now_candle_is_plus()

    cur_price = candles.get_now_close()
    investment_amount = usdt_balance * config.FRACTION_RATIO # 투자 금액 계산
    margin = investment_amount * leverage # 레버리지 적용한 마진 계산
    quantity = margin / cur_price

    # price 계산
    # 지정가로 팔것이기 때문에, is_buy이면 현재 가격보다 훨씬 낮게 처리 (3배 곱해주기)
    multiplier = cur_price * config.LIMIT_MULTIPLIER if is_buy else 1/config.LIMIT_MULTIPLIER
    price = cur_price * multiplier

    return is_buy, quantity, price


## 사용하는쪽(포지션이 있을때): 순환매 vs 익절 vs 손절 vs loop
def should_sunhwan_mae() -> bool:
    return True


def should_take_profit() -> bool:
    return True


def should_stop_loss() -> bool:
    # TODO: - 물렸을때 대부분 내 물량이 많이 들어갔을때 하루정도 다음날이면
    ## 복구하는 경우가 많음 -> 하루 ~ 이틀정도 지켜보기
    return True


def is_profit() -> bool:
    # TODO:
    return True


# private

## 평균 * 3 보다\n현재 캔들 거래량이 큰가?
def _get_zscores(values: list) -> ndarray | Iterable | int | float:
    np_previous_volumes = np.array(values)
    return stats.zscore(np_previous_volumes)


def _get_filtered_zscore_mean(values: list, COUNT_OF_CANDLES: int, ZSCORE_FILTER_CONST: int = 1) -> float:
    z_scores = _get_zscores(values)

    # 걸러낸 값들 중 70개 캔들 거래량 평균값 계산
    filtered_values = np.array([])
    for i, x in enumerate(values):
        if abs(z_scores[i]) < ZSCORE_FILTER_CONST:
            filtered_values = np.append(filtered_values, x)

    return filtered_values.mean()


def _can_entry_volume(now_volume: float, avg_volume: float) -> bool:
    return avg_volume * config.OVER_MULTIPLIER_VOLUME <= now_volume


def _is_over_profit_ratio(candles: candle.Candles, count_of_candles: int) -> bool:
    total_variable_ratio = 0

    for i in range(1, count_of_candles):
        open = candles.opens[i]
        close = candles.closes[i]
        total_variable_ratio += abs((open - close) / open)

    total_variable_ratio /= count_of_candles

    return config.LEVERAGE * config.FEE <= total_variable_ratio
