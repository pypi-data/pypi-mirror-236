# -*- encoding:utf-8 -*-
"""
    横截面下因子评估方式--因子分组
"""
import numpy as np
import pandas as pd
import pdb, functools
from collections import namedtuple
from ultron.utilities.logger import kd_logger


class GroupTuple(namedtuple('GroupTuple', ('returns', 'state'))):
    __slots__ = ()

    def __repr__(self):
        return "\nreturns:{}\nstate:{}".format(self.returns, self.state)


def valid_check(func):
    """检测度量的输入是否正常，非正常显示info，正常继续执行被装饰方法"""

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.valid:
            return func(self, *args, **kwargs)
        else:
            kd_logger.info('metrics input is invalid or zero order gen!')

    return wrapper


class Group(object):

    @classmethod
    def general(cls,
                factors,
                returns,
                group,
                dummy,
                hold=1,
                skip=0,
                checkna=True,
                show_log=True):
        return cls(factors=factors,
                   returns=returns,
                   group=group,
                   dummy=dummy,
                   hold=hold,
                   skip=skip,
                   checkna=checkna,
                   show_log=show_log).fit_group()

    def __init__(self,
                 factors,
                 returns,
                 group,
                 dummy,
                 hold=1,
                 skip=0,
                 checkna=True,
                 show_log=True):
        self.valid = False
        self.factors = factors if dummy is not None else factors * dummy
        self.dummy = dummy
        self.group = group
        self.hold = hold
        self.skip = skip
        self.returns = self.yields(returns)
        self.checkna = checkna
        if self.factors is not None and self.returns is not None:
            self.valid = True

    def yields(self, returns):
        returns = returns * self.dummy if self.dummy is not None else returns
        returns = returns.shift(-self.skip)
        returns = np.exp(returns) - 1
        ret_mkt_fnd = (returns * self.dummy).mean(
            axis=1) if self.dummy is not None else returns.mean(axis=1)
        return returns.sub(ret_mkt_fnd, axis='rows')

    @valid_check
    def fit_group(self):
        megedata = np.exp(
            np.log(self.returns + 1).rolling(self.hold, min_periods=1).sum().
            shift(-(self.hold - 1)).stack() / self.hold) - 1

        megedata = pd.concat(
            [megedata, self.factors.stack(),
             self.dummy.stack()], axis=1)

        megedata.columns = ['er_fnd', 'factor', 'dummy']
        megedata = megedata.loc[megedata.dummy == 1]
        nanframe = megedata.loc[(megedata.factor.isna())
                                & (~megedata.er_fnd.isna())]
        megedata = megedata.loc[~megedata.factor.isna()]
        megedata["quantile"] = megedata["factor"].groupby(
            level=0, group_keys=False).rank(pct=True)

        megedata["quantile"] = (megedata["quantile"] *
                                self.group).astype('int') + 1

        megedata.loc[megedata['quantile'] == self.group + 1,
                     'quantile'] = self.group

        megedata.index.names = ['trade_date', 'code']

        returns = np.log(megedata.reset_index().groupby(
            ['trade_date', 'quantile'])['er_fnd'].mean().unstack() + 1)

        returns.columns = pd.Series(
            map(lambda x: 'G' + str(x + 1), range(0, returns.shape[1])))
        if self.checkna and not nanframe.empty:
            returns['GN'] = nanframe.groupby(axis=0, level=0).er_fnd.mean()
        state = returns.mean()
        return GroupTuple(returns=returns.reset_index(), state=state)
