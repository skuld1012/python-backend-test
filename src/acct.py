# Boilerplate:
from decimal import Decimal

class NewAccount():
    """
    Class to handle account balance and transfer money.
    """
    def __init__(self):
        """
        Initialize account balance and transaction list which store transaction information.
        """
        self._balance = Decimal("0.0")
        self._transList = []
    
    def Balance(self):
        """
        return current balance.
        """
        return self._balance
    
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
        del self._transList[:]

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
            

