'''
Created on 16 Apr, 2016

@author: ted.zhang
'''
import sqlite3 as sql
# import apsw

ACCOUNT_INSERT = """INSERT INTO account ('acct_name','acct_type','balance','created_at','last_updated_at') 
                    VALUES (:acct_name,:acct_type,:balance,:created_at,:last_updated_at);"""
ACCOUNT_UPDATE_BALANCE = """UPDATE account SET balance=:balance,last_updated_at=:last_updated_at 
                            WHERE acct_name=:acct_name AND acct_type=:acct_type;"""
ACCOUNT_DELETE_ = "DELETE FROM account WHERE acct_name=:acct_name AND acct_type=:acct_type"
ACCOUNT_SELECT_ALL = "SELECT * FROM account;"
ACCOUNT_SELECT_BY_KEYS = "SELECT * FROM account WHERE acct_name=:acct_name AND acct_type=:acct_type"

DB_STRING = "db/backend_test.db"
# Can add additional functional query like pagination

class AcctDao():
    
    def __init__(self, connPath):
        self._conn = sql.connect(connPath)
        self._cur = self._conn.cursor()
    
    def insertAcct(self, newAcct):
        try:
            paramDict = {'acct_name':newAcct.getAcctName(), 
                         'acct_type':newAcct.getAcctType(),
                         'balance':int(newAcct.Balance()*100),
                         'created_at':newAcct.getCreatedAt(),
                         'last_updated_at':newAcct.getLastUpdatedAt() }
            self._cur.execute(ACCOUNT_INSERT, paramDict)
            self.commit()
            return self._cur.lastrowid
        except sql.Error ,ex:
            print ex
            self._conn.rollback()
            return -1
    
    def updateBalance(self, balance, acctName, acctType, lastUpdateAt):
        try:
            paramDict = {'balance':int(balance*100),
                         'last_updated_at':lastUpdateAt,
                         'acct_name':acctName, 
                         'acct_type':acctType}
            self._cur.execute(ACCOUNT_UPDATE_BALANCE, paramDict)
            self.commit()
            return self._cur.rowcount
        except sql.Error ,ex:
            print ex
            self._conn.rollback()
            return 0
    
    def delete(self, acct_name, acct_type):
        pass
    
    def queryAll(self):
        pass
    
    def queryByAcctNameAndType(self, acctName, acctType):
        try:
            paramDict = {'acct_name':acctName,
                         'acct_type':acctType}
            self._cur.execute(ACCOUNT_SELECT_BY_KEYS, paramDict)
            rows = self._cur.fetchall()
            result = []
            for row in rows:
                pass
            return result
        except sql.Error ,ex:
            print ex
            self._conn.rollback()
            return []
    
    def commit(self):
        self._conn.commit()    
    
    def close(self):
        self._conn.close()

