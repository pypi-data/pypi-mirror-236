from binance_candle import Market
from pprint import pprint

if __name__ == '__main__':
    proxy_host = None # http://xxx.xx.xx.xx
    # 币币交易：SPOT；U本位合约：UM；币本位合约：CM
    instType = 'UM'
    # 实例化行情Market
    market = Market(instType,proxy_host=proxy_host)
    # 单个产品的深度信息 limit : 数量
    pprint(market.get_depth('BTCUSDT', limit=10))
