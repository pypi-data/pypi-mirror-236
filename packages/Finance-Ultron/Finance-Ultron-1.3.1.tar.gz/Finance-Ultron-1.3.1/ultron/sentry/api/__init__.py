# -*- coding: utf-8 -*-

from ultron.sentry.Analysis import transform
from ultron.sentry.Analysis.SeriesValues import SeriesValues

from ultron.sentry.api.Analysis import ADDED
from ultron.sentry.api.Analysis import SUBBED
from ultron.sentry.api.Analysis import MUL
from ultron.sentry.api.Analysis import DIV
from ultron.sentry.api.Analysis import MOD
from ultron.sentry.api.Analysis import SIGN
from ultron.sentry.api.Analysis import CURRENT
from ultron.sentry.api.Analysis import LAST
from ultron.sentry.api.Analysis import SQRT
from ultron.sentry.api.Analysis import DIFF
from ultron.sentry.api.Analysis import EXP
from ultron.sentry.api.Analysis import LOG2
from ultron.sentry.api.Analysis import LOG10
from ultron.sentry.api.Analysis import LOG
from ultron.sentry.api.Analysis import POW
from ultron.sentry.api.Analysis import ABS
from ultron.sentry.api.Analysis import AVG

from ultron.sentry.api.Analysis import RETURNSimple
from ultron.sentry.api.Analysis import RETURNLog

from ultron.sentry.api.Analysis import ACOS
from ultron.sentry.api.Analysis import ACOSH
from ultron.sentry.api.Analysis import ASIN
from ultron.sentry.api.Analysis import ASINH
from ultron.sentry.api.Analysis import NORMINV
from ultron.sentry.api.Analysis import CEIL
from ultron.sentry.api.Analysis import FLOOR
from ultron.sentry.api.Analysis import ROUND
from ultron.sentry.api.Analysis import SIGMOID
from ultron.sentry.api.Analysis import TANH
from ultron.sentry.api.Analysis import RELU
from ultron.sentry.api.Analysis import SHIFT
from ultron.sentry.api.Analysis import DELTA
from ultron.sentry.api.Analysis import FRAC
from ultron.sentry.api.Analysis import SIGLOG2ABS
from ultron.sentry.api.Analysis import SIGLOG10ABS
from ultron.sentry.api.Analysis import SIGLOGABS
from ultron.sentry.api.Analysis import SIGSQRTABS
from ultron.sentry.api.Analysis import IIF
from ultron.sentry.api.Analysis import INDUSTRY

from ultron.sentry.api.Analysis import EMA
from ultron.sentry.api.Analysis import MACD
from ultron.sentry.api.Analysis import WMA
from ultron.sentry.api.Analysis import RSI
from ultron.sentry.api.Analysis import MARETURNLog
from ultron.sentry.api.Analysis import MCORR
from ultron.sentry.api.Analysis import MRes
from ultron.sentry.api.Analysis import MMeanRes
from ultron.sentry.api.Analysis import MCoef
from ultron.sentry.api.Analysis import MRSquared
from ultron.sentry.api.Analysis import MSharp
from ultron.sentry.api.Analysis import MSortino
from ultron.sentry.api.Analysis import MMaxDrawdown
from ultron.sentry.api.Analysis import MMDrawdown
from ultron.sentry.api.Analysis import MA
from ultron.sentry.api.Analysis import MADiff
from ultron.sentry.api.Analysis import MADecay
from ultron.sentry.api.Analysis import MMAX
from ultron.sentry.api.Analysis import MMedian
from ultron.sentry.api.Analysis import MARGMAX
from ultron.sentry.api.Analysis import MMIN
from ultron.sentry.api.Analysis import MARGMIN
from ultron.sentry.api.Analysis import MRANK
from ultron.sentry.api.Analysis import MPERCENT
from ultron.sentry.api.Analysis import MAXIMUM
from ultron.sentry.api.Analysis import MINIMUM
from ultron.sentry.api.Analysis import MQUANTILE
from ultron.sentry.api.Analysis import MCPS
from ultron.sentry.api.Analysis import MDIFF
from ultron.sentry.api.Analysis import MMaxDiff
from ultron.sentry.api.Analysis import MMinDiff
from ultron.sentry.api.Analysis import MALLTRUE
from ultron.sentry.api.Analysis import MANYTRUE
from ultron.sentry.api.Analysis import MSUM
from ultron.sentry.api.Analysis import MPRO
from ultron.sentry.api.Analysis import MVARIANCE
from ultron.sentry.api.Analysis import MConVariance
from ultron.sentry.api.Analysis import MIR
from ultron.sentry.api.Analysis import MZScore
from ultron.sentry.api.Analysis import MSTD
from ultron.sentry.api.Analysis import MKURT
from ultron.sentry.api.Analysis import MSKEW
from ultron.sentry.api.Analysis import MNPOSITIVE
from ultron.sentry.api.Analysis import MAPOSITIVE

from ultron.sentry.api.Analysis import CSSoftmax
from ultron.sentry.api.Analysis import CSDemean
from ultron.sentry.api.Analysis import CSSTD
from ultron.sentry.api.Analysis import CSSKEW
from ultron.sentry.api.Analysis import CSSUM
from ultron.sentry.api.Analysis import CSRank
from ultron.sentry.api.Analysis import CSTopN
from ultron.sentry.api.Analysis import CSBottomN
from ultron.sentry.api.Analysis import CSTopNQuantile
from ultron.sentry.api.Analysis import CSBottomNQuantile
from ultron.sentry.api.Analysis import CSMean
from ultron.sentry.api.Analysis import CSMeanAdjusted
from ultron.sentry.api.Analysis import CSQuantiles
from ultron.sentry.api.Analysis import CSZScore
from ultron.sentry.api.Analysis import CSFillNA
from ultron.sentry.api.Analysis import CSRes
from ultron.sentry.api.Analysis import CSNeut
from ultron.sentry.api.Analysis import CSProj
from ultron.sentry.api.Analysis import CSFloorDiv
from ultron.sentry.api.Analysis import CSSignPower
from ultron.sentry.api.Analysis import CSReverse
from ultron.sentry.api.Analysis import CSInverse
from ultron.sentry.api.Analysis import CSWinsorize

__all__ = [
    "transform", "SIGN", "SeriesValues", "AVG", "EMA", "WMA","MACD", "RSI",
    "MARETURNLog", "MCORR", "MRes", "MCoef", "MRSquared","MSharp", "MSortino",
    "MMaxDrawdown", "MMDrawdown", "MA", "MADiff", "MADecay", "MMAX","MMeanRes",
    "MARGMAX", "MMIN", "MARGMIN", "MKURT","MSKEW","MMedian", "MRANK", "MPERCENT",
    "MAXIMUM", "MINIMUM","MQUANTILE", "MCPS", "MDIFF", "MMaxDiff", "MMinDiff", "MALLTRUE",
    "MANYTRUE", "MSUM", "MPRO", "MVARIANCE", "ADDED", "SUBBED", "MUL", "DIV",
    "MOD", "MSTD", "MIR", "MZScore", "MNPOSITIVE", "MAPOSITIVE", "CURRENT",
    "LAST", "SQRT", "DIFF", "TANH", "RETURNSimple", "RETURNLog", "SIGLOG2ABS",
    "FRAC","SIGLOG10ABS", "SIGLOGABS", "SIGSQRTABS", "EXP", "LOG2", "LOG10", "LOG",
    "POW", "ABS", "ACOS", "ACOSH", "ASIN", "ASINH", "NORMINV", "CEIL", "FLOOR",
    "ROUND", "SIGMOID", "TANH", "RELU","SHIFT", "DELTA", "IIF", "INDUSTRY",
    "CSSoftmax","CSWinsorize", "CSInverse", "CSReverse", "CSRank", "CSTopN", "CSBottomN",
    "CSTopNQuantile", "CSBottomNQuantile", "CSMean", "CSMeanAdjusted","MConVariance",
    "CSQuantiles", "CSZScore", "CSFillNA", "CSRes", "CSNeut", "CSProj",
    "CSDemean", "CSSTD", "CSSKEW", "CSSUM","CSSignPower","CSFloorDiv"
]
