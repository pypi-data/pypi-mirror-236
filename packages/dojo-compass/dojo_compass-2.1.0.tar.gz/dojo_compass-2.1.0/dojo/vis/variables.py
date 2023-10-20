"""Global variables for the dashboard."""
import datetime
import random
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List, Set, Union

import jsons

from dojo.environments.uniswapV3 import UniV3ActionType
from dojo.vis import variables


def random_continue(value):
    """TODO."""
    return value * 0.5 + value * (1.0 - (random.random() - 0.5)) * 0.5


@dataclass
class Bookmark:
    """Users can create bookmarks by clicking in the graph."""

    name: str
    block: int


@dataclass
class Action:
    """Holds information about taken actions."""

    type: UniV3ActionType
    info: str = None

    __annotations__ = {"type": UniV3ActionType, "info": str}


@dataclass
class Portfolio:
    """Holds information about an agents portfolio."""

    token0: float
    token1: float

    __annotations__ = {"token0": float, "token1": float}


@dataclass
class Liquidities:
    """Holds the wallet as well as the LP portfolio."""

    lp: Portfolio
    wallet: Portfolio

    __annotations__ = {"lp": Portfolio, "wallet": Portfolio}


@dataclass
class PoolData:
    """TODO."""

    price: Union[float, None]
    liquidity: Union[int, None]
    __annotations__ = {"price": Union[float, None], "liquidity": Union[int, None]}


@dataclass
class AgentData:
    """TODO."""

    reward: Union[float, None]
    actions: Union[List[Action], None]
    liquidities: Union[Liquidities, None]
    __annotations__ = {
        "reward": Union[float, None],
        "actions": Union[List[Action], None],
        "liquidities": Union[Liquidities, None],
    }


@dataclass
class BlockData:
    """Per block data."""

    pooldata: Dict[str, PoolData]
    agentdata: List[AgentData]
    signals: Dict[str, float]
    __annotations__ = {
        "pooldata": Dict[str, PoolData],
        "agentdata": List[AgentData],
        "signals": Dict[str, float],
    }


@dataclass
class PoolInfo:
    """TODO."""

    name: str
    token0: str
    token1: str
    fee: float
    __annotations__ = {"name": str, "token0": str, "token1": str, "fee": float}


@dataclass
class Params:
    """Simulation params."""

    progress_value: Union[float, None]
    agents: Union[List[str], None]
    pool_info: List[PoolInfo]
    start_date: Union[datetime.datetime, None]
    end_date: Union[datetime.datetime, None]
    signal_names: Set[str] = field(default_factory=set)

    __annotations__ = {
        "progress_value": Union[float, None],
        "agents": Union[List[str], None],
        "pool_info": List[PoolInfo],
        "start_date": Union[datetime.datetime, str, None],
        "end_date": Union[datetime.datetime, str, None],
        "signal_names": Set[str],
    }


@dataclass
class Data:
    """Full data."""

    blockdata: BlockData
    params: Params
    __annotations__ = {"blockdata": Dict[int, BlockData], "params": Params}


def _def_value_data():
    """Helper function."""
    pooldata = {}
    agentdata = AgentData(reward=None, actions=[], liquidities=None)
    return BlockData(pooldata=pooldata, agentdata=[agentdata], signals={})


def _def_value_params():
    """Helper function."""
    return Params(
        progress_value=None,
        agents=[],
        pool=None,
        start_date=None,
        end_date=None,
    )


data = Data(
    params=Params(
        progress_value=1,
        agents=[],
        pool_info=[],
        start_date=datetime.datetime(1900, 1, 1),
        end_date=datetime.datetime(1900, 1, 20),
    ),
    blockdata=defaultdict(_def_value_data),
)

bookmarks = []


is_demo = False


def reset():
    """Set back all variables to initial state."""
    global data
    data = Data(
        params=Params(
            progress_value=1,
            agents=[],
            pool_info=[],
            start_date=datetime.datetime(1900, 1, 1),
            end_date=datetime.datetime(1900, 1, 20),
        ),
        blockdata=defaultdict(_def_value_data),
    )


def _from_file(filepath):
    with open(filepath) as f:
        variables.data = jsons.loads(f.read(), variables.Data)
