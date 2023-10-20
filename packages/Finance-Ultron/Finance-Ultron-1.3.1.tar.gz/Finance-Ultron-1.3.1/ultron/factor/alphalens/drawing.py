# -*- encoding:utf-8 -*-
import pandas as pd
from openpyxl import load_workbook, Workbook
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import os
from . import plotting
from . import saving
from . import utils
import pdb


class GridFigure(object):
    """
    It makes life easier with grid plots
    """

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.fig = plt.figure(figsize=(14, rows * 7))
        self.gs = gridspec.GridSpec(rows, cols, wspace=0.4, hspace=0.3)
        self.curr_row = 0
        self.curr_col = 0

    def next_row(self):
        if self.curr_col != 0:
            self.curr_row += 1
            self.curr_col = 0
        subplt = plt.subplot(self.gs[self.curr_row, :])
        self.curr_row += 1
        return subplt

    def next_cell(self):
        if self.curr_col >= self.cols:
            self.curr_row += 1
            self.curr_col = 0
        subplt = plt.subplot(self.gs[self.curr_row, self.curr_col])
        self.curr_col += 1
        return subplt

    def close(self):
        plt.close(self.fig)
        self.fig = None
        self.gs = None


class ExcelContext:

    def __init__(self, path, name, ids):
        file_name = os.path.join(path, "{0}.xlsx".format(name))
        if not os.path.exists(file_name):
            self.handle = pd.ExcelWriter(file_name, engine='openpyxl')
        else:
            book = load_workbook(file_name)
            self.handle = pd.ExcelWriter(file_name, engine='openpyxl')
            self.handle.book = book
        self.ids = ids

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.handle.save()


@saving.customize
@saving.plot_name(['summary'])
@plotting.customize
def draw_summary_sheet(factor_data,
                       alpha_beta,
                       mean_quant_rateret,
                       mean_ret_spread_quant,
                       ic,
                       autocorrelation,
                       quantile_turnover,
                       path,
                       plot_names,
                       ids=None):

    name = 'summary'
    context_manager = ExcelContext(path=path, name=name, ids=ids)
    with context_manager as obj:
        periods = utils.get_forward_returns_columns(factor_data.columns)
        periods = list(map(lambda p: pd.Timedelta(p).days, periods))

        saving.save_quantile_statistics_table(factor_data,
                                              ids=obj.ids,
                                              handle=obj.handle)
        saving.save_returns_table(alpha_beta,
                                  mean_quant_rateret,
                                  mean_ret_spread_quant,
                                  ids=obj.ids,
                                  handle=obj.handle)

        saving.save_information_table(ic, ids=obj.ids, handle=obj.handle)
        saving.save_turnover_table(quantile_turnover,
                                   ids=obj.ids,
                                   handle=obj.handle)
        saving.save_autocorrelation_table(autocorrelation,
                                          ids=obj.ids,
                                          handle=obj.handle)

        fr_cols = len(periods)
        vertical_sections = 2 + fr_cols * 3
        gf = GridFigure(rows=vertical_sections, cols=1)

        plotting.plot_quantile_returns_bar(
            mean_quant_rateret,
            by_group=False,
            ylim_percentiles=None,
            ax=gf.next_row(),
        )

        plt.savefig(plot_names[0])
        gf.close()


@saving.customize
@saving.plot_name(['returns', 'returns_group'])
@plotting.customize
def draw_returns_sheet(long_short,
                       group_neutral,
                       factor_data,
                       factor_returns,
                       alpha_beta,
                       mean_quant_rateret,
                       mean_ret_spread_quant,
                       mean_quant_rateret_bydate,
                       mean_quant_ret_bydate,
                       std_spread_quant,
                       mean_quant_rateret_group,
                       path,
                       plot_names,
                       ids=None):

    name = 'returns'

    context_manager = ExcelContext(path=path, name=name, ids=ids)

    with context_manager as obj:
        fr_cols = len(factor_returns.columns)
        vertical_sections = 2 + fr_cols * 3
        gf = GridFigure(rows=vertical_sections, cols=1)
        saving.save_returns_table(alpha_beta,
                                  mean_quant_rateret,
                                  mean_ret_spread_quant,
                                  handle=obj.handle)

        plotting.plot_quantile_returns_bar(
            mean_quant_rateret,
            by_group=False,
            ylim_percentiles=None,
            ax=gf.next_row(),
        )

        plotting.plot_quantile_returns_violin(mean_quant_rateret_bydate,
                                              ylim_percentiles=(1, 99),
                                              ax=gf.next_row())

        # Compute cumulative returns from daily simple returns, if '1D'
        # returns are provided.
        if "1D" in factor_returns:
            title = ("Factor Weighted " +
                     ("Group Neutral " if group_neutral else "") +
                     ("Long/Short " if long_short else "") +
                     "Portfolio Cumulative Return (1D Period)")

            plotting.plot_cumulative_returns(factor_returns["1D"],
                                             period="1D",
                                             title=title,
                                             ax=gf.next_row())

            plotting.plot_cumulative_returns_by_quantile(
                mean_quant_ret_bydate["1D"], period="1D", ax=gf.next_row())

        ax_mean_quantile_returns_spread_ts = [
            gf.next_row() for x in range(fr_cols)
        ]
        plotting.plot_mean_quantile_returns_spread_time_series(
            mean_ret_spread_quant,
            std_err=std_spread_quant,
            bandwidth=0.5,
            ax=ax_mean_quantile_returns_spread_ts,
        )
        plt.savefig(plot_names[0])
        gf.close()

        if mean_quant_rateret_group is not None:
            num_groups = len(
                mean_quant_rateret_group.index.get_level_values(
                    "group").unique())

            vertical_sections = 1 + (((num_groups - 1) // 2) + 1)
            gf = GridFigure(rows=vertical_sections, cols=2)

            ax_quantile_returns_bar_by_group = [
                gf.next_cell() for _ in range(num_groups)
            ]
            plotting.plot_quantile_returns_bar(
                mean_quant_rateret_group,
                by_group=True,
                ylim_percentiles=(5, 95),
                ax=ax_quantile_returns_bar_by_group,
            )
            plt.savefig(plot_names[1])
            gf.close()


@saving.customize
@saving.plot_name(['information'])
@plotting.customize
def draw_information_sheet(factor_data,
                           ic,
                           mean_monthly_ic,
                           mean_group_ic,
                           path,
                           plot_names,
                           ids=None):

    name = 'information'
    context_manager = ExcelContext(path=path, name=name, ids=ids)
    #plotting.plot_information_table(ic)
    with context_manager as obj:
        saving.save_information_table(ic, handle=obj.handle)

        columns_wide = 2
        fr_cols = len(ic.columns)
        rows_when_wide = ((fr_cols - 1) // columns_wide) + 1
        vertical_sections = fr_cols + 3 * rows_when_wide + 2 * fr_cols
        gf = GridFigure(rows=vertical_sections, cols=columns_wide)

        ax_ic_ts = [gf.next_row() for _ in range(fr_cols)]
        plotting.plot_ic_ts(ic, ax=ax_ic_ts)

        ax_ic_hqq = [gf.next_cell() for _ in range(fr_cols * 2)]
        plotting.plot_ic_hist(ic, ax=ax_ic_hqq[::2])
        plotting.plot_ic_qq(ic, ax=ax_ic_hqq[1::2])

        if mean_monthly_ic is not None:
            ax_monthly_ic_heatmap = [gf.next_cell() for x in range(fr_cols)]
            plotting.plot_monthly_ic_heatmap(mean_monthly_ic,
                                             ax=ax_monthly_ic_heatmap)

        if mean_group_ic is not None:
            plotting.plot_ic_by_group(mean_group_ic, ax=gf.next_row())
        plt.savefig(plot_names[0])
        gf.close()


@saving.customize
@saving.plot_name(['turnover'])
@plotting.customize
def draw_turnover_sheet(turnover_periods,
                        factor_data,
                        autocorrelation,
                        quantile_turnover,
                        path,
                        plot_names,
                        ids=None):
    name = 'turnover'
    context_manager = ExcelContext(path=path, name=name, ids=ids)
    with context_manager as obj:
        if turnover_periods is None:
            input_periods = utils.get_forward_returns_columns(
                factor_data.columns,
                require_exact_day_multiple=True,
            ).to_numpy()
            turnover_periods = utils.timedelta_strings_to_integers(
                input_periods)
        else:
            turnover_periods = utils.timedelta_strings_to_integers(
                turnover_periods, )

        saving.save_turnover_table(quantile_turnover,
                                   ids=obj.ids,
                                   handle=obj.handle)

        saving.save_autocorrelation_table(autocorrelation,
                                          ids=obj.ids,
                                          handle=obj.handle)

        fr_cols = len(turnover_periods)
        columns_wide = 1
        rows_when_wide = ((fr_cols - 1) // 1) + 1
        vertical_sections = fr_cols + 3 * rows_when_wide + 2 * fr_cols
        gf = GridFigure(rows=vertical_sections, cols=columns_wide)

        for period in turnover_periods:
            if quantile_turnover[period].isnull().all().all():
                continue
            plotting.plot_top_bottom_quantile_turnover(
                quantile_turnover[period], period=period, ax=gf.next_row())

        for period in autocorrelation:
            if autocorrelation[period].isnull().all():
                continue
            plotting.plot_factor_rank_auto_correlation(autocorrelation[period],
                                                       period=period,
                                                       ax=gf.next_row())

        plt.savefig(plot_names[0])
        gf.close()


@plotting.customize
def draw_full_sheet(returns, information, turnover, path, ids=None):
    draw_summary_sheet(factor_data=returns.factor_data,
                       alpha_beta=returns.alpha_beta,
                       mean_quant_rateret=returns.mean_quant_rateret,
                       mean_ret_spread_quant=returns.mean_ret_spread_quant,
                       ic=information.ic,
                       autocorrelation=turnover.autocorrelation,
                       quantile_turnover=turnover.quantile_turnover,
                       path=path,
                       ids=ids)
    draw_returns_sheet(
        long_short=True,
        group_neutral=False,
        factor_data=returns.factor_data,
        factor_returns=returns.factor_returns,
        alpha_beta=returns.alpha_beta,
        mean_quant_rateret=returns.mean_quant_rateret,
        mean_ret_spread_quant=returns.mean_ret_spread_quant,
        mean_quant_rateret_bydate=returns.mean_quant_rateret_bydate,
        mean_quant_ret_bydate=returns.mean_quant_ret_bydate,
        std_spread_quant=returns.std_spread_quant,
        mean_quant_rateret_group=returns.mean_quant_rateret_group,
        path=path,
        ids=ids)

    draw_information_sheet(factor_data=information.factor_data,
                           ic=information.ic,
                           mean_monthly_ic=information.mean_monthly_ic,
                           mean_group_ic=information.mean_group_ic,
                           path=path,
                           ids=ids)

    draw_turnover_sheet(turnover_periods=None,
                        factor_data=turnover.factor_data,
                        autocorrelation=turnover.autocorrelation,
                        quantile_turnover=turnover.quantile_turnover,
                        path=path,
                        ids=ids)
