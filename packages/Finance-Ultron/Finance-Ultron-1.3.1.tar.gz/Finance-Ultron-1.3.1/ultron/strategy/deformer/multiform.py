# -*- coding: utf-8 -*-
import pdb, hashlib, json
import pandas as pd
from ultron.strategy.experimental.single_factor import SingleFactor
from ultron.strategy.deformer.base import create_model_base
from ultron.strategy.composite.processing import Processing
from ultron.utilities.logger import kd_logger
from ultron.kdutils.create_id import create_id
from ultron.tradingday import *


class Multiform(create_model_base()):

    def __init__(self, features=None, **kwargs):
        super().__init__(features=features, **kwargs)
        self.id = None

    def _create_id(self):
        if self.id is None:
            s = hashlib.md5(json.dumps(
                self.kwargs).encode(encoding="utf-8")).hexdigest()
            self.id = "{0}".format(create_id(original=s, digit=10))
        return self.id

    def predict(self, x: pd.DataFrame, returns, **kwargs):
        kd_logger.info("predict multi dimension data")
        model_name_parts = set(self.model_name.split('.'))
        if 'combine' in model_name_parts:
            return self.impl.predict(
                x,
                returns=returns).rename(columns={'combine': self._create_id()})
        elif 'model' in model_name_parts:
            index = x.set_index(['trade_date', 'code']).index
            data = pd.DataFrame(self.impl.predict(x).flatten(),
                                index=index,
                                columns=[self._create_id()])
            data.reset_index(inplace=True)
            return data

    def rolling(self, x: pd.DataFrame, **kwargs):
        kd_logger.info("rolling {0} data".format(self.kwargs['window']))
        processing = Processing()
        return processing.rolling_standard(x, self.kwargs['window'],
                                           [self._create_id()])

    def weekday(self, x: pd.DataFrame, returns, **kwargs):
        kd_logger.info("weekday {0} data".format(self.kwargs['weekday']))
        dates = makeSchedule(x.trade_date.min(), x.trade_date.max(), '1b',
                             'china.sse', BizDayConventions.Preceding)
        if self.kwargs['weekday'] > 0:
            dates = [
                d for d in dates if d.weekday() == (self.kwargs['weekday'] - 1)
            ]
        x = x.set_index('trade_date').loc[dates].reset_index()

        sf = SingleFactor(factor_data=None,
                          market_data=None,
                          codes=None,
                          columns=None)

        period_data = sf._transformer(normalize_data=x,
                                      returns=returns.copy(),
                                      columns=[self._create_id()],
                                      period='1b')
        period_data['trade_date'] = pd.to_datetime(period_data['trade_date'])
        return period_data

    def signal(self, x: pd.DataFrame, returns, **kwargs):
        kd_logger.info("into  {0} signal data".format(self.kwargs['bins']))
        processing = Processing()
        return processing.to_signal(x,
                                    returns,
                                    self._create_id(),
                                    bins=self.kwargs['bins'])

    def calculate_result(self, x: pd.DataFrame, returns, **kwargs):
        combine_data = self.predict(x=x, returns=returns)
        rolling_data = self.rolling(x=combine_data)
        weekday_data = self.weekday(x=rolling_data, returns=returns)
        signal_data = self.signal(x=weekday_data, returns=returns)
        return signal_data['signal'].reset_index()
