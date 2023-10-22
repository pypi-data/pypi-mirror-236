from typing import Dict
from .indicators import Indicator
from warnings import warn
import numpy as np
from functools import wraps

class Score:
    """
    打分标准
    """

    def __init__(self, indicator: Indicator, strategy: str) -> None:
        self.indcator = indicator
        self.strategy = strategy
    
    def check(func):
        '''
        return None or the result.
        '''
        @wraps(func)
        def wrapper(self,*args, **kwargs):
            if self.indcator.isvalid==False:
                return np.nan
            result = func(self,*args, **kwargs)
            return result
        return wrapper

    def score(self, value, threshold, ascending=False, maxscore=None, interval=1):
        """打分器"""
        if maxscore is None:
            maxscore = len(threshold)

        for t in threshold:
            # threshold降序(越大越好) 升序(越小越好)
            if ((not ascending) and (value >= t)) or (ascending and value <= t):
                return maxscore-threshold.index(t)*interval
        return 0.0

    @property
    @check
    def return_(self) -> float:
        """绝对收益得分"""
        thresholds: Dict = {"股票多头": [0.25, 0.2, 0.15, 0.1, 0.05,0.0],
                            "股票多空": [0.25, 0.2, 0.15, 0.1, 0.05,0.0],

                            "市场中性": [0.15, 0.12, 0.08, 0.05, 0.0],
                            "债券策略": [0.15, 0.12, 0.08, 0.05, 0.0],
                            "套利策略": [0.15, 0.12, 0.08, 0.05, 0.0],

                            "CTA策略": [0.2, 0.16, 0.12, 0.08, 0.0],
                            "复合策略": [0.2, 0.16, 0.12, 0.08, 0.0],
                            "其他": [0.2, 0.16, 0.12, 0.08, 0.0],
                            }

        threshold = thresholds.get(self.strategy, thresholds["股票多头"])
        ret = self.indcator.annulized_return

        return self.score(ret, threshold,maxscore=30,interval=5)

    @property
    @check    
    def excessreturn(self) -> float:
        """相对收益得分"""
        thresholds: Dict = {"股票多头": [0.2, 0.15, 0.1, 0.05, 0.0],
                            "股票多空": [0.2, 0.15, 0.1, 0.05, 0.0],

                            "市场中性": [0.1, 0.06, 0.03, 0.0],
                            "债券策略": [0.1, 0.06, 0.03, 0.0],
                            "套利策略": [0.1, 0.06, 0.03, 0.0],

                            "CTA策略": [0.15, 0.1, 0.05, 0.0],
                            "复合策略": [0.15, 0.1, 0.05, 0.0],
                            "其他": [0.15, 0.1, 0.05, 0.0],
                            }

        threshold = thresholds.get(self.strategy, thresholds["股票多头"])
        
        excess_return = self.indcator.annulized_excess_return
        if self.strategy == "股票多头":
            return self.score(excess_return, threshold,maxscore=20,interval=4)
        else:
            return self.score(excess_return, threshold,maxscore=20,interval=5)

    @property
    @check    
    def relative_drawdown(self) -> float:
        """相对回撤得分"""
        thresholds: Dict = {"股票多头": [-0.05, 0.0, 0.05, 0.08, 0.12],
                            "股票多空": [-0.05, 0.0, 0.05, 0.08, 0.12],

                            "市场中性": [0.0, 0.02, 0.04, 0.06, 0.08],
                            "债券策略": [0.0, 0.02, 0.04, 0.06, 0.08],
                            "套利策略": [0.0, 0.02, 0.04, 0.06, 0.08],

                            "CTA策略": [-0.03, 0.0, 0.03, 0.06, 0.1],
                            "复合策略": [-0.03, 0.0, 0.03, 0.06, 0.1],
                            "其他": [-0.03, 0.0, 0.03, 0.06, 0.1],
                            }
        threshold = thresholds.get(self.strategy, thresholds["股票多头"])

        relative_dd = self.indcator.relative_drawdown
        return self.score(relative_dd, threshold, ascending=True,maxscore=20,interval=4)

    @property
    @check    
    def sharpe(self) -> float:
        """夏普比率得分"""
        threshold = [2, 1.5, 1.2, 1, 0]
        sharpe = self.indcator.sharpe()

        return self.score(sharpe, threshold,maxscore=10,interval=2)

    @property
    @check    
    def sortino(self) -> float:
        """索提诺比率得分"""
        threshold = [2, 1.5, 1.2, 1, 0]
        sortino = self.indcator.sortino()

        return self.score(sortino, threshold,maxscore=10,interval=2)

    @property
    @check    
    def ir(self) -> float:
        """信息比率得分"""
        threshold = [1, 0.75, 0.5, 0.25, 0]
        ir = self.indcator.ir
        
        return self.score(ir, threshold,maxscore=10,interval=2)
