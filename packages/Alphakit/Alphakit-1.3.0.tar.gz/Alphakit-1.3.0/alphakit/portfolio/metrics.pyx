# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np


def TopNWeight(dummy, indata, hold, n, mode=0):
    invar = indata * dummy
    returndata = invar.apply(lambda x: x[x.nlargest(n, keep='all').index],
                             axis=1)
    returndata[~returndata.isna()] = 1
    if mode != 0:
        returndata = returndata * indata
    returndata = returndata.div(returndata.sum(min_count=1, axis=1),
                                axis='rows')
    returndata = returndata.rolling(window=hold, min_periods=1).sum() / hold
    return returndata


# weightM的index是生成weight的日期，默认第二天开盘交易,weightM>0
# depret:计算return的矩阵，
# 例如：计算多头超额->ret_f1r_oo-ret_zz500_f1r_oo
# 计算空头超额->ret_zz500_f1r_oo-ret_f1r_oo
# 计算单边->ret_f1r_oo
# 返回的是单边换手率：即一买一卖算一次换手
# freq: daily=252，monthly=12,weekly=50
def CalRet(weightM,
           ret_f1r_oo,
           ret_zz500_f1r_oo,
           freq,
           cost=0.003,
           leveage=None):
    out = pd.Series(index=['ret', 'sharpe', 'turnover', 'maxdd'],
                    dtype='float')
    weightM[weightM <= 0] = np.nan
    tvs = abs(weightM.sub(weightM.shift(1), fill_value=0)).sum(
        axis=1, min_count=1) * 0.5
    if leveage == None:
        leveage = 1
    pnl = np.log((
        (np.exp(ret_f1r_oo) - 1) * weightM).sum(axis=1, min_count=1) -
                 (np.exp(ret_zz500_f1r_oo) - 1) - tvs * cost + 1) * leveage
    tv = tvs.mean()
    retL = pnl.mean() * freq
    retL_std = pnl.std() * np.sqrt(freq)
    sharpL = retL / retL_std
    pnlL = pnl.cumsum()
    maxdd = pnlL.expanding().max() - pnlL
    maxddL = maxdd.max()
    ret2mddL = retL / maxddL
    out['ret'] = retL
    out['sharpe'] = sharpL
    out['turnover'] = tv
    out['maxdd'] = maxddL
    out['ret2maxdd'] = ret2mddL
    return out, pnl, tvs
