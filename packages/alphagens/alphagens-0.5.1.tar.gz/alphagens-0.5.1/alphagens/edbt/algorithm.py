import tqdm
import typing
from .broker import SimulatedBroker
from .engine import SimulationEngine
from .account import Account
from .strategy import BaseStrategy

class Algorithm:
    def __init__(self, strategy_cls: typing.Type[BaseStrategy], trade_dates, data_portal, capital_base=1e6):
        self._engine = SimulationEngine(trade_dates, data_portal)
        self._broker = SimulatedBroker(self._engine)
        self._account = Account(self._engine, capital_base=1e6)

    def run_backtest(self, strategy_cls: typing.Type[BaseStrategy]):
        strategy = strategy_cls(self._engine, self._broker, self._account)
        return strategy.run_backtest()
    