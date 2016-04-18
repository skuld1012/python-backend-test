'''
Created on 16 Apr, 2016

@author: ted.zhang
'''

import acct
import sqlite3 as sql
from decimal import Decimal
# import apsw

ACCOUNT_INSERT = """INSERT INTO account ('acct_name','acct_type','balance','created_at','last_updated_at') 
                    VALUES (:acct_name,:acct_type,:balance,:created_at,:last_updated_at);"""
ACCOUNT_UPDATE_BALANCE = """UPDATE account SET balance=:balance,last_updated_at=:last_updated_at 
                            WHERE acct_name=:acct_name AND acct_type=:acct_type;"""
ACCOUNT_DELETE_ = "DELETE FROM account WHERE acct_name=:acct_name AND acct_type=:acct_type"
ACCOUNT_SELECT_ALL = "SELECT * FROM account;"
ACCOUNT_SELECT_BY_ID = "SELECT * FROM account WHERE id=:id;"

DB_STRING = "db/backend_test.db"
# Can add additional functional query like pagination

class AcctDao():
    """
    Persistence layer of accounts
    """
    def __init__(self, connPath, testMode=None, conn=None):
        self._connPath = connPath
        if testMode is None:
            self._testMode = False
        else:
            self._testMode = True
            self._conn = conn
    
    def getConnection(self):
        if self._testMode:
            return self._conn
        else:
            return sql.connect(self._connPath)
    
    def insertAcct(self, newAcct):
        self._conn = self.getConnection()
        self._cur = self._conn.cursor()
        try:
            paramDict = {'acct_name':newAcct.getAcctName(),
                         'acct_type':newAcct.getAcctType(),
                         'balance':int(newAcct.Balance() * 100),
                         'created_at':newAcct.getCreatedAt(),
                         'last_updated_at':newAcct.getLastUpdatedAt() }
            self._cur.execute(ACCOUNT_INSERT, paramDict)
            self._conn.commit()
            return self._cur.lastrowid
        except sql.Error , ex:
            print ex
            self._conn.rollback()
            return -1
        finally:
            if not self._testMode:
                self._conn.close()
    
    def persistBalance(self, balance, acctName, acctType, lastUpdateAt):
        self._conn = self.getConnection()
        self._cur = self._conn.cursor()
        try:
            paramDict = {'balance':int(balance * 100),
                         'last_updated_at':lastUpdateAt,
                         'acct_name':acctName,
                         'acct_type':acctType}
            self._cur.execute(ACCOUNT_UPDATE_BALANCE, paramDict)
            self._conn.commit()
            return self._cur.rowcount
        except sql.Error , ex:
            print ex
            self._conn.rollback()
            return 0
        finally:
            if not self._testMode:
                self._conn.close()
    
    def queryAll(self):
        self._conn = self.getConnection()
        # Select dictionary cursor
        self._conn.row_factory = sql.Row
        self._cur = self._conn.cursor()
        try:
            self._cur.execute(ACCOUNT_SELECT_ALL)
            rows = self._cur.fetchall()
            result = []
            for row in rows:
                result.append(acct.NewAccount(row["id"],
                                              row["acct_name"],
                                              row["acct_type"],
                                              Decimal("%0.2f" % (row["balance"] / 100.0)),  # Can create utility function
                                              row["created_at"],
                                              row["last_updated_at"]))
            return result
        except sql.Error , ex:
            print ex
            self._conn.rollback()
            return []
        finally:
            if not self._testMode:
                self._conn.close()
    
    def queryByAcctId(self, acctId):
        self._conn = self.getConnection()
        # Select dictionary cursor
        self._conn.row_factory = sql.Row
        self._cur = self._conn.cursor()
        try:
            paramDict = {'id':acctId }
            self._cur.execute(ACCOUNT_SELECT_BY_ID, paramDict)
            row = self._cur.fetchone()
            account = acct.NewAccount(row["id"],
                                      row["acct_name"],
                                      row["acct_type"],
                                      Decimal("%0.2f" % (row["balance"] / 100.0)),
                                      row["created_at"],
                                      row["last_updated_at"])
            return account
        except sql.Error , ex:
            print ex
            self._conn.rollback()
            return []
        finally:
            if not self._testMode:
                self._conn.close()
            
    def close(self):
        """
        This method needs to be called under test mode (unittest)
        """
        if self._testMode:
            self._conn.close()

    
