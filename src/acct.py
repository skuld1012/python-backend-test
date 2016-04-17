'''
Created on 15 Apr, 2016

@author: ted.zhang
'''

from decimal import Decimal

ACCT_TYPE_USER = 0
ACCT_TYPE_REVENUE = 1
ACCT_TYPE_TAX = 2
ACCT_TYPE_COMMISSION = 3

class NewAccount():
    """
    Class to handle account balance and transfer money.
    """
    def __init__(self):
        """
        Initialize account balance and transaction list which store transaction information.
        """
        self._balance = Decimal("0.0")
        self._acctType = 0
        self._transList = []
        self._id = -1
        self._acctName = ""
    
    def updateBalance(self, balance):
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
    
    def MoveMoney(self, amount, fromAcct, toAcct):
        """
        Transfer money between accounts. Account balance will be updated after Close method is called.
        """
        fromAcct.Withdraw(amount)
        toAcct.Deposit(amount)
        self._acctSet.add(fromAcct)
        self._acctSet.add(toAcct)
    
    def Close(self):
        """
        Close transaction handler and update all stored account balance.
        """
        while self._acctSet:
            acct = self._acctSet.pop()
            acct.commit()
        self._acctSet.clear()
