# {'orderId': 8389765621363230614, 'symbol': 'ETHUSDT', 'status': 'NEW', 'clientOrderId': 'Xud6KNLffu3pMeHVWUIY5O', 'price': '517.77', 'avgPrice': '0.00', 'origQty': '0.360', 'executedQty': '0.000', 'cumQty': '0.000', 'cumQuote': '0.00000', 'timeInForce': 'GTC', 'type': 'LIMIT', 'reduceOnly': False, 'closePosition': False, 'side': 'BUY', 'positionSide': 'BOTH', 'stopPrice': '0.00', 'workingType': 'CONTRACT_PRICE', 'priceProtect': False, 'origType': 'LIMIT', 'priceMatch': 'NONE', 'selfTradePreventionMode': 'NONE', 'goodTillDate': 0, 'updateTime': 1697355326343}
import position
from enum import Enum

class Status(Enum):
    NEW = 0
    PARTIALLY_FILLED = 1
    FILLED = 2
    CANCELED = 3
    REJECTED = 4
    EXPIRED = 5

class OrderInfo:
    def __init__(self, data):
        self.orderId = data['orderId']
        self.symbol = data['symbol']

        status_data = data['status']
        if status_data == 'NEW':
            self.status = Status.NEW
        elif status_data == 'PARTIALLY_FILLED':
            self.status = Status.PARTIALLY_FILLED
        elif status_data == 'FILLED':
            self.status = Status.FILLED
        elif status_data == 'CANCELED':
            self.status = Status.CANCELED
        elif status_data == 'REJECTED':
            self.status = Status.REJECTED
        else:
            self.status = Status.EXPIRED


        self.clientOrderId = data['clientOrderId']
        self.price = data['price']
        self.avgPrice = data['avgPrice']
        self.origQty = data['origQty']
        self.executedQty = data['executedQty']
        self.cumQuote = data['cumQuote']
        self.timeInForce = data['timeInForce']
        self.type = data['type']
        self.reduceOnly = data['reduceOnly']
        self.closePosition = data['closePosition']
        self.side = data['side']
        self.positionSide = data['positionSide']
        self.stopPrice = data['stopPrice']
        self.workingType = data['workingType']
        self.priceProtect = data['priceProtect']
        self.origType = data['origType']
        self.priceMatch = data['priceMatch']
        self.selfTradePreventionMode = data['selfTradePreventionMode']
        self.goodTillDate = data['goodTillDate']
        self.updateTime = data['updateTime']

    def __str__(self):
        return f"주문 ID: {self.orderId}\n심볼: {self.symbol}\n상태: {self.status}\n가격: {self.price}\n" \
               f"평균 가격: {self.avgPrice}\n원래 수량: {self.origQty}\n실행된 수량: {self.executedQty}\n" \
               f"누적 금액: {self.cumQuote}\n유효 기간: {self.timeInForce}\n주문 유형: {self.type}\n" \
               f"주문 취소 가능 여부: {self.reduceOnly}\n포지션 종료 여부: {self.closePosition}\n" \
               f"매매 방향: {self.side}\n포지션 종류: {self.positionSide}\n중지 가격: {self.stopPrice}\n" \
               f"작동 유형: {self.workingType}\n가격 일치: {self.priceMatch}\n" \
               f"자체 거래 방지 모드: {self.selfTradePreventionMode}\n만료 날짜: {self.goodTillDate}\n" \
               f"가격 보호 여부: {self.priceProtect}\n원래 유형: {self.origType}\n" \
               f"업데이트 시간: {self.updateTime}"

# data = {
#     'orderId': 8389765621363230614,
#     'symbol': 'ETHUSDT',
#     'status': 'CANCELED',
#     'clientOrderId': 'Xud6KNLffu3pMeHVWUIY5O',
#     'price': '517.77',
#     'avgPrice': '0.00000',
#     'origQty': '0.360',
#     'executedQty': '0',
#     'cumQuote': '0',
#     'timeInForce': 'GTC',
#     'type': 'LIMIT',
#     'reduceOnly': False,
#     'closePosition': False,
#     'side': 'BUY',
#     'positionSide': 'BOTH',
#     'stopPrice': '0',
#     'workingType': 'CONTRACT_PRICE',
#     'priceMatch': 'NONE',
#     'selfTradePreventionMode': 'NONE',
#     'goodTillDate': 0,
#     'priceProtect': False,
#     'origType': 'LIMIT',
#     'time': 1697355326343,
#     'updateTime': 1697355341690
# }