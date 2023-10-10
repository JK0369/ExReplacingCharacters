from typing import Iterable

import numpy as np
import pandas as pd
import scipy.stats as stats
from datetime import datetime, timedelta

from numpy import ndarray

import candle


# public

## 사용하는쪽(포지션이 없을때): true(진입) vs false(loop)
def should_entry_position(
        btc_candles: candle.Candles,
        eth_candles: candle.Candles,
        COUNT_OF_CANDLES: int = 70
) -> bool:
    # 거래량 비교: can_entry_volume
    now_volume = btc_candles.get_now_volume()
    previous_volumes = btc_candles.get_previous_volume()
    avg_volume = _get_filtered_zscore_mean(values=previous_volumes, COUNT_OF_CANDLES=COUNT_OF_CANDLES)
    can_entry_volume = _can_entry_volume(now_volume=now_volume, avg_volume=avg_volume)

    # 캔들 비교: 이전 5분봉도 현재 캔들 봉과 양봉 or 음봉 동일

    # 현재 변동률이 수익을 얻기 쉬운 구간인지 확인

    return can_entry_volume

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
    return avg_volume * 3 <= now_volume

## 이전 5분봉도 현재 캔들 봉과 양봉, 음봉 동일?
# TODO:

## 현재 이더리움 변동률이 수익 구간?
# TODO: