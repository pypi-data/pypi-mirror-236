import pandas as pd
from ..data.data_portal import BaseDataPortal

class SimulationEngine:
    """模拟市场
    """
    def __init__(self, trade_dates: pd.DatetimeIndex, data_portal: BaseDataPortal):
        self.trade_dates: pd.DatetimeIndex = trade_dates
        self._data_portal: BaseDataPortal = data_portal
        self.iter = iter(trade_dates)
        self.current_date: pd.Timestamp = None
        self.spot_prices: pd.Series = None
    
    def on_session_start(self):
        self._next()

    def _next(self):
        self.current_date = next(self.iter)
        self.spot_prices = self._data_portal.prices.loc[self.current_date] #TODO: 索引改进, 目前会消耗200ms