from . import Micro
import traceback
from flask import jsonify
import datetime


# open account
import uuid
import random
from sqlalchemy import func
from sqlalchemy.sql import label
import sys
from .process import AddNewTransactionTrading,AddNewExecutionReport
from datetime import datetime
from ..initdb import db_session
from .models import TransactionTrading, ExecutionReport, User
from sqlalchemy import desc,asc
from sqlalchemy import or_

# 1. check data
# 2. check order is exist?
# 3. send request to trade_app


@Micro.route('/add-transaction-trading')
@Micro.json
def add_transaction_trading(MsgType=None,TradeReportID=None, Commission=None, LastQty=None, LastPx=None, TransactTime=None, Side=None, Symbol=None, OrderID=None,
                            SecondaryOrderID=None, Account=None, Currency=None, Quantity=None, AllocAccount=None, AllocSettlCurrency=None,
                            AllocQty=None,SecondaryClOrdID = None, ClOrdID = None):
    try:
        transaction_trading = {
            'TradeReportID': TradeReportID,
            'Commission': Commission,
            'LastQty': LastQty,
            'LastPx': LastPx,
            'TransactTime': TransactTime,
            'Side': Side,
            'Symbol': Symbol,
            'OrderID': OrderID,
            'SecondaryOrderID': SecondaryOrderID,
            'Account': Account,
            'Currency': Currency,
            'Quantity': Quantity,
            'AllocAccount': AllocAccount,
            'AllocSettlCurrency': AllocSettlCurrency,
            'AllocQty': AllocQty
        }
        with db_session() as session:
            transactTrading = TransactionTrading(**transaction_trading)
            session.add(transactTrading)
            print("Add New Transaction Trading Success")
        return {
            "status" : 1,
            "message": "add transaction trading success"
        }
    except:
        traceback.print_exc()
        return {
            "status" : 0,
            "message": "add transaction trading Error"
        }
@Micro.route('/add-execution-report')
@Micro.json
def add_execution_report(MsgType=None,Account=None,ClOrdID=None,OrderID=None,OrigClOrdID=None,OrderQty=None,LeavesQty=None,CumQty=None,OrdType=None,
                    OrdStatus=None,Price=None,Symbol=None,Side=None,Currency=None,AllocSettlCurrency=None,TimeInForce=None,TransactTime=None,
                    Commission=None, AllocAccount=None,SecondaryOrderID=None,TimeZone=None,ExecStyle=None,DisplayName=None,UserID=None,LastQty=None,LastPx=None):
    try:
        print(OrdStatus)
        execution_report = {
            'Account': Account, 
            'ClOrdID': ClOrdID, 
            'OrderID': OrderID, 
            'OrigClOrdID': OrigClOrdID,
            'OrderQty': OrderQty, 
            'LeavesQty': LeavesQty, 
            'CumQty': CumQty,
            'OrdType': OrdType, 
            'OrdStatus': OrdStatus, 
            'Price': Price, 
            'Side': Side, 
            'Symbol': Symbol, 
            'Currency': Currency,
            'AllocSettlCurrency': AllocSettlCurrency, 
            'TimeInForce': TimeInForce, 
            'TransactTime': TransactTime, 
            'Commission': Commission, 
            'AllocAccount': AllocAccount, 
            'SecondaryOrderID': SecondaryOrderID, 
            'execution_style': ExecStyle,
            'DisplayName': DisplayName,
            'UserID': UserID
        }
        with db_session() as session:
            all_report = session.query(ExecutionReport).filter(ExecutionReport.OrderID == OrderID).all()
            for item in all_report:
                item.live = False
                session.add(item)
            report = ExecutionReport(**execution_report)
            session.add(report)
            print("Add New Report Success")
            print(ExecutionReport.to_dict(report))
        return {
            "status" : 1,
            "message": "add execution report success"
        }
    except:
        traceback.print_exc()
        return {
            "status" : 0,
            "message": "add execution report error"
        }

@Micro.route('/get-all-execution-report')
@Micro.json
def get_All_execution_report(UserID=None):
    try:
        with db_session() as session:
            all_report = session.query(ExecutionReport).filter(ExecutionReport.live == True, ExecutionReport.UserID == UserID).order_by(desc(ExecutionReport.TransactTime)).limit(100)
            result = []
            for row in all_report:
                # print(row.TransactTime)
                item = ExecutionReport.to_dict(row)
                item["TransactTime"] = str(row.TransactTime.strftime("%c"))
                print(item["TransactTime"])
                result.append(item)
            print(result[0])
            return {
                "status" : 1,
                "message": "get execution report success",
                "all_report": result
            }
    except:
        traceback.print_exc()
        return {
            "status" : 0,
            "message": "get execution report error"
        }
    

@Micro.route('/get-top-lastest-execution-report')
@Micro.json
def get_top_lastest_execution_report():
    try:
        with db_session() as session:
            all_report = session.query(ExecutionReport).filter(ExecutionReport.live ==True , or_(ExecutionReport.OrdStatus == "New", ExecutionReport.OrdStatus == "Filled")).order_by(desc(ExecutionReport.createAt)).limit(20)

            result = []
            for row in all_report:
                # print(row.TransactTime)
                item = ExecutionReport.to_dict(row)
                user = session.query(User).filter(User.id == item["UserID"]).first()
                item["DisplayName"]= user.username
                item["TransactTime"] = str(row.TransactTime.strftime("%c"))
                item["createAt"] = str(row.createAt.strftime("%c"))
                result.append(item)
            print(result)
            return {
                "status" : 1,
                "message": "add execution report success",
                "all_report": result
            }
    except:
        traceback.print_exc()
        return {
            "status" : 0,
            "message": "add execution report error"
        }
@Micro.route('/get-top-lastest-trade-history-otc-execution-report')
@Micro.json
def get_top_lastest_trade_history_otc_execution_report():
    try:
        with db_session() as session:
            all_report = session.query(ExecutionReport).filter(ExecutionReport.live ==True ,ExecutionReport.OrdStatus == "Filled").order_by(desc(ExecutionReport.createAt)).limit(20).all()
            result=[]
            for row in all_report:
                # print(row.TransactTime)
                item = ExecutionReport.to_dict(row)
                result.append(item)
            print(result)
            return {
                "status" : 1,
                "message": "get-top-lastest-trade-history-otc execution report success",
                "all_report": result
            }
    except:
        traceback.print_exc()
        return {
            "status" : 0,
            "message": "get-top-lastest-trade-history-otc execution report error"
        }

