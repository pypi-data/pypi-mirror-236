from datetime import datetime, timedelta
from tracemalloc import start
from typing import List, Tuple
import pandas as pd
from pandas.core.dtypes.common import is_datetime64_any_dtype, is_numeric_dtype
from warnings import warn
from .indicators import Indicator
from .score import Score
from .object import TimeSerise
# from functools import cached_property, cache
from .util import truncate_timeseries

class Product:

    net_values = TimeSerise()
    benchmark = TimeSerise()

    def __init__(
        self,
        net_values: pd.Series = None,       # 产品净值序列
        benchmark: pd.Series = None,        # 业绩基准净值序列
        name: str = None,                   # 产品名称
        foundation_date: datetime = None,   # 产品创立时间
        manager: str = None,                # 基金经理
        code=None,                          # 产品创立时间
        size=None,                          # 产品规模
        strategy_type=None,                 # 策略类型
    ) -> None:
        self.name = name
        self.net_values = net_values
        self.benchmark = benchmark


        if (name is None) & (self.net_values is not None):
            self.name = self.net_values.name

        self.foundation_date = foundation_date
        if (foundation_date is None) & (self.net_values is not None):
            self.foundation_date = self.start

        self.manager = manager
        self.code = code
        self.size = size
        self.strategy_type = strategy_type

    def _validate(self):
        """
        检查业绩基准是否满足要求
        检查净值的日期是否与业绩基准对齐
        """
        if (self.net_values is not None) & (self.benchmark is not None):
            # benchmark是否需要更新
            if (self.benchmark.index.min() > self.start) | (self.benchmark.index.max() < self.end):
                del self.benchmark
                warn(f"{self.name}的benchmark的值不足以覆盖产品净值区间,已移除benchmark,请重新传入")


            # detect abnormal index
            abnormal_index = self.net_values.index[~self.net_values.index.isin(
                self.benchmark.index)]
            if len(abnormal_index) > 0:
                correction = {}
                for error_index in abnormal_index:
                    correct_index = self.benchmark.index.asof(error_index)
                    correction[error_index] = correct_index

                self.net_values.rename(correction, inplace=True)
                self.net_values = self.net_values[~self.net_values.index.duplicated(
                    keep='first')]

    @property
    def _tradedays(self):
        return self.benchmark.index

    @property
    def start(self):
        return self.net_values.index.min()

    @property
    def end(self):
        return self.net_values.index.max()

    @property
    def years(self):
        """产品存续总时长"""
        return (self.end-self.start).days/365

    # @cache
    def _truncate_product(self, start_dt:pd.Series, end_dt:pd.Series) -> Tuple[pd.Series,pd.Series]:
        sub_nv = truncate_timeseries(self.net_values,start_time=start_dt,end_time=end_dt)
        sub_bm = truncate_timeseries(self.benchmark,start_time=start_dt,end_time=end_dt)
        return (sub_nv,sub_bm)

    # @cache
    def _get_indicator(self, start_dt:pd.Series, end_dt:pd.Series) -> Indicator:
        """返回产品在某一区间内的指标"""
        nv, bm = self._truncate_product(start_dt, end_dt)
        return Indicator(nv, bm)

    # @cache
    def _get_score(self, start_dt:pd.Series, end_dt:pd.Series) -> Score:
        """返回产品在某一区间内的打分"""
        period_indicator = self._get_indicator(start_dt, end_dt)
        return Score(period_indicator, self.strategy_type)

    def _get_rollingback_periods(self, interval:str, window_size:str, wacth_point:str) -> List[Tuple[pd.Timestamp, pd.Timestamp]]:
        """
        滚动切分产品时间段
        parameters:
            interval:每次向前回溯的间隔
            window_size:每个评价期的长度,最后一个评价期会合并超出部分的净值
            wacth_point:回溯起始时间点
        return:
            List[Tuple(start_point,end_point)]
        """

        # 计算评价周期数
        interval = pd.to_timedelta(interval)
        window_size = pd.to_timedelta(window_size)
        total_duration = pd.to_timedelta(wacth_point-self.start)
        if total_duration<window_size:
            # 产品总时长不足一个评价期
            num_windows = 1
        else: 
            num_windows = int((total_duration-window_size)/interval)+1

        periods = []
        for i in range(num_windows):
            end_point = wacth_point-i*interval
            if i == num_windows-1:
                # 最后一个周期
                start_point = self.start
            else:
                start_point = end_point - window_size
            periods.append((start_point, end_point))

        return periods

    def _get_periods(self, mode:str, segments:List[int], watch_point:str) -> List[Tuple[pd.Timestamp, pd.Timestamp]]:
        """
        指定回溯的起始点和时段切分设置，获取分析需要的周期
        parameters:
            segments:切分时间点设置,
            watch_point:回溯的起始日期，
            mode:"all":获取自不同起点至今的时间段
                :"range":获取不同起点之间的时间段
        """

        starts_dt = [
            watch_point-timedelta(d) for d in segments if watch_point-timedelta(d) >= self.start]
        if mode == "all":
            ends_dt = [watch_point for _ in range(len(starts_dt))]
        elif mode == "range":
            ends_dt = starts_dt.copy()
        starts_dt.append(self.start)
        ends_dt.insert(0, watch_point)

        return list(zip(starts_dt, ends_dt))

    # 指标

    def statistics(self, start_dt=None, end_dt=None, fields:List[str]=None) -> pd.Series:
        """
        产品区间指标
        fields:
            total_return
            annulized_return
        """
        if fields is None:
            fields = ["total_return","total_benchmark_return","annulized_return","annulized_excess_return","drawdown","relative_drawdown","volatility","annulized_volatility","alpha","beta","sharpe","ir","sortino"]
        if isinstance(fields,str):
            fields = [fields]
        
        if start_dt is None:
            start_dt = self.start
        else:
            start_dt = pd.Timestamp(start_dt)

        if end_dt is None:
            end_dt = self.end
        else:
            start_dt = pd.Timestamp(start_dt)

        ind = self._get_indicator(start_dt, end_dt)

        temp_values = []
        for field in fields:
            value = getattr(ind,field)
            if callable(value):
                value = value()
            temp_values.append(value)
        temp_values.append(getattr(ind,"_start"))
        temp_values.append(getattr(ind,"_end"))
        temp_values.append(getattr(ind,"nv_num"))

        temp_values.extend([start_dt,end_dt])
        index = fields.copy()
        index.extend(["nv_start","nv_end","nv_num","start_date","end_date"])

        return pd.Series(data=temp_values,index=index)



    def rolling_statistics(self, start_dt=None, end_dt=None, window="365d", interval='1d', fields:List[str]=None) -> pd.DataFrame:
        """
        产品滚动业绩指标
        parameters:
            start_dt:滚动起始日
            end_dt:滚动终止日
            window:窗口期大小
            intervals:回滚间隔
        return:
            pd.Dataframe:
                index:datetimeindex
                values:区间收益
        """
        if start_dt == None:
            start_dt = self.start
        else:
            start_dt = pd.Timestamp(start_dt)

        if end_dt == None:
            end_dt = self.end
        else:
            end_dt = pd.to_datetime(end_dt)

        if start_dt > end_dt:
            raise ValueError("滚动起始日不能晚于终止日")

        if fields is None:
            fields = ["total_return","total_benchmark_return","annulized_return","annulized_excess_return","drawdown","relative_drawdown","volatility","annulized_volatility","alpha","beta","sharpe","ir","sortino"]
        if isinstance(fields,str):
            fields = [fields]
        
        periods = self._get_rollingback_periods(
            interval=interval,
            window_size=window,
            wacth_point=end_dt
        )

        temp = []
        for period in periods:
            if period[0] < start_dt:
                continue
            
            stats = self.statistics(period[0],period[1],fields)
            temp.append(stats)
        return pd.DataFrame(temp).set_index(["start_date","end_date"])
    
    def segment_statistics(self,end_date=None, segments=None, mode="all", fields:List[str]=None) -> pd.DataFrame:
        """
        指定终止日,按segments的时间长度进行回溯
        parameters:
            segments:切分时间点设置,默认[180, 365, 365*2, 365*3](半年,一年,2年,3年)
            end_date:回溯的起始日期，默认到最新净值(最后一个净值),
            mode:"all":获取自不同起点至今的时间段
                :"range":获取不同起点之间的时间段
            fields:需要的字段
        """
        if end_date == None:
            end_date = self.end
        else:
            end_date = pd.to_datetime(end_date)
        
        if segments is None:
            days = [180, 365, 365*2, 365*3]
        else:
            days = segments        
        if isinstance(days,int):
            days = [days]
        
        if fields is None:
            fields = ["total_return","total_benchmark_return","annulized_return","annulized_excess_return","drawdown","relative_drawdown","volatility","annulized_volatility","alpha","beta","sharpe","ir","sortino"]
        if isinstance(fields,str):
            fields = [fields]

        periods = self._get_periods(
            mode=mode,
            segments=days,
            watch_point=end_date
        )

        temp = []
        for period in periods:
            if period[0] < self.start:
                continue
            
            stats = self.statistics(period[0],period[1],fields)
            temp.append(stats)
        return pd.DataFrame(temp).set_index(["start_date","end_date"])


    def score(self,start_dt=None,end_dt=None,fields=None) -> pd.Series:
        if start_dt == None:
            start_dt = self.start
        else:
            start_dt = pd.Timestamp(start_dt)

        if end_dt == None:
            end_dt = self.end
        else:
            end_dt = pd.to_datetime(end_dt)
        
        if fields is None:
            fields = ["return_","excessreturn","relative_drawdown","sharpe","sortino","ir"]
        if isinstance(fields,str):
            fields = [fields]
        
        score = self._get_score(start_dt,end_dt)

        temp_values = []
        for field in fields:
            value = getattr(score,field)
            if callable(value):
                value = value()
            temp_values.append(value)
        
        temp_values.extend([start_dt,end_dt])
        index = fields.copy()
        index.extend(["start_date","end_date"])
        
        return pd.Series(data=temp_values,index=index)

    def rolling_score(self, start_dt=None, end_dt=None, window="365d", interval='1d', fields:List[str]=None) -> pd.DataFrame:

        if start_dt == None:
            start_dt = self.start
        else:
            start_dt = pd.Timestamp(start_dt)

        if end_dt == None:
            end_dt = self.end
        else:
            end_dt = pd.to_datetime(end_dt)

        if start_dt > end_dt:
            raise ValueError("滚动起始日不能晚于终止日")

        if fields is None:
            fields = ["return_","excessreturn","relative_drawdown","sharpe","sortino","ir"]
        if isinstance(fields,str):
            fields = [fields]
        
        periods = self._get_rollingback_periods(
            interval=interval,
            window_size=window,
            wacth_point=end_dt
        )

        temp = []
        for period in periods:
            if period[0] < start_dt:
                continue
            
            scores = self.score(period[0],period[1],fields)
            temp.append(scores)
        return pd.DataFrame(temp).set_index(["start_date","end_date"])

    def segment_scores(self,end_date=None, segments=None, mode="all", fields:List[str]=None) -> pd.DataFrame:
        """
        指定终止日,按segments的时间长度进行回溯
        parameters:
            segments:切分时间点设置,默认[180, 365, 365*2, 365*3](半年,一年,2年,3年)
            end_date:回溯的起始日期，默认到最新净值(最后一个净值),
            mode:"all":获取自不同起点至今的时间段
                :"range":获取不同起点之间的时间段
            fields:需要的字段
        """
        if end_date == None:
            end_date = self.end
        else:
            end_date = pd.to_datetime(end_date)
        
        if segments is None:
            days = [180, 365, 365*2, 365*3]
        else:
            days = segments        
        if isinstance(days,int):
            days = [days]
        
        if fields is None:
            fields = ["return_","excessreturn","relative_drawdown","sharpe","sortino","ir"]
        if isinstance(fields,str):
            fields = [fields]

        periods = self._get_periods(
            mode=mode,
            segments=days,
            watch_point=end_date
        )

        temp = []
        for period in periods:
            if period[0] < self.start:
                continue
            
            stats = self.score(period[0],period[1],fields)
            temp.append(stats)
        return pd.DataFrame(temp).set_index(["start_date","end_date"])
