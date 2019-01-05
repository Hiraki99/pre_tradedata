import json
import uuid
import datetime
import requests,traceback
from decimal import *
from flask_socketio import emit
from ..initdb import db_session
from configparser import ConfigParser
from .models import ExecutionReport,TransactionTrading 
from .config import celery
from ..initdb import db_session
config = ConfigParser()
config.read('config.env')

@celery.task
def AddNewTransactionTrading(json):
    with db_session() as session:
        transactTrading = TransactionTrading(**json)
        session.add(transactTrading)
        print("Add New Transaction Trading Success")
@celery.task
def AddNewExecutionReport(json):
    with db_session() as session:
        report = ExecutionReport(**json)
        session.add(report)
        print("Add New Report Success")

