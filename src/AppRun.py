'''
Created on 16 Apr, 2016

@author: ted.zhang
'''

import acct,acctService,transService,traceback
from decimal import Decimal

if __name__ == '__main__':
    
    accountService = acctService.AccountService()
    transactionService = transService.TransService()
    transHandler = acct.NewTransaction()
    
    while True:
        try:
            print "*****************************************"
            print "TED CREDIT LTD. ACCOUNT ADMIN SYSTEM v1.0"
            print "Please select a service:"
            print "1. Create new account"
            print "2. List all accounts "
            print "3. Deposit money"
            print "4. Transfer money"
            print "5. Transaction settlement"
            print "6. Show transaction history"
            print "7. Exit"
            var = raw_input("Please enter: ")
            if var == "7":
                print "System shutdown. Thank you for using our service!"
                print "*************************************************"
                break
            elif var == "1":
                print "================================================="
                newacct = acct.NewAccount()
                acctName = raw_input("Please enter account name: ")
                print "0: USER"
                print "1: REVENUE"
                print "2: TAX"
                print "3: COMMISSION"
                acctType = raw_input("Please enter account type number (0=USER;1=REVENUE;2=TAX;3=COMMISSION): ")
                accountService.createNewAccount(newacct, acctName, int(acctType))
                print "Account " + acctName + " successfully created."
            elif var == "2":
                print "================================================="
                accounts = accountService.getAllAccounts()
                for account in accounts:
                    print account
                print "Please use the account IDs in money transfer function."
            elif var == "3":
                print "================================================="
                acctId = raw_input("Please enter Account ID: ")
                account = accountService.getAccountById(int(acctId))
                amount = raw_input("Please enter transfer amount: ")
                transHandler.MoveMoney(Decimal(amount), None, account)
                print "Deposit complete. Remember to SETTLE the transactions before exit."
            elif var == "4":
                print "================================================="
                acctIdFrom = raw_input("Please enter From Account ID: ")
                acctIdTo = raw_input("Please enter To Account ID: ")
                amount = raw_input("Please enter transfer amount: ")
                accountFrom = accountService.getAccountById(int(acctIdFrom))
                accountTo = accountService.getAccountById(int(acctIdTo))
                transHandler.MoveMoney(Decimal(amount), accountFrom, accountTo)
                print "***Money transfer complete. Remember to SETTLE the transactions before exit.***"
            elif var == "5":
                print "================================================="
                print "Transaction settling..."
                transHandler.Close(accountService, transactionService)
                print "Transaction settlement complete."
            elif var == "6":
                print "================================================="
                trans = transactionService.queryAllHistory()
                for tran in trans:
                    print tran
            else:
                print "================================================="
                print "Invalid choice..."
        except (RuntimeError, TypeError, NameError), ex:
            print ex
            traceback.print_exc()
            continue
    