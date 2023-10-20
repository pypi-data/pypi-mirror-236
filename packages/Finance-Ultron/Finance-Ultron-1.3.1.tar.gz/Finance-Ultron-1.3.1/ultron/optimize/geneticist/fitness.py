# -*- encoding:utf-8 -*-
import time, pdb
import pandas as pd
from sklearn.model_selection import KFold
from sklearn.model_selection import TimeSeriesSplit
from ultron.optimize.model.modelbase import load_module
from ultron.utilities.logger import kd_logger


def model_fitness(features, model_name, X, Y, params, default_value, mode,
                  n_splits):
    #kf = KFold(n_splits=n_splits, shuffle=False)
    windows = None if 'windows' not in params else params['windows']
    tss = TimeSeriesSplit(max_train_size=windows, n_splits=n_splits)
    res = []
    start_time = time.time()
    kd_logger.info("{0}:model_name:{1},params:{2},fitness".format(
        'start'.ljust(6), model_name.ljust(20),
        str(params).ljust(30)))
    front_pos = 0
    for train_index, test_index in tss.split(X):
        train_pos = train_index[front_pos:]
        front_pos = train_index[-1] + 1
        x_train = X.iloc[train_pos]
        y_train = Y.iloc[train_pos].values
        x_test = X.iloc[test_index]
        y_test = Y.iloc[test_index].values
        model = load_module(model_name)(features=features, **params)
        if 'sample_weight' in x_train.columns:
            kd_logger.info(
                "{0}:model_name:{1},params:{2},sample weight".format(
                    'fit'.ljust(6), model_name.ljust(20),
                    str(params).ljust(30)))
            model.fit(x_train.drop('sample_weight', axis=1),
                      y_train,
                      sample_weight=x_train['sample_weight'])
        else:
            kd_logger.info(
                "{0}:model_name:{1},params:{2},nosample weight".format(
                    'fit'.ljust(6), model_name.ljust(20),
                    str(params).ljust(30)))
            model.fit(x_train, y_train)
        res.append({mode: model.__getattribute__(mode)(x_test, y_test)})

    kd_logger.info(
        "{0}:model_name:{1},params:{2},fitness cost time:{3}".format(
            'finish'.ljust(6), model_name.ljust(20),
            str(params).ljust(30),
            str((time.time() - start_time)).ljust(10)))

    result = pd.DataFrame(res)
    return default_value if result.empty else result[mode].mean()