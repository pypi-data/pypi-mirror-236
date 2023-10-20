# -*- coding: utf-8 -*-


import copy
import six
import numpy as np
cimport numpy as np
cimport cython
from ultron.sentry.Analysis.SeriesValues cimport SeriesValues
from ultron.sentry.Analysis.SecurityValueHolders cimport SecurityValueHolder
from ultron.sentry.Analysis.SecurityValueHolders import build_holder
from ultron.sentry.Math.MathConstants cimport NAN


cdef class CrossSectionValueHolder(SecurityValueHolder):

    cdef public SecurityValueHolder _inner
    cdef public SecurityValueHolder _group

    def __init__(self, innerValue, groups=None):
        super(CrossSectionValueHolder, self).__init__()
        self._inner = build_holder(innerValue)
        self._group = build_holder(groups) if groups else None
        if self._group:
            self._window = max(self._inner.window, self._group.window)
            self._dependency = list(set(self._inner.fields + self._group.fields))
        else:
            self._window = self._inner.window
            self._dependency = copy.deepcopy(self._inner.fields)
        self.updated = 0
        self.cached = None

    @property
    def symbolList(self):
        return self._inner.symbolList

    cpdef push(self, dict data):
        self._inner.push(data)
        if self._group:
            self._group.push(data)
        self.updated = 0


cdef class CSTopNSecurityValueHolder(CrossSectionValueHolder):

    cdef int _n;

    def __init__(self, innerValue, n, groups=None):
        super(CSTopNSecurityValueHolder, self).__init__(innerValue, groups)
        self._n = n

    cdef _cal_impl(self):
        cdef SeriesValues raw_values = self._inner.value_all()

        if self._group:
            self.cached = raw_values.top_n(self._n, self._group.value_all())
        else:
            self.cached = raw_values.top_n(self._n)
        self.updated = 1

    cpdef value_all(self):
        if self.updated:
            return self.cached
        else:
            self._cal_impl()
            return self.cached

    cpdef double value_by_name(self, name):
        if self.updated:
            return self.cached[name]
        else:
            self._cal_impl()
            return self.cached[name]

    cpdef SeriesValues value_by_names(self, list names):
        cdef SeriesValues raw_values = self._inner.value_by_names(names)
        if self._group:
            raw_values = raw_values.top_n(self._n, self._group.value_by_names(names))
        else:
            raw_values = raw_values.top_n(self._n)
        return raw_values

    def __str__(self):
        if self._group:
            return "\mathrm{{CSTopN}}({0}, {1}, groups={2})".format(str(self._inner), self._n, str(self._group))
        else:
            return "\mathrm{{CSTopN}}({0}, {1})".format(str(self._inner), self._n)


cdef class CSTopNPercentileSecurityValueHolder(CrossSectionValueHolder):

    cdef double _n;

    def __init__(self, innerValue, n, groups=None):
        super(CSTopNPercentileSecurityValueHolder, self).__init__(innerValue, groups)
        self._n = n

    cdef _cal_impl(self):
        cdef SeriesValues raw_values = self._inner.value_all()

        if self._group:
            self.cached = raw_values.top_n_percentile(self._n, self._group.value_all())
        else:
            self.cached = raw_values.top_n_percentile(self._n)
        self.updated = 1

    cpdef value_all(self):
        if self.updated:
            return self.cached
        else:
            self._cal_impl()
            return self.cached

    cpdef double value_by_name(self, name):
        if self.updated:
            return self.cached[name]
        else:
            self._cal_impl()
            return self.cached[name]

    cpdef SeriesValues value_by_names(self, list names):
        cdef SeriesValues raw_values = self._inner.value_by_names(names)
        if self._group:
            raw_values = raw_values.top_n_percentile(self._n, self._group.value_by_names(names))
        else:
            raw_values = raw_values.top_n_percentile(self._n)
        return raw_values

    def __str__(self):
        if self._group:
            return "\mathrm{{CSTopNPercentile}}({0}, {1}, groups={2})".format(str(self._inner), self._n, str(self._group))
        else:
            return "\mathrm{{CSTopNPercentile}}({0}, {1})".format(str(self._inner), self._n)


cdef class CSBottomNSecurityValueHolder(CrossSectionValueHolder):

    cdef int _n;

    def __init__(self, innerValue, n, groups=None):
        super(CSBottomNSecurityValueHolder, self).__init__(innerValue, groups)
        self._n = n

    cdef _cal_impl(self):
        cdef SeriesValues raw_values = self._inner.value_all()

        if self._group:
            self.cached = raw_values.bottom_n(self._n, self._group.value_all())
        else:
            self.cached = raw_values.bottom_n(self._n)
        self.updated = 1

    cpdef value_all(self):
        if self.updated:
            return self.cached
        else:
            self._cal_impl()
            return self.cached

    cpdef double value_by_name(self, name):
        if self.updated:
            return self.cached[name]
        else:
            self._cal_impl()
            return self.cached[name]

    cpdef SeriesValues value_by_names(self, list names):
        cdef SeriesValues raw_values = self._inner.value_by_names(names)
        if self._group:
            raw_values = raw_values.bottom_n(self._n, self._group.value_by_names(names))
        else:
            raw_values = raw_values.bottom_n(self._n)
        return raw_values

    def __str__(self):
        if self._group:
            return "\mathrm{{CSBottomN}}({0}, {1}, groups={2})".format(str(self._inner), self._n, str(self._group))
        else:
            return "\mathrm{{CSBottomN}}({0}, {1})".format(str(self._inner), self._n)


cdef class CSBottomNPercentileSecurityValueHolder(CrossSectionValueHolder):

    cdef double _n;

    def __init__(self, innerValue, n, groups=None):
        super(CSBottomNPercentileSecurityValueHolder, self).__init__(innerValue, groups)
        self._n = n

    cdef _cal_impl(self):
        cdef SeriesValues raw_values = self._inner.value_all()

        if self._group:
            self.cached = raw_values.bottom_n_percentile(self._n, self._group.value_all())
        else:
            self.cached = raw_values.bottom_n_percentile(self._n)
        self.updated = 1

    cpdef value_all(self):
        if self.updated:
            return self.cached
        else:
            self._cal_impl()
            return self.cached

    cpdef double value_by_name(self, name):
        if self.updated:
            return self.cached[name]
        else:
            self._cal_impl()
            return self.cached[name]

    cpdef SeriesValues value_by_names(self, list names):
        cdef SeriesValues raw_values = self._inner.value_by_names(names)
        if self._group:
            raw_values = raw_values.bottom_n_percentile(self._n, self._group.value_by_names(names))
        else:
            raw_values = raw_values.bottom_n_percentile(self._n)
        return raw_values

    def __str__(self):
        if self._group:
            return "\mathrm{{CSBottomNPercentile}}({0}, {1}, groups={2})".format(str(self._inner), self._n, str(self._group))
        else:
            return "\mathrm{{CSBottomNPercentile}}({0}, {1})".format(str(self._inner), self._n)


cdef class CSSoftmaxSecurityValueHolder(CrossSectionValueHolder):
    def __init__(self, innerValue, groups=None):
        super(CSSoftmaxSecurityValueHolder, self).__init__(innerValue, groups)

    cdef _cal_impl(self):
        cdef SeriesValues raw_values = self._inner.value_all()

        if self._group:
            self.cached = raw_values.softmax(self._group.value_all())
        else:
            self.cached = raw_values.softmax()
        self.updated = 1

    cpdef value_all(self):
        if self.updated:
            return self.cached
        else:
            self._cal_impl()
            return self.cached

    cpdef double value_by_name(self, name):
        if self.updated:
            return self.cached[name]
        else:
            self._cal_impl()
            return self.cached[name]

    cpdef SeriesValues value_by_names(self, list names):
        cdef SeriesValues raw_values = self._inner.value_by_names(names)
        if self._group:
            raw_values = raw_values.softmax(self._group.value_by_names(names))
        else:
            raw_values = raw_values.softmax()
        return raw_values

    def __str__(self):
        if self._group:
            return "\mathrm{{CSSoftmax}}({0}, groups={1})".format(str(self._inner), str(self._group))
        else:
            return "\mathrm{{CSSoftmax}}({0})".format(str(self._inner))

cdef class CSDemeanSecurityValueHolder(CrossSectionValueHolder):
    
    def __init__(self, innerValue, groups=None):
        super(CSDemeanSecurityValueHolder, self).__init__(innerValue, groups)

    cdef _cal_impl(self):
        cdef SeriesValues raw_values = self._inner.value_all()

        if self._group:
            self.cached = raw_values.demean(self._group.value_all())
        else:
            self.cached = raw_values.demean()
        self.updated = 1

    cpdef value_all(self):
        if self.updated:
            return self.cached
        else:
            self._cal_impl()
            return self.cached

    cpdef double value_by_name(self, name):
        if self.updated:
            return self.cached[name]
        else:
            self._cal_impl()
            return self.cached[name]

    cpdef SeriesValues value_by_names(self, list names):
        cdef SeriesValues raw_values = self._inner.value_by_names(names)
        if self._group:
            raw_values = raw_values.demean(self._group.value_by_names(names))
        else:
            raw_values = raw_values.demean()
        return raw_values

    def __str__(self):
        if self._group:
            return "\mathrm{{CSDeman}}({0}, groups={1})".format(str(self._inner), str(self._group))
        else:
            return "\mathrm{{CSDeman}}({0})".format(str(self._inner))


cdef class CSRankedSecurityValueHolder(CrossSectionValueHolder):

    def __init__(self, innerValue, groups=None):
        super(CSRankedSecurityValueHolder, self).__init__(innerValue, groups)

    cdef _cal_impl(self):
        cdef SeriesValues raw_values = self._inner.value_all()

        if self._group:
            self.cached = raw_values.rank(self._group.value_all())
        else:
            self.cached = raw_values.rank()
        self.updated = 1

    cpdef value_all(self):
        if self.updated:
            return self.cached
        else:
            self._cal_impl()
            return self.cached

    cpdef double value_by_name(self, name):
        if self.updated:
            return self.cached[name]
        else:
            self._cal_impl()
            return self.cached[name]

    cpdef SeriesValues value_by_names(self, list names):
        cdef SeriesValues raw_values = self._inner.value_by_names(names)
        if self._group:
            raw_values = raw_values.rank(self._group.value_by_names(names))
        else:
            raw_values = raw_values.rank()
        return raw_values

    def __str__(self):
        if self._group:
            return "\mathrm{{CSRank}}({0}, groups={1})".format(str(self._inner), str(self._group))
        else:
            return "\mathrm{{CSRank}}({0})".format(str(self._inner))

cdef class CSInverseSecurityValueHolder(CrossSectionValueHolder):
    def __init__(self, innerValue, groups=None):
        super(CSInverseSecurityValueHolder, self).__init__(innerValue, groups)

    cdef _cal_impl(self):
        cdef SeriesValues raw_values = self._inner.value_all()
        self.cached = ~raw_values
        self.updated = 1

    cpdef value_all(self):
        if self.updated:
            return self.cached
        else:
            self._cal_impl()
            return self.cached
    
    cpdef double value_by_name(self, name):
        if self.updated:
            return self.cached[name]
        else:
            self._cal_impl()
            return self.cached[name]
    
    cpdef SeriesValues value_by_names(self, list names):
        cdef SeriesValues raw_values = self._inner.value_by_names(names)
        raw_values= ~raw_values
        return  raw_values

    def __str__(self):
        if self._group:
            return "\mathrm{{CSInverse}}({0}, groups={1})".format(str(self._inner), str(self._group))
        else:
            return "\mathrm{{CSInverse}}({0})".format(str(self._inner))

cdef class CSReverseSecurityValueHolder(CrossSectionValueHolder):
    
    def __init__(self, innerValue, groups=None):
        super(CSReverseSecurityValueHolder, self).__init__(innerValue, groups)
    
    cdef _cal_impl(self):
        cdef SeriesValues raw_values = self._inner.value_all()
        self.cached = -raw_values
        self.updated = 1
    
    cpdef value_all(self):
        if self.updated:
            return self.cached
        else:
            self._cal_impl()
            return self.cached
    
    cpdef double value_by_name(self, name):
        if self.updated:
            return self.cached[name]
        else:
            self._cal_impl()
            return self.cached[name]

    cpdef SeriesValues value_by_names(self, list names):
        cdef SeriesValues raw_values = self._inner.value_by_names(names)
        raw_values= -raw_values
        return  raw_values

    def __str__(self):
        if self._group:
            return "\mathrm{{CSReverse}}({0}, groups={1})".format(str(self._inner), str(self._group))
        else:
            return "\mathrm{{CSReverse}}({0})".format(str(self._inner))

cdef class CSSumSecurityValueHolder(CrossSectionValueHolder):
    def __init__(self, innerValue, groups=None):
        super(CSSumSecurityValueHolder, self).__init__(innerValue, groups)

    cdef _cal_impl(self):
        cdef SeriesValues raw_values = self._inner.value_all()

        if self._group:
            self.cached = raw_values.sum(self._group.value_all())
        else:
            self.cached = raw_values.sum()
        self.updated = 1

    cpdef value_all(self):
        if self.updated:
            return self.cached
        else:
            self._cal_impl()
            return self.cached

    cpdef double value_by_name(self, name):
        if self.updated:
            return self.cached[name]
        else:
            self._cal_impl()
            return self.cached[name]

    cpdef SeriesValues value_by_names(self, list names):
        cdef SeriesValues raw_values = self._inner.value_by_names(names)
        if self._group:
            raw_values = raw_values.sum(self._group.value_by_names(names))
        else:
            raw_values = raw_values.sum()
        return raw_values

    def __str__(self):
        if self._group:
            return "\mathrm{{CSSum}}({0}, groups={1})".format(str(self._inner), str(self._group))
        else:
            return "\mathrm{{CSSum}}({0})".format(str(self._inner))

cdef class CSSkewSecurityValueHolder(CrossSectionValueHolder):
    def __init__(self, innerValue, groups=None):
        super(CSSkewSecurityValueHolder, self).__init__(innerValue, groups)

    cdef _cal_impl(self):
        cdef SeriesValues raw_values = self._inner.value_all()

        if self._group:
            self.cached = raw_values.skew(self._group.value_all())
        else:
            self.cached = raw_values.skew()
        self.updated = 1

    cpdef value_all(self):
        if self.updated:
            return self.cached
        else:
            self._cal_impl()
            return self.cached

    cpdef double value_by_name(self, name):
        if self.updated:
            return self.cached[name]
        else:
            self._cal_impl()
            return self.cached[name]

    cpdef SeriesValues value_by_names(self, list names):
        cdef SeriesValues raw_values = self._inner.value_by_names(names)
        if self._group:
            raw_values = raw_values.skew(self._group.value_by_names(names))
        else:
            raw_values = raw_values.skew()
        return raw_values

    def __str__(self):
        if self._group:
            return "\mathrm{{CSSkew}}({0}, groups={1})".format(str(self._inner), str(self._group))
        else:
            return "\mathrm{{CSSkew}}({0})".format(str(self._inner))


cdef class CSStdSecurityValueHolder(CrossSectionValueHolder):
    def __init__(self, innerValue, groups=None):
        super(CSStdSecurityValueHolder, self).__init__(innerValue, groups)

    cdef _cal_impl(self):
        cdef SeriesValues raw_values = self._inner.value_all()

        if self._group:
            self.cached = raw_values.std(self._group.value_all())
        else:
            self.cached = raw_values.std()
        self.updated = 1

    cpdef value_all(self):
        if self.updated:
            return self.cached
        else:
            self._cal_impl()
            return self.cached

    cpdef double value_by_name(self, name):
        if self.updated:
            return self.cached[name]
        else:
            self._cal_impl()
            return self.cached[name]

    cpdef SeriesValues value_by_names(self, list names):
        cdef SeriesValues raw_values = self._inner.value_by_names(names)
        if self._group:
            raw_values = raw_values.std(self._group.value_by_names(names))
        else:
            raw_values = raw_values.std()
        return raw_values

    def __str__(self):
        if self._group:
            return "\mathrm{{CSStd}}({0}, groups={1})".format(str(self._inner), str(self._group))
        else:
            return "\mathrm{{CSStd}}({0})".format(str(self._inner))


cdef class CSAverageSecurityValueHolder(CrossSectionValueHolder):
    def __init__(self, innerValue, groups=None):
        super(CSAverageSecurityValueHolder, self).__init__(innerValue, groups)

    cdef _cal_impl(self):
        cdef SeriesValues raw_values = self._inner.value_all()

        if self._group:
            self.cached = raw_values.mean(self._group.value_all())
        else:
            self.cached = raw_values.mean()
        self.updated = 1

    cpdef value_all(self):
        if self.updated:
            return self.cached
        else:
            self._cal_impl()
            return self.cached

    cpdef double value_by_name(self, name):
        if self.updated:
            return self.cached[name]
        else:
            self._cal_impl()
            return self.cached[name]

    cpdef SeriesValues value_by_names(self, list names):
        cdef SeriesValues raw_values = self._inner.value_by_names(names)
        if self._group:
            raw_values = raw_values.mean(self._group.value_by_names(names))
        else:
            raw_values = raw_values.mean()
        return raw_values

    def __str__(self):
        if self._group:
            return "\mathrm{{CSMean}}({0}, groups={1})".format(str(self._inner), str(self._group))
        else:
            return "\mathrm{{CSMean}}({0})".format(str(self._inner))


cdef class CSPercentileSecurityValueHolder(CrossSectionValueHolder):

    def __init__(self, innerValue, groups=None):
        super(CSPercentileSecurityValueHolder, self).__init__(innerValue, groups)

    cdef _cal_impl(self):
        cdef SeriesValues raw_values = self._inner.value_all()

        if self._group:
            self.cached = raw_values.percentile(self._group.value_all())
        else:
            self.cached = raw_values.percentile()
        self.updated = 1

    cpdef value_all(self):
        if self.updated:
            return self.cached
        else:
            self._cal_impl()
            return self.cached

    cpdef double value_by_name(self, name):
        if self.updated:
            return self.cached[name]
        else:
            self._cal_impl()
            return self.cached[name]

    cpdef SeriesValues value_by_names(self, list names):
        cdef SeriesValues raw_values = self._inner.value_by_names(names)
        if self._group:
            raw_values = raw_values.percentile(self._group.value_by_names(names))
        else:
            raw_values = raw_values.percentile()
        return raw_values

    def __str__(self):
        if self._group:
            return "\mathrm{{CSPercentile}}({0}, groups={1})".format(str(self._inner), str(self._group))
        else:
            return "\mathrm{{CSPercentile}}({0})".format(str(self._inner))


cdef class CSAverageAdjustedSecurityValueHolder(CrossSectionValueHolder):
    def __init__(self, innerValue, groups=None):
        super(CSAverageAdjustedSecurityValueHolder, self).__init__(innerValue, groups)

    cpdef value_all(self):

        cdef SeriesValues raw_values

        if self.updated:
            return self.cached
        else:
            raw_values = self._inner.value_all()
            if self._group:
                self.cached = raw_values - raw_values.mean(self._group.value_all())
            else:
                self.cached = raw_values - raw_values.mean()
            self.updated = 1
            return self.cached

    cpdef double value_by_name(self, name):

        cdef SeriesValues raw_values

        if self.updated:
            return self.cached[name]
        else:
            raw_values = self._inner.value_all()
            if self._group:
                self.cached = raw_values - raw_values.mean(self._group.value_all())
            else:
                self.cached = raw_values - raw_values.mean()
            self.updated = 1
            return self.cached[name]

    cpdef SeriesValues value_by_names(self, list names):
        raw_values = self._inner.value_by_names(names)
        if self._group:
            self.cached = raw_values - raw_values.mean(self._group.value)
        else:
            self.cached = raw_values - raw_values.mean()
        return raw_values[names]

    def __str__(self):
        if self._group:
            return "\mathrm{{CSMeanAdjusted}}({0}, groups={1})".format(str(self._inner), str(self._group))
        else:
            return "\mathrm{{CSMeanAdjusted}}({0})".format(str(self._inner))


cdef class CSZScoreSecurityValueHolder(CrossSectionValueHolder):
    def __init__(self, innerValue, groups=None):
        super(CSZScoreSecurityValueHolder, self).__init__(innerValue, groups)

    cdef _cal_impl(self):
        cdef SeriesValues raw_values = self._inner.value_all()

        if self._group:
            self.cached = raw_values.zscore(self._group.value_all())
        else:
            self.cached = raw_values.zscore()
        self.updated = 1

    cpdef value_all(self):
        if self.updated:
            return self.cached
        else:
            self._cal_impl()
            return self.cached

    cpdef double value_by_name(self, name):
        if self.updated:
            return self.cached[name]
        else:
            self._cal_impl()
            return self.cached[name]

    cpdef SeriesValues value_by_names(self, list names):
        cdef SeriesValues raw_values = self._inner.value_by_names(names)
        if self._group:
            raw_values = raw_values.zscore(self._group.value_by_names(names))
        else:
            raw_values = raw_values.zscore()
        return raw_values

    def __str__(self):
        if self._group:
            return "\mathrm{{CSZscore}}({0}, groups={1})".format(str(self._inner), str(self._group))
        else:
            return "\mathrm{{CSZscore}}({0})".format(str(self._inner))


cdef class CSFillNASecurityValueHolder(CrossSectionValueHolder):
    def __init__(self, innerValue, groups=None):
        super(CSFillNASecurityValueHolder, self).__init__(innerValue, groups)

    cdef _cal_impl(self):
        cdef SeriesValues raw_values = self._inner.value_all()

        if self._group:
            self.cached = raw_values.fillna(self._group.value_all())
        else:
            self.cached = raw_values.fillna()
        self.updated = 1

    cpdef value_all(self):
        if self.updated:
            return self.cached
        else:
            self._cal_impl()
            return self.cached

    cpdef double value_by_name(self, name):
        if self.updated:
            return self.cached[name]
        else:
            self._cal_impl()
            return self.cached[name]

    cpdef SeriesValues value_by_names(self, list names):
        cdef SeriesValues raw_values = self._inner.value_by_names(names)
        if self._group:
            raw_values = raw_values.fillna(self._group.value_by_names(names))
        else:
            raw_values = raw_values.fillna()
        return raw_values

    def __str__(self):
        if self._group:
            return "\mathrm{{CSFillNA}}({0}, groups={1})".format(str(self._inner), str(self._group))
        else:
            return "\mathrm{{CSFillNA}}({0})".format(str(self._inner))

cdef class CSWinsorizeSecurityValueHolder(CrossSectionValueHolder):
    
    cdef int _nums_stds;
    def __init__(self, innerValue, nums_stds, groups=None):
        super(CSWinsorizeSecurityValueHolder, self).__init__(innerValue, groups)
        self._nums_stds = nums_stds

    cdef _cal_impl(self):
        cdef SeriesValues raw_values = self._inner.value_all()

        if self._group:
            self.cached = raw_values.winsorize(self._nums_stds, self._group.value_all())
        else:
            self.cached = raw_values.winsorize(self._nums_stds)
        self.updated = 1

    cpdef value_all(self):
        if self.updated:
            return self.cached
        else:
            self._cal_impl()
            return self.cached
    
    cpdef SeriesValues value_by_names(self, list names):
        cdef SeriesValues raw_values = self._inner.value_by_names(names)
        if self._group:
            raw_values = raw_values.winsorize(self._nums_stds, self._group.value_by_names(names))
        else:
            raw_values = raw_values.winsorize(self._nums_stds)
        return raw_values

    def __str__(self):
        if self._group:
            return "\mathrm{{CSWinsorize}}({0}, {1}, groups={2})".format(str(self._inner), self._nums_stds, str(self._group))
        else:
            return "\mathrm{{CSWinsorize}}({0}, {1})".format(str(self._inner), self._nums_stds)

cdef class CSNeutSecurityValueHolder(SecurityValueHolder):

    cdef public SecurityValueHolder _left
    cdef public SecurityValueHolder _right

    def __init__(self, left, right):
        super(CSNeutSecurityValueHolder, self).__init__()
        self._left = build_holder(left)
        self._right = build_holder(right)

        self._window = max(self._left.window, self._right.window)
        self._dependency = list(set(self._left.fields + self._right.fields))
        self.updated = 0
        self.cached = None

    @property
    def symbolList(self):
        return self._left.symbolList

    cpdef push(self, dict data):
        self._left.push(data)
        self._right.push(data)
        self.updated = 0

    cpdef value_all(self):
        cdef SeriesValues left_raw_values
        cdef SeriesValues right_raw_values

        if self.updated:
            return self.cached
        else:
            left_raw_values = self._left.value_all()
            right_raw_values = self._left.value_all()
            self.cached = left_raw_values.neut(right_raw_values)
            self.updated = 1
            return self.cached
    
    cpdef double value_by_name(self, name):

        cdef SeriesValues left_raw_values
        cdef SeriesValues right_raw_values

        if self.updated:
            return self.cached[name]
        else:
            left_raw_values = self._left.value_all()
            right_raw_values = self._right.value_all()
            self.cached = left_raw_values.neut(right_raw_values)
            self.updated = 1
            return self.cached[name]

    cpdef SeriesValues value_by_names(self, list names):
        cdef SeriesValues left_raw_values
        cdef SeriesValues right_raw_values
        left_raw_values = self._left.value_by_names(names)
        right_raw_values = self._right.value_by_names(names)
        raw_values = left_raw_values.neut(right_raw_values)
        return raw_values

    def __str__(self):
        return "\mathrm{{CSNeut}}({0}, {1})".format(str(self._left), str(self._right))

cdef class CSFloorDivSecurityValueHolder(SecurityValueHolder):
    
    cdef public SecurityValueHolder _left
    cdef public SecurityValueHolder _right

    def __init__(self, left, right):
        super(CSFloorDivSecurityValueHolder, self).__init__()
        self._left = build_holder(left)
        self._right = build_holder(right)

        self._window = max(self._left.window, self._right.window)
        self._dependency = list(set(self._left.fields + self._right.fields))
        self.updated = 0
        self.cached = None

    @property
    def symbolList(self):
        return self._left.symbolList

    cpdef push(self, dict data):
        self._left.push(data)
        self._right.push(data)
        self.updated = 0

    cpdef value_all(self):
        cdef SeriesValues left_raw_values
        cdef SeriesValues right_raw_values

        if self.updated:
            return self.cached
        else:
            left_raw_values = self._left.value_all()
            right_raw_values = self._left.value_all()
            self.cached = left_raw_values.floor_div(right_raw_values)
            self.updated = 1
            return self.cached
    
    cpdef double value_by_name(self, name):

        cdef SeriesValues left_raw_values
        cdef SeriesValues right_raw_values

        if self.updated:
            return self.cached[name]
        else:
            left_raw_values = self._left.value_all()
            right_raw_values = self._right.value_all()
            self.cached = left_raw_values.floor_div(right_raw_values)
            self.updated = 1
            return self.cached[name]

    cpdef SeriesValues value_by_names(self, list names):
        cdef SeriesValues left_raw_values
        cdef SeriesValues right_raw_values
        left_raw_values = self._left.value_by_names(names)
        right_raw_values = self._right.value_by_names(names)
        raw_values = left_raw_values.floor_div(right_raw_values)
        return raw_values

    def __str__(self):
        return "\mathrm{{CSFloorDiv}}({0}, {1})".format(str(self._left), str(self._right))



cdef class CSSignPowerSecurityValueHolder(SecurityValueHolder):
    
    cdef public SecurityValueHolder _left
    cdef public SecurityValueHolder _right

    def __init__(self, left, right):
        super(CSSignPowerSecurityValueHolder, self).__init__()
        self._left = build_holder(left)
        self._right = build_holder(right)

        self._window = max(self._left.window, self._right.window)
        self._dependency = list(set(self._left.fields + self._right.fields))
        self.updated = 0
        self.cached = None

    @property
    def symbolList(self):
        return self._left.symbolList

    cpdef push(self, dict data):
        self._left.push(data)
        self._right.push(data)
        self.updated = 0

    cpdef value_all(self):
        cdef SeriesValues left_raw_values
        cdef SeriesValues right_raw_values

        if self.updated:
            return self.cached
        else:
            left_raw_values = self._left.value_all()
            right_raw_values = self._left.value_all()
            self.cached = left_raw_values.sign_power(right_raw_values)
            self.updated = 1
            return self.cached
    
    cpdef double value_by_name(self, name):

        cdef SeriesValues left_raw_values
        cdef SeriesValues right_raw_values

        if self.updated:
            return self.cached[name]
        else:
            left_raw_values = self._left.value_all()
            right_raw_values = self._right.value_all()
            self.cached = left_raw_values.sign_power(right_raw_values)
            self.updated = 1
            return self.cached[name]

    cpdef SeriesValues value_by_names(self, list names):
        cdef SeriesValues left_raw_values
        cdef SeriesValues right_raw_values
        left_raw_values = self._left.value_by_names(names)
        right_raw_values = self._right.value_by_names(names)
        raw_values = left_raw_values.sign_power(right_raw_values)
        return raw_values

    def __str__(self):
        return "\mathrm{{CSSignPower}}({0}, {1})".format(str(self._left), str(self._right))


cdef class CSProjSecurityValueHolder(SecurityValueHolder):

    cdef public SecurityValueHolder _left
    cdef public SecurityValueHolder _right

    def __init__(self, left, right):
        super(CSProjSecurityValueHolder, self).__init__()
        self._left = build_holder(left)
        self._right = build_holder(right)

        self._window = max(self._left.window, self._right.window)
        self._dependency = list(set(self._left.fields + self._right.fields))
        self.updated = 0
        self.cached = None

    @property
    def symbolList(self):
        return self._left.symbolList

    cpdef push(self, dict data):
        self._left.push(data)
        self._right.push(data)
        self.updated = 0

    cpdef value_all(self):
        cdef SeriesValues left_raw_values
        cdef SeriesValues right_raw_values

        if self.updated:
            return self.cached
        else:
            left_raw_values = self._left.value_all()
            right_raw_values = self._left.value_all()
            self.cached = left_raw_values.proj(right_raw_values)
            self.updated = 1
            return self.cached
    
    cpdef double value_by_name(self, name):

        cdef SeriesValues left_raw_values
        cdef SeriesValues right_raw_values

        if self.updated:
            return self.cached[name]
        else:
            left_raw_values = self._left.value_all()
            right_raw_values = self._right.value_all()
            self.cached = left_raw_values.proj(right_raw_values)
            self.updated = 1
            return self.cached[name]

    cpdef SeriesValues value_by_names(self, list names):
        cdef SeriesValues left_raw_values
        cdef SeriesValues right_raw_values
        left_raw_values = self._left.value_by_names(names)
        right_raw_values = self._right.value_by_names(names)
        raw_values = left_raw_values.proj(right_raw_values)
        return raw_values

    def __str__(self):
        return "\mathrm{{CSProj}}({0}, {1})".format(str(self._left), str(self._right))


cdef class CSResidueSecurityValueHolder(SecurityValueHolder):

    cdef public SecurityValueHolder _left
    cdef public SecurityValueHolder _right

    def __init__(self, left, right):
        super(CSResidueSecurityValueHolder, self).__init__()
        self._left = build_holder(left)
        self._right = build_holder(right)

        self._window = max(self._left.window, self._right.window)
        self._dependency = list(set(self._left.fields + self._right.fields))
        self.updated = 0
        self.cached = None

    @property
    def symbolList(self):
        return self._left.symbolList

    cpdef push(self, dict data):
        self._left.push(data)
        self._right.push(data)
        self.updated = 0

    cpdef value_all(self):

        cdef SeriesValues left_raw_values
        cdef SeriesValues right_raw_values

        if self.updated:
            return self.cached
        else:
            left_raw_values = self._left.value_all()
            right_raw_values = self._right.value_all()
            self.cached = left_raw_values.res(right_raw_values)
            self.updated = 1
            return self.cached

    cpdef double value_by_name(self, name):

        cdef SeriesValues left_raw_values
        cdef SeriesValues right_raw_values

        if self.updated:
            return self.cached[name]
        else:
            left_raw_values = self._left.value_all()
            right_raw_values = self._right.value_all()
            self.cached = left_raw_values.res(right_raw_values)
            self.updated = 1
            return self.cached[name]

    cpdef SeriesValues value_by_names(self, list names):
        cdef SeriesValues left_raw_values
        cdef SeriesValues right_raw_values
        left_raw_values = self._left.value_by_names(names)
        right_raw_values = self._right.value_by_names(names)
        raw_values = left_raw_values.res(right_raw_values)
        return raw_values

    def __str__(self):
        return "\mathrm{{CSRes}}({0}, {1})".format(str(self._left), str(self._right))
