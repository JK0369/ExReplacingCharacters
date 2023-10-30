class Trade:
    def __init__(self, data):
        self.symbol = data['symbol']
        self.id = data['id']
        self.order_id = data['orderId']
        self.side = data['side']
        self.is_buy = self.side == 'BUY'
        self.price = float(data['price'])
        self.quantity = float(data['qty'])
        self.realized_pnl = float(data['realizedPnl'])
        self.margin_asset = data['marginAsset']
        self.quote_qty = float(data['quoteQty'])
        self.commission = float(data['commission'])
        self.commission_asset = data['commissionAsset']
        self.time = float(data['time'])
        self.position_side = data['positionSide']
        self.buyer = data['buyer']
        self.maker = data['maker']

        # PnL이 0이면 포지션을 더한 것
        if self.realized_pnl == 0:
            self.is_add_position = True
            self.is_long_position = self.is_buy
        else:
            self.is_add_position = False
            # PnL이 0이 아니면 포지션을 정리한 것
            ## buy이면서 PnL이 변경되었다면, short
            ## sell이면서 PnL이 변경되었다면, long
            self.is_long_position = not self.is_buy

    def __str__(self):
        return f"Trade: Symbol={self.symbol}, ID={self.id}, Order ID={self.order_id}, Side={self.side}, " \
               f"Price={self.price}, Quantity={self.quantity}, Realized PnL={self.realized_pnl}, " \
               f"Margin Asset={self.margin_asset}, Quote Qty={self.quote_qty}, Commission={self.commission}, " \
               f"Commission Asset={self.commission_asset}, Time={self.time}, Position Side={self.position_side}, " \
               f"Buyer={self.buyer}, Maker={self.maker}, is_add_position={self.is_add_position}, is_long_position={self.is_long_position}"

def get_index_at_latest_position(trades: list[Trade]) -> int:
    # 처음 포지션 진입한 인덱스 리턴
    index = -1

    for trade in trades:
        index += 1
        if trade.realized_pnl == 0:
            return index

    return index if index != -1 else 0
