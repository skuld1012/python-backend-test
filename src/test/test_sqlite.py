'''
Created on 16 Apr, 2016

@author: ted.zhang
'''

import unittest, acct, acctService, transService, sqlite3
from decimal import Decimal

class SqliteIntegrationTestCases(unittest.TestCase):

    def setUp(self):
        try:
            self._conn = sqlite3.connect(':memory:')
            cur = self._conn.cursor()
            cur.execute("""CREATE TABLE 'account' (
            `id`    INTEGER PRIMARY KEY AUTOINCREMENT,
            `acct_name`    TEXT NOT NULL,
            `acct_type`    INTEGER NOT NULL DEFAULT 0,
            `balance`    INTEGER NOT NULL DEFAULT 0,
            `created_at`    TEXT NOT NULL,
            `last_updated_at`    TEXT NOT NULL,
            UNIQUE (`acct_name`, `acct_type`) ON CONFLICT REPLACE);""")
    
            cur.execute("""CREATE TABLE 'transaction' (
            `trans_id`    INTEGER PRIMARY KEY AUTOINCREMENT,
            `from_acct_id`    INTEGER DEFAULT -1,
            `to_acct_id`    INTEGER DEFAULT -1,
            `amount`    INTEGER NOT NULL DEFAULT 0,
            `created_at`    TEXT NOT NULL);""")
            self._conn.commit()
        
        except (sqlite3.Error, RuntimeError, TypeError, NameError), ex:
            print ex
        
        self._acctService = acctService.AccountService(":memory:", True, self._conn)
        self._transService = transService.TransService(":memory:", True, self._conn)
        self._transHandler = acct.NewTransaction()
        
        newacct1 = acct.NewAccount()
        newacct2 = acct.NewAccount()
        newacct3 = acct.NewAccount()
        newacct4 = acct.NewAccount()
        self._acctService.createNewAccount(newacct1, "test1", 0)
        self._acctService.createNewAccount(newacct2, "test2", 1)
        self._acctService.createNewAccount(newacct3, "test3", 2)
        self._acctService.createNewAccount(newacct4, "test4", 3)
        
        # Store $100.00 into newacct and newacct2
        self._transHandler.MoveMoney(Decimal("100.0"), None, newacct1)
        self._transHandler.MoveMoney(Decimal("100.0"), None, newacct2)
        
        self._transHandler.Close(self._acctService, self._transService)
        
    def tearDown(self):
        self._acctService.destroyIfTestMode()
        self._transService.destroyIfTestMode()
        self._conn.close()

    def testCreatedAcct(self):
        newacct1 = self._acctService.getAccountById(1)
        newacct2 = self._acctService.getAccountById(2)
        newacct3 = self._acctService.getAccountById(3)
        newacct4 = self._acctService.getAccountById(4)
        
        self.assertEqual(newacct1.getId(), 1)
        self.assertEqual(newacct2.getId(), 2)
        self.assertEqual(newacct3.getId(), 3)
        self.assertEqual(newacct4.getId(), 4)
        
        self.assertEqual(newacct1.getAcctName(), "test1")
        self.assertEqual(newacct2.getAcctName(), "test2")
        self.assertEqual(newacct3.getAcctName(), "test3")
        self.assertEqual(newacct4.getAcctName(), "test4")
        
        self.assertEqual(newacct1.getAcctType(), 0)
        self.assertEqual(newacct2.getAcctType(), 1)
        self.assertEqual(newacct3.getAcctType(), 2)
        self.assertEqual(newacct4.getAcctType(), 3)
    
    def testPersistedAcctBalance(self):
        newacct1 = self._acctService.getAccountById(1)
        newacct2 = self._acctService.getAccountById(2)
        newacct3 = self._acctService.getAccountById(3)
        newacct4 = self._acctService.getAccountById(4)
        
        #Move $10.00 from newaact1 to newacct3
        self._transHandler.MoveMoney(Decimal("10.0"), newacct1, newacct3)
        #Move $20.00 from newaact2 to newacct4
        self._transHandler.MoveMoney(Decimal("20.0"), newacct2, newacct4)
        
        self._transHandler.Close(self._acctService, self._transService)
        
        newacct1 = self._acctService.getAccountById(1)
        newacct2 = self._acctService.getAccountById(2)
        newacct3 = self._acctService.getAccountById(3)
        newacct4 = self._acctService.getAccountById(4)
        
        # Verify all accounts' balance are correct
        self.assertEqual(newacct1.Balance(), Decimal("90.00"))
        self.assertEqual(newacct2.Balance(), Decimal("80.00"))
        self.assertEqual(newacct3.Balance(), Decimal("10.00"))
        self.assertEqual(newacct4.Balance(), Decimal("20.00"))
    
    def testCreatedTransHist(self):
        trans = self._transService.queryAllHistory()
        for tran in trans:
            # Verify the 2 deposit transaction during setUp
            self.assertEqual(tran.getAmount(), Decimal("100.0"))
