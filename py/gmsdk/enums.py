#!/usr/bin/env python
# encoding: utf-8



ExecType_New = 1
ExecType_DoneForDay = 4
ExecType_Canceled = 5
ExecType_PendingCancel = 6
ExecType_Stopped = 7
ExecType_Rejected = 8
ExecType_Suspended = 9
ExecType_PendingNew = 10
ExecType_Calculated = 11
ExecType_Expired = 12
ExecType_Restated = 13
ExecType_PendingReplace = 14
ExecType_Trade = 15
ExecType_TradeCorrect = 16
ExecType_TradeCancel = 17
ExecType_OrderStatus = 18
ExecType_CancelRejected = 19
ExecType_OptionInquiry_Failed = 20
ExecType_OptionExercise_Ok = 21
ExecType_OptionExercise_Failed = 22
ExecType_CancelOptionExercise_Ok = 23
ExecType_CancelOptionExercise_Failed = 24
ExecType_CombinePosition_Ok = 25
ExecType_CombinePosition_Failed = 26
ExecType_UncombinePosition_Ok = 27
ExecType_UncombinePosition_Failed = 28
OrderStatus_New = 1
OrderStatus_PartiallyFilled = 2
OrderStatus_Filled = 3
OrderStatus_DoneForDay = 4
OrderStatus_Canceled = 5
OrderStatus_PendingCancel = 6
OrderStatus_Stopped = 7
OrderStatus_Rejected = 8
OrderStatus_Suspended = 9
OrderStatus_PendingNew = 10
OrderStatus_Calculated = 11
OrderStatus_Expired = 12
OrderStatus_AcceptedForBidding = 13
OrderStatus_PendingReplace = 14
OrderRejectReason_UnknownReason = 1
OrderRejectReason_RiskRuleCheckFailed = 2
OrderRejectReason_NoEnoughCash = 3
OrderRejectReason_NoEnoughPosition = 4
OrderRejectReason_IllegalStrategyID = 5
OrderRejectReason_IllegalSymbol = 6
OrderRejectReason_IllegalVolume = 7
OrderRejectReason_IllegalPrice = 8
OrderRejectReason_NoMatchedTradingChannel = 9
OrderRejectReason_AccountForbidTrading = 10
OrderRejectReason_TradingChannelNotConnected = 11
OrderRejectReason_StrategyForbidTrading = 12
OrderRejectReason_NotInTradingSession = 13
CancelOrderRejectReason_OrderFinalized = 101
CancelOrderRejectReason_UnknownOrder = 102
CancelOrderRejectReason_BrokerOption = 103
CancelOrderRejectReason_AlreadyInPendingCancel = 104
OrderSide_Bid = 1
OrderSide_Ask = 2

OrderType_LMT = 0
OrderType_BOC = 1
OrderType_BOP = 2
OrderType_B5TC = 3
OrderType_B5TL = 4
OrderType_IOC = 5
OrderType_FOK = 6
OrderType_AON = 7
OrderType_MTL = 8
OrderType_EXE = 9

PositionEffect_Open = 1
PositionEffect_Close = 2
PositionEffect_CloseToday = 3
PositionEffect_CloseYesterday = 4
SecurityType_ChinaStock = 1
SecurityType_ChinaFuture = 2
SecurityType_ChinaOption = 3
CashChangeReason_Trade = 1
CashChangeReason_CashInout = 2


def _gen_c_enum():
    ec = [
        OrderStatus,
        OrderRejectReason,
        OrderSide,
        OrderType,
        ExecType,
        PositionEffect]
    c_res = []

    for e in ec:
        t = [(v, k) for k, v in list(e.__dict__.items()) if not k.startswith('__')]
        t = sorted(t)
        r = []
        r.append('// %s enum define' % e.__name__)
        for v, k in t:
            r.append("const char %s_%s = '%s';" % (e.__name__, k, v))
        c_res.append('\n'.join(r))
    print('\n\n'.join(c_res))


def _gen_csharp_enum():
    ec = [
        OrderStatus,
        OrderRejectReason,
        OrderSide,
        OrderType,
        ExecType,
        PositionEffect]
    csharp_res = []

    for e in ec:
        t = [(v, k) for k, v in list(e.__dict__.items()) if not k.startswith('__')]
        t = sorted(t)
        r = []
        r.append('// %s enum define' % e.__name__)
        r.append('public partial class %s' % e.__name__)
        r.append('{')
        for v, k in t:
            r.append("    public static readonly byte %s = Convert.ToByte('%s');" % (k, v))
        r.append('}')
        csharp_res.append('\n'.join(r))
    print('\n\n'.join(csharp_res))


def main():
    #_gen_c_enum()
    #_gen_csharp_enum()
    pass

# if __name__ == '__main__':
#     main()
