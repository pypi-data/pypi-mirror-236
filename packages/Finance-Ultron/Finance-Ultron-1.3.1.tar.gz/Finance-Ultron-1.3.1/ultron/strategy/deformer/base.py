# -*- coding: utf-8 -*-
import abc, warnings, arrow, pdb, copy
import pandas as pd
from ultron.factor.utilities import encode
from ultron.factor.utilities import decode
from ultron.factor.combine.modelbase import load_model as loader_combine
from ultron.optimize.model.loader import load_model as loader_model
from ultron.factor.combine.modelbase import load_module as load_combine_module
from ultron.optimize.model.modelbase import load_module as load_model_module
from ultron.factor.combine.modelbase import check_module as check_combine_module
from ultron.optimize.model.modelbase import check_module as check_model_module
from ultron.factor.data.transformer import Transformer
from ultron.factor.combine.modelbase import *
from ultron.optimize.model.treemodel import *
from ultron.optimize.model.linearmodel import *


class Base(object):

    def __init__(self,
                 features=None,
                 universe=None,
                 horizon=None,
                 batch=None,
                 freq=None,
                 paramo=None,
                 **kwargs):
        if features is not None:
            self.formulas = Transformer(features)
            self.features = self.formulas.names
        else:
            self.features = None
        self.kwargs = copy.deepcopy(kwargs)
        self.universe = universe
        self.batch = batch
        self.freq = freq
        self.horizon = horizon
        self.paramo = paramo
        self.impl = None
        self.name = None
        self.trained_time = None
        self.start_time = None
        self.end_time = None
        self.id = None

    def update_features(self, features):
        self.formulas = Transformer(features)
        self.features = self.formulas.names

    def set_formual(self, formulas):
        self.formulas = formulas
        self.features = self.formulas.names

    def create_model(self, name, **kwargs):
        self.name = name
        self.impl = load_model_module(name)(
            features=self.features, **
            kwargs) if check_model_module(name) else load_combine_module(name)(
                features=self.features, **kwargs)

    def fit(self, x: pd.DataFrame, **kwargs):
        pass
        #if 'trade_date' in x.columns:
        #    trade_dates = pd.to_datetime(
        #        x['trade_date']).dt.strftime('%Y-%m-%d')
        #    self.start_time = trade_dates.min()
        #    self.end_time = trade_dates.max()

    def load_impl(self, model_desc):
        model_name = model_desc['model_name']
        model_name_parts = set(model_name.split('.'))
        if 'combine' in model_name_parts:
            self.impl = loader_combine(model_desc=model_desc)
        elif 'model' in model_name_parts:
            self.impl = loader_model(model_desc=model_desc)
        self.model_name = model_name
        self.features = self.impl.features
        self.formulas = self.impl.formulas

    def model_encode(self, model_desc):
        return encode(model_desc)

    @classmethod
    def model_decode(cls, model_desc):
        return decode(model_desc)

    @abc.abstractmethod
    def dump(self):
        if self.__class__.__module__ == '__main__':
            warnings.warn(
                "model is defined in a main module. The model_name may not be correct."
            )

        model_desc = dict(model_name=self.__class__.__module__ + "." +
                          self.__class__.__name__,
                          language='python',
                          saved_time=arrow.now().format("YYYY-MM-DD HH:mm:ss"),
                          id=self.id,
                          name=self.name,
                          universe=self.universe,
                          features=list(self.features),
                          batch=self.batch,
                          freq=self.freq,
                          horizon=self.horizon,
                          params=self.model_encode(self.kwargs),
                          paramo=self.model_encode(self.paramo),
                          formulas=encode(self.formulas))
        return model_desc

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
                          id=self.id,
                          name=self.name,
                          features=list(self.features),
                          universe=self.universe,
                          trained_time=self.trained_time,
                          start_time=self.start_time,
                          end_time=self.end_time,
                          batch=self.batch,
                          freq=self.freq,
                          horizon=self.horizon,
                          params=self.model_encode(self.kwargs),
                          paramo=self.model_encode(self.paramo),
                          desc=self.impl.save(),
                          formulas=encode(self.formulas))
        return model_desc

    @classmethod
    @abc.abstractmethod
    def load(cls, model_desc: dict):
        obj_layout = cls()
        obj_layout.id = model_desc['id']
        obj_layout.name = model_desc['name']
        obj_layout.features = model_desc['features']
        obj_layout.universe = model_desc['universe']
        obj_layout.formulas = decode(model_desc['formulas'])
        obj_layout.trained_time = model_desc['trained_time']
        obj_layout.start_time = model_desc['start_time']
        obj_layout.end_time = model_desc['end_time']
        obj_layout.horizon = model_desc['horizon']
        obj_layout.batch = model_desc['batch']
        obj_layout.freq = model_desc['freq']
        obj_layout.kwargs = cls.model_decode(model_desc['params'])
        obj_layout.paramo = cls.model_decode(model_desc['paramo'])
        model_name = model_desc['desc']['model_name']
        model_name_parts = set(model_name.split('.'))
        obj_layout.model_name = model_name
        if 'combine' in model_name_parts:
            obj_layout.impl = loader_combine(model_desc=model_desc['desc'])
        elif 'model' in model_name_parts:
            obj_layout.impl = loader_model(model_desc=model_desc['desc'])
        return obj_layout


def create_model_base(party_name=None):
    if not party_name:
        return Base
    else:

        class ExternalLibBase(Base):
            _lib_name = party_name

            def save(self):
                model_desc = super().save()
                return model_desc

            @classmethod
            def load(cls, model_desc: dict):
                obj_layout = super().load(model_desc)
                return obj_layout

        return ExternalLibBase
