class StrategyBase(object):
    mmm = ""
    bbb = "bbb in class"
    def __init__(self, *args, **kwargs):
        xxx = "xxx"
        self.bbb = "bbb in init!"
        self.mmm = "ok!!!!!!!!!!!!!!!!!!!"
        self.ccc = "ccccc"
        print( "this is a test!! in base __init__")
        #print (self.strategy_id)
        #super(Mystrategy, self).__init__(*args, **kwargs)

    def on_schedule(self):
        pass

    def befor_day(self):
        pass

    def after_day(self):
        pass

    def on_login(self):
        pass

    def on_error(self, code, msg):
        pass

    def on_tick(self, tick):
        pass

    def on_bar(self, bar):
        pass

    def on_execrpt(self, res):
        pass

    def on_order_status(self, order):
        pass

    def on_order_new(self, res):
        pass

    def run(self):
        #未来可能会用golang 或c/c++改写
        bar = "kkkk"
        self.on_bar(bar)
        print ("running!!!!")
        return 0

