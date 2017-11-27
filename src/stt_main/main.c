package main

import(
	"fmt"
    ""
)

                        start_time,
                        end_time,
                        initial_cash=1000000,
                        transaction_ratio=1,
                        commission_ratio=0,
                        slippage_ratio=0,
                        price_type=1,
                        bench_symbol='',
                        check_cache=1):

                 username='',
                 password='',
                 strategy_id='',
                 subscribe_symbols='',
                 mode=2,
                 config_file=None,
                 config_file_encoding='utf-8',
                 td_addr='',
                 gm_addr=''):

        self.gm_addr = gm_addr
        self.td_addr = td_addr
        self.username = username
        self.password = password
        self.strategy_id = strategy_id


    def on_execrpt( self, res ):
        pass

    def on_order_status( self, order ):
        pass

    def on_order_new( self, res ):
        pass

    def on_order_filled( self, res ):
        pass

    def on_order_partiall_filled( self, res ):
        pass

    def on_order_stop_executed( self, res ):
        pass

    def on_order_canceled( self, res ):
        pass

    def on_order_cancel_rejected( self, res ):
        pass


func main(){
   init()  // 多合约，多级别
      on_login() //
   get_data()
   
   while {  // goroutine for  sub data 
      befor_trading()
      after_trading(){
	     //调仓位 换股，换策略
      }
   }
   while { // another goroutine : sub data
      on_tick(){
		 risk(){}
      }
      on_bar( 1m ) { //针对每个合约都需要做？
        get_last_n_bar() { } // goroutine  send and receive data!
		risk(){}
	  }
      on_bar( 30m ) { //针对每个合约都需要做？
        get_last_n_bar() { } // goroutine  send and receive data!
		risk(){}
	  }
      on_bar( 4H ) { //针对每个合约都需要做？
        get_last_n_bar() { } // goroutine  send and receive data!
		risk(){}
	  }
      on_error() // 其它问题?
	  on_disconn() //网络出问题？

      //如果有多个级别的数据，只能串行处理，根据收到的时间先后来处理。
      // 风险控制如何处理？
   }
}
