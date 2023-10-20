# -*- coding: utf-8 -*-

import copy
import numpy as np
cimport numpy as np
cimport cython
from ultron.sentry.Math.Accumulators.IAccumulators cimport Accumulator
from ultron.sentry.Analysis.SeriesValues cimport SeriesValues
from ultron.sentry.Analysis.SecurityValueHolders cimport SecuritySingleValueHolder
from ultron.sentry.Analysis.SecurityValueHolders cimport SecurityBinaryValueHolder
from ultron.sentry.Analysis.SecurityValueHolders cimport build_holder
from ultron.sentry.Math.Accumulators.StatefulAccumulators cimport MovingAverageDiff
from ultron.sentry.Math.Accumulators.StatefulAccumulators cimport MovingAverage
from ultron.sentry.Math.Accumulators.StatefulAccumulators cimport MovingDecay
from ultron.sentry.Math.Accumulators.StatefulAccumulators cimport MovingMedian
from ultron.sentry.Math.Accumulators.StatefulAccumulators cimport MovingPercentage
from ultron.sentry.Math.Accumulators.StatefulAccumulators cimport MovingMax
from ultron.sentry.Math.Accumulators.StatefulAccumulators cimport MovingArgMax
from ultron.sentry.Math.Accumulators.StatefulAccumulators cimport MovingMin
from ultron.sentry.Math.Accumulators.StatefulAccumulators cimport MovingArgMin
from ultron.sentry.Math.Accumulators.StatefulAccumulators cimport MovingRank
from ultron.sentry.Math.Accumulators.StatefulAccumulators cimport MovingQuantile
from ultron.sentry.Math.Accumulators.StatefulAccumulators cimport MovingIR
from ultron.sentry.Math.Accumulators.StatefulAccumulators cimport MovingSkewness
from ultron.sentry.Math.Accumulators.StatefulAccumulators cimport MovingKurtosis
from ultron.sentry.Math.Accumulators.StatefulAccumulators cimport MovingZScore
from ultron.sentry.Math.Accumulators.StatefulAccumulators cimport MovingMaxDiff
from ultron.sentry.Math.Accumulators.StatefulAccumulators cimport MovingMinDiff
from ultron.sentry.Math.Accumulators.StatefulAccumulators cimport MovingMinMaxCps
from ultron.sentry.Math.Accumulators.StatefulAccumulators cimport MovingMinMaxDiff
from ultron.sentry.Math.Accumulators.StatefulAccumulators cimport MovingAllTrue
from ultron.sentry.Math.Accumulators.StatefulAccumulators cimport MovingAnyTrue
from ultron.sentry.Math.Accumulators.StatefulAccumulators cimport MovingSum
from ultron.sentry.Math.Accumulators.StatefulAccumulators cimport MovingProduct
from ultron.sentry.Math.Accumulators.StatefulAccumulators cimport MovingVariance
from ultron.sentry.Math.Accumulators.StatefulAccumulators cimport MovingStandardDeviation
from ultron.sentry.Math.Accumulators.StatefulAccumulators cimport MovingCountedPositive
from ultron.sentry.Math.Accumulators.StatefulAccumulators cimport MovingPositiveAverage
from ultron.sentry.Math.Accumulators.StatefulAccumulators cimport MovingCountedNegative
from ultron.sentry.Math.Accumulators.StatefulAccumulators cimport MovingNegativeAverage
from ultron.sentry.Math.Accumulators.StatefulAccumulators cimport MovingPositiveDifferenceAverage
from ultron.sentry.Math.Accumulators.StatefulAccumulators cimport MovingNegativeDifferenceAverage
from ultron.sentry.Math.Accumulators.StatefulAccumulators cimport MovingRSI
from ultron.sentry.Math.Accumulators.StatefulAccumulators cimport MovingCorrelation
from ultron.sentry.Math.Accumulators.StatefulAccumulators cimport MovingResidue
from ultron.sentry.Math.Accumulators.StatefulAccumulators cimport MovingMeanResidue
from ultron.sentry.Math.Accumulators.StatefulAccumulators cimport MovingConVariance
from ultron.sentry.Math.Accumulators.StatefulAccumulators cimport MovingCoef
from ultron.sentry.Math.Accumulators.StatefulAccumulators cimport MovingRSquared
from ultron.sentry.Math.Accumulators.StatefulAccumulators cimport MovingLogReturn
from ultron.sentry.Math.Accumulators.StatefulAccumulators cimport MovingSharp
from ultron.sentry.Math.Accumulators.StatefulAccumulators cimport MovingSortino
from ultron.sentry.Math.Accumulators.StatefulAccumulators cimport MovingMaxDrawdown
from ultron.sentry.Math.Accumulators.StatefulAccumulators cimport MovingDrawdown
from ultron.sentry.Math.MathConstants cimport NAN



cdef class SecurityMovingAverageDiff(SecuritySingleValueHolder):
    def __init__(self, window, x):
        super(SecurityMovingAverageDiff, self).__init__(window, MovingAverageDiff, x)

    def __str__(self):
        if self._compHolder:
            return "\\mathrm{{MADiff}}({0}, {1})".format(self._window - self._compHolder.window, str(self._compHolder))
        else:
            return str(self._holderTemplate)


cdef class SecurityMovingAverage(SecuritySingleValueHolder):
    def __init__(self, window, x):
        super(SecurityMovingAverage, self).__init__(window, MovingAverage, x)

    def __str__(self):
        if self._compHolder:
            return "\\mathrm{{MA}}({0}, {1})".format(self._window - self._compHolder.window, str(self._compHolder))
        else:
            return str(self._holderTemplate)


cdef class SecurityMovingDecay(SecuritySingleValueHolder):
    def __init__(self, window, x):
        super(SecurityMovingDecay, self).__init__(window, MovingDecay, x)

    def __str__(self):
        if self._compHolder:
            return "\\mathrm{{MADecay}}({0}, {1})".format(self._window - self._compHolder.window, str(self._compHolder))
        else:
            return str(self._holderTemplate)


cdef class SecurityMovingPercentage(SecuritySingleValueHolder):
    def __init__(self, window, x):
        super(SecurityMovingPercentage, self).__init__(window, MovingPercentage, x)

    def __str__(self):
        if self._compHolder:
            return "\\mathrm{{MPercent}}({0}, {1})".format(self._window - self._compHolder.window, str(self._compHolder))
        else:
            return str(self._holderTemplate)

cdef class SecurityMovingMedian(SecuritySingleValueHolder):
    def __init__(self, window, x):
        super(SecurityMovingMedian, self).__init__(window, MovingMedian, x)

    def __str__(self):
        if self._compHolder:
            return "\\mathrm{{MMedian}}({0}, {1})".format(self._window - self._compHolder.window, str(self._compHolder))
        else:
            return str(self._holderTemplate)

cdef class SecurityMovingMax(SecuritySingleValueHolder):
    def __init__(self, window, x):
        super(SecurityMovingMax, self).__init__(window, MovingMax, x)

    def __str__(self):
        if self._compHolder:
            return "\\mathrm{{MMax}}({0}, {1})".format(self._window - self._compHolder.window, str(self._compHolder))
        else:
            return str(self._holderTemplate)


cdef class SecurityMovingArgMax(SecuritySingleValueHolder):
    def __init__(self, window, x):
        super(SecurityMovingArgMax, self).__init__(window, MovingArgMax, x)

    def __str__(self):
        if self._compHolder:
            return "\\mathrm{{MArgMax}}({0}, {1})".format(self._window - self._compHolder.window, str(self._compHolder))
        else:
            return str(self._holderTemplate)


cdef class SecurityMovingMin(SecuritySingleValueHolder):
    def __init__(self, window, x):
        super(SecurityMovingMin, self).__init__(window, MovingMin, x)

    def __str__(self):
        if self._compHolder:
            return "\\mathrm{{MMin}}({0}, {1})".format(self._window - self._compHolder.window, str(self._compHolder))
        else:
            return str(self._holderTemplate)


cdef class SecurityMovingArgMin(SecuritySingleValueHolder):
    def __init__(self, window, x):
        super(SecurityMovingArgMin, self).__init__(window, MovingArgMin, x)

    def __str__(self):
        if self._compHolder:
            return "\\mathrm{{MArgMin}}({0}, {1})".format(self._window - self._compHolder.window, str(self._compHolder))
        else:
            return str(self._holderTemplate)


cdef class SecurityMovingRank(SecuritySingleValueHolder):
    def __init__(self, window, x):
        super(SecurityMovingRank, self).__init__(window, MovingRank, x)

    def __str__(self):
        if self._compHolder:
            return "\\mathrm{{MRank}}({0}, {1})".format(self._window - self._compHolder.window, str(self._compHolder))
        else:
            return str(self._holderTemplate)


cdef class SecurityMovingQuantile(SecuritySingleValueHolder):
    def __init__(self, window, x):
        super(SecurityMovingQuantile, self).__init__(window, MovingQuantile, x)

    def __str__(self):
        if self._compHolder:
            return "\\mathrm{{MQuantile}}({0}, {1})".format(self._window - self._compHolder.window, str(self._compHolder))
        else:
            return str(self._holderTemplate)

cdef class SecurityMovingMaxDiff(SecuritySingleValueHolder):
    def __init__(self, window, x):
        super(SecurityMovingMaxDiff, self).__init__(window, MovingMaxDiff, x)
    
    def __str__(self):
        if self._compHolder:
            return "\\mathrm{{MMaxDiff}}({0}, {1})".format(self._window - self._compHolder.window, str(self._compHolder))
        else:
            return str(self._holderTemplate)

cdef class SecurityMovingMinDiff(SecuritySingleValueHolder):
    def __init__(self, window, x):
        super(SecurityMovingMinDiff, self).__init__(window, MovingMinDiff, x)
    
    def __str__(self):
        if self._compHolder:
            return "\\mathrm{{MMinDiff}}({0}, {1})".format(self._window - self._compHolder.window, str(self._compHolder))
        else:
            return str(self._holderTemplate)

cdef class SecurityMovingMinMaxCps(SecuritySingleValueHolder):
    def __init__(self, window, x):
        super(SecurityMovingMinMaxCps, self).__init__(window, MovingMinMaxCps, x)
    
    def __str__(self):
        if self._compHolder:
            return "\\mathrm{{MCPS}}({0}, {1})".format(self._window - self._compHolder.window, str(self._compHolder))
        else:
            return str(self._holderTemplate)

cdef class SecurityMovingMinMaxDiff(SecuritySingleValueHolder):
    def __init__(self, window, x):
        super(SecurityMovingMinMaxDiff, self).__init__(window, MovingMinMaxDiff, x)
    
    def __str__(self):
        if self._compHolder:
            return "\\mathrm{{MDIFF}}({0}, {1})".format(self._window - self._compHolder.window, str(self._compHolder))
        else:
            return str(self._holderTemplate)

cdef class SecurityMovingAllTrue(SecuritySingleValueHolder):
    def __init__(self, window, x):
        super(SecurityMovingAllTrue, self).__init__(window, MovingAllTrue, x)

    def __str__(self):
        if self._compHolder:
            return "\\mathrm{{MAllTrue}}({0}, {1})".format(self._window - self._compHolder.window, str(self._compHolder))
        else:
            return str(self._holderTemplate)


cdef class SecurityMovingAnyTrue(SecuritySingleValueHolder):
    def __init__(self, window, x):
        super(SecurityMovingAnyTrue, self).__init__(window, MovingAnyTrue, x)

    def __str__(self):
        if self._compHolder:
            return "\\mathrm{{MAnyTrue}}({0}, {1})".format(self._window - self._compHolder.window, str(self._compHolder))
        else:
            return str(self._holderTemplate)


cdef class SecurityMovingSum(SecuritySingleValueHolder):
    def __init__(self, window, x):
        super(SecurityMovingSum, self).__init__(window, MovingSum, x)

    def __str__(self):
        if self._compHolder:
            return "\\mathrm{{MSum}}({0}, {1})".format(self._window - self._compHolder.window, str(self._compHolder))
        else:
            return str(self._holderTemplate)

cdef class SecurityMovingProduct(SecuritySingleValueHolder):
    def __init__(self, window, x):
        super(SecurityMovingProduct, self).__init__(window, MovingProduct, x)
    
    def __str__(self):
        if self._compHolder:
            return "\\mathrm{{MPro}}({0}, {1})".format(self._window - self._compHolder.window, str(self._compHolder))
        else:
            return str(self._holderTemplate)

cdef class SecurityMovingVariance(SecuritySingleValueHolder):
    def __init__(self, window, x):
        super(SecurityMovingVariance, self).__init__(window, MovingVariance, x)

    def __str__(self):
        if self._compHolder:
            return "\\mathrm{{MVariance}}({0}, {1})".format(self._window - self._compHolder.window, str(self._compHolder))
        else:
            return str(self._holderTemplate)

cdef class SecurityMovingIR(SecuritySingleValueHolder):
    def __init__(self, window, x):
        super(SecurityMovingIR, self).__init__(window, MovingIR, x)

    def __str__(self):
        if self._compHolder:
            return "\\mathrm{{MIR}}({0}, {1})".format(self._window - self._compHolder.window, str(self._compHolder))
        else:
            return str(self._holderTemplate)


cdef class SecurityMovingKurtosis(SecuritySingleValueHolder):
    def __init__(self, window, x):
        super(SecurityMovingKurtosis, self).__init__(window, MovingKurtosis, x)

    def __str__(self):
        if self._compHolder:
            return "\\mathrm{{MKURT}}({0}, {1})".format(self._window - self._compHolder.window, str(self._compHolder))
        else:
            return str(self._holderTemplate)

cdef class SecurityMovingSkewness(SecuritySingleValueHolder):
    def __init__(self, window, x):
        super(SecurityMovingSkewness, self).__init__(window, MovingSkewness, x)

    def __str__(self):
        if self._compHolder:
            return "\\mathrm{{MSKEW}}({0}, {1})".format(self._window - self._compHolder.window, str(self._compHolder))
        else:
            return str(self._holderTemplate)


cdef class SecurityMovingZScore(SecuritySingleValueHolder):
    def __init__(self, window, x):
        super(SecurityMovingZScore, self).__init__(window, MovingZScore, x)

    def __str__(self):
        if self._compHolder:
            return "\\mathrm{{MZscore}}({0}, {1})".format(self._window - self._compHolder.window, str(self._compHolder))
        else:
            return str(self._holderTemplate)


cdef class SecurityMovingStandardDeviation(SecuritySingleValueHolder):
    def __init__(self, window, x):
        super(SecurityMovingStandardDeviation, self).__init__(window, MovingStandardDeviation, x)

    def __str__(self):
        if self._compHolder:
            return "\\mathrm{{MStd}}({0}, {1})".format(self._window - self._compHolder.window, str(self._compHolder))
        else:
            return str(self._holderTemplate)


cdef class SecurityMovingCountedPositive(SecuritySingleValueHolder):
    def __init__(self, window, x):
        super(SecurityMovingCountedPositive, self).__init__(window, MovingCountedPositive, x)

    def __str__(self):
        if self._compHolder:
            return "\\mathrm{{MNPositive}}({0}, {1})".format(self._window - self._compHolder.window, str(self._compHolder))
        else:
            return str(self._holderTemplate)


cdef class SecurityMovingPositiveAverage(SecuritySingleValueHolder):
    def __init__(self, window, x):
        super(SecurityMovingPositiveAverage, self).__init__(window, MovingPositiveAverage, x)

    def __str__(self):
        if self._compHolder:
            return "\\mathrm{{MAPositive}}({0}, {1})".format(self._window - self._compHolder.window, str(self._compHolder))
        else:
            return str(self._holderTemplate)


cdef class SecurityMovingCountedNegative(SecuritySingleValueHolder):
    def __init__(self, window, x):
        super(SecurityMovingCountedNegative, self).__init__(window, MovingCountedNegative, x)

    def __str__(self):
        if self._compHolder:
            return "\\mathrm{{MNNegative}}({0}, {1})".format(self._window - self._compHolder.window, str(self._compHolder))
        else:
            return str(self._holderTemplate)


cdef class SecurityMovingNegativeAverage(SecuritySingleValueHolder):
    def __init__(self, window, x):
        super(SecurityMovingNegativeAverage, self).__init__(window, MovingNegativeAverage, x)

    def __str__(self):
        if self._compHolder:
            return "\\mathrm{{MANegative}}({0}, {1})".format(self._window - self._compHolder.window, str(self._compHolder))
        else:
            return str(self._holderTemplate)


cdef class SecurityMovingPositiveDifferenceAverage(SecuritySingleValueHolder):
    def __init__(self, window, x):
        super(SecurityMovingPositiveDifferenceAverage, self).__init__(window, MovingPositiveDifferenceAverage, x)


cdef class SecurityMovingNegativeDifferenceAverage(SecuritySingleValueHolder):
    def __init__(self, window, x):
        super(SecurityMovingNegativeDifferenceAverage, self).__init__(window, MovingNegativeDifferenceAverage, x)


cdef class SecurityMovingRSI(SecuritySingleValueHolder):
    def __init__(self, window, x):
        super(SecurityMovingRSI, self).__init__(window, MovingRSI, x)

    def __str__(self):
        if self._compHolder:
            return "\\mathrm{{MRSI}}({0}, {1})".format(self._window - self._compHolder.window, str(self._compHolder))
        else:
            return str(self._holderTemplate)


cdef class SecurityMovingLogReturn(SecuritySingleValueHolder):
    def __init__(self, window, x):
        super(SecurityMovingLogReturn, self).__init__(window, MovingLogReturn, x)


cdef class SecurityMovingMaxDrawdown(SecuritySingleValueHolder):
    def __init__(self, window, x):
        super(SecurityMovingMaxDrawdown, self).__init__(window, MovingDrawdown, x)


cdef class SecurityMovingMovingDrawdown(SecuritySingleValueHolder):
    def __init__(self, window, x):
        super(SecurityMovingMovingDrawdown, self).__init__(window, MovingMaxDrawdown, x)


cdef class SecurityMovingSortino(SecurityBinaryValueHolder):
    def __init__(self, window, x, y):
        super(SecurityMovingSortino, self).__init__(window, MovingSortino, x, y)
        
    def __str__(self):
        return str(self._holderTemplate)

cdef class SecurityMovingSharp(SecurityBinaryValueHolder):
    def __init__(self, window, x, y):
        super(SecurityMovingSharp, self).__init__(window, MovingSharp, x, y)

    def __str__(self):
        return str(self._holderTemplate)

cdef class SecurityMovingResidue(SecurityBinaryValueHolder):
    def __init__(self, window, x, y):
        super(SecurityMovingResidue, self).__init__(window, MovingResidue, x, y)

    def __str__(self):
        return str(self._holderTemplate)


cdef class SecurityMovingMeanResidue(SecurityBinaryValueHolder):
    def __init__(self, window, x, y):
        super(SecurityMovingMeanResidue, self).__init__(window, MovingMeanResidue, x, y)

    def __str__(self):
        return str(self._holderTemplate)


cdef class SecurityMovingConVariance(SecurityBinaryValueHolder):
    def __init__(self, window, x, y):
        super(SecurityMovingConVariance, self).__init__(window, MovingConVariance, x, y)

    def __str__(self):
        return str(self._holderTemplate)



cdef class SecurityMovingCoef(SecurityBinaryValueHolder):
    def __init__(self, window, x, y):
        super(SecurityMovingCoef, self).__init__(window, MovingCoef, x, y)

    def __str__(self):
        return str(self._holderTemplate)


cdef class SecurityMovingRSquared(SecurityBinaryValueHolder):
    def __init__(self, window, x, y):
        super(SecurityMovingRSquared, self).__init__(window, MovingRSquared, x, y)

    def __str__(self):
        return str(self._holderTemplate)


cdef class SecurityMovingCorrelation(SecurityBinaryValueHolder):
    def __init__(self, window, x, y):
        super(SecurityMovingCorrelation, self).__init__(window, MovingCorrelation, x, y)

    def __str__(self):
        return str(self._holderTemplate)

