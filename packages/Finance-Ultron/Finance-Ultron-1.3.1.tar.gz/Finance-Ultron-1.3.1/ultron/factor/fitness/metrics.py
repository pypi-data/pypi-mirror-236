# -*- encoding:utf-8 -*-
"""
    横截面下因子评估方式--因子绩效
"""
import copy, functools, pdb
import numpy as np
import pandas as pd
from scipy.stats import norm
from collections import namedtuple
from ultron.utilities.logger import kd_logger
from ultron.kdutils.progress import Progress

DALIY_PER_YEAR = 252
WEEKLY_PER_YEAR = 52
MONTHLY_PER_YEAR = 12
QUARTERLY_PER_YEAR = 4
YEARLY_PER_YEAR = 1

OLNY_LONG = 'long'
OLNY_SHORT = 'short'
BOTH_SIDE = 'both'

POSITIVE = 1
NEGATIVE = -1

EXCESS = 1
ABSOLUTE = -1


class EvaluateTuple(
        namedtuple(
            'EvaluateTuple',
            ('returns_mean', 'returns_std', 'sharp', 'turnover', 'maxdd',
             'returns_mdd', 'win_rate', 'ic', 'ir', 'fitness', 'category',
             'count_series', 'returns_series', 'ic_series', 'turnover_series'))
):

    __slots__ = ()

    def __repr__(self):
        return "\nreturns_mean:{}\nreturns_std:{}\nsharp:{}\nturnover:{}\n" \
                "maxdd:{}\nreturns_mdd:{}\nwin_rate:{}\nic:{}\nir:{}\nfitness:{}\n" \
                "category:{}".format(self.returns_mean,self.returns_std,
                    self.sharp,self.turnover,self.maxdd,self.returns_mdd,self.win_rate,
                    self.ic,self.ir,self.fitness,self.category)


class MetricsTuple(
        namedtuple('EvaluateTuple',
                   ('long_evaluate', 'short_evaluate', 'both_evaluate', 'hold',
                    'freq', 'direction', 'category'))):
    __slots__ = ()

    def __repr__(self):
        return "long_evaluate:{}\nshort_evaluate:{}\nboth_evaluate:{},\nhold:{},freq:{},direction:{},category:{}".format(
            self.long_evaluate, self.short_evaluate, self.both_evaluate,
            self.hold, self.freq, self.direction, self.category)


def valid_check(func):
    """检测度量的输入是否正常，非正常显示info，正常继续执行被装饰方法"""

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.valid:
            return func(self, *args, **kwargs)
        else:
            kd_logger.info('metrics input is invalid or zero order gen!')

    return wrapper


class Metrics(object):

    @classmethod
    def general(cls,
                returns,
                factors,
                hold=1,
                skip=0,
                dummy=None,
                freq=DALIY_PER_YEAR,
                show_log=True,
                is_series=False):
        metrics = cls(returns=returns,
                      factors=factors,
                      hold=hold,
                      freq=freq,
                      skip=skip,
                      dummy=dummy,
                      show_log=show_log,
                      is_series=is_series)
        return metrics.fit_metrics()

    def __init__(
            self,
            returns,
            factors,
            hold=1,
            category=EXCESS,
            freq=DALIY_PER_YEAR,
            dummy=None,
            skip=0,  #今天出信号，过skip天再假意
            show_log=True,
            is_series=False,
            method='max'):
        # 验证输入的数据是否可度量，便于valid_check装饰器工作
        self.valid = False
        self.category = category
        self.dummy = dummy
        self.skip = skip
        #self.returns = returns.sub(returns.mean(
        #    axis=1), axis='rows') if self.category == EXCESS else returns
        self.returns = self.yields(returns)
        self.factors = self.score(factors, method)
        self.freq = freq
        self.hold = hold
        self.direction = None
        self.show_log = show_log
        self.is_series = is_series
        if self.returns is not None and self.factors is not None:
            self.valid = True

    def yields(self, returns):
        returns = returns * self.dummy if self.dummy is not None else returns
        returns = returns.shift(-self.skip)
        returns = np.exp(returns) - 1
        ret_mkt_fnd = (returns * self.dummy).mean(
            axis=1) if self.dummy is not None else returns.mean(axis=1)
        return returns.sub(ret_mkt_fnd, axis='rows')

    def score(self, factors, method='std'):
        factors = factors * self.dummy if self.dummy is not None else factors
        if method == 'std':
            rank = factors.rank(axis=1, method='dense')
            score = (rank - 0.5).div(rank.max(axis=1), axis='rows') - 0.5
            return score.pow(3)
        else:
            rank = factors.rank(axis=1, method='max')
            count = rank.count(axis=1)
            rank = (rank - 3. / 8.).div(count + 1. / 4., axis='rows')
            score = pd.DataFrame(norm.ppf(rank),
                                 index=rank.index,
                                 columns=rank.columns)
            return score

    @valid_check
    def fit_metrics(self):
        with Progress(3, 0, label='factor fit metrics') as progress:
            long_weight, short_weight, both_weight = self.create_weight()
            if self.show_log: progress.show(a_progress=1)
            long_evaluate = self.evaluate(returns=self.returns,
                                          weight=long_weight,
                                          freq=self.freq,
                                          category=OLNY_LONG)
            if self.show_log: progress.show(a_progress=2)
            short_evaluate = self.evaluate(returns=self.returns,
                                           weight=short_weight,
                                           freq=self.freq,
                                           category=OLNY_SHORT)
            if self.show_log: progress.show(a_progress=3)
            both_evaluate = self.evaluate(returns=self.returns,
                                          weight=both_weight,
                                          freq=self.freq,
                                          category=BOTH_SIDE)

            self.show_log: progress.show(a_progress=4)
        return MetricsTuple(long_evaluate=long_evaluate,
                            short_evaluate=short_evaluate,
                            both_evaluate=both_evaluate,
                            freq=self.freq,
                            hold=self.hold,
                            category=self.category,
                            direction=self.direction)

    def create_weight(self):
        right_weight = copy.deepcopy(self.factors)
        right_weight[right_weight <= 0] = np.nan
        right_weight = right_weight.div(right_weight.sum(axis=1, min_count=1),
                                        axis='rows')
        right_weight = right_weight.rolling(self.hold,
                                            min_periods=1).sum() / self.hold

        left_weight = copy.deepcopy(self.factors)
        left_weight[left_weight >= 0] = np.nan
        left_weight = left_weight.div(left_weight.sum(axis=1, min_count=1),
                                      axis='rows')
        left_weight = left_weight.rolling(self.hold,
                                          min_periods=1).sum() / self.hold

        both_weight = right_weight.sub(left_weight, fill_value=0)
        ret_diff = (self.returns * right_weight).sum(
            axis=1).mean() - (self.returns * left_weight).sum(axis=1).mean()
        if ret_diff > 0:
            self.direction = POSITIVE
            long_weight = copy.deepcopy(right_weight)
            short_weight = copy.deepcopy(left_weight)
        else:
            self.direction = NEGATIVE
            long_weight = copy.deepcopy(left_weight)
            short_weight = copy.deepcopy(right_weight)
            both_weight = copy.deepcopy(-both_weight)

        return long_weight, short_weight, both_weight

    def evaluate(self,
                 returns,
                 weight,
                 freq=DALIY_PER_YEAR,
                 category=OLNY_LONG):
        #rets_sum = (returns * weight).sum(axis=1)
        rets_sum = np.log((returns * weight).sum(axis=1, min_count=1) + 1)
        rets_mean = rets_sum.mean() * freq
        rets_std = rets_sum.std() * np.sqrt(freq)
        sharp = rets_mean / rets_std
        tv_series = abs(weight.sub(weight.shift(1),
                                   fill_value=0)).sum(axis=1, min_count=1)
        tv = tv_series.mean() * 0.5
        pnl = rets_sum.cumsum()
        maxdd = (pnl.expanding().max() - pnl).max()
        ret2mdd = rets_mean / maxdd
        win_rate = rets_sum[rets_sum >
                            0].count() / rets_sum[~rets_sum.isna()].count()
        ic_series = weight.corrwith(returns, axis=1, method='spearman')
        ic = ic_series.mean()
        ir = ic / ic_series.std()
        fitness = sharp * np.sqrt(abs(rets_mean) / tv)
        returns_series = rets_sum if self.is_series else None
        ic_series = ic_series if self.is_series else None
        turnover_series = tv_series if self.is_series else None
        count_series = weight.count(axis=1) if self.is_series else None

        return EvaluateTuple(returns_mean=rets_mean,
                             returns_std=rets_std,
                             sharp=sharp,
                             turnover=tv,
                             maxdd=maxdd,
                             returns_mdd=ret2mdd,
                             win_rate=win_rate,
                             ic=ic,
                             ir=ir,
                             fitness=fitness,
                             category=category,
                             count_series=count_series,
                             returns_series=returns_series,
                             ic_series=ic_series,
                             turnover_series=turnover_series)
