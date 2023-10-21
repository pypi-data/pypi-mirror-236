from okx_candle import CandleServer, CandleRule

if __name__ == '__main__':
    # 币币交易：SPOT；永续合约：SWAP；交割合约：FUTURES；期权：OPTION
    instType = 'SWAP'
    # 永续合约，默认规则
    candleServer = CandleServer(instType, CandleRule)
    # 下载2023-01-01 ~ 2023-01-02 全部instType的历史K线
    candleServer.download_candles_by_date(
        start='2023-01-01',
        end='2023-01-02',
    )
