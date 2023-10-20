import os, pdb
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm
from functools import wraps
from . import utils

DECIMAL_TO_BPS = 10000


def customize(func):

    @wraps(func)
    def call_w_path(*args, **kwargs):
        path = kwargs['path'] if 'path' in kwargs else './'
        if not os.path.exists(path):
            os.makedirs(path)
        return func(*args, **kwargs)

    return call_w_path


def create_plot(path, ids, name):
    if ids is None:
        plot_name = os.path.join(path, "{0}.png".format(name))
    else:
        plot_name = os.path.join(path, ids, "{0}.png".format(name))
    dir_path, _ = os.path.split(plot_name)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)
    return plot_name


def plot_name(names):

    def decorate(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            ids = kwargs['ids']
            path = kwargs['path']
            news_names = [
                create_plot(name=name, path=path, ids=ids) for name in names
            ]
            return func(*args, **kwargs, plot_names=news_names)

        return wrapper

    return decorate


def ids_name(name):

    def decorate(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            ids = kwargs.pop('ids', None)
            new_name = name if ids is None else '{0}_{1}'.format(ids, name)
            return func(*args, **kwargs, name=new_name)

        return wrapper

    return decorate


@ids_name('returns')
def save_returns_table(alpha_beta,
                       mean_ret_quantile,
                       mean_ret_spread_quantile,
                       name='returns',
                       handle=None):
    """Save the returns table to a file.
    """
    returns_table = pd.DataFrame()
    returns_table = returns_table.append(alpha_beta)
    returns_table.loc["Mean Period Wise Return Top Quantile (bps)"] = \
        mean_ret_quantile.iloc[-1] * DECIMAL_TO_BPS
    returns_table.loc["Mean Period Wise Return Bottom Quantile (bps)"] = \
        mean_ret_quantile.iloc[0] * DECIMAL_TO_BPS
    returns_table.loc["Mean Period Wise Spread (bps)"] = \
        mean_ret_spread_quantile.mean() * DECIMAL_TO_BPS
    utils.save_file(table=returns_table.apply(lambda x: x.round(3)),
                    name=name,
                    handle=handle)


@ids_name('turnover')
def save_turnover_table(quantile_turnover, name='turnover', handle=None):
    turnover_table = pd.DataFrame()
    for period in sorted(quantile_turnover.keys()):
        for quantile, p_data in quantile_turnover[period].iteritems():
            turnover_table.loc["Quantile {} Mean Turnover ".format(quantile),
                               "{}D".format(period)] = p_data.mean()

    utils.save_file(table=turnover_table.apply(lambda x: x.round(3)),
                    name=name,
                    handle=handle)


@ids_name('auto_corr')
def save_autocorrelation_table(autocorrelation_data,
                               name='auto_corr',
                               handle=None):
    auto_corr = pd.DataFrame()
    for period, p_data in autocorrelation_data.iteritems():
        auto_corr.loc["Mean Factor Rank Autocorrelation",
                      "{}D".format(period)] = p_data.mean()

    utils.save_file(table=auto_corr.apply(lambda x: x.round(3)),
                    name=name,
                    handle=handle)


@ids_name('ic_summary')
def save_information_table(ic_data, name='ic_summary', handle=None):
    ic_summary_table = pd.DataFrame()
    ic_summary_table["IC Mean"] = ic_data.mean()
    ic_summary_table["IC Std."] = ic_data.std()
    ic_summary_table["Risk-Adjusted IC"] = \
        ic_data.mean() / ic_data.std()
    t_stat, p_value = stats.ttest_1samp(ic_data, 0)
    ic_summary_table["t-stat(IC)"] = t_stat
    ic_summary_table["p-value(IC)"] = p_value
    ic_summary_table["IC Skew"] = stats.skew(ic_data)
    ic_summary_table["IC Kurtosis"] = stats.kurtosis(ic_data)

    utils.save_file(table=ic_summary_table.apply(lambda x: x.round(3)).T,
                    name=name,
                    handle=handle)


@ids_name('quantile_stats')
def save_quantile_statistics_table(factor_data,
                                   name='quantile_stats',
                                   handle=None):
    quantile_stats = factor_data.groupby('factor_quantile') \
        .agg(['min', 'max', 'mean', 'std', 'count'])['factor']
    quantile_stats['count %'] = quantile_stats['count'] \
        / quantile_stats['count'].sum() * 100.

    utils.save_file(table=quantile_stats, name=name, handle=handle)
