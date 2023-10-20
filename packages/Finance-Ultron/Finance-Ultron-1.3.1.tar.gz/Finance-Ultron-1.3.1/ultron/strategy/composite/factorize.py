# -*- coding: utf-8 -*-
import pdb
import pandas as pd
from ultron.factor.combine.combine_engine import CombineEngine


class Factorize(object):

    @classmethod
    def general(cls, factors_data, factors_columns, technique, **kwargs):
        return cls().calculate_result(factors_data=factors_data,
                                      factors_columns=factors_columns,
                                      technique=technique,
                                      **kwargs)

    def calculate_result(self, factors_data, factors_columns, technique,
                         **kwargs):
        name = 'factor' if 'name' not in kwargs else kwargs['name']
        if technique == 'equal':
            equal_combine = CombineEngine.create_engine('equal_combine')
            factors_df = factors_data.copy()
            equal_data = equal_combine(factors_df, factors_columns)
            return pd.DataFrame(equal_data,
                                index=factors_df.set_index(
                                    ['trade_date', 'code']).index,
                                columns=[name])

        elif technique == 'ic_equal':
            span = 3 if 'span' not in kwargs else kwargs['span']
            hist_ic_combine = CombineEngine.create_engine('hist_ic_combine')
            factors_df = factors_data.copy()
            ic_equal, _ = hist_ic_combine(
                factors_df[['trade_date', 'code'] + factors_columns],
                factors_df[['trade_date', 'code', 'nxt1_ret']],
                factors_columns,
                span=span,
                method='equal')
            ic_equal.rename(columns={'combine': name}, inplace=True)
            return ic_equal

        elif technique == 'max_ic':
            span = 3 if 'span' not in kwargs else kwargs['span']
            method = 'sample' if 'sample' not in kwargs else kwargs['method']
            weight_limit = True if 'weight_limit' not in kwargs else kwargs[
                'weight_limit']
            max_ic_combine = CombineEngine.create_engine('max_ic_combine')
            factors_df = factors_data.copy()
            ir_df, hist_ic = max_ic_combine(
                factors_df[['trade_date', 'code'] + factors_columns],
                factors_df[['trade_date', 'code', 'nxt1_ret']],
                factors_columns,
                span=span,
                method=method,
                weight_limit=weight_limit)
            ir_df.rename(columns={'combine': name}, inplace=True)
            return ir_df