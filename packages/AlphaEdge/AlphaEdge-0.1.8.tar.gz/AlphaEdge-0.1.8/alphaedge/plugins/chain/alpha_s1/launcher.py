# -*- encoding:utf-8 -*-
import pdb, datetime, os, json
import pandas as pd
import numpy as np
from enum import Enum

from ultron.tradingday import *
from ultron.strategy.deformer import FusionDump, FusionLoad
from ultron.kdutils.file import load_pickle
from jdwdata.RetrievalAPI import get_data_by_map, get_factors
from alphaedge.plugins.chain.engine import Engine
from alphaedge.plugins.quantum import establish, Trainer, Predictor
from alphakit.const import *
from alphakit.factor import *
from alphakit.portfolio import *
from alphakit.data import *
#from alphaedge.api import FusionDump


class LANCHER(Enum):
    CREATOR = 1
    TRAIN = 2
    PREDICT = 3
    CALLCORE = 4


class Launcher(Engine):

    def __init__(self, policy_id, directory, **kwargs):
        super(Launcher, self).__init__(policy_id, **kwargs)
        self.directory = directory

    def create_model(self, begin_date, end_date, feature_file):

        def create_ridge(features, universe, batch, freq, horizon,
                         fit_intercept, positive, count):
            return FusionDump('RidgeRegression',
                              features=features,
                              universe=universe,
                              batch=batch,
                              freq=freq,
                              horizon=horizon,
                              alpha=0.001 * count * batch,
                              fit_intercept=fit_intercept,
                              positive=positive)

        features = pd.read_csv(feature_file, header=None).astype('str')
        features = features.values[:, 0].tolist()
        universe_sets = ['dummy120_fst']
        data = get_data_by_map(columns=universe_sets,
                               begin_date=begin_date,
                               end_date=end_date,
                               method='ddb')
        count_sets = {}
        for u in universe_sets:
            t = data['dummy120_fst']
            count_sets[u] = int(t.count(axis=1).mean())

        model_list = model_list = [
            create_ridge(features=features,
                         universe='dummy120_fst',
                         batch=5,
                         freq='1b',
                         horizon=10,
                         fit_intercept=False,
                         positive=True,
                         count=count_sets['dummy120_fst']),
            create_ridge(features=features,
                         universe='dummy120_fst',
                         batch=10,
                         freq='1b',
                         horizon=2,
                         fit_intercept=False,
                         positive=True,
                         count=count_sets['dummy120_fst']),
            create_ridge(features=features,
                         universe='dummy120_fst',
                         batch=10,
                         freq='1b',
                         horizon=3,
                         fit_intercept=False,
                         positive=True,
                         count=count_sets['dummy120_fst']),
            create_ridge(features=features,
                         universe='dummy120_fst',
                         batch=10,
                         freq='1b',
                         horizon=4,
                         fit_intercept=False,
                         positive=True,
                         count=count_sets['dummy120_fst']),
            create_ridge(features=features,
                         universe='dummy120_fst',
                         batch=10,
                         freq='1b',
                         horizon=5,
                         fit_intercept=False,
                         positive=True,
                         count=count_sets['dummy120_fst']),
            create_ridge(features=features,
                         universe='dummy120_fst',
                         batch=150,
                         freq='1b',
                         horizon=1,
                         fit_intercept=False,
                         positive=True,
                         count=count_sets['dummy120_fst']),
            create_ridge(features=features,
                         universe='dummy120_fst',
                         batch=5,
                         freq='-1ys',
                         horizon=10,
                         fit_intercept=False,
                         positive=True,
                         count=count_sets['dummy120_fst']),
            create_ridge(features=features,
                         universe='dummy120_fst',
                         batch=10,
                         freq='-1ys',
                         horizon=2,
                         fit_intercept=False,
                         positive=True,
                         count=count_sets['dummy120_fst']),
            create_ridge(features=features,
                         universe='dummy120_fst',
                         batch=10,
                         freq='-1ys',
                         horizon=3,
                         fit_intercept=False,
                         positive=True,
                         count=count_sets['dummy120_fst']),
            create_ridge(features=features,
                         universe='dummy120_fst',
                         batch=10,
                         freq='-1ys',
                         horizon=4,
                         fit_intercept=False,
                         positive=True,
                         count=count_sets['dummy120_fst']),
            create_ridge(features=features,
                         universe='dummy120_fst',
                         batch=5,
                         freq='-1ys',
                         horizon=5,
                         fit_intercept=False,
                         positive=True,
                         count=count_sets['dummy120_fst']),
            create_ridge(features=features,
                         universe='dummy120_fst',
                         batch=150,
                         freq='-1ys',
                         horizon=20,
                         fit_intercept=False,
                         positive=True,
                         count=count_sets['dummy120_fst'])
        ]
        main_model = create_ridge(features=[],
                                  universe='dummy120_fst',
                                  batch=10,
                                  freq='-1ys',
                                  horizon=3,
                                  fit_intercept=False,
                                  positive=True,
                                  count=count_sets['dummy120_fst'])

        establish(groups_model=model_list,
                  main_model=main_model,
                  directory=self.directory,
                  policy_id=self.policy_id)

    def load_params(self):

        def load_desc(m, type):
            desc_dir = os.path.join(self.directory, str(self.policy_id), type,
                                    "desc")
            filename = os.path.join(desc_dir, "{0}.h5".format(m))
            desc = load_pickle(filename)
            return FusionLoad(desc)

        policy_file = os.path.join(self.directory, str(self.policy_id),
                                   "policy.json")
        with open(policy_file, 'r') as json_file:
            policy_data = json.load(json_file)
        desc_main = load_desc(policy_data['main'], 'main')
        features = []
        nested_list = policy_data['groups'].values()
        nested_list = [item for sublist in nested_list for item in sublist]
        max_window = 0
        for m in nested_list:
            desc = load_desc(m, 'groups')
            max_freq = freqDates(desc.freq) if freqDates(
                desc.freq) > freqDates(desc_main.freq) else freqDates(
                    desc_main.freq)
            features += desc.features
            max_window = max_window if max_window > (
                desc.horizon + desc.batch + max_freq * 2 + desc_main.horizon +
                desc_main.batch) else (desc.horizon + desc.batch +
                                       max_freq * 2 + desc_main.horizon +
                                       desc_main.batch)
        return {'features': list(set(features)), 'max_window': int(max_window)}

    def prepare(self, featurelist, begin_date, end_date):
        data = get_data_by_map(columns=[
            'dummy120_fst', 'ret_o2o', 'negMarketValue', 'dummy_test_f1r_open',
            'dummy120_fst_close'
        ],
                               begin_date=begin_date,
                               end_date=end_date,
                               method='ddb')
        vardummy = data['dummy120_fst']
        dummy = data['dummy120_fst_close'] * data['dummy_test_f1r_open']
        fcap = data['negMarketValue']
        fcap[fcap <= 0] = np.nan
        retstd = 1 / np.sqrt(fcap.rolling(window=120, min_periods=1).mean())
        factors = get_factors(begin_date=begin_date,
                              end_date=end_date,
                              ids=featurelist,
                              freq='D',
                              format_data=1)
        dimension_data = pd.DataFrame()
        for ff in factors.keys():
            f = standardize(winsorize(factors[ff] * vardummy)).unstack()
            f[np.isnan(f)] = 0
            f.name = ff
            dimension_data = pd.concat([dimension_data, f], axis=1)
        dimension_data.reset_index(inplace=True)
        dimension_data.rename(columns={
            'level_0': 'code',
            'level_1': 'trade_date'
        },
                              inplace=True)

        chg_pct = data['ret_o2o'].unstack()
        chg_pct.name = 'chg_pct'
        ret_std = retstd.copy()
        retstd = retstd.unstack()
        retstd.name = 'sample_weight'
        vardummy = vardummy.unstack()
        vardummy.name = 'dummy'
        total_data = dimension_data.merge(chg_pct, on=[
            'trade_date', 'code'
        ]).merge(retstd, on=['trade_date',
                             'code']).merge(vardummy,
                                            on=['trade_date', 'code'])
        total_data = total_data[total_data['dummy'] == 1.0]
        total_data.dropna(inplace=True)
        return total_data, dummy, ret_std

    ### 此处可以考虑针对不同持仓收益率传入不同的total_data
    def create_groups(self, total_data, begin_date, end_date):
        ### 子策略训练
        trainer = Trainer(directory=self.directory,
                          policy_id=self.policy_id,
                          k_split=self.k_split,
                          offset=2,
                          is_log=False,
                          is_shift=True,
                          is_normal=False,
                          is_groups=1)
        trainer.calculate(train_data=total_data,
                          begin_date=begin_date,
                          end_date=end_date)

        ### 子策略预测
        predictor = Predictor(directory=self.directory,
                              policy_id=self.policy_id,
                              k_split=self.k_split,
                              is_log=False,
                              is_shift=False,
                              is_groups=1)
        factors_data = predictor.calculate(total_data=total_data,
                                           begin_date=begin_date,
                                           end_date=end_date)
        return factors_data.reset_index().sort_values(
            by=['trade_date', 'code'])

    def create_main(self, total_data, begin_date, end_date):
        ### 主策略训练
        total_data = total_data.sort_values(by=['trade_date', 'code'])
        trainer = Trainer(directory=self.directory,
                          policy_id=self.policy_id,
                          offset=2,
                          is_log=False,
                          is_shift=True,
                          is_groups=0)
        trainer.calculate(train_data=total_data,
                          begin_date=begin_date,
                          end_date=end_date)

        ### 主策略预测
        returns_data = total_data[['trade_date', 'code', 'chg_pct']]
        predictor = Predictor(directory=self.directory,
                              policy_id=self.policy_id,
                              is_log=False,
                              is_shift=False,
                              is_groups=0)
        factors_data = predictor.calculate(total_data=total_data,
                                           begin_date=begin_date,
                                           end_date=end_date)
        return factors_data.reset_index().sort_values(
            by=['trade_date', 'code'])

    def calculate(self, total_data, begin_date, end_date):
        suber_data = self.create_groups(total_data=total_data,
                                        begin_date=begin_date,
                                        end_date=end_date)
        returns_data = total_data[[
            'trade_date', 'code', 'chg_pct', 'sample_weight'
        ]]
        suber_data = suber_data.merge(returns_data, on=['trade_date', 'code'])
        suber_data.dropna(inplace=True)
        predict_data = self.create_main(total_data=suber_data,
                                        begin_date=begin_date,
                                        end_date=end_date)
        return predict_data

    def prepare_opt(self, begin_date, end_date, benchmark):
        data = get_data_by_map(columns=BARRA_ALL_K,
                               begin_date=begin_date,
                               end_date=end_date,
                               method='ddb')
        risk_exposure = getdataset(data, BARRA_ALL_K)
        risk_exposure.columns = risk_exposure.columns.str.removeprefix('f_')
        risk_exposure.reset_index(inplace=True)

        covstr = list('fcov_' + i for i in BARRA_ALL)
        data = get_data_by_map(columns=covstr,
                               begin_date=begin_date,
                               end_date=end_date,
                               method='ddb')
        risk_cov = pd.DataFrame()
        for f in covstr:
            factor = data[f].unstack()
            factor.name = f
            risk_cov = pd.concat([risk_cov, factor], axis=1)
        risk_cov.columns = risk_cov.columns.str.removeprefix('fcov_')
        risk_cov.reset_index(inplace=True)
        risk_cov.rename(columns={
            'level_0': 'Factor',
            'level_1': 'trade_date'
        },
                        inplace=True)

        data = get_data_by_map(columns=['SRISK', 'sw1'] + [benchmark],
                               begin_date=begin_date,
                               end_date=end_date,
                               method='ddb')
        specific_risk = data['SRISK']
        industry = data['sw1']
        weighted = data[benchmark]

        return risk_exposure, risk_cov, specific_risk, industry, weighted

    def makeweight(self, dummy, er, useweight, benchmark, count, begin_date,
                   end_date):
        newer = er.pivot(index='trade_date',
                         columns='code',
                         values=er.columns[-1]).reindex(index=dummy.index,
                                                        columns=dummy.columns)
        er = standardize(winsorize(newer)) * useweight
        riskstyle = [
            'BETA', 'MOMENTUM', 'SIZE', 'EARNYILD', 'RESVOL', 'GROWTH', 'BTOP',
            'LEVERAGE', 'LIQUIDTY'
        ]
        configure = {
            'industry_effective': BARRA_INDUSTRY,
            'industry_invalid': [],
            'turn_over_target': 1,
            'weights_bandwidth': 1,
            'lbound': 0.0,
            'ubound': 0.005,
            'is_benchmark': 0,
            'benchmark_boundary': 'relative',
            'benchmark_lower': 0,
            'benchmark_upper': 1.01,
            'total_boundary': 'relative',
            'total_lower': 0.99,
            'total_upper': 1.01,
            'effective_industry_boundary': 'absolute',
            'effective_industry_lower': -0.05,
            'effective_industry_upper': 0.05,
            'invalid_industry_boundary': 'absolute',
            'invalid_industry_lower': -0.05,
            'invalid_industry_upper': 0.05,
            'riskstyle': riskstyle,
            'riskstyle_boundary': 'absolute',
            'riskstyle_lower': -0.3,
            'riskstyle_upper': 0.3,
            'method': 'long_risk_neutral'
        }

        risk_exposure, risk_cov, specific_risk, industry, weighted = self.prepare_opt(
            begin_date, end_date, benchmark)
        positions = er_opt(er=er,
                           configure=configure,
                           risk_exposure=risk_exposure,
                           risk_cov=risk_cov,
                           specific_risk=specific_risk,
                           industry=industry,
                           weighted=weighted,
                           begin_date=begin_date,
                           end_date=end_date)
        weight = positions.pivot(index='trade_date',
                                 columns='code',
                                 values='weight')
        weight = weight.reindex(index=dummy.index, columns=dummy.columns)
        weight[weight <= 0.0001] = np.nan
        weight = TopNWeight(dummy, weight, 1, count,
                            1).unstack().reset_index().dropna()
        weight = weight.rename(columns={0: 'weight'})
        return weight

    def run(self, **kwargs):
        begin_date = kwargs['start_date']
        end_date = kwargs['end_date']
        params = self.load_params()
        data_begin_date = advanceDateByCalendar(
            'china.sse', begin_date, "-{}b".format(params['max_window']),
            BizDayConventions.Following).strftime('%Y-%m-%d')
        if kwargs['op'] == LANCHER.CREATOR.value:
            self.create_model(begin_date=begin_date,
                              end_date=end_date,
                              feature_file=kwargs['feature_file'])
        elif kwargs['op'] == LANCHER.CALLCORE.value:
            total_data, dummy, ret_std = self.prepare(params['features'],
                                                      data_begin_date,
                                                      end_date)
            er = self.calculate(total_data, data_begin_date, end_date)
            weight = self.makeweight(dummy, er, ret_std, 'zz1000wt', 300,
                                     begin_date, end_date)
            return weight