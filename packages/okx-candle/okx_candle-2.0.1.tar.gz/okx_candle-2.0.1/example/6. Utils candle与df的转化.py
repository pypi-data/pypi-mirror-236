from okx_candle import Market
from okx_candle.utils import candle_to_df, df_to_candle
from pprint import pprint

if __name__ == '__main__':
    # 币币交易：SPOT；永续合约：SWAP；交割合约：FUTURES；期权：OPTION
    instType = 'SWAP'
    # 实例化行情Market
    market = Market(instType, timezone='Asia/Shanghai')
    # 按照起始时间获取历史K线
    result = market.get_history_candle(
        symbol='BTC-USDT-SWAP',
        start='2023-01-01 00:00:00',
        end='2023-01-01 10:00:00',
        bar='1m',
    )
    candle = result['data']
    # <candle:np.ndarray> 转化为 <df:pd.DataFrame>
    df = candle_to_df(candle)
    pprint(df)
    # <df:pd.DataFrame> 转化为 <candle:np.ndarray>
    candle = df_to_candle(df)
    pprint(candle)
