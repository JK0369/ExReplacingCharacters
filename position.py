import config
from enum import Enum
import datetime

import utils


class PositionType(Enum):
    NONE = 0
    LONG = 1
    SHORT = 2


class Info:
    def __init__(self, symbol, position_side, position_amt, entry_price, break_even_price, mark_price,
                 unrealized_profit, liquidation_price, leverage, max_notional_value, margin_type, isolated_margin,
                 is_auto_add_margin, notional, isolated_wallet, update_time):
        self.symbol = symbol
        self.position_amt = float(position_amt)
        self.entry_price = entry_price
        self.break_even_price = break_even_price
        self.mark_price = mark_price
        self.unrealized_profit = float(unrealized_profit)
        self.liquidation_price = liquidation_price
        self.leverage = leverage
        self.max_notional_value = max_notional_value
        self.margin_type = margin_type
        self.isolated_margin = isolated_margin
        self.is_auto_add_margin = is_auto_add_margin
        self.notional = notional
        self.isolated_wallet = isolated_wallet
        self.update_time = utils.get_ymd_time(update_time)

        if self.position_amt < 0:
            self.position_type = PositionType.SHORT
        elif 0 < self.position_amt:
            self.position_type = PositionType.LONG
        else:
            self.position_type = PositionType.NONE
        # ROI(%) = [손익 / 초기 가치] * 100 * Leverager
        if float(entry_price) == 0:
            self.roi_ratio = 0
        else:
            self.roi_ratio = (float(unrealized_profit) / float(entry_price)) * 100 * config.LEVERAGE

    @classmethod
    def from_api_response(cls, api_response):
        return cls(
            api_response['symbol'],
            api_response['positionSide'],
            api_response['positionAmt'],
            api_response['entryPrice'],
            api_response['breakEvenPrice'],
            api_response['markPrice'],
            api_response['unRealizedProfit'],
            api_response['liquidationPrice'],
            api_response['leverage'],
            api_response['maxNotionalValue'],
            api_response['marginType'],
            api_response['isolatedMargin'],
            api_response['isAutoAddMargin'],
            api_response['notional'],
            api_response['isolatedWallet'],
            api_response['updateTime']
        )

    def __str__(self):
        return f"Symbol: {self.symbol}\n" \
               f"Position Amount: {self.position_amt}\n" \
               f"Entry Price: {self.entry_price}\n" \
               f"Break Even Price: {self.break_even_price}\n" \
               f"Mark Price: {self.mark_price}\n" \
               f"Unrealized Profit: {self.unrealized_profit}\n" \
               f"Liquidation Price: {self.liquidation_price}\n" \
               f"Leverage: {self.leverage}\n" \
               f"Max Notional Value: {self.max_notional_value}\n" \
               f"Margin Type: {self.margin_type}\n" \
               f"Isolated Margin: {self.isolated_margin}\n" \
               f"Is Auto Add Margin: {self.is_auto_add_margin}\n" \
               f"Notional: {self.notional}\n" \
               f"Isolated Wallet: {self.isolated_wallet}\n" \
               f"Update Time:  {self.update_time}\n" \
               f"ROI ratio: {self.roi_ratio}%\n"

# Symbol: ETHUSDT
# Position Side: BOTH
# Position Amount: -1.000
# Entry Price: 1603.66
# Break Even Price: 1602.85817
# Mark Price: 1603.06010686
# Unrealized Profit: 0.59989314
# Liquidation Price: 2963.08489378
# Leverage: 20
# Max Notional Value: 15000000
# Margin Type: cross
# Isolated Margin: 0.00000000
# Is Auto Add Margin: false
# Notional: -1603.06010686
# Isolated Wallet: 0
# Update Time: 1697869962226
