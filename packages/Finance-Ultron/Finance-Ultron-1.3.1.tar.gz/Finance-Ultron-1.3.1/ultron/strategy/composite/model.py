# -*- coding: utf-8 -*-
import pandas as pd
from ultron.optimize.model.loader import load_model


class Model(object):

    @classmethod
    def general(cls, factors_data, factors_columns, model_desc, **kwargs):
        return cls().calculate_result(factors_data=factors_data,
                                      factors_columns=factors_columns,
                                      model_desc=model_desc,
                                      **kwargs)

    def calculate_result(self, factors_data, factors_columns, model_desc,
                         **kwargs):
        name = 'factor' if 'name' not in kwargs else kwargs['name']
        model = load_model(model_desc)
        factor = model.predict(factors_data[factors_columns])
        factor = pd.DataFrame(factor.flatten(),
                              index=factors_data.set_index(
                                  ['trade_date', 'code']).index,
                              columns=[name])
        return factor