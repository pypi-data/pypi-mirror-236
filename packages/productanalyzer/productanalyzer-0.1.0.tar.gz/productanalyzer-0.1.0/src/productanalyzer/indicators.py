from typing import Tuple
import numpy as np
import pandas as pd
from math import pow, sqrt
import statsmodels.api as sm
from functools import wraps

class Indicator:
    """
    计算时间序列的各项指标
    net_value 和 benchmark的index必须一致
    假设净值序列等间隔分布
    """

    def __init__(self, net_values: pd.Series, benchmark: pd.Series) -> None:
        self.net_values = net_values
        self.benchmark = benchmark.reindex(net_values.index)
        self.isvalid = self.check_valid()

    def check_valid(self):
        if self.nv_num<2:
            return False

        intervals = pd.Series(self.net_values.index).diff().dropna()
        if max(intervals)>pd.Timedelta("50d"):
            return False
        
        return True

    def check(func):
        '''
        return None or the result.
        '''
        @wraps(func)
        def wrapper(self,*args, **kwargs):
            if self.isvalid==False:
                return np.nan
            result = func(self,*args, **kwargs)
            return result
        return wrapper

    @property
    def _returns(self):
        return self.net_values.pct_change().dropna()

    @property
    def _logreturns(self):
        return (np.log(self.net_values) - np.log(self.net_values.shift(1))).dropna()
    
    @property
    def _returns_benchmark(self):
        return self.benchmark.pct_change().dropna()

    @property
    def _excess_return_arithmetic(self):
        return self._returns - self._returns_benchmark

    @property
    def _excess_return_geometric(self):
        return (1+self._returns)/(1+self._returns_benchmark) - 1
    


    @property
    def _start(self) -> pd.Timestamp:
        if self.nv_num == 0:
            return np.nan
        return self.net_values.index.min()

    @property
    def _end(self) -> pd.Timestamp:
        if self.nv_num == 0:
            return np.nan
        return self.net_values.index.max()

    @property
    @check
    def interval(self) -> float:
        """
        净值序列的横跨天数
        """
        start_dt = pd.to_datetime(self._start)
        end_dt = pd.to_datetime(self._end)
        days = (end_dt-start_dt).days
        return days

    @property
    @check
    def interval_year(self) -> float:
        """
        净值序列的横跨年数
        """
        return self.interval/365

    @property
    def nv_num(self):
        """
        净值样本数量
        """
        return len(self.net_values)

    @property
    @check
    def nv_freq(self) -> float:
        """
        净值数据频率：平均每两个净值之间的间隔天数
        周频数据应约为 7
        """
        if self.nv_num == 0:
            return 0 
        return self.interval/self.nv_num

    @property
    @check
    def nv_per_year(self) -> float:
        """
        平均每年有多少个净值数据（用于年化）
        """
        return self.nv_num/self.interval_year

    @property
    @check
    def total_return(self) -> float:
        """
        区间总收益
        """
        return self._calc_return()

    @property
    @check
    def total_benchmark_return(self) -> float:
        """
        业绩基准区间总收益
        """
        return self._calc_return(bm=True)

    @property
    @check
    def annulized_return(self) -> float:
        """区间年化收益"""
        return self._calc_return(annulized=True)

    @property
    @check
    def annulized_benchmark_return(self):
        """区间业绩基准年化收益"""
        return self._calc_return(annulized=True, bm=True)

    @property
    @check
    def annulized_excess_return(self):
        """区间简单超额年化收益"""
        return self.annulized_return-self.annulized_benchmark_return

    # @cache
    def _calc_return(self, annulized=False, bm=False):
        if not bm:
            p_series = self.net_values
        elif bm:
            p_series = self.benchmark

        if len(p_series) == 0:
            return 0

        s = p_series.iloc[0]
        e = p_series.iloc[-1]
        ret = e/s-1

        if not annulized:
            return ret

        elif annulized:
            years = self.interval_year
            if years == 0:
                return 0
            else:
                return pow(ret+1, 1/years) - 1

    @property
    @check
    def volatility(self) -> float:
        """区间波动率"""
        return self._returns.std(ddof=1)

    @property
    @check
    def annulized_volatility(self) -> float:
        """
        区间年化波动率，频率是nv_freq
        转化为年化波动率 公式:sqrt(days in year(365)/nv_freq)*vol = sqrt(days*num_nv/interval)*vol = sqrt(num_nv/year_interval)*vol
        """
        if self.nv_freq == 0:
            return 0
        return sqrt(365/self.nv_freq)*self.volatility

    @property
    @check
    def alpha(self) -> float:
        """区间年化alpha"""
        return self._calc_alphabeta[0]

    @property
    @check
    def beta(self) -> float:
        """区间beta"""
        return self._calc_alphabeta[1]

    @property
    def _calc_alphabeta(self) -> Tuple[float, float]:
        
        y = self._returns
        X = self._returns_benchmark
        
        if len(X) == 1:
            return 0,1
        
        X = sm.add_constant(X)
        mod = sm.OLS(y, X)
        res = mod.fit()
        # 区间alpha
        alpha = res.params.const
        # 年化alpha
        if alpha<-1:
            annulized_alpha = np.nan
        else:
            annulized_alpha = np.power(alpha+1, 365/self.nv_freq) - 1
        # beta
        beta = res.params.iloc[1]

        return annulized_alpha, beta

    @property
    @check
    def corr(self) -> float:
        """相关系数"""
        return self._returns.corr(self._returns_benchmark)

    # @cache
    def calc_drawdown(self, bm=False):
        if not bm:
            p_series = self.net_values
        elif bm:
            p_series = self.benchmark
        
        if len(p_series) == 0:
            return 0
        
        water_mark = p_series.cummax()
        drawdown = 1-p_series/water_mark
        return max(drawdown)

    @property
    @check
    def drawdown(self) -> float:
        """区间最大回撤"""
        return self.calc_drawdown()

    @property
    @check
    def drawdown_benchmark(self) -> float:
        """业绩基准区间最大回撤"""
        return self.calc_drawdown(bm=True)

    @property
    @check
    def relative_drawdown(self) -> float:
        """区间相对回撤"""
        return self.drawdown-self.drawdown_benchmark

    # @cache
    @check
    def sharpe(self, rf=0.015) -> float:
        """
        夏普比率
        parameters:
        rf:无风险收益率
        """
        if self.annulized_volatility == 0:
            return 0
        return (self.annulized_return-rf)/self.annulized_volatility

    @property
    @check
    def ir(self) -> float:
        """信息比率"""
        alpha, beta = self._calc_alphabeta
        exceed_return = self._returns - beta * self._returns_benchmark
        # 超额序列波动率
        std_er = exceed_return.std(ddof=1)
        # 年化超额波动率
        annulized_std_er = sqrt(365/self.nv_freq)*std_er
        # 信息比率
        if annulized_std_er == 0:
            return 0
        ir = alpha/annulized_std_er
        return ir

    @property
    @check
    def downside_deviation(self):
        ret = self._returns.copy()
        ret[ret > 0] = 0
        downside_variance = ret.pow(2).sum()/len(ret)
        downside_deviation = sqrt(downside_variance)
        return downside_deviation

    # @cache
    @check
    def sortino(self, mar=0.015) -> float:
        """
        索提诺比率
        -----------
        parameters:
        mar:minimal accepted return 要求最低回报率(目标回报率)

        note:
        下行方差 = 低于mar的return与mar之间的差值的平方/总样本数(自由度为0)
        下行标准差 = sqrt(下行方差)

        年化索提诺:(年化收益率-mar)/年化下行标准差
        """
        # TODO : mar应该对于周频数据生效，目前取0

        downside_deviation = self.downside_deviation
        if (downside_deviation == 0) or (self.nv_freq == 0):
            return 0 
        # 转化为年化下行波动率 公式：sqrt(days/avgdays_per_nv)*vol = sqrt(days*num_nv/interval)*vol = sqrt(num_nv/year_interval)*vol
        annulized_downside_deviation = sqrt(
            365/self.nv_freq)*downside_deviation

        if annulized_downside_deviation == 0:
            return 0
        return (self.annulized_return-mar)/annulized_downside_deviation
