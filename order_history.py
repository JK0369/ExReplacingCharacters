from datetime import datetime

class OrderHistory:
    def __init__(self, data):
        self.orderId = data['orderId']
        self.symbol = data['symbol']
        self.status = data['status']
        self.clientOrderId = data['clientOrderId']
        self.price = float(data['price'])
        self.avgPrice = float(data['avgPrice'])
        self.origQty = float(data['origQty'])
        self.executedQty = float(data['executedQty'])
        self.cumQuote = float(data['cumQuote'])
        self.timeInForce = data['timeInForce']
        self.type = data['type']
        self.reduceOnly = data['reduceOnly']
        self.closePosition = data['closePosition']
        self.side = data['side']
        self.positionSide = data['positionSide']
        self.stopPrice = float(data['stopPrice'])
        self.workingType = data['workingType']
        self.priceMatch = data['priceMatch']
        self.selfTradePreventionMode = data['selfTradePreventionMode']
        self.goodTillDate = data['goodTillDate']
        self.priceProtect = data['priceProtect']
        self.origType = data['origType']
        self.time = datetime.fromtimestamp(data['time'] / 1000.0)
        self.updateTime = data['updateTime']

    def __str__(self):
        return f"Order ID: {self.orderId}\nSymbol: {self.symbol}\nStatus: {self.status}\nClient Order ID: {self.clientOrderId}\nPrice: {self.price}\nAverage Price: {self.avgPrice}\nOriginal Quantity: {self.origQty}\nExecuted Quantity: {self.executedQty}\nCumulative Quote: {self.cumQuote}\nTime in Force: {self.timeInForce}\nType: {self.type}\nReduce Only: {self.reduceOnly}\nClose Position: {self.closePosition}\nSide: {self.side}\nPosition Side: {self.positionSide}\nStop Price: {self.stopPrice}\nWorking Type: {self.workingType}\nPrice Match: {self.priceMatch}\nSelf Trade Prevention Mode: {self.selfTradePreventionMode}\nGood Till Date: {self.goodTillDate}\nPrice Protect"

# [
#     {
#         "symbol": "BTCUSDT",
#         "orderId": 12345678,
#         "clientOrderId": "my_order_id_1",
#         "price": "60000.0",
#         "origQty": "1.0",
#         "executedQty": "0.0",
#         "cumulativeQuoteQty": "0.0",
#         "status": "NEW",
#         "timeInForce": "GTC",
#         "type": "LIMIT",
#         "side": "BUY",
#         "stopPrice": "0.0",
#         "updateTime": 1641234567890,
#         "time": 1641234567890
#     },
#     {
#         "symbol": "ETHUSDT",
#         "orderId": 12345679,
#         "clientOrderId": "my_order_id_2",
#         "price": "4000.0",
#         "origQty": "2.0",
#         "executedQty": "1.0",
#         "cumulativeQuoteQty": "4000.0",
#         "status": "PARTIALLY_FILLED",
#         "timeInForce": "GTC",
#         "type": "LIMIT",
#         "side": "SELL",
#         "stopPrice": "0.0",
#         "updateTime": 1641234567900,
#         "time": 1641234567900
#     },
#     // 다른 주문들...
# ]
