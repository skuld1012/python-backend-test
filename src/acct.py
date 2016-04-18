'''
Created on 15 Apr, 2016

@author: ted.zhang
'''

import datetime
from decimal import Decimal

ACCT_TYPE_USER = 0
ACCT_TYPE_REVENUE = 1
ACCT_TYPE_TAX = 2
ACCT_TYPE_COMMISSION = 3

ACCT_SWITCHER = {
    ACCT_TYPE_USER: "USER",
    ACCT_TYPE_REVENUE: "REVENUE",
    ACCT_TYPE_TAX: "TAX",
    ACCT_TYPE_COMMISSION: "COMMISSION"
}

class NewAccount():
    """
    Class to handle account balance and transfer money.
    """
    def __init__(self, acctId=None, acctName=None, acctType=None, balance=None, createdAt=None, lastUpdatedAt=None):
        """
        Initialize account balance and transaction list which store transaction information.
        """
        self._balance = Decimal("0.0")
        self._acctType = 0
        self._transList = []
        self._id = -1
        self._acctName = ""
        if acctId is not None:
            self._id = acctId
            self._acctName = acctName
            self._acctType = acctType
            self._balance = balance
            self._createdAt = createdAt
            self._lastUpdatedAt = lastUpdatedAt
    
    def setBalance(self, balance):
        self._balance = balance
    
    def getId(self):
        return self._id
    
    def setId(self, acctId):
        self._id = acctId
    
    def Balance(self):
        """
        return current balance.
        """
        return self._balance
    
    def getAcctName(self):
        return self._acctName
    
    def setAcctName(self, acctName):
        self._acctName = acctName
    
    def getAcctType(self):
        return self._acctType
    
    def setAcctType(self, acctType):
        self._acctType = acctType
    
    def getCreatedAt(self):
        return self._createdAt
    
    def setCreatedAt(self, createdAt):
        self._createdAt = createdAt
    
    def getLastUpdatedAt(self):
        return self._lastUpdatedAt
    
    def setLastUpdatedAt(self, lastUpdatedAt):
        self._lastUpdatedAt = lastUpdatedAt
    
    def Withdraw(self, amount):
        """
        Withdraw money from account and store the transaction into list.
        """
        self._transList.append(-amount)
        
    def Deposit(self, amount):
        """
        Deposit money to account and store and transaction into list.
        """
        self._transList.append(amount)
    
    def commit(self):
        """
        Commit the transactions and update the current account balance.
        """
        for amount in self._transList:
            self._balance = self._balance + amount
        else:
            del self._transList[:]
            
    def __str__(self):
        return "Account ID " + str(self._id) + ", name " + self._acctName + ", type " + self.getTypeStr() + " has balance: " + str(self.Balance())
    
    def getTypeStr(self):
        """
        Get account type String representation
        """
        return ACCT_SWITCHER[self._acctType]

# Can move this class to another Module file          
class NewTransaction():
    """
    Class to handle money transactions between accounts.
    """
    def __init__(self):
        """
        Initialize the account set which stores all accounts which are needed to be updated later.
        """
        self._acctSet = set()
        self._transHisList = []
    
    def MoveMoney(self, amount, fromAcct, toAcct):
        """
        Transfer money between accounts. Account balance will be updated after Close method is called.
        """
        fromAcctId = -1
        toAcctId = -1
        
        
        if fromAcct is not None:
            fromAcct.Withdraw(amount)
            self._acctSet.add(fromAcct)
            fromAcctId = fromAcct.getId()
            
        if toAcct is not None:
            toAcct.Deposit(amount)
            self._acctSet.add(toAcct)
            toAcctId = toAcct.getId()
            
        transHist = TransHistory(-1, fromAcctId, toAcctId, amount)
        self._transHisList.append(transHist)
    
    def Close(self, accountService=None, transactionService=None):
        """
        Close transaction handler and update all stored account balance.
        Update balances and transaction histories with passed in service objects.
        """
        accts = []
        trans = []
        while self._acctSet:
            acct = self._acctSet.pop()
            acct.commit()
            accts.append(acct)
        
        currentDatetime = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        for transHist in self._transHisList:
            transHist.setCreatedAt(currentDatetime)
            trans.append(transHist)
        
        del self._transHisList[:]
        
        if accountService is not None:
            for account in accts:
                accountService.persistBalance(account)
        
        if transactionService is not None:
            for trans in trans:
                transactionService.createNewTransHistory(trans.getFromAcctId(), 
                                                         trans.getToAcctId(), 
                                                         trans.getAmount(), 
                                                         trans.getCreatedAt())

class TransHistory():
    """
    Object represents an instance of transaction history in transactions table
    """
    
    def __init__(self, transId, fromAcctId, toAcctId, amount, createdAt=None):
        self._transId = transId
        self._fromAcctId = fromAcctId
        self._toAcctId = toAcctId
        self._amount = amount
        self._createdAt = createdAt
        
    def getTransId(self):
        return self._transId
    
    def getFromAcctId(self):
        return self._fromAcctId
    
    def getToAcctId(self):
        return self._toAcctId
    
    def getAmount(self):
        return self._amount
    
    def getCreatedAt(self):
        return self._createdAt
    
    def setCreatedAt(self, createdAt):
        self._createdAt = createdAt
    
    def __str__(self):
        return "Money " + str(self._amount) + " transfers from Account ID " + str(self._fromAcctId) + " to Account ID " + str(self._toAcctId) + " on " + self._createdAt