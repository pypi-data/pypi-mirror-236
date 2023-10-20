# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd



def rolling_window(a, window):
    """
    返回2D array的滑窗array的array
    """
    nanarr = np.empty((window - 1, a.shape[1]))
    nanarr[:] = np.nan
    a = np.vstack((nanarr, a))
    shape = (a.shape[0] - window + 1, window, a.shape[-1])
    strides = (a.strides[0], ) + a.strides
    a_rolling = np.lib.stride_tricks.as_strided(a,
                                                shape=shape,
                                                strides=strides)
    return a_rolling


def getdataset(invars, sets_cols):
    outset = pd.DataFrame()
    for c in sets_cols:
        v = invars[c].unstack()
        v.name = c
        outset = pd.concat([outset, v], axis=1)
    outset.index.rename(['code', 'trade_date'], inplace=True)
    return outset