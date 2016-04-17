'''
Created on 17 Apr, 2016

@author: ted.zhang
'''
import acctDao,datetime

class AccountService(object):
    '''
    classdocs
    '''
    
    def __init__(self, acct):
        self._acct = acct
        self._dao = acctDao.AcctDao(acctDao.DB_STRING)
    
    def createNewAccount(self, acctName, acctType):
        self._acct.setAcctName(acctName)
        self._acct.setAcctType(acctType)
        
        currentDatetime = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self._acct.setCreatedAt(currentDatetime)
        self._acct.setLastUpdatedAt(currentDatetime)
        
        acctId = self._dao.insertAcct(self._acct)
        self._acct.setId(acctId)
    
    def updateBalance(self):
        currentDatetime = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        rowcount = self._dao.updateBalance(self._acct.Balance(), 
                                           self._acct.getAcctName(), 
                                           self._acct.getAcctType(), 
                                           currentDatetime)
        if rowcount == 1:
            print "Balance of " + self._acct.getAcctName() + " with type " 
            + str(self._acct.getAcctType()) + " is updated and persisted successfully."   
    
    def destroy(self):
        self._dao.close()    
        