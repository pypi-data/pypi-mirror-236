# -*- encoding:utf-8 -*-
import pandas as pd
import warnings
from collections import namedtuple

from . import performance as perf
from . import utils


class SummaryTuple(
        namedtuple(
            'SummaryTuple',
            ('factor_data', 'mean_quant_ret', 'std_quantile',
             'mean_quant_rateret', 'mean_quant_ret_bydate', 'std_quant_daily',
             'mean_quant_rateret_bydate', 'compstd_quant_daily', 'alpha_beta',
             'mean_ret_spread_quant', 'std_spread_quant', 'ic',
             'quantile_turnover', 'autocorrelation'))):
    __slots__ = ()


class ReturnsTuple(
        namedtuple(
            'ReturnsTuple',
            ('long_short', 'group_neutral', 'factor_data', 'factor_returns',
             'mean_quant_ret', 'std_quantile', 'mean_quant_rateret',
             'mean_quant_ret_bydate', 'std_quant_daily',
             'mean_quant_rateret_bydate', 'compstd_quant_daily', 'alpha_beta',
             'mean_ret_spread_quant', 'std_spread_quant',
             'mean_return_quantile_group',
             'mean_return_quantile_group_std_err', 'mean_quant_rateret_group'))
):
    __slots__ = ()


class InformationTuple(
        namedtuple('ImformationTuple',
                   ('factor_data', 'ic', 'mean_monthly_ic', 'mean_group_ic'))):
    __slots__ = ()


class EventReturnsTuple(
        namedtuple(
            'EventReturnsTuple',
            ('factor_data', 'avg_cumulative_returns', 'avg_cumret_by_group'))):
    __slots__ = ()


class TurnoverTuple(
        namedtuple('TurnoverTuple',
                   ('turnover_periods', 'factor_data', 'quantile_factor',
                    'quantile_turnover', 'autocorrelation'))):
    __slots__ = ()


def create_summary_aggregate_sheet(factor_data,
                                   long_short=True,
                                   group_neutral=False):
    # Returns Analysis
    mean_quant_ret, std_quantile = perf.mean_return_by_quantile(
        factor_data,
        by_group=False,
        demeaned=long_short,
        group_adjust=group_neutral,
    )

    mean_quant_rateret = mean_quant_ret.apply(
        utils.rate_of_return, axis=0, base_period=mean_quant_ret.columns[0])

    mean_quant_ret_bydate, std_quant_daily = perf.mean_return_by_quantile(
        factor_data,
        by_date=True,
        by_group=False,
        demeaned=long_short,
        group_adjust=group_neutral,
    )

    mean_quant_rateret_bydate = mean_quant_ret_bydate.apply(
        utils.rate_of_return,
        axis=0,
        base_period=mean_quant_ret_bydate.columns[0],
    )

    compstd_quant_daily = std_quant_daily.apply(
        utils.std_conversion, axis=0, base_period=std_quant_daily.columns[0])

    alpha_beta = perf.factor_alpha_beta(factor_data,
                                        demeaned=long_short,
                                        group_adjust=group_neutral)

    mean_ret_spread_quant, std_spread_quant = perf.compute_mean_returns_spread(
        mean_quant_rateret_bydate,
        factor_data["factor_quantile"].max(),
        factor_data["factor_quantile"].min(),
        std_err=compstd_quant_daily,
    )

    periods = utils.get_forward_returns_columns(factor_data.columns)
    periods = list(map(lambda p: pd.Timedelta(p).days, periods))

    # Information Analysis
    ic = perf.factor_information_coefficient(factor_data)

    # Turnover Analysis
    quantile_factor = factor_data["factor_quantile"]

    quantile_turnover = {
        p: pd.concat(
            [
                perf.quantile_turnover(quantile_factor, q, p)
                for q in range(1,
                               int(quantile_factor.max()) + 1)
            ],
            axis=1,
        )
        for p in periods
    }

    autocorrelation = pd.concat(
        [
            perf.factor_rank_autocorrelation(factor_data, period)
            for period in periods
        ],
        axis=1,
    )
    return SummaryTuple(factor_data=factor_data,
                        mean_quant_ret=mean_quant_ret,
                        std_quantile=std_quantile,
                        mean_quant_rateret=mean_quant_rateret,
                        mean_quant_ret_bydate=mean_quant_ret_bydate,
                        std_quant_daily=std_quant_daily,
                        mean_quant_rateret_bydate=mean_quant_rateret_bydate,
                        compstd_quant_daily=compstd_quant_daily,
                        alpha_beta=alpha_beta,
                        mean_ret_spread_quant=mean_ret_spread_quant,
                        std_spread_quant=std_spread_quant,
                        ic=ic,
                        quantile_turnover=quantile_turnover,
                        autocorrelation=autocorrelation)


def create_returns_aggregate_sheet(factor_data,
                                   long_short=True,
                                   group_neutral=False,
                                   by_group=False):
    factor_returns = perf.factor_returns(factor_data, long_short,
                                         group_neutral)

    mean_quant_ret, std_quantile = perf.mean_return_by_quantile(
        factor_data,
        by_group=False,
        demeaned=long_short,
        group_adjust=group_neutral,
    )

    mean_quant_rateret = mean_quant_ret.apply(
        utils.rate_of_return, axis=0, base_period=mean_quant_ret.columns[0])

    mean_quant_ret_bydate, std_quant_daily = perf.mean_return_by_quantile(
        factor_data,
        by_date=True,
        by_group=False,
        demeaned=long_short,
        group_adjust=group_neutral,
    )

    mean_quant_rateret_bydate = mean_quant_ret_bydate.apply(
        utils.rate_of_return,
        axis=0,
        base_period=mean_quant_ret_bydate.columns[0],
    )

    compstd_quant_daily = std_quant_daily.apply(
        utils.std_conversion, axis=0, base_period=std_quant_daily.columns[0])

    alpha_beta = perf.factor_alpha_beta(factor_data, factor_returns,
                                        long_short, group_neutral)

    mean_ret_spread_quant, std_spread_quant = perf.compute_mean_returns_spread(
        mean_quant_rateret_bydate,
        factor_data["factor_quantile"].max(),
        factor_data["factor_quantile"].min(),
        std_err=compstd_quant_daily,
    )

    if by_group:
        (
            mean_return_quantile_group,
            mean_return_quantile_group_std_err,
        ) = perf.mean_return_by_quantile(
            factor_data,
            by_date=False,
            by_group=True,
            demeaned=long_short,
            group_adjust=group_neutral,
        )

        mean_quant_rateret_group = mean_return_quantile_group.apply(
            utils.rate_of_return,
            axis=0,
            base_period=mean_return_quantile_group.columns[0],
        )
    else:
        mean_return_quantile_group = None
        mean_return_quantile_group_std_err = None
        mean_quant_rateret_group = None
    return ReturnsTuple(
        long_short=long_short,
        group_neutral=group_neutral,
        factor_data=factor_data,
        factor_returns=factor_returns,
        mean_quant_ret=mean_quant_ret,
        std_quantile=std_quantile,
        mean_quant_rateret=mean_quant_rateret,
        mean_quant_ret_bydate=mean_quant_ret_bydate,
        std_quant_daily=std_quant_daily,
        mean_quant_rateret_bydate=mean_quant_rateret_bydate,
        compstd_quant_daily=compstd_quant_daily,
        alpha_beta=alpha_beta,
        mean_ret_spread_quant=mean_ret_spread_quant,
        std_spread_quant=std_spread_quant,
        mean_return_quantile_group=mean_return_quantile_group,
        mean_return_quantile_group_std_err=mean_return_quantile_group_std_err,
        mean_quant_rateret_group=mean_quant_rateret_group)


def create_information_aggregate_sheet(factor_data,
                                       group_neutral=False,
                                       by_group=False):
    ic = perf.factor_information_coefficient(factor_data, group_neutral)
    if not by_group:
        mean_monthly_ic = perf.mean_information_coefficient(
            factor_data,
            group_adjust=group_neutral,
            by_group=False,
            by_time="M",
        )
    else:
        mean_monthly_ic = None
    if by_group:
        mean_group_ic = perf.mean_information_coefficient(
            factor_data, group_adjust=group_neutral, by_group=True)
    else:
        mean_group_ic = None
    return InformationTuple(factor_data,
                            ic=ic,
                            mean_monthly_ic=mean_monthly_ic,
                            mean_group_ic=mean_group_ic)


def create_turnover_aggregate_sheet(factor_data, turnover_periods=None):
    if turnover_periods is None:
        input_periods = utils.get_forward_returns_columns(
            factor_data.columns,
            require_exact_day_multiple=True,
        ).to_numpy()
        turnover_periods = utils.timedelta_strings_to_integers(input_periods)
    else:
        turnover_periods = utils.timedelta_strings_to_integers(
            turnover_periods, )

    quantile_factor = factor_data["factor_quantile"]

    quantile_turnover = {
        p: pd.concat(
            [
                perf.quantile_turnover(quantile_factor, q, p)
                for q in quantile_factor.sort_values().unique().tolist()
            ],
            axis=1,
        )
        for p in turnover_periods
    }

    autocorrelation = pd.concat(
        [
            perf.factor_rank_autocorrelation(factor_data, period)
            for period in turnover_periods
        ],
        axis=1,
    )

    return TurnoverTuple(turnover_periods=turnover_periods,
                         factor_data=factor_data,
                         quantile_factor=quantile_factor,
                         autocorrelation=autocorrelation,
                         quantile_turnover=quantile_turnover)


def create_full_aggregate_sheet(factor_data,
                                long_short=True,
                                group_neutral=False,
                                by_group=False):

    returns_tuple = create_returns_aggregate_sheet(factor_data,
                                                   long_short=long_short,
                                                   group_neutral=group_neutral,
                                                   by_group=by_group)
    information_tuple = create_information_aggregate_sheet(
        factor_data, group_neutral=group_neutral, by_group=by_group)

    turnover_tuple = create_turnover_aggregate_sheet(factor_data)

    return returns_tuple, information_tuple, turnover_tuple


def create_event_returns_aggregate_sheet(factor_data,
                                         returns,
                                         avgretplot=(5, 15),
                                         long_short=True,
                                         group_neutral=False,
                                         std_bar=True,
                                         by_group=False):

    before, after = avgretplot

    avg_cumulative_returns = perf.average_cumulative_return_by_quantile(
        factor_data,
        returns,
        periods_before=before,
        periods_after=after,
        demeaned=long_short,
        group_adjust=group_neutral,
    )

    if by_group:
        avg_cumret_by_group = perf.average_cumulative_return_by_quantile(
            factor_data,
            returns,
            periods_before=before,
            periods_after=after,
            demeaned=long_short,
            group_adjust=group_neutral,
            by_group=True,
        )
    else:
        avg_cumret_by_group = None
    return EventReturnsTuple(factor_data=factor_data,
                             avg_cumulative_returns=avg_cumulative_returns,
                             avg_cumret_by_group=avg_cumret_by_group)
