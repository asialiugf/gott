#!/usr/bin/env python
# encoding: utf-8

import sys
if sys.version_info.major == 3:
    from .api import md, td, StrategyBase, get_strerror, get_version, set_timeout_val, get_timeout_val
    from .enums import *
    from .util import to_dict
    from .gm import Cash, Position, Order, ExecRpt, Tick, Bar, DailyBar, Indicator
else:
    from api import md, td, StrategyBase, get_strerror, get_version, set_timeout_val, get_timeout_val
    from enums import *
    from util import to_dict
    from gm import Cash, Position, Order, ExecRpt, Tick, Bar, DailyBar, Indicator
