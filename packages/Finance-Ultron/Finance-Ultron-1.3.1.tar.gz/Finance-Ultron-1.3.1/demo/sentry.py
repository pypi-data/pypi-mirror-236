import pdb, time
import pandas as pd
import numpy as np
from ultron.sentry.api import CSRes, MRes, MCoef

start_date = '2010-01-01'
end_date = '2020-01-01'


def create_data(date_index, codes, name):
    data = np.random.rand(len(date_index), len(codes))
    data = pd.DataFrame(index=date_index, columns=codes, data=data)
    data = data.stack()
    data.name = name
    return data


def create_factors(start_date, end_date, n=500, m=300):
    date_index = pd.date_range(start=start_date, end=end_date)
    date_index.name = 'trade_date'
    codes = ["code_" + str(i) for i in range(0, n)]

    factors_res = [
        create_data(date_index=date_index,
                    codes=codes,
                    name="factor_{}".format(str(i))) for i in range(0, m)
    ]
    factors_res.append(
        create_data(date_index=date_index, codes=codes, name="nxt1_ret"))
    factors_data = pd.concat(factors_res, axis=1)

    factors_data = factors_data.reset_index().rename(
        columns={'level_1': 'code'})
    return factors_data


##构建因子 + 收益率
factors_data = create_factors(start_date=start_date,
                              end_date=end_date,
                              n=50,
                              m=30)
features = [
    col for col in factors_data.columns
    if col not in ['trade_date', 'code', 'nxt1_ret']
]

pdb.set_trace()
factors_data = factors_data.sort_values(by=['trade_date', 'code'])
print("shape:{0}".format(factors_data.shape))

exp0 = CSRes(MCoef(10, 'factor_1', 'factor_2'), MCoef(5, 'factor_1',
                                                      'factor_3'))
factor0_data = exp0.transform(factors_data.set_index('trade_date'),
                              category_field='code',
                              name='fac1')

start_time = time.time()
exp1 = CSRes('factor_0', 'factor_1')
factor1_data = exp1.transform(factors_data.set_index('trade_date'),
                              category_field='code',
                              name='fac1')
print("factor1_data epoll:{0}".format(time.time() - start_time))

pdb.set_trace()
start_time = time.time()
exp2 = MRes(10, 'factor_0', 'factor_5')
factor2_data = exp1.transform(factors_data.set_index('trade_date'),
                              category_field='code',
                              name='fac2')
print("factor2_data epoll:{0}".format(time.time() - start_time))