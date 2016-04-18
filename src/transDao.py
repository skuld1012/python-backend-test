'''
Created on 16 Apr, 2016

@author: ted.zhang
'''

import acct
import sqlite3 as sql
from decimal import Decimal

TRANS_INSERT = """INSERT INTO 'transaction' ('from_acct_id','to_acct_id','amount','created_at')  
                    VALUES (:from_acct_id,:to_acct_id,:amount,:created_at);"""
TRANS_SELECT_ALL = "SELECT * FROM 'transaction';"
# TRANS_SELECT_FROM = "SELECT * FROM transaction WHERE from_acct_id=:acct_id;"
# TRANS_SELECT_TO = "SELECT * FROM transaction WHERE to_acct_id=:acct_id;"  

DB_STRING = "db/backend_test.db"                  

class TransDao:
    """
    Persistence layer of transaction histories
    """
    def __init__(self, connPath, testMode=None):
        self._connPath = connPath
        if testMode is None:
            self._testMode = False
        else:
            self._testMode = True
    
    def persistTransHistory(self, from_acct_id, to_acct_id, amount, created_at):
        self._conn = sql.connect(self._connPath)
        self._cur = self._conn.cursor()
        try:
            paramDict = {'from_acct_id':from_acct_id, 
                         'to_acct_id':to_acct_id,
                         'amount':int(amount*100),
                         'created_at':created_at }
            self._cur.execute(TRANS_INSERT, paramDict)
            self._conn.commit()
            return self._cur.lastrowid
        except sql.Error ,ex:
            print ex
            self._conn.rollback()
            return -1
        finally:
            if not self._testMode:
                self._conn.close()
    
    def queryAllTransHistory(self):
        self._conn = sql.connect(self._connPath)
        # Select dictionary cursor
        self._conn.row_factory = sql.Row
        self._cur = self._conn.cursor()
        try:
            self._cur.execute(TRANS_SELECT_ALL)
            rows = self._cur.fetchall()
            result = []
            for row in rows:
                result.append(acct.TransHistory(row["trans_id"], 
                                                row["from_acct_id"], 
                                                row["to_acct_id"], 
                                                Decimal("%0.2f" % (row["amount"] / 100.0)), 
                                                row["created_at"]))
            return result
        except sql.Error ,ex:
            print ex
            self._conn.rollback()
            return []
        finally:
            if not self._testMode:
                self._conn.close()
                
    def close(self):
        if self._testMode:
            self._conn.close()