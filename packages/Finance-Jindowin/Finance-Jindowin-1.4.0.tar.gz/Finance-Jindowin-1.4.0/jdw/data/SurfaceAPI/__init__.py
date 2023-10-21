# -*- coding: utf-8 -*-
from jdw.data.SurfaceAPI.universe import FutUniverse
from jdw.data.SurfaceAPI.universe import StkUniverse
from jdw.data.SurfaceAPI.universe import FutDummy
from jdw.data.SurfaceAPI.universe import UniverseDummy
from jdw.data.SurfaceAPI.stock.industry import Industry as StkIndustry
from jdw.data.SurfaceAPI.stock.risk_model import RiskModel
from jdw.data.SurfaceAPI.stock.factors import StkFactors
from jdw.data.SurfaceAPI.index_component import IndexComponent
from jdw.data.SurfaceAPI.index_market import IndexMarket
from jdw.data.SurfaceAPI.stock.market_stock import MarketStock
from jdw.data.SurfaceAPI.stock.yields import StkYields
from jdw.data.SurfaceAPI.futures.basic import Basic as FutBasic
from jdw.data.SurfaceAPI.futures.yields import FutYields
from jdw.data.SurfaceAPI.futures.factors import FutFactors
from jdw.data.SurfaceAPI.futures.classify import FutClassify
from jdw.data.SurfaceAPI.futures.index_market import IndexMarket as FutIndexMarket
from jdw.data.SurfaceAPI.dummy import Dummy
from jdw.data.SurfaceAPI.utilities import create_stats


def create_yields(df,
                  horizon=0,
                  offset=0,
                  no_code=False,
                  is_log=True,
                  is_pandas=True):
    data = create_stats(df=df.rename(columns={'nxt1_ret': 'chgPct'}),
                        horizon=horizon,
                        offset=offset,
                        no_code=no_code,
                        is_log=is_log).sort_values(by=['trade_date', 'code'])
    return data if is_pandas else data.set_index(['trade_date', 'code'
                                                  ])['nxt1_ret'].unstack()
