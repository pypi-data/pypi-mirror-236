# -*- coding: utf-8 -*-
import abc, warnings, arrow, pdb, copy, importlib
import pandas as pd
from ultron.factor.utilities import encode
from ultron.factor.utilities import decode
from ultron.factor.data.transformer import Transformer
from ultron.factor.combine.combine_method import *


class ModelBase():

    def __init__(self, features=None, **kwargs):
        if features is not None:
            self.formulas = Transformer(features)
            self.features = self.formulas.names
        else:
            self.features = None
        self.kwargs = copy.deepcopy(kwargs)
        self.trained_time = None
        self.start_time = None
        self.end_time = None

    def fit(self, x: pd.DataFrame, is_train=True, **kwargs):
        self.trained_time = arrow.now().format("YYYY-MM-DD HH:mm:ss")
        if not is_train:
            return
        self.start_time = None if 'start_time' not in kwargs else kwargs[
            'start_time']
        self.end_date = None if 'end_date' not in kwargs else kwargs['end_date']
        return self.calc(x=x, **kwargs)

    def predict(self, x: pd.DataFrame, **kwargs):
        return self.calc(x=x, **kwargs)

    def calc(self, x: pd.DataFrame, **kwargs):
        pass

    def model_encode(self):
        return encode(self.kwargs)

    @classmethod
    def model_decode(cls, model_desc):
        return decode(model_desc)

    @abc.abstractmethod
    def save(self):
        if self.__class__.__module__ == '__main__':
            warnings.warn(
                "model is defined in a main module. The model_name may not be correct."
            )
        model_desc = dict(model_name=self.__class__.__module__ + "." +
                          self.__class__.__name__,
                          language='python',
                          saved_time=arrow.now().format("YYYY-MM-DD HH:mm:ss"),
                          features=list(self.features),
                          trained_time=self.trained_time,
                          start_time=self.start_time,
                          end_time=self.end_time,
                          desc=self.model_encode(),
                          formulas=encode(self.formulas))
        return model_desc

    @classmethod
    @abc.abstractmethod
    def load(cls, model_desc: dict):
        obj_layout = cls()
        obj_layout.features = model_desc['features']
        obj_layout.formulas = decode(model_desc['formulas'])
        obj_layout.trained_time = model_desc['trained_time']
        obj_layout.start_time = model_desc['start_time']
        obj_layout.end_time = model_desc['end_time']
        obj_layout.kwargs = cls.model_decode(model_desc['desc'])
        return obj_layout


def create_model_base(party_name=None):
    if not party_name:
        return ModelBase
    else:

        class ExternalLibBase(ModelBase):
            _lib_name = party_name

            def save(self):
                model_desc = super().save()
                return model_desc

            @classmethod
            def load(cls, model_desc: dict):
                obj_layout = super().load(model_desc)
                return obj_layout

        return ExternalLibBase


def load_module(name):
    module = importlib.import_module('ultron.factor.combine.modelbase')
    if name in module.__dict__:
        return module.__getattribute__(name)
    raise ValueError("{0} not in combine".format(name))


def check_module(name):
    module = importlib.import_module('ultron.factor.combine.modelbase')
    return name in module.__dict__


def load_model(model_desc):
    model_name = model_desc['model_name']
    model_name_parts = set(model_name.split('.'))
    if 'EqualCombine' in model_name_parts:
        return EqualCombine.load(model_desc)
    elif 'HistICCombine' in model_name_parts:
        return HistICCombine.load(model_desc)
    elif 'HistRetCombine' in model_name_parts:
        return HistRetCombine.load(model_desc)
    elif 'MaxICCombine' in model_name_parts:
        return MaxICCombine.load(model_desc)


class EqualCombine(create_model_base()):

    def __init__(self, features=None):
        super().__init__(features=features)

    def calc(self, x: pd.DataFrame, **kwargs):
        factors_df = x.copy()
        equal_data = equal_combine(factor_df=x[self.features],
                                   factor_list=self.features)
        data = pd.DataFrame(equal_data,
                            index=factors_df.set_index(['trade_date',
                                                        'code']).index,
                            columns=['combine'])
        data.reset_index(inplace=True)
        return data

    def save(self):
        model_desc = super().save()
        return model_desc


class HistRetCombine(create_model_base()):

    def __init__(self, features=None, **kwargs):
        super().__init__(features=features, **kwargs)

    def calc(self, x: pd.DataFrame, **kwargs):
        features = ['trade_date', 'code'] + self.features
        hist_ret_df, _ = hist_ret_combine(factor_df=x[features],
                                          factor_list=self.features,
                                          mret_df=kwargs['returns'],
                                          span=self.kwargs['span'],
                                          method=self.kwargs['method'],
                                          half_life=self.kwargs['half_life'])
        return hist_ret_df


class HistICCombine(create_model_base()):

    def __init__(self, features=None, **kwargs):
        super().__init__(features=features, **kwargs)

    def calc(self, x: pd.DataFrame, **kwargs):
        features = ['trade_date', 'code'] + self.features
        hist_ic_df, _ = hist_ic_combine(factor_df=x[features],
                                        factor_list=self.features,
                                        mret_df=kwargs['returns'],
                                        span=self.kwargs['span'],
                                        method=self.kwargs['method'],
                                        half_life=self.kwargs['half_life'])
        return hist_ic_df


class MaxICCombine(create_model_base()):

    def __init__(self, features=None, **kwargs):
        super().__init__(features=features, **kwargs)

    def calc(self, x: pd.DataFrame, **kwargs):
        features = ['trade_date', 'code'] + self.features
        max_ic_df, _ = max_ic_combine(factor_df=x[features],
                                      factor_list=self.features,
                                      mret_df=kwargs['returns'],
                                      span=self.kwargs['span'],
                                      method=self.kwargs['method'],
                                      weight_limit=self.kwargs['weight_limit'])
        return max_ic_df
