'''
Created on 16 Apr, 2016

@author: ted.zhang
'''

import unittest,acct,acctService
import sqlite3 as sql
from decimal import Decimal

class SqliteTestCases(unittest.TestCase):

    def setUp(self):
        self._acctService = acctService.AccountService(":memory:", True)
    
    def tearDown(self):
        self._acctService.destroyIfTestMode()

    def testInsertAcct(self):
        pass
    
    def testUpdateAcctBalance(self):
        pass
    
    def testInsertTrans(self):
        pass
    
    def testQueryAcct(self):
        pass
    
    def testQueryTrans(self):
        pass
    
    