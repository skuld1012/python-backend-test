'''
Created on 17 Apr, 2016

@author: ted.zhang
'''

import acctDao,datetime

class AccountService():
    '''
    Service layer for account operation. Wrap all persistence logics.
    '''
    
    def __init__(self, connPath=None, testMode=None, conn=None):
        """
        testMode is for unittest memory db. If set to true, conn should use memory db connection.
        Please see test_sqlite.py
        """
        if connPath is None:
            self._dao = acctDao.AcctDao(acctDao.DB_STRING, testMode)
        else:
            self._dao = acctDao.AcctDao(connPath, testMode, conn)
    
    def createNewAccount(self, acct, acctName, acctType):
        acct.setAcctName(acctName)
        acct.setAcctType(acctType)
        
        currentDatetime = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        acct.setCreatedAt(currentDatetime)
        acct.setLastUpdatedAt(currentDatetime)
        
        acctId = self._dao.insertAcct(acct)
        acct.setId(acctId)
    
    def persistBalance(self, acct):
        currentDatetime = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        rowcount = self._dao.persistBalance(acct.Balance(), 
                                           acct.getAcctName(), 
                                           acct.getAcctType(), 
                                           currentDatetime)
        if rowcount is not 1:
            print "Balance of " + acct.getAcctName() + " with type " + str(acct.getAcctType()) + " is updated and persisted with error."      
        
    def getAllAccounts(self):
        return self._dao.queryAll()
    
    def getAccountById(self, acctId):
        return self._dao.queryByAcctId(acctId)
    
    def destroyIfTestMode(self):
        """
        This method needs to be called under test mode (unittest)
        """
        self._dao.close()