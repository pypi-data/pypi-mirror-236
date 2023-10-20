# -*- coding: utf-8 -*-

import pdb
import numpy as np
from ultron.strategy.experimental.single_factor import SingleFactor


class Processing(object):

    def __init__(self):
        self._single_factor = SingleFactor()

    def rolling_standard(self, factor_data, windows, columns):
        if windows > 1:
            normalize_data = self._single_factor.normalize(
                factor_data=factor_data.copy(),
                windows=windows,
                columns=columns)
        else:
            normalize_data = factor_data.copy()
        return normalize_data

    def to_signal(self,
                  factor_data,
                  returns_data,
                  factor_name,
                  bins,
                  direction=1):
        total_data = returns_data.merge(
            factor_data[['trade_date', 'code', factor_name]],
            on=['trade_date', 'code'])
        position = self._single_factor.quantile_v2(
            normalize_data=total_data.copy(),
            factor_name=factor_name,
            n_bins=bins)
        top_pos = 1 if direction == 1 else -1
        bottom_pos = 1 if direction == -1 else -1
        position['signal'] = np.where(
            position['group'] == bins, top_pos,
            np.where(position['group'] == 1, bottom_pos, 0))
        position.factor_name = factor_name
        return position