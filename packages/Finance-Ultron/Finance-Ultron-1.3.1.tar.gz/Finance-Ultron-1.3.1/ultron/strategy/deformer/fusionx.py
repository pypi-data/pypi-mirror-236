# -*- coding: utf-8 -*-
import hashlib, json, pdb, copy
import pandas as pd
from ultron.factor.utilities import encode, decode
from ultron.strategy.deformer.base import create_model_base
from ultron.kdutils.create_id import create_id
from ultron.utilities.logger import kd_logger


def create_model_id(name, universe, features, horizon, batch, freq, paramo,
                    kwargs):
    paramo = {} if paramo is None else copy.deepcopy(paramo)
    kwargs = {} if kwargs is None else copy.deepcopy(kwargs)
    horizon = 0 if horizon is None else horizon
    batch = 0 if batch is None else batch
    freq = 0 if freq is None else freq
    s = hashlib.md5(
        json.dumps({
            'name':
            name,
            'universe':
            universe,
            'horizon':
            horizon,
            'batch':
            batch,
            'freq':
            freq,
            'features':
            sorted(features if isinstance(features, list) else []),
            **kwargs,
            **paramo
        }).encode(encoding="utf-8")).hexdigest()
    return "{0}".format(create_id(original=s, digit=10))


def dump(name=None,
         features=None,
         universe=None,
         horizon=None,
         batch=None,
         freq=None,
         paramo=None,
         **kwargs):
    #model_class = create_model_base()
    model = FusionX(name=name,
                    features=features,
                    universe=universe,
                    horizon=horizon,
                    batch=batch,
                    freq=freq,
                    paramo=paramo,
                    **kwargs)
    paramo = {} if model.paramo is None else copy.deepcopy(model.paramo)
    kwargs = {} if model.kwargs is None else copy.deepcopy(model.kwargs)
    model.id = create_model_id(name=model.name,
                               universe=model.universe,
                               features=model.features,
                               horizon=model.horizon,
                               batch=model.batch,
                               freq=model.freq,
                               paramo=model.paramo,
                               kwargs=model.kwargs)
    return model.dump()


def load(desc):
    obj_layout = FusionX()
    obj_layout.id = desc['id']
    obj_layout.name = desc['name']
    obj_layout.universe = desc['universe']
    obj_layout.features = desc['features']
    obj_layout.model_name = desc['model_name']
    obj_layout.language = desc['language']
    obj_layout.formulas = decode(desc['formulas'])
    kwargs = create_model_base().model_decode(desc['params'])
    obj_layout.kwargs = kwargs
    obj_layout.freq = desc['freq']
    obj_layout.batch = desc['batch']
    obj_layout.horizon = desc['horizon']
    obj_layout.paramo = create_model_base().model_decode(desc['paramo'])
    obj_layout.create_model(name=desc['name'], **kwargs)
    return obj_layout


class FusionX(create_model_base()):

    def __init__(self,
                 name=None,
                 features=None,
                 universe=None,
                 horizon=None,
                 batch=None,
                 freq=None,
                 paramo=None,
                 **kwargs):
        super().__init__(features=features,
                         universe=universe,
                         horizon=horizon,
                         batch=batch,
                         freq=freq,
                         paramo=paramo,
                         **kwargs)
        if isinstance(name, str):
            super().create_model(name=name, **kwargs)
        self._create_id(name=self.name,
                        universe=self.universe,
                        features=self.features,
                        horizon=self.horizon,
                        batch=self.batch,
                        freq=self.freq,
                        paramo=self.paramo,
                        kwargs=self.kwargs)
        #self._model_party = set(self.model_name.split('.'))

    def update_features(self, features):
        super().update_features(features)
        self.id = create_model_id(name=self.name,
                                  universe=self.universe,
                                  features=self.features,
                                  horizon=self.horizon,
                                  batch=self.batch,
                                  freq=self.freq,
                                  paramo=self.paramo,
                                  kwargs=self.kwargs)

    def _create_id(self, name, universe, features, horizon, batch, freq,
                   paramo, kwargs):
        if self.id is None:
            self.id = create_model_id(name=name,
                                      universe=universe,
                                      features=features,
                                      horizon=horizon,
                                      batch=batch,
                                      freq=freq,
                                      paramo=paramo,
                                      kwargs=kwargs)
        return self.id

    ### 模型训练
    def fit(self, x, y=None, **kwargs):
        super().fit(x=x, **kwargs)
        #x = self.formulas.transform(
        #    'code', x.set_index('trade_date')).reset_index().sort_values(
        #        by=['trade_date', 'code'])
        if 'combine' in self.impl.__class__.__module__:
            self.impl.fit(x, is_train=False, **kwargs)
        elif 'model' in self.impl.__class__.__module__:
            self.impl.fit(x, y, **kwargs)

    @property
    def category(self):
        if 'combine' in self.impl.__class__.__module__:
            return 'combine'
        elif 'model' in self.impl.__class__.__module__:
            return 'model'

    def predict(self, x: pd.DataFrame, returns=None, **kwargs):
        begin_date = x['trade_date'].min()
        end_date = x['trade_date'].max()
        #x = self.formulas.transform(
        #    'code', x.set_index('trade_date')).reset_index().sort_values(
        #        by=['trade_date', 'code'])
        if 'combine' in self.impl.__class__.__module__:
            kd_logger.info("combine predict dimension {0}~{1} data".format(
                begin_date, end_date))
            return self.impl.predict(
                x, returns=returns).rename(columns={'combine': self.id})
        elif 'model' in self.impl.__class__.__module__:
            kd_logger.info("model predict dimension {0}~{1} data".format(
                begin_date, end_date))
            index = x.set_index(['trade_date', 'code']).index
            data = pd.DataFrame(self.impl.predict(x).flatten(),
                                index=index,
                                columns=[self.id])
            #data.reset_index(inplace=True)
            return data
