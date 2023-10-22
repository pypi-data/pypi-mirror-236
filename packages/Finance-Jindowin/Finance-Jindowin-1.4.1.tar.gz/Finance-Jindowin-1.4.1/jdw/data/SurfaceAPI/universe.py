# -*- coding: utf-8 -*-
import abc, sys, pdb
import pandas as pd
from sqlalchemy import select, and_, not_, or_
from jdw.data.SurfaceAPI.engine import FetchKDEngine


class BaseUniverse(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def condition(self):
        pass

    @property
    def name(self):
        pass

    def __add__(self, rhs):
        return OrUniverse(self, rhs)

    def __sub__(self, rhs):
        return XorUniverse(self, rhs)

    def __and__(self, rhs):
        return AndUniverse(self, rhs)

    def __or__(self, rhs):
        return OrUniverse(self, rhs)

    def isin(self, rhs):
        return AndUniverse(self, rhs)

    @classmethod
    def load(cls, u_desc: dict):
        pass

    def query(self, start_date: str = None, end_date: str = None, dates=None):
        query = select([
            self._table_model.trade_date, self._table_model.code
        ]).where(self._query_statements(start_date, end_date, dates)).order_by(
            self._table_model.trade_date, self._table_model.code)
        return pd.read_sql(query, self._engine.client())

    def _query_statements(self,
                          start_date: str = None,
                          end_date: str = None,
                          dates=None):
        return and_(
            self.condition(),
            self._table_model.trade_date.in_(dates) if dates else
            self._table_model.trade_date.between(start_date, end_date))


class OrUniverse(BaseUniverse):

    def __init__(self, lhs: BaseUniverse, rhs: BaseUniverse):
        self.lhs = lhs
        self.rhs = rhs
        self._table_model = lhs._table_model
        self._engine = lhs._engine

    def condition(self):
        return or_(self.lhs.condition(), self.rhs.condition())

    @property
    def name(self):
        name = [self.lhs.name, self.rhs.name]
        name.sort()
        return "{0}|or|{1}".format(name[0], name[1])

    def save(self):
        return dict(u_type=self.__class__.__name__,
                    lhs=self.lhs.save(),
                    rhs=self.rhs.save())

    @classmethod
    def load(cls, u_desc: dict):
        lhs = u_desc['lhs']
        rhs = u_desc['rhs']
        return cls(
            lhs=getattr(sys.modules[__name__], lhs['u_type']).load(lhs),
            rhs=getattr(sys.modules[__name__], rhs['u_type']).load(rhs),
        )

    def __eq__(self, other):
        return self.lhs == other.lhs and self.rhs == other.rhs and isinstance(
            other, OrUniverse)


class AndUniverse(BaseUniverse):

    def __init__(self, lhs: BaseUniverse, rhs: BaseUniverse):
        self.lhs = lhs
        self.rhs = rhs
        self._table_model = lhs._table_model
        self._engine = lhs._engine

    def condition(self):
        return and_(self.lhs.condition(), self.rhs.condition())

    @property
    def name(self):
        name = [self.lhs.name, self.rhs.name]
        name.sort()
        return "{0}|and|{1}".format(name[0], name[1])

    def save(self):
        return dict(u_type=self.__class__.__name__,
                    lhs=self.lhs.save(),
                    rhs=self.rhs.save())

    @classmethod
    def load(cls, u_desc: dict):
        lhs = u_desc['lhs']
        rhs = u_desc['rhs']
        return cls(
            lhs=getattr(sys.modules[__name__], lhs['u_type']).load(lhs),
            rhs=getattr(sys.modules[__name__], rhs['u_type']).load(rhs),
        )

    def __eq__(self, other):
        return self.lhs == other.lhs and self.rhs == other.rhs and isinstance(
            other, AndUniverse)


class XorUniverse(BaseUniverse):

    def __init__(self, lhs: BaseUniverse, rhs: BaseUniverse):
        self.lhs = lhs
        self.rhs = rhs
        self._table_model = lhs._table_model
        self._engine = lhs._engine

    def condition(self):
        return and_(self.lhs.condition(), not_(self.rhs.condition()))

    @property
    def name(self):
        name = [self.lhs.name, self.rhs.name]
        name.sort()
        return "{0}|xor|{1}".format(name[0], name[1])

    def save(self):
        return dict(u_type=self.__class__.__name__,
                    lhs=self.lhs.save(),
                    rhs=self.rhs.save())

    @classmethod
    def load(cls, u_desc: dict):
        lhs = u_desc['lhs']
        rhs = u_desc['rhs']
        return cls(
            lhs=getattr(sys.modules[__name__], lhs['u_type']).load(lhs),
            rhs=getattr(sys.modules[__name__], rhs['u_type']).load(rhs),
        )

    def __eq__(self, other):
        return self.lhs == other.lhs and self.rhs == other.rhs and isinstance(
            other, XorUniverse)


class Universe(BaseUniverse):

    def __init__(self, u_name, table_name=None):
        self._engine = FetchKDEngine()
        self.u_name = u_name.lower()
        self._table_name = table_name
        self._table_model = self._engine.table_model(self._table_name)

    def condition(self):
        return getattr(self._table_model, self.u_name) == 1 and getattr(
            self._table_model, 'flag') == 1

    @property
    def name(self):
        return self.u_name

    def save(self):
        return dict(u_type=self.__class__.__name__, u_name=self.u_name)

    def __eq__(self, other):
        return self.u_name == other.u_name


class FutUniverse(Universe):

    def __init__(self, u_name, table_name=None):
        super(FutUniverse,
              self).__init__(u_name,
                             table_name=('fut_derived_universe' if table_name
                                         is None else table_name))


class StkUniverse(Universe):

    def __init__(self, u_name, table_name=None):
        super(StkUniverse,
              self).__init__(u_name,
                             table_name=('stk_derived_universe' if table_name
                                         is None else table_name))


class StkDummy(Universe):

    def __init__(self, u_name, table_name=None):
        super(StkDummy,
              self).__init__(u_name,
                             table_name=('stk_derived_dummy' if table_name
                                         is None else table_name))


class FutDummy(Universe):

    def __init__(self, u_name, table_name=None):
        super(FutDummy,
              self).__init__(u_name,
                             table_name=('fut_derived_dummy' if table_name
                                         is None else table_name))


class UniverseDummy(Universe):

    def __init__(self, u_name, table_name=None):
        super(UniverseDummy,
              self).__init__(u_name,
                             table_name=('fut_universe_dummy' if table_name
                                         is None else table_name))