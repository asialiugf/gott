#!/usr/bin/env python
# encoding: utf-8


# 共用的配置或通讯层面的错诿 1000~1499

SUCCESS                                  = 0     # "成功"

ERR_CONFIG_FILE_NOT_EXIST                = 1001  # "策略配置文件不存圿"
ERR_CONFIG_PARSE                         = 1002  # "策略配置文件格式错误"
ERR_AUTH_CONNECT                         = 1003  # "无法连接掘金认证服务"
ERR_AUTH_LOGIN                           = 1004  # "无法登录掘金认证服务"
ERR_REQUEST_TIMEOUT                      = 1005  # "请求超时"
ERR_INVALID_PARAMETER                    = 1006  # "非法参数"
ERR_STRATEGY_INIT                        = 1007  # "策略未初始化"
ERR_INTERNAL_INIT_ERROR                  = 1008  # "SDK内部初始化错诿"
ERR_API_SERVER_CONNECT                   = 1009  # "无法连接掘金API服务"

# 业务层面错误砿 共有部分＿ 1500~1999

ERR_INVALID_SYMBOL                       = 1501  # "非法证券代码"
ERR_INVALID_DATE                         = 1502  # "非法日期格式"
ERR_INVALID_STRATEGY_ID                  = 1503  # "非法策略ID"

# 交易部分 2000 ~ 2999

ERR_TD_CONNECT                           = 2000  # "交易服务连接失败"
ERR_TD_LOGIN                             = 2001  # "交易服务登录失败"
ERR_TD_TIMEOUT                           = 2002  # "交易命令请求超时"
ERR_TD_NO_RESULT                         = 2003  # "该条件没查到数据"
ERR_TD_INVALID_SESSION                   = 2004  # "交易请求没有登陆"
ERR_TD_INVALID_PARAMETER                 = 2005  # "交易请求参数非法"
ERR_TD_STRATEGY_LOCKED                   = 2006  # "策略被禁止交昿"
ERR_TD_SERVER_ERROR                      = 2007  # "交易服务内部错误"
ERR_TD_CORRUPT_DATA                      = 2008  # "返回数据包错诿"
ERR_TD_CONNECT_CLOSE                     = 2009  # "交易服务连接断开"


# 数据服务部分 3000~3999

ERR_MD_CONNECT                           = 3000  # "数据服务连接失败"
ERR_MD_LOGIN                             = 3001  # "数据服务登录失败"
ERR_MD_TIMEOUT                           = 3002  # "数据服务请求超时"
ERR_MD_NO_RESULT                         = 3003  # "该条件没查到数据"
ERR_MD_BUFFER_ALLOC                      = 3005  # "分配缓冲区错诿"
ERR_MD_INVALID_PARAMETER                 = 3006  # "数据请求参数非法"
ERR_MD_SERVER_ERROR                      = 3007  # "数据服务内部错误"
ERR_MD_CORRUPT_DATA                      = 3008  # "返回数据包错诿"
ERR_MD_CONNECT_CLOSE                     = 3009  # "数据服务连接断开"

#回测部分 4000~4999

ERR_BT_INVALID_TIMESPAN                  = 4000  # "回测时间区间错误"
ERR_BT_INVALID_INITIAL_CASH              = 4001  # "回测请求参数非法"
ERR_BT_INVALID_TRANSACTION_RATIO         = 4002  # "回测请求参数非法"
ERR_BT_INVALID_COMMISSION_RATIO          = 4003  # "回测请求参数非法"
ERR_BT_INVALID_SLIPPAGE_RATIO            = 4004  # "回测请求参数非法"
ERR_BT_READ_CACHE_ERROR                  = 4005  # "回测读取缓存数据错误"
ERR_BT_WRITE_CACHE_ERROR                 = 4006  # "回测写入缓存数据错误"
ERR_BT_CONNECT                           = 4007  # "回测服务连接失败"
ERR_BT_RESULT                            = 4008  # "回测绩效生成失败"


#网络错误 10000~19999
ERR_NET_ERROR                            = 10000 # "网络错误"

def _gen_error_from_c_define():
    f = '../../c/inc/error.h'
    r = []
    with open(f) as e:
        for l in e:
            l = l.strip()
            if l.startswith('#define'):
                t = l.split()
                if len(t) != 5:
                    print('illegal line: %s. skip...' % l)
                else:
                    r.append('%-40s = %-4s  %s %s' % (t[1], t[2], '#', t[4]))
            else:
                r.append(l.replace('/*', '#').replace('*/', ''))
    print('\n'.join(r))

def _gen_c_str_error_from_c_define():
    f = '../../c/inc/error.h'
    r = []
    with open(f) as e:
        for l in e:
            l = l.strip()
            if l.startswith('#define'):
                t = l.split()
                if len(t) != 5:
                    print('illegal line: %s. skip...' % l)
                else:
                    tmp = 'strerror[%s]' % t[1]
                    r.append('%-50s = %s;' % (tmp, t[4]))
            else:
                r.append(l)
    print('\n'.join(r))

if __name__ == '__main__':
#     #_gen_c_str_error_from_c_define()
    _gen_error_from_c_define()
