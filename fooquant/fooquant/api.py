#!/usr/bin/env python
# encoding: utf-8


import logging
import sys

if sys.version_info.major == 3:
    from configparser import ConfigParser
    from . import errors
    from .util import Event
    from .gm import *
else:
    from ConfigParser import ConfigParser
    import codecs
    import errors
    from util import Event
    from gm import *

# common event
_g_ev_timer = Event()

# market data event
_g_ev_md_login = Event()
_g_ev_md_event = Event()
_g_ev_md_tick = Event()
_g_ev_md_bar = Event()
_g_ev_md_error = Event()

# trade event
_g_ev_td_login = Event()
_g_ev_td_execrpt = Event()
_g_ev_td_order_status = Event()
_g_ev_td_order_rejected = Event()
_g_ev_td_order_new = Event()
_g_ev_td_order_filled = Event()
_g_ev_td_order_partially_filled = Event()
_g_ev_td_order_stop_executed = Event()
_g_ev_td_order_cancelled = Event()
_g_ev_td_order_cancel_rejected = Event()
_g_ev_td_error = Event()
_g_ev_td_backtest_finish = Event()
_g_ev_td_option_inquiry = Event()


def _on_timer_cb(interval):
    _g_ev_timer.fire(interval)


def _on_md_event_cb(event):
    _g_ev_md_event.fire(event)


def _on_md_tick_cb(tick):
    _g_ev_md_tick.fire(tick)


def _on_md_bar_cb(bar):
    _g_ev_md_bar.fire(bar)


def _on_md_error_cb(code, message):
    _g_ev_md_error.fire(code, message)


def _on_md_login_cb():
    _g_ev_md_login.fire()


def _on_td_login_cb():
    _g_ev_td_login.fire()


def _on_td_execrpt_cb(execrpt):
    _g_ev_td_execrpt.fire(execrpt)


def _on_td_order_status(order):
    _g_ev_td_order_status.fire(order)


def _on_td_order_rejected(order):
    _g_ev_td_order_rejected.fire(order)


def _on_td_order_new(order):
    _g_ev_td_order_new.fire(order)


def _on_td_order_filled(order):
    _g_ev_td_order_filled.fire(order)


def _on_td_order_partially_filled(order):
    _g_ev_td_order_partially_filled.fire(order)


def _on_td_order_stop_executed(order):
    _g_ev_td_order_stop_executed.fire(order)


def _on_td_order_cancelled(order):
    _g_ev_td_order_cancelled.fire(order)


def _on_td_order_cancel_rejected(execrpt):
    _g_ev_td_order_cancel_rejected.fire(execrpt)


def _on_td_error_cb(code, message):
    _g_ev_td_error.fire(code, message)


def _on_td_backtest_finish_cb(indicator):
    _g_ev_td_backtest_finish.fire(indicator)


def _on_td_option_inquiry_cb(option_inquiry):
    _g_ev_td_option_inquiry.fire(option_inquiry)


# set common callbacks
gm_set_timer_callback(_on_timer_cb)

# set market data callbacks
gm_md_set_login_callback(_on_md_login_cb)
gm_md_set_event_callback(_on_md_event_cb)
gm_md_set_tick_callback(_on_md_tick_cb)
gm_md_set_bar_callback(_on_md_bar_cb)
gm_md_set_error_callback(_on_md_error_cb)

# set trade callbacks
gm_td_set_login_callback(_on_td_login_cb)
gm_td_set_execrpt_callback(_on_td_execrpt_cb)
gm_td_set_order_status_callback(_on_td_order_status)
gm_td_set_order_rejected_callback(_on_td_order_rejected)
gm_td_set_order_new_callback(_on_td_order_new)
gm_td_set_order_filled_callback(_on_td_order_filled)
gm_td_set_order_partially_filled_callback(_on_td_order_partially_filled)
gm_td_set_order_cancelled_callback(_on_td_order_cancelled)
gm_td_set_order_stop_executed_callback(_on_td_order_stop_executed)
gm_td_set_order_cancel_rejected_callback(_on_td_order_cancel_rejected)
gm_td_set_error_callback(_on_td_error_cb)
gm_td_set_backtest_finish_callback(_on_td_backtest_finish_cb)
gm_td_set_option_inquiry_callback(_on_td_option_inquiry_cb)


def get_version():
    return gm_version()


def get_strerror(error_code):
    return gm_strerror(error_code)


def set_timeout_val(seconds):
    return gm_set_timeout_val(seconds)


def get_timeout_val():
    return gm_get_timeout_val()


# endif


class MdApi(object):
    def __init__(self):
        self.ev_login = _g_ev_md_login
        self.ev_event = _g_ev_md_event
        self.ev_tick = _g_ev_md_tick
        self.ev_bar = _g_ev_md_bar
        self.ev_error = _g_ev_md_error

        self.subscribed_symbols = set()

    def init(self,
             username,
             password,
             mode=1,
             subscribe_symbols='',
             start_time='',
             end_time='',
             gm_addr=''
             ):
        ''' connect to live market data server and login
            MD_MODE_NULL       = 1,  // 不接收行情流
            MD_MODE_LIVE       = 2,  // 接收实时行情
            MD_MODE_SIMULATED  = 3,  // 接收模拟行情
            MD_MODE_PLAYBACK   = 4   // 接收回放行情
        '''
        self.mode = mode
        self._add_sub_symbols(subscribe_symbols)
        ret = gm_login(str(username), str(password), str(gm_addr))
        if ret:
            return ret

        return gm_md_init(
            mode,
            str(subscribe_symbols),
            str(start_time),
            str(end_time))

    def run(self):
        ''' run to get stream md data. necessary for Live/Simulated/Playback mode.'''
        if self.mode == 4:  # playback
            gm_run()
        else:
            while True:
                gm_poll()

    def close(self):
        ''' logout and disconnect'''
        gm_logout()

    def reconnect(self):
        ''' reconnect '''
        return gm_md_reconnect()

    def _add_sub_symbols(self, symbols):
        symbol_list = list(filter(bool, [s.strip() for s in symbols.split(',')]))
        self.subscribed_symbols.update(symbol_list)

    def _remove_sub_symbols(self, symbols):
        symbol_list = list(filter(bool, [s.strip() for s in symbols.split(',')]))
        self.subscribed_symbols.difference_update(symbol_list)

    def subscribe(self, symbols):
        self._add_sub_symbols(symbols)
        return gm_md_subscribe(str(symbols))

    def resubscribe(self, symbols):
        # self._add_sub_symbols(symbols)
        return gm_md_resubscribe(str(symbols))

    def unsubscribe(self, symbols):
        self._remove_sub_symbols(symbols)
        return gm_md_unsubscribe(str(symbols))

    def get_ticks(self, symbols, begin_time, end_time):
        return gm_md_get_ticks(str(symbols), str(begin_time), str(end_time))

    def get_last_ticks(self, symbols):
        return gm_md_get_last_ticks(str(symbols))

    def get_last_n_ticks(self, symbol, n, end_time=""):
        return gm_md_get_last_n_ticks(str(symbol), n, str(end_time))

    def get_bars(self, symbols, bar_type, begin_time, end_time):
        return gm_md_get_bars(str(symbols), bar_type, str(begin_time), str(end_time))

    def get_last_bars(self, symbols, bar_type):
        return gm_md_get_last_bars(str(symbols), bar_type)

    def get_last_n_bars(self, symbol, bar_type, n, end_time=""):
        return gm_md_get_last_n_bars(str(symbol), bar_type, n, str(end_time))

    def get_dailybars(self, symbols, begin_time, end_time):
        return gm_md_get_dailybars(str(symbols), str(begin_time), str(end_time))

    def get_last_dailybars(self, symbols):
        return gm_md_get_last_dailybars(str(symbols))

    def get_last_n_dailybars(self, symbol, n, end_time=""):
        return gm_md_get_last_n_dailybars(str(symbol), n, str(end_time))

    def get_instruments(self, exchange, sec_type, is_active):
        return gm_md_get_instruments(str(exchange), sec_type, is_active)

    def get_instruments_by_name(self, name):
        return gm_md_get_instruments_by_name(str(name))

    def get_constituents(self, index_symbol):
        return gm_md_get_constituents(str(index_symbol))

    def get_financial_index(self, symbol, t_begin, t_end):
        return gm_md_get_financial_index(str(symbol), str(t_begin), str(t_end))

    def get_last_financial_index(self, symbol_list):
        return gm_md_get_last_financial_index(str(symbol_list))

    def get_last_n_financial_index(self, symbol, n):
        return gm_md_get_last_n_financial_index(str(symbol), n)

    def get_share_index(self, symbol, t_begin, t_end):
        return gm_md_get_share_index(str(symbol), str(t_begin), str(t_end))

    def get_last_share_index(self, symbol_list):
        return gm_md_get_last_share_index(str(symbol_list))

    def get_last_n_share_index(self, symbol, n):
        return gm_md_get_last_n_share_index(str(symbol), n)

    def get_market_index(self, symbol, t_begin, t_end):
        return gm_md_get_market_index(str(symbol), str(t_begin), str(t_end))

    def get_last_market_index(self, symbol_list):
        return gm_md_get_last_market_index(str(symbol_list))

    def get_last_n_market_index(self, symbol, n):
        return gm_md_get_last_n_market_index(str(symbol), n)

    def get_calendar(self, exchange, start_time, end_time):
        return gm_md_get_calendar(str(exchange), str(start_time), str(end_time))

    def get_stock_adj(self, symbol, start_time, end_time):
        return gm_md_get_stock_adj(str(symbol), str(start_time), str(end_time))

    def get_divident(self, symbol, start_time, end_time):
        return gm_md_get_divident(str(symbol), str(start_time), str(end_time))

    def get_virtual_contract(self, vsymbol, start_time, end_time):
        return gm_md_get_virtual_contract(str(vsymbol), str(start_time), str(end_time))


class TdApi(object):
    def __init__(self):
        self.ev_login = _g_ev_td_login
        self.ev_execrpt = _g_ev_td_execrpt
        self.ev_order_status = _g_ev_td_order_status
        self.ev_order_rejected = _g_ev_td_order_rejected
        self.ev_order_new = _g_ev_td_order_new
        self.ev_order_filled = _g_ev_td_order_filled
        self.ev_order_partially_filled = _g_ev_td_order_partially_filled
        self.ev_order_stop_executed = _g_ev_td_order_stop_executed
        self.ev_order_cancelled = _g_ev_td_order_cancelled
        self.ev_order_cancel_rejected = _g_ev_td_order_cancel_rejected
        self.ev_error = _g_ev_td_error
        self.ev_backtest_finish = _g_ev_td_backtest_finish
        self.ev_option_inquiry = _g_ev_td_option_inquiry

    def init(self,
             username,
             password,
             strategy_id,
             td_addr='',
             ):
        ''' connect to trade server and login '''
        ret = gm_login(str(username), str(password), '')
        if ret:
            return ret

        return gm_td_init(str(strategy_id), str(td_addr))

    def close(self):
        ''' logout and disconnect'''
        gm_logout()

    def run(self):
        ''' run to get stream td data. '''
        while True:
            gm_poll()

    def reconnect(self):
        ''' reconnect '''
        return gm_td_reconnect()

    def open_long(self, exchange, sec_id, price, volume):
        return gm_td_open_long(str(exchange), str(sec_id), float(price), float(volume))

    def open_short(self, exchange, sec_id, price, volume):
        return gm_td_open_short(str(exchange), str(sec_id), float(price), float(volume))

    def close_long(self, exchange, sec_id, price, volume):
        return gm_td_close_long(str(exchange), str(sec_id), float(price), float(volume))

    def close_short(self, exchange, sec_id, price, volume):
        return gm_td_close_short(str(exchange), str(sec_id), float(price), float(volume))

    def close_long_yesterday(self, exchange, sec_id, price, volume):
        return gm_td_close_long_yesterday(str(exchange), str(sec_id), float(price), float(volume))

    def close_short_yesterday(self, exchange, sec_id, price, volume):
        return gm_td_close_short_yesterday(str(exchange), str(sec_id), float(price), float(volume))

    def place_order(self, order):
        return gm_td_place_order(order)

    def cancel_order(self, cl_ord_id):
        return gm_td_cancel_order(str(cl_ord_id))

    def open_long_sync(self, exchange, sec_id, price, volume):
        return gm_td_open_long_sync(str(exchange), str(sec_id), float(price), float(volume))

    def open_short_sync(self, exchange, sec_id, price, volume):
        return gm_td_open_short_sync(str(exchange), str(sec_id), float(price), float(volume))

    def close_long_sync(self, exchange, sec_id, price, volume):
        return gm_td_close_long_sync(str(exchange), str(sec_id), float(price), float(volume))

    def close_short_sync(self, exchange, sec_id, price, volume):
        return gm_td_close_short_sync(str(exchange), str(sec_id), float(price), float(volume))

    def close_long_yesterday_sync(self, exchange, sec_id, price, volume):
        return gm_td_close_long_yesterday_sync(str(exchange), str(sec_id), float(price), float(volume))

    def close_short_yesterday_sync(self, exchange, sec_id, price, volume):
        return gm_td_close_short_yesterday_sync(str(exchange), str(sec_id), float(price), float(volume))

    def place_order_sync(self, order):
        return gm_td_place_order_sync(order)

    def cancel_order_sync(self, cl_ord_id):
        return gm_td_cancel_order_sync(str(cl_ord_id))

    def get_order(self, cl_ord_id):
        return gm_td_get_order(str(cl_ord_id))

    def get_orders(self, start_time, end_time):
        return gm_td_get_orders(str(start_time), str(end_time))

    def get_orders_by_symbol(self, exchange, sec_id, start_time, end_time):
        return gm_td_get_orders_by_symbol(str(exchange), str(sec_id), str(start_time), str(end_time))

    def get_unfinished_orders(self):
        return gm_td_get_unfinished_orders()

    def get_cash(self):
        return gm_td_get_cash()

    def get_position(self, exchange, sec_id, side):
        return gm_td_get_position(str(exchange), str(sec_id), side)

    def get_positions(self):
        return gm_td_get_positions()

    def get_indicator(self):
        return gm_td_get_indicator()

    def get_broker_accounts(self):
        return gm_td_get_broker_accounts()

    def get_broker_cash(self):
        return gm_td_get_broker_cash()

    def get_broker_positions(self):
        return gm_td_get_broker_positions()

    def option_inquiry(self, exchange, sec_id):
        gm_td_option_inquiry(str(exchange), str(sec_id))

    def option_exercise(self, exercise_order):
        return gm_td_option_exercise(exercise_order)

    def cancel_option_exercise(self, exchange, exec_order_id):
        return gm_td_cancel_option_exercise(str(exchange), str(exec_order_id))

    def combine_position(self, exchange, sec_id, side, volume):
        return gm_td_combine_position(str(exchange), str(sec_id), side, volume)

    def uncombine_position(self, exchange, sec_id, side, volume):
        return gm_td_uncombine_position(str(exchange), str(sec_id), side, volume)


md = MdApi()
td = TdApi()


class StrategyBase(object):
    def __init__(self,
                 username='',
                 password='',
                 strategy_id='',
                 subscribe_symbols='',
                 mode=2,
                 config_file=None,
                 config_file_encoding='utf-8',
                 td_addr='',
                 gm_addr=''):

        self.logger = logging.getLogger(__name__)
        self.gm_addr = gm_addr
        self.td_addr = td_addr
        self.username = username
        self.password = password
        self.strategy_id = strategy_id
        self.subscribe_symbols = subscribe_symbols
        self.mode = mode
        self.config_file = config_file
        self.start_time = None
        self.end_time = None
        self.initial_cash = None
        self.transaction_ratio = None
        self.commission_ratio = None
        self.slippage_ratio = None

        self.md = md
        self.td = td

        self.md.ev_login += self.on_login
        self.md.ev_event += self.on_md_event
        self.md.ev_tick += self.on_tick
        self.md.ev_bar += self.on_bar
        self.md.ev_error += self.on_error

        self.td.ev_login += self.on_login
        self.td.ev_execrpt += self.on_execrpt
        self.td.ev_order_status += self.on_order_status
        self.td.ev_order_rejected += self.on_order_rejected
        self.td.ev_order_new += self.on_order_new
        self.td.ev_order_filled += self.on_order_filled
        self.td.ev_order_partially_filled += self.on_order_partially_filled
        self.td.ev_order_stop_executed += self.on_order_stop_executed
        self.td.ev_order_cancelled += self.on_order_cancelled
        self.td.ev_order_cancel_rejected += self.on_order_cancel_rejected
        self.td.ev_error += self.on_error
        self.td.ev_backtest_finish += self.on_backtest_finish
        self.td.ev_option_inquiry += self.on_option_inquiry

        self.ev_timer = _g_ev_timer
        self.ev_timer += self.on_timer

        self.run_loop = True
        self.init_ret = 0
        self.config = None
        if self.config_file:
            default_cfg = {
                'mode': 2,
                'gm_addr': '',
                'td_addr': '',
                'initial_cash': 1000000,
                'transaction_ratio': 1,
                'commission_ratio': 0,
                'slippage_ratio': 0,
                'price_type': 1
            }
            if sys.version_info.major == 3:
                self.config = ConfigParser(default_cfg)
                self.config.read(self.config_file, encoding=config_file_encoding)
            else:
                self.config = ConfigParser(default_cfg)
                with codecs.open(self.config_file, 'r', encoding=config_file_encoding) as f:
                    self.config.readfp(f)
            self.gm_addr = self.config.get('strategy', 'gm_addr')
            self.td_addr = self.config.get('strategy', 'td_addr')
            self.username = self.config.get('strategy', 'username')
            self.password = self.config.get('strategy', 'password')
            self.strategy_id = self.config.get('strategy', 'strategy_id')
            self.subscribe_symbols = self.config.get('strategy', 'subscribe_symbols')
            self.mode = self.config.getint('strategy', 'mode')
            if self.mode == 4:
                try:
                    self.start_time = self.config.get('backtest', 'start_time')
                    self.end_time = self.config.get('backtest', 'end_time')
                    try:
                        self.initial_cash = self.config.getfloat('backtest', 'initial_cash')
                    except TypeError:
                        self.initial_cash = default_cfg['initial_cash']
                    try:
                        self.transaction_ratio = self.config.getfloat('backtest', 'transaction_ratio')
                    except TypeError:
                        self.transaction_ratio = default_cfg['transaction_ratio']
                    try:
                        self.commission_ratio = self.config.getfloat('backtest', 'commission_ratio')
                    except TypeError:
                        self.commission_ratio = default_cfg['commission_ratio']
                    try:
                        self.slippage_ratio = self.config.getfloat('backtest', 'slippage_ratio')
                    except TypeError:
                        self.slippage_ratio = default_cfg['slippage_ratio']
                    try:
                        self.price_type = self.config.getint('backtest', 'price_type')
                    except TypeError:
                        self.price_type = default_cfg['price_type']
                except:
                    pass
            self.init_ret = strategy_init_with_config(str(self.config_file))
        else:
            self.init_ret = strategy_init_ex(
                str(self.username),
                str(self.password),
                str(self.strategy_id),
                str(self.subscribe_symbols),
                self.mode,
                str(self.td_addr),
                '',
                '',
                str(self.gm_addr))

    def backtest_config(self,
                        start_time,
                        end_time,
                        initial_cash=1000000,
                        transaction_ratio=1,
                        commission_ratio=0,
                        slippage_ratio=0,
                        price_type=1,
                        bench_symbol='',
                        check_cache=1):
        self.start_time = start_time
        self.end_time = end_time
        self.initial_cash = initial_cash
        self.transaction_ratio = transaction_ratio
        self.commission_ratio = commission_ratio
        self.slippage_ratio = slippage_ratio
        self.price_type = price_type
        self.bench_symbol = bench_symbol
        self.check_cache = check_cache
        return strategy_backtest_config(
            str(self.start_time),
            str(self.end_time),
            self.initial_cash,
            self.transaction_ratio,
            self.commission_ratio,
            self.slippage_ratio,
            self.price_type,
            self.bench_symbol,
            self.check_cache)

    def on_tick(self, tick):
        pass

    def on_bar(self, bar):
        pass

    def on_login(self):
        pass

    def on_execrpt(self, execrpt):
        pass

    def on_order_status(self, order):
        pass

    def on_order_rejected(self, order):
        pass

    def on_order_new(self, order):
        pass

    def on_order_filled(self, order):
        pass

    def on_order_partially_filled(self, order):
        pass

    def on_order_stop_executed(self, order):
        pass

    def on_order_cancelled(self, order):
        pass

    def on_order_cancel_rejected(self, execrpt):
        pass

    def on_error(self, code, msg):
        pass

    def on_backtest_finish(self, indicator):
        pass

    def on_option_inquiry(self, option_inquiry):
        pass

    def on_md_event(self, event):
        pass

    def on_timer(self, interval):
        pass

    def run(self):
        if self.init_ret:
            return self.init_ret
        else:
            if self.mode == 4:  # playback
                return gm_run()
            else:
                while self.run_loop:
                    gm_poll()

    def stop(self):
        # return gm_logout()
        self.run_loop = False

    def get_version(self):
        return get_version()

    def get_strerror(self, error_code):
        return get_strerror(error_code)

    def set_timeout_val(self, seconds):
        return set_timeout_val(seconds)

    def get_timeout_val(self):
        return get_timeout_val()

    def set_timer(self, interval):
        gm_set_timer(interval)

    def unset_timer(self, interval):
        gm_unset_timer(interval)

    ## trade service
    def place_order(self, order):
        return self.td.place_order(order)

    def cancel_order(self, cl_ord_id):
        return self.td.cancel_order(cl_ord_id)

    def open_long(self, exchange, sec_id, price, volume):
        return self.td.open_long(exchange, sec_id, price, volume)

    def close_long(self, exchange, sec_id, price, volume):
        return self.td.close_long(exchange, sec_id, price, volume)

    def open_short(self, exchange, sec_id, price, volume):
        return self.td.open_short(exchange, sec_id, price, volume)

    def close_short(self, exchange, sec_id, price, volume):
        return self.td.close_short(exchange, sec_id, price, volume)

    def close_long_yesterday(self, exchange, sec_id, price, volume):
        return self.td.close_long_yesterday(exchange, sec_id, price, volume)

    def close_short_yesterday(self, exchange, sec_id, price, volume):
        return self.td.close_short_yesterday(exchange, sec_id, price, volume)

    def close_long_yesterday_sync(self, exchange, sec_id, price, volume):
        return self.td.close_long_yesterday_sync(exchange, sec_id, price, volume)

    def close_short_yesterday_sync(self, exchange, sec_id, price, volume):
        return self.td.close_short_yesterday_sync(exchange, sec_id, price, volume)

    def place_order_sync(self, order):
        return self.td.place_order_sync(order)

    def cancel_order_sync(self, cl_ord_id):
        return self.td.cancel_order_sync(cl_ord_id)

    def open_long_sync(self, exchange, sec_id, price, volume):
        return self.td.open_long_sync(exchange, sec_id, price, volume)

    def close_long_sync(self, exchange, sec_id, price, volume):
        return self.td.close_long_sync(exchange, sec_id, price, volume)

    def open_short_sync(self, exchange, sec_id, price, volume):
        return self.td.open_short_sync(exchange, sec_id, price, volume)

    def close_short_sync(self, exchange, sec_id, price, volume):
        return self.td.close_short_sync(exchange, sec_id, price, volume)

    def get_position(self, exchange, sec_id, side):
        return self.td.get_position(exchange, sec_id, side)

    def get_positions(self):
        return self.td.get_positions()

    def get_cash(self):
        return self.td.get_cash()

    def get_order(self, cl_ord_id):
        return self.td.get_order(cl_ord_id)

    def get_orders(self, start_time, end_time):
        return self.td.get_orders(start_time, end_time)

    def get_orders_by_symbol(self, exchange, sec_id, start_time, end_time):
        return self.td.get_orders_by_symbol(exchange, sec_id, start_time, end_time)

    def get_unfinished_orders(self):
        return self.td.get_unfinished_orders()

    def get_indicator(self):
        return self.td.get_indicator()

    def get_broker_accounts(self):
        return self.td.get_broker_accounts()

    def get_broker_cash(self):
        return self.td.get_broker_cash()

    def get_broker_positions(self):
        return self.td.get_broker_positions()

    def option_inquiry(self, exchange, sec_id):
        self.td.option_inquiry(exchange, sec_id)

    def option_exercise(self, exercise_order):
        return self.td.option_exercise(exercise_order)

    def cancel_option_exercise(self, exchange, exec_order_id):
        return self.td.cancel_option_exercise(exchange, exec_order_id)

    def combine_position(self, exchange, sec_id, side, volume):
        return self.td.combine_position(exchange, sec_id, side, volume)

    def uncombine_position(self, exchange, sec_id, side, volume):
        return self.td.uncombine_position(exchange, sec_id, side, volume)

    ## market data service
    def get_ticks(self, symbols, begin_time, end_time):
        return self.md.get_ticks(symbols, begin_time, end_time)

    def get_last_ticks(self, symbols):
        return self.md.get_last_ticks(symbols)

    def get_last_n_ticks(self, symbol, n, end_time=''):
        return self.md.get_last_n_ticks(symbol, n, end_time)

    def get_bars(self, symbols, bar_type, begin_time, end_time):
        return self.md.get_bars(symbols, bar_type, begin_time, end_time)

    def get_last_bars(self, symbols, bar_type):
        return self.md.get_last_bars(symbols, bar_type)

    def get_last_n_bars(self, symbol, bar_type, n, end_time=''):
        return self.md.get_last_n_bars(symbol, bar_type, n, end_time)

    def get_dailybars(self, symbols, begin_time, end_time):
        return self.md.get_dailybars(symbols, begin_time, end_time)

    def get_last_dailybars(self, symbols):
        return self.md.get_last_dailybars(symbols)

    def get_last_n_dailybars(self, symbol, n, end_time=''):
        return self.md.get_last_n_dailybars(symbol, n, end_time)

    def subscribe(self, symbols):
        return self.md.subscribe(symbols)

    def resubscribe(self, symbols):
        return self.md.resubscribe(symbols)

    def unsubscribe(self, symbols):
        return self.md.unsubscribe(symbols)

    def get_instruments(self, exchange, sec_type, is_active):
        return self.md.get_instruments(exchange, sec_type, is_active)

    def get_instruments_by_name(self, name):
        return self.md.get_instruments_by_name(name)

    def get_constituents(self, index_symbol):
        return self.md.get_constituents(index_symbol)

    def get_financial_index(self, symbol, t_begin, t_end):
        return self.md.get_financial_index(symbol, t_begin, t_end)

    def get_last_financial_index(self, symbol_list):
        return self.md.get_last_financial_index(symbol_list)

    def get_last_n_financial_index(self, symbol, n):
        return self.md.get_last_n_financial_index(symbol, n)

    def get_share_index(self, symbol, t_begin, t_end):
        return self.md.get_share_index(symbol, t_begin, t_end)

    def get_last_share_index(self, symbol_list):
        return self.md.get_last_share_index(symbol_list)

    def get_last_n_share_index(self, symbol, n):
        return self.md.get_last_n_share_index(symbol, n)

    def get_market_index(self, symbol, t_begin, t_end):
        return self.md.get_market_index(symbol, t_begin, t_end)

    def get_last_market_index(self, symbol_list):
        return self.md.get_last_market_index(symbol_list)

    def get_last_n_market_index(self, symbol, n):
        return self.md.get_last_n_market_index(symbol, n)

    def get_calendar(self, exchange, start_time, end_time):
        return self.md.get_calendar(exchange, start_time, end_time)

    def get_stock_adj(self, symbol, start_time, end_time):
        return self.md.get_stock_adj(symbol, start_time, end_time)

    def get_divident(self, symbol, start_time, end_time):
        return self.md.get_divident(symbol, start_time, end_time)

    def get_virtual_contract(self, vsymbol, start_time, end_time):
        return self.md.get_virtual_contract(vsymbol, start_time, end_time)
