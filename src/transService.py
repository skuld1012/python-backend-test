'''
Created on 17 Apr, 2016

@author: ted.zhang
'''

import transDao

class TransService(object):
    '''
    Service layer for transaction history operations. Wrap all persistence logics.
    '''

    def __init__(self, connPath=None, testMode=None):
        if connPath is None:
            self._dao = transDao.TransDao(transDao.DB_STRING, testMode)
        else:
            self._dao = transDao.TransDao(connPath, testMode)
    
    def createNewTransHistory(self, from_acct_id, to_acct_id, amount, created_at):
        return self._dao.persistTransHistory(from_acct_id, to_acct_id, amount, created_at)
    
    def queryAllHistory(self):
        """
        Get all transaction history from database.
        """
        return self._dao.queryAllTransHistory()