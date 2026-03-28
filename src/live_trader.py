import time

class LiveTrader:

    def __init__(self, model, execution_engine, symbol):

        self.model = model
        self.execution = execution_engine
        self.symbol = symbol

        self.position = 0

    def run(self):

        while True:

            price = self.execution.get_price(self.symbol)

            #  you can replace this with real-time spread logic
            signal = self.model.generate_signal(price)

            # ENTRY
            if signal == 1 and self.position == 0:
                self.execution.place_order(self.symbol, "BUY", 0.01)
                self.position = 1

            elif signal == -1 and self.position == 0:
                self.execution.place_order(self.symbol, "SELL", 0.01)
                self.position = -1

            # EXIT
            elif signal == 0 and self.position != 0:
                side = "SELL" if self.position == 1 else "BUY"
                self.execution.place_order(self.symbol, side, 0.01)
                self.position = 0

            time.sleep(5)  # run every 5 sec
