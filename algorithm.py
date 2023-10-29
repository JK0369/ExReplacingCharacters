from typing import Iterable

import numpy as np
import scipy.stats as stats

from numpy import ndarray

import candle
import config
import db
import entry
import position
import trade_history
import utils


# public

## 사용하는쪽(포지션이 없을때): true(진입) vs false(loop)
def should_entry_position(
        btc_candles: candle.Candles,
        target_candles: candle.Candles
) -> bool:
    is_현재_거래량_터짐 = _is_now_거래량_터짐(candles=btc_candles)

    # 캔들 비교: 이전 5분봉도 현재 캔들 봉과 양봉 or 음봉 동일
    same_candle_now_and_previous = btc_candles.is_same_candle_now_and_previous()

    # 5분봉3틱
    if not btc_candles.is_5분봉_3틱():
        return False

    # 꼬리가 나오지 않았으면 pass
    if not btc_candles.get_is_now_candle_꼬리_생김():
        return False

    # 수익구간이어야함
    if not btc_candles._is_now_candle_변동률이_수익구간():
        return False

    return is_현재_거래량_터짐 and same_candle_now_and_previous

# 진입할 때 양 획득 (quantity)
def get_entry_position_at_firsttime(
        candles: candle.Candles,
        usdt_balance: float
) -> float:
    cur_price = candles.get_now_close()
    investment_amount = usdt_balance * config.FRACTION_RATIO  # 투자 금액 계산
    margin = investment_amount * config.LEVERAGE  # 레버리지 적용한 마진 계산
    quantity = margin / cur_price
    return quantity


# 진입 양 획득 (quantity)
def get_entry_quantity(entered_usdt: float, total_usdt: float, cur_target_coin_price: float) -> float:
    ## 4개의 구간
    # 현재 진입한 양을 기준으로 계산
    # 0: break
    # 0초과 ~ 2/45 이하: 1/45 매수
    # 0/45 초과 ~ 7/45 이하: 2/45 매수
    # 7/45 초과 ~ 17/45 이하: 4/45 매수
    # 21/45 초과 ~ 37/45 이하: 8/45 매수
    # 37/45 초과: 익절 or 손절

    entry_ratio = entered_usdt / total_usdt

    # step
    s1 = 0
    s2 = (2 / config.FRACTION_RATIO)
    s3 = (7 / config.FRACTION_RATIO)
    s4 = (21 / config.FRACTION_RATIO)
    s5 = (37 / config.FRACTION_RATIO)

    # 포지션 최대 크기 = 가용 잔고(USDT) / 현재 이더 가격 * 레버리지
    remaining_usdt = total_usdt - entered_usdt
    max_position = remaining_usdt / cur_target_coin_price * config.LEVERAGE

    if 0 == entry_ratio:
        return max_position * config.FRACTION_RATIO
    elif s1 < entry_ratio <= s2:
        return max_position * 1 * config.FRACTION_RATIO
    elif s2 < entry_ratio <= s3:
        return max_position * 2 * config.FRACTION_RATIO
    elif s3 < entry_ratio <= s4:
        return max_position * 4 * config.FRACTION_RATIO
    elif s4 < entry_ratio <= s5:
        return max_position * 8 * config.FRACTION_RATIO
    else:
        return 0


# buy, sell 여부 (True이면 롱자리, False이면 숏자리)
def get_should_entry_long_position(candles: candle.Candles) -> bool:
    return not candles.get_now_candle_is_plus()


def get_limit_price(candles: candle.Candles, should_long: bool) -> float:
    cur_price = candles.get_now_close()
    return cur_price * (1 + config.LIMIT_RATIO) if should_long else cur_price * (1 - config.LIMIT_RATIO)


def get_entry_category(
        position_info: position.Info,
        trade_history_list: list[trade_history.Trade],
        candles: candle.Candles,
        total_usdt_balance: float
) -> entry.Category:
    # 히스토리를 분석하여 반털지, 물탈지 등을 판단

    if _should_익절(position_info.roi_ratio, candles):
        return entry.Category.익절
    elif _should_반털(position_info, trade_history_list, total_usdt_balance):
        return entry.Category.반털
    elif _should_물타기(candles, position_info, trade_history_list, candles.get_now_candle_is_plus()):
        return entry.Category.물타기
    elif _should_손절(position_info, trade_history_list):
        return entry.Category.손절
    else:
        return entry.Category.대기


def _should_익절(roi_ratio: float, candles: candle.Candles) -> bool:
    # 5% 이상 수익중인 경우
    # 횡보하고 있는 경우 (어디로 갈지 모르니 바로 털기)
    if 5 < roi_ratio:
        return True
    elif 2 < roi_ratio and _get_is_횡보(candles):
        return True
    else:
        return False


# 반털
def _should_반털(position_info: position.Info, trade_history_list: list[trade_history.Trade],
               total_usdt_balance) -> bool:
    roi_ratio = position_info.roi_ratio

    # 수익구간이어야함
    if not 0 < roi_ratio:
        return False

    # 수수료 포함하여 계산했을때 수익이 나야함
    if not config.LEVERAGE * db.fee_ratio * 2 < roi_ratio:
        return False

    # 내 포지션이 현재 많이 진입해있고 캔들이 손실 구간 갔다가 다시 이득구간 올라온 경우 반털해야함
    ## 1시간이 지났고, 아직 내 물량이 5/45 넘게 남아있는 경우 반털 필수
    over_1hour = utils.get_is_over_time_from_now(target_minute=60)
    if over_1hour and (total_usdt_balance * config.반털_거래량_기준_FRACTION_RATIO) < position_info.position_amt:
        return True

    # 최근에 포지션을 정리하여 이득을 봤으면 pass
    latest_trade = trade_history_list[0]
    if not latest_trade.is_add_position and 0 < latest_trade.realized_pnl:
        return False

    # 현재 진입 물량이 내 전체 물량의 5/45 이하이면 skip
    if position_info.position_amt <= (total_usdt_balance * config.반털_거래량_기준_FRACTION_RATIO):
        return False

    return True


def _should_물타기(candles: candle.Candles, position_info: position.Info,
                trade_history_list: list[trade_history.Trade],
                is_now_candle_plus: bool) -> bool:
    roi_ratio = position_info.roi_ratio

    if not roi_ratio < 0:
        return False

    # 1. 이전 진입 포지션에 비하여 많이 빠진 경우
    index = trade_history.get_index_at_latest_position(trade_history_list)
    now_price = candles.get_now_close()
    latest_trade_price = trade_history_list[index].price
    target_diff = abs(latest_trade_price - now_price)

    ## 변동률 기준: 12개 캔들의 diff보다 큰 경우
    ### zscore를 이용하여 1시간(5분봉 12개) 캔들 diff (high - low) 획득
    diffs = [high - low for high, low in zip(candles.highs[0:11], candles.lows[0:11])]
    price_mean = _get_filtered_zscore_mean(values=diffs)

    if not price_mean < target_diff:
        return False

    # 2. 순간적으로 많이 빠진 경우 (거래량 터진경우)
    if not _is_now_거래량_터짐(candles=candles):
        return False

    # 3. 꼬리가 생기지 않으면 pass
    if not candles.get_is_now_candle_꼬리_생김():
        return False

    return True


def _should_손절(position_info: position.Info, trade_history_list: list[trade_history.Trade]) -> bool:
    roi_ratio = position_info.roi_ratio
    # TODO:
    ## 물렸을때 대부분 내 물량이 많이 들어갔을때 하루정도 다음날이면
    ## 복구하는 경우가 많음 -> 하루 ~ 이틀정도 지켜보기
    ## 1. 내가 물타기 한 시점 파악 -> 3일 전이면 pass

    ## 2. 진입한 물량이 많이 들어가지 않았으면 pass

    ## 3. 반털 구간에서 멀지 않은 경우 pass

    if not roi_ratio < 0:
        return False

    return False


def _get_is_횡보(candles: candle.Candles) -> bool:
    # 횡보로직: 이전 5분봉 캔들 1시간 전고 평균값이 작은 경우
    # 12개의 캔들 전고 평균값 획득
    avg_ratio = candles.get_variable_ratio(cnt=12)
    return avg_ratio < config.횡보_변동폭_기준_ratio * config.LEVERAGE


# private

## 평균 * 3 보다\n현재 캔들 거래량이 큰가?
def _get_zscores(values: list) -> ndarray | Iterable | int | float:
    np_previous_volumes = np.array(values)
    return stats.zscore(np_previous_volumes)


def _get_filtered_zscore_mean(values: list, count_of_5_minute_candles: int = config.COUNT_OF_5_MINUTE_CANDLES,
                              ZSCORE_FILTER_CONST: int = 1) -> float:
    z_scores = _get_zscores(values)

    # 걸러낸 값들 중 70개 캔들 거래량 평균값 계산
    filtered_values = np.array([])
    for i, x in enumerate(values):
        if not i <= count_of_5_minute_candles:
            break

        if abs(z_scores[i]) < ZSCORE_FILTER_CONST:
            filtered_values = np.append(filtered_values, x)

    return filtered_values.mean()


def _is_now_거래량_터짐(candles: candle.Candles) -> bool:
    previous_volumes = candles.get_previous_volumes()
    previous_candles_zscore_mean = _get_filtered_zscore_mean(values=previous_volumes)
    now_volume = candles.get_now_volume()
    return previous_candles_zscore_mean * config.OVER_MULTIPLIER_VOLUME <= now_volume