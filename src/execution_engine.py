from binance.client import Client

class ExecutionEngine:

    def __init__(self, api_key, api_secret):

        self.client = Client(api_key, api_secret)

    def get_price(self, symbol):

        ticker = self.client.get_symbol_ticker(symbol=symbol)
        return float(ticker['price'])

    def place_order(self, symbol, side, quantity):

        order = self.client.order_market(
            symbol=symbol,
            side=side,
            quantity=quantity
        )

        return order
    