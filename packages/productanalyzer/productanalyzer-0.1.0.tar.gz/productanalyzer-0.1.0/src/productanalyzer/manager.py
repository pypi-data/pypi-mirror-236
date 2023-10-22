from typing import Dict, List
from .product import Product
import pandas as pd

class Manager:

    def __init__(self) -> None:
        self.products: Dict[str, Product] = {}
        self.name: str = ""

    def add_product(self, prod: Product) -> None:
        self.products[prod.name] = prod

    def remove_product(self, prod_name: str) -> None:
        if prod_name in self.products:
            self.products.pop(prod_name)

    @property
    def AUM(self) -> float:
        aum = 0
        for p in self.products.values():
            aum += p.size
        return aum

    @property
    def prods_year(self) -> Dict[str, float]:
        d = {}
        for prod_name, prod in self.products.items():
            d[prod_name] = prod.years

        return d

    @property
    def prod_gt_1y(self) -> List[str]:
        return [name for name, year in self.prods_year.items() if year >= 1.0]

    def performance(self,start=None,end=None,fields=None) -> pd.DataFrame:
        """
        计算管理人在一段时间内旗下各产品的业绩表现
        fields:所需的字段
        """
        perf_series_list = []
        for product_name,product in self.products.items():
            p_performance = product.statistics(start,end,fields)               
            p_performance["name"] = product_name
            perf_series_list.append(p_performance)
        performance_df = pd.concat(perf_series_list,axis=1).T
        del perf_series_list
        return performance_df
    
    def rolling_performance(self,start_dt=None, end_dt=None, window="365d", interval='90d', fields:List[str]=None)-> pd.DataFrame:
        rollingperf_df_list = []
        for product_name,product in self.products.items():
            p_performance = product.rolling_statistics(start_dt,end_dt,window=window,interval=interval,fields=fields)               
            p_performance["name"] = product_name
            rollingperf_df_list.append(p_performance)
        performance_df = pd.concat(rollingperf_df_list)
        del rollingperf_df_list
        return performance_df

    def segment_performance(self, end_date=None, segments=None, mode="all", fields:List[str]=None)-> pd.DataFrame:
        segmentperf_df_list = []
        for product_name,product in self.products.items():
            p_performance = product.segment_statistics(end_date=end_date, segments=segments, mode=mode, fields=fields)               
            p_performance["name"] = product_name
            segmentperf_df_list.append(p_performance)
        performance_df = pd.concat(segmentperf_df_list)
        del segmentperf_df_list
        return performance_df

    def score(self,start=None,end=None,fields=None):
        """
        计算管理人在一段时间内旗下各产品的得分情况
        fields:所需的字段
        """
        score_series_list = []
        for product_name,product in self.products.items():
            p_score = product.score(start,end,fields)
            p_score["name"] = product_name
            score_series_list.append(p_score)
        score_df = pd.concat(score_series_list,axis=1).T
        del score_series_list
        return score_df

    def rolling_score(self,start_dt=None, end_dt=None, window="365d", interval='90d', fields:List[str]=None):
        rollingscore_df_list = []
        for product_name,product in self.products.items():
            p_score = product.rolling_score(start_dt,end_dt,window=window,interval=interval,fields=fields)               
            p_score["name"] = product_name
            rollingscore_df_list.append(p_score)
        score_df = pd.concat(rollingscore_df_list)
        del rollingscore_df_list
        return score_df

    def segment_score(self, end_date=None, segments=None, mode="all", fields:List[str]=None)-> pd.DataFrame:
        segmentscore_df_list = []
        for product_name,product in self.products.items():
            p_score = product.segment_scores(end_date=end_date, segments=segments, mode=mode, fields=fields)               
            p_score["name"] = product_name
            segmentscore_df_list.append(p_score)
        score_df = pd.concat(segmentscore_df_list)
        del segmentscore_df_list
        return score_df

    @property
    def prod_netvalues(self):
        nv_list = [p.net_values for _,p in self.products.items()]
        index=[pname for pname,_ in self.products.items()]
        return pd.DataFrame(nv_list,index=index).T

