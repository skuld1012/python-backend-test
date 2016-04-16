import unittest, acct
from decimal import Decimal

class AcctTestCase(unittest.TestCase):
    def test_transaction(self):
        useracct = acct.NewAccount()
        revenueacct = acct.NewAccount()
        taxacct = acct.NewAccount()
        commissionacct = acct.NewAccount()

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

        # Verify that the money doesn't move until the transaction is closed
        shouldbe = Decimal("0.0")
        was = useracct.Balance()
        if shouldbe != was:
            self.fail("Money was moved before the transaction was closed.")
        trans.Close()

        shouldbe = Decimal("-10.70")
        was = useracct.Balance()
        if was != shouldbe:
            self.fail("Wrong user balance. Was %g, should be %g" % (was, shouldbe))

        shouldbe = Decimal("9.00")
        was = revenueacct.Balance()
        if was != shouldbe:
            self.fail("Wrong revenue balance. Was %g, should be %g" % (was, shouldbe))

        shouldbe = Decimal(".7")
        was = taxacct.Balance()
        if was != shouldbe:
            self.fail("Wrong tax balance. Was %g, should be %g" % (was, shouldbe))

        shouldbe = Decimal("1.00")
        was = commissionacct.Balance()
        if was != shouldbe:
            self.fail("Wrong commission balance. Was %g, should be %g" % (was, shouldbe))


