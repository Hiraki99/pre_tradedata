#!/bin/bash
# $app1 = "runDeposit.py"
# $app2 = "runGateway.py"
# $app3 = "runTrade.py"
test=`ps aux | grep "runPreTradeData" | grep -v grep -c`
if [ $test == 0 ]; then
        #pip install -r requirements.txt
        python3 runPreTradeData.py --env=pre_trade_data >> logs-pre-trade.log  &
        celery -A runPreTradeData.celery worker -l info &
        echo "[INFO] Service is starting"
        exit
else
        echo "[WARN] Service is already running"
        exit
fi