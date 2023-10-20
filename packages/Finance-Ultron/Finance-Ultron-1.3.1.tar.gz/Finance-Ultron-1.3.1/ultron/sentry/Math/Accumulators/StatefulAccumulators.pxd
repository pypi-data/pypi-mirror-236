# -*- coding: utf-8 -*-

cimport numpy as np
from ultron.sentry.Math.Accumulators.impl cimport Deque
from ultron.sentry.Math.Accumulators.IAccumulators cimport Accumulator


cdef class StatefulValueHolder(Accumulator):

    cdef public Deque _deque

    cpdef size_t size(self)
    cpdef bint isFull(self)


cdef class Shift(StatefulValueHolder):

    cdef public double _popout
    cdef public Accumulator _x

    cpdef int lag(self)
    cpdef push(self, dict data)
    cpdef double result(self)


cdef class Delta(StatefulValueHolder):

    cdef public double _popout
    cdef double _current
    cdef public Accumulator _x

    cpdef int lag(self)
    cpdef push(self, dict data)
    cpdef double result(self)


cdef class WAverage(StatefulValueHolder):
    cdef public double _average
    cdef public double _weight
    cdef public double _runningSum
    cdef public int _inner_window
    cdef public Accumulator _inner

    cpdef push(self, dict data)
    cpdef double result(self)
    

cdef class SingleValuedValueHolder(StatefulValueHolder):

    cdef public Accumulator _x


cdef class SortedValueHolder(SingleValuedValueHolder):

    cdef list _sortedArray
    cdef double _cur_pos
    cdef double _lastx
    cpdef push(self, dict data)


cdef class MovingMedian(SortedValueHolder):

    cpdef double result(self)

    
cdef class MovingMax(SortedValueHolder):

    cpdef double result(self)


cdef class MovingPercentage(SortedValueHolder):

    cpdef double result(self)

    
cdef class MovingArgMax(SortedValueHolder):

    cpdef double result(self)


cdef class MovingMin(SortedValueHolder):

    cpdef double result(self)


cdef class MovingArgMin(SortedValueHolder):

    cpdef double result(self)


cdef class MovingRank(SortedValueHolder):

    cpdef double result(self)


cdef class MovingQuantile(SortedValueHolder):

    cpdef double result(self)


cdef class MovingMaxDiff(SortedValueHolder):
    

    cdef public int _n

    cpdef double result(self)


cdef class MovingMinDiff(SortedValueHolder):
    
    cdef public int _n

    cpdef double result(self)

cdef class MovingMinMaxCps(SortedValueHolder):

    cdef public int _n

    cpdef double result(self)

cdef class MovingMinMaxDiff(SortedValueHolder):

    cdef public int _n
    
    cpdef double result(self)

cdef class MovingAllTrue(SingleValuedValueHolder):

    cdef public size_t _countedTrue

    cpdef push(self, dict data)
    cpdef double result(self)


cdef class MovingAnyTrue(SingleValuedValueHolder):

    cdef public size_t _countedTrue

    cpdef push(self, dict data)
    cpdef double result(self)


cdef class MovingAverageDiff(SingleValuedValueHolder):

    cdef public double _runningSum

    cdef public double _lastx

    cpdef push(self, dict data)
    cpdef double result(self)


cdef class MovingSum(SingleValuedValueHolder):

    cdef public double _runningSum

    cpdef push(self, dict data)
    cpdef double result(self)


cdef class MovingAverage(SingleValuedValueHolder):

    cdef public double _runningSum

    cpdef push(self, dict data)
    cpdef double result(self)


cdef class MovingDecay(SingleValuedValueHolder):
    cdef public double _runningSum
    cdef double _runningWeightedSum
    cdef double _newestValue

    cpdef push(self, dict data)
    cpdef double result(self)


cdef class MovingPositiveAverage(SingleValuedValueHolder):

    cdef public double _runningPositiveSum
    cdef public int _runningPositiveCount

    cpdef push(self, dict data)
    cpdef double result(self)


cdef class MovingPositiveDifferenceAverage(SingleValuedValueHolder):

    cdef public MovingAverage _runningAverage

    cpdef push(self, dict data)
    cpdef double result(self)


cdef class MovingNegativeDifferenceAverage(SingleValuedValueHolder):

    cdef public MovingAverage _runningAverage

    cpdef push(self, dict data)
    cpdef double result(self)


cdef class MovingRSI(SingleValuedValueHolder):

    cdef public MovingPositiveDifferenceAverage _posDiffAvg
    cdef public MovingNegativeDifferenceAverage _negDiffAvg

    cpdef push(self, dict data)
    cpdef double result(self)


cdef class MovingNegativeAverage(SingleValuedValueHolder):

    cdef public double _runningNegativeSum
    cdef public int _runningNegativeCount

    cpdef push(self, dict data)
    cpdef double result(self)


cdef class MovingVariance(SingleValuedValueHolder):

    cdef public double _runningSum
    cdef public double _runningSumSquare
    cdef public int _isPop

    cpdef push(self, dict data)
    cpdef double result(self)


cdef class MovingStandardDeviation(SingleValuedValueHolder):

    cdef public double _runningSum
    cdef public double _runningSumSquare
    cdef public int _isPop

    cpdef push(self, dict data)
    cpdef double result(self)


cdef class MovingZScore(SingleValuedValueHolder):

    cdef public double _runningSum
    cdef public double _runningSumSquare
    cdef public int _isPop
    cdef public double _lastx

    cpdef push(self, dict data)
    cpdef double result(self)


cdef class MovingIR(SingleValuedValueHolder):

    cdef public double _runningSum
    cdef public double _runningSumSquare
    cdef public int _isPop
    
    cpdef push(self, dict data)
    cpdef double result(self)


cdef class MovingKurtosis(SingleValuedValueHolder):
    cdef public double _runningSum
    cdef public double _runningSumFourthPower
    cdef public int _isPop

    cpdef push(self, dict data)
    cpdef double result(self)


cdef class MovingSkewness(SingleValuedValueHolder):
    cdef public double _runningSum
    cdef public double _runningSumSquare
    cdef public double _runningSumCube
    cdef public int _isPop

    cpdef push(self, dict data)
    cpdef double result(self)


cdef class MovingNegativeVariance(SingleValuedValueHolder):

    cdef public double _runningNegativeSum
    cdef public double _runningNegativeSumSquare
    cdef public int _runningNegativeCount
    cdef public int _isPop

    cpdef push(self, dict data)
    cpdef double result(self)


cdef class MovingCountedPositive(SingleValuedValueHolder):

    cdef public int _counts

    cpdef push(self, dict data)
    cpdef double result(self)


cdef class MovingCountedNegative(SingleValuedValueHolder):

    cdef public int _counts

    cpdef push(self, dict data)
    cpdef double result(self)


cdef class MovingCorrelation(StatefulValueHolder):

    cdef public double _runningSumLeft
    cdef public double _runningSumRight
    cdef public double _runningSumSquareLeft
    cdef public double _runningSumSquareRight
    cdef public double _runningSumCrossSquare
    cdef Accumulator _x
    cdef Accumulator _y
    cdef Deque _deque_y

    cpdef push(self, dict data)
    cpdef double result(self)


cdef class MovingProduct(SingleValuedValueHolder):

    cdef public double _runningProduct

    cpdef push(self, dict data)
    cpdef double result(self)


cdef class MovingConVariance(StatefulValueHolder):

    cdef public double _runningSumLeft
    cdef public double _runningSumRight
    cdef public double _runningSum
    cdef public double _runningSumSquareLeft
    cdef public double _runningSumSquareRight
    cdef Accumulator _x
    cdef Accumulator _y
    cdef Deque _deque_y
    cdef public int _isPop

    cpdef push(self, dict data)
    cpdef double result(self)

    
cdef class MACD(Accumulator):

    cdef public Accumulator _short_average
    cdef public Accumulator _long_average

    cpdef push(self, dict data)
    cpdef double result(self)


cdef class MovingLogReturn(SingleValuedValueHolder):

    cdef public double _runningReturn

    cpdef push(self, dict data)
    cpdef double result(self)


cdef class MovingSharp(StatefulValueHolder):

    cdef public MovingAverage _mean
    cdef public MovingVariance _var
    cdef Accumulator _x
    cdef Accumulator _y
    cdef Deque _deque_y

    cpdef push(self, dict data)
    cpdef double result(self)


cdef class MovingSortino(StatefulValueHolder):

    cdef public MovingAverage _mean
    cdef public MovingNegativeVariance _negativeVar
    cdef Accumulator _x
    cdef Accumulator _y
    cdef Deque _deque_y

    cpdef push(self, dict data)
    cpdef double result(self)


cdef class MovingDrawdown(StatefulValueHolder):

    cdef MovingMax _maxer
    cdef double _runningCum
    cdef double _currentMax
    cdef Accumulator _x

    cpdef push(self, dict data)
    cpdef double result(self)


cdef class MovingMaxDrawdown(StatefulValueHolder):

    cdef MovingDrawdown _drawdownCalculator
    cdef MovingMin _minimer
    cdef Accumulator _x

    cpdef push(self, dict data)
    cpdef double result(self)


cdef class MovingResidue(StatefulValueHolder):

    cdef public double _cross
    cdef public double _xsquare
    cdef public double _lastx
    cdef public double _lasty
    cdef Accumulator _x
    cdef Accumulator _y
    cdef Deque _deque_y

    cpdef push(self, dict data)
    cpdef double result(self)
    cpdef bint isFull(self)


cdef class MovingMeanResidue(StatefulValueHolder):
    cdef public double _cross
    cdef public double _xsquare
    cdef public double _runningx
    cdef public double _runningy

    cdef Accumulator _x
    cdef Accumulator _y
    cdef Deque _deque_y

    cpdef push(self, dict data)
    cpdef double result(self)
    cpdef bint isFull(self)


cdef class MovingCoef(StatefulValueHolder):
    cdef public double _cross
    cdef public double _xsquare
    cdef public double _lastx
    cdef public double _lasty
    cdef Accumulator _x
    cdef Accumulator _y
    cdef Deque _deque_y

    cpdef push(self, dict data)
    cpdef double result(self)
    cpdef bint isFull(self)

cdef class MovingRSquared(StatefulValueHolder):
    cdef public double _cross
    cdef public double _xsquare
    cdef public double _ysquare
    cdef public double _lastx
    cdef public double _lasty
    cdef Accumulator _x
    cdef Accumulator _y
    cdef Deque _deque_y

    cpdef push(self, dict data)
    cpdef double result(self)
    cpdef bint isFull(self)
