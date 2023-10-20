# -*- coding: utf-8 -*-
import pandas as pd
from ultron.strategy.optimize import Optimize
from ultron.strategy.strategy import create_params
from jdw.data.SurfaceAPI.stock.risk_model import FactorRiskModel


def to_risk_model(risk_exposure, risk_cov, specific_risk):
    risk_exposure = risk_exposure.merge(specific_risk,
                                        on=['trade_date', 'code'])

    new_risk_cov = risk_cov.set_index('Factor')
    new_risk_exp = risk_exposure.set_index('code')

    risk_cov_groups = new_risk_cov.groupby('trade_date')
    risk_exp_groups = new_risk_exp.groupby('trade_date')

    models = {}
    for ref_date, cov_g in risk_cov_groups:
        exp_g = risk_exp_groups.get_group(ref_date)
        factor_names = cov_g.index.tolist()
        factor_cov = cov_g.loc[factor_names, factor_names] / 10000.
        factor_loading = exp_g.loc[:, factor_names]
        idsync = exp_g['srisk'] * exp_g['srisk'] / 10000
        models[ref_date] = FactorRiskModel(factor_cov, factor_loading, idsync)
    return pd.Series(models)


# er,risk_exposure,risk_cov,specific_risk,industry,weighted: metrics
def er_opt(er, configure, risk_exposure, risk_cov, specific_risk, industry,
           weighted, begin_date, end_date):
    factors = er.unstack().reset_index()
    factors.rename(columns={0: 'er'}, inplace=True)
    factors.dropna(inplace=True)

    specific_risk = specific_risk.unstack().reset_index()
    specific_risk.rename(columns={0: 'srisk'}, inplace=True)

    weighted = weighted.unstack().reset_index()
    weighted.rename(columns={0: 'weight'}, inplace=True)

    industry = industry.unstack().reset_index()
    industry.rename(columns={0: 'industry_code'}, inplace=True)
    industry.dropna(inplace=True)
    industry = industry.loc[industry.industry_code != 'nan']
    industry_dummy = pd.get_dummies(industry.set_index(['trade_date', 'code'
                                                        ])['industry_code'],
                                    dtype=float).reset_index()
    total_data = industry.merge(
        weighted, on=['trade_date', 'code'],
        how='outer').merge(risk_exposure,
                           on=['trade_date', 'code'
                               ]).merge(industry_dummy,
                                        on=['trade_date', 'code'
                                            ]).merge(factors,
                                                     on=['trade_date', 'code'])
    factor_model = to_risk_model(risk_exposure=risk_exposure,
                                 risk_cov=risk_cov,
                                 specific_risk=specific_risk)

    params = create_params(**configure)
    optimize = Optimize(alpha_model=None,
                        category='onlylong',
                        features=['er'],
                        begin_date=begin_date,
                        end_date=end_date,
                        risk_model=factor_model,
                        total_data=total_data)
    positions = optimize.rebalance_positions(params)
    return positions
