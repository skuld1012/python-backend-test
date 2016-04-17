'''
Created on 16 Apr, 2016

@author: ted.zhang
'''

import acct,acctService
from decimal import Decimal

if __name__ == '__main__':
    useracct = acct.NewAccount()
    useracctService = acctService.AccountService(useracct)
    useracctService.createNewAccount("Ted", acct.ACCT_TYPE_USER)
    
    revenueacct = acct.NewAccount()
    revenueacctService = acctService.AccountService(revenueacct)
    revenueacctService.createNewAccount("Ted Ltd", acct.ACCT_TYPE_REVENUE)
    
    taxacct = acct.NewAccount()
    taxacctService = acctService.AccountService(taxacct)
    taxacctService.createNewAccount("Ted Ltd", acct.ACCT_TYPE_TAX)
    
    commissionacct = acct.NewAccount()
    commissionacctService = acctService.AccountService(commissionacct)
    commissionacctService.createNewAccount("Ted Ltd", acct.ACCT_TYPE_COMMISSION)
    
    retailprice = Decimal("10.00")
    taxrate = Decimal(".07")
    commissionrate = Decimal(".10")
    taxamt = retailprice * taxrate
    price = retailprice + taxamt
    commission = retailprice * commissionrate

    trans = acct.NewTransaction()
    trans.MoveMoney(price, useracct, revenueacct)
    trans.MoveMoney(taxamt, revenueacct, taxacct)
    trans.MoveMoney(commission, revenueacct, commissionacct)
    
    trans.Close()
    useracctService.updateBalance()
    revenueacctService.updateBalance()
    taxacctService.updateBalance()
    commissionacctService.updateBalance()
    
    useracctService.destroy()
    revenueacctService.destroy()
    taxacctService.destroy()
    commissionacctService.destroy()
    
    
    