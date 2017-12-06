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

