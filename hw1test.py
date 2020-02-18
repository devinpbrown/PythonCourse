import unittest
from Homework1 import *

class mytest(unittest.TestCase):
#addCash function
    def test_adc(self): #proper function
        a = Portfolio()
        a.addCash(100)
        self.assertEqual(a.id['Cash'], 100)
        self.assertTrue(a.log == ["Added $100 to 'Cash'."])
    def test_adc1(self): #no strings
        a = Portfolio()
        a.addCash('string')
        self.assertEqual(a.id['Cash'], 0)
    def test_adc2(self): #no negative values
        a = Portfolio()
        a.addCash(-20)
        self.assertEqual(a.id['Cash'], 0)

#withdrawCash function
    def test_wdc(self): #checking proper function
        a = Portfolio()
        a.addCash(100)
        a.withdrawCash(50)
        self.assertEqual(a.id['Cash'], 50)
        self.assertTrue(a.log == ["Added $100 to 'Cash'.", "Withdrew $50 from 'Cash'."])
    def test_wdc1(self): #no strings
        a = Portfolio()
        a.addCash(100)
        a.withdrawCash('string') #withdrawing string
        self.assertEqual(a.id['Cash'], 100)
    def test_wdc2(self): #no negative values
        a = Portfolio()
        a.addCash(100)
        a.withdrawCash(-20) #withdrawing negative value
        self.assertEqual(a.id['Cash'], 100)
    def test_wdc3(self): #no overdraw
        a = Portfolio()
        a.addCash(100)
        a.withdrawCash(101) #overdrawing
        self.assertEqual(a.id['Cash'], 100)

#buyStock Function
    def test_bs(self): #proper function, no previously existing stock
        a = Portfolio()
        s = Stock('ABC', 20)
        a.addCash(100)
        a.buyStock(s, 2)
        self.assertEqual(a.id['Cash'], 60)
        self.assertEqual(a.id['Stocks'], {'ABC': 2})
        self.assertTrue(a.log == ["Added $100 to 'Cash'.", "Purchased 2 shares of stock ABC for $40."])
    def test_bs1(self): #proper function, adding to existing stock
        a = Portfolio()
        s = Stock('ABC', 20)
        a.addCash(100)
        a.buyStock(s, 2)
        a.buyStock(s, 2)
        self.assertEqual(a.id['Cash'], 20)
        self.assertEqual(a.id['Stocks'], {'ABC': 4})
        self.assertTrue(a.log == ["Added $100 to 'Cash'.", "Purchased 2 shares of stock ABC for $40.", "Purchased 2 shares of stock ABC for $40."])
    def test_bs2(self): #no overdraw
        a = Portfolio()
        s = Stock('ABC', 20)
        a.addCash(100)
        a.buyStock(s, 6) #buying too much stock - overdrawing
        self.assertEqual(a.id['Cash'], 100)
        self.assertEqual(a.id['Stocks'], {})
        self.assertTrue(a.log == ["Added $100 to 'Cash'."])
    def test_bs3(self): #ensuring number of shares entered correctly
        a = Portfolio()
        s = Stock('ABC', 20)
        a.addCash(100)
        a.buyStock(s, 'string') #purchasing string amount
        self.assertEqual(a.id['Cash'], 100)
        self.assertEqual(a.id['Stocks'], {})
        self.assertTrue(a.log == ["Added $100 to 'Cash'."])
    def test_bs4(self): #ensuring asset entered
        a = Portfolio()
        s = Stock('ABC', 20)
        a.addCash(100)
        a.buyStock(a, 2) #buying non-asset
        self.assertEqual(a.id['Cash'], 100)
        self.assertEqual(a.id['Stocks'], {})
        self.assertTrue(a.log == ["Added $100 to 'Cash'."])
    def test_bs5(self): #no fractions of stocks purchased
        a = Portfolio()
        s = Stock('ABC', 20)
        a.addCash(100)
        a.buyStock(a, 2.5) #buying fractional shares
        self.assertEqual(a.id['Cash'], 100)
        self.assertEqual(a.id['Stocks'], {})
        self.assertTrue(a.log == ["Added $100 to 'Cash'."])

#sellStock
    def test_ss(self): #proper function 1: erasing entry for complete sales
        a = Portfolio()
        s = Stock('ABC', 20)
        a.addCash(100)
        a.buyStock(s, 2)
        a.sellStock(s, 2)
        self.assertEqual(a.id['Stocks'], {})
    def test_ss1(self): #proper function 2: subtracting from existing port
        a = Portfolio()
        s = Stock('ABC', 20)
        a.addCash(100)
        a.buyStock(s, 2)
        a.sellStock(s, 1)
        self.assertEqual(a.id['Stocks'], {'ABC': 1})
    def test_ss2(self): #no overdraw
        a = Portfolio()
        s = Stock('ABC', 20)
        a.addCash(100)
        a.buyStock(s, 2)
        a.sellStock(s, 3) #selling too many stocks
        self.assertEqual(a.id['Cash'], 60)
        self.assertEqual(a.id['Stocks'], {'ABC': 2})
        self.assertTrue(a.log == ["Added $100 to 'Cash'.", "Purchased 2 shares of stock ABC for $40."])
    def test_ss3(self): #ensuring number of shares entered correctly
        a = Portfolio()
        s = Stock('ABC', 20)
        a.addCash(100)
        a.buyStock(s, 2)
        a.sellStock(s, 'string') #selling string
        self.assertEqual(a.id['Cash'], 60)
        self.assertEqual(a.id['Stocks'], {'ABC': 2})
        self.assertTrue(a.log == ["Added $100 to 'Cash'.", "Purchased 2 shares of stock ABC for $40."])
    def test_ss4(self): #ensuring stock entered
        a = Portfolio()
        s = Stock('ABC', 20)
        a.addCash(100)
        a.buyStock(s, 2)
        a.sellStock(a, 2) #selling non-asset
        self.assertEqual(a.id['Cash'], 60)
        self.assertEqual(a.id['Stocks'], {'ABC': 2})
        self.assertTrue(a.log == ["Added $100 to 'Cash'.", "Purchased 2 shares of stock ABC for $40."])
    def test_ss5(self): #no selling portions
        a = Portfolio()
        s = Stock('ABC', 20)
        a.addCash(100)
        a.buyStock(s, 2)
        a.sellStock(a, 1.5) #fraction of stock
        self.assertEqual(a.id['Cash'], 60)
        self.assertEqual(a.id['Stocks'], {'ABC': 2})
        self.assertTrue(a.log == ["Added $100 to 'Cash'.", "Purchased 2 shares of stock ABC for $40."])
    def test_ss6(self): #no selling stock not in portfolio
        a = Portfolio()
        s = Stock('ABC', 20)
        s2 = Stock('DEF', 10)
        a.addCash(100)
        a.buyStock(s, 2)
        a.sellStock(s2, 2) #selling stock not in portfolio
        self.assertEqual(a.id['Cash'], 60)
        self.assertEqual(a.id['Stocks'], {'ABC': 2})
        self.assertTrue(a.log == ["Added $100 to 'Cash'.", "Purchased 2 shares of stock ABC for $40."])

#buyMutualFund
    def test_bmf(self): #proper function, no previously existing MF
        a = Portfolio()
        mf = MutualFund('MF1')
        a.addCash(100)
        a.buyMutualFund(mf, 40)
        self.assertEqual(a.id['Cash'], 60)
        self.assertEqual(a.id['Mutual Funds'], {'MF1': 40})
        self.assertTrue(a.log == ["Added $100 to 'Cash'.", "Purchased 40 shares of mutual fund MF1 for $40."])
    def test_bmf1(self): #proper function, adding to existing mutual fund
        a = Portfolio()
        mf = MutualFund('MF1')
        a.addCash(100)
        a.buyMutualFund(mf, 40)
        a.buyMutualFund(mf, 40)
        self.assertEqual(a.id['Cash'], 20)
        self.assertEqual(a.id['Mutual Funds'], {'MF1': 80})
        self.assertTrue(a.log == ["Added $100 to 'Cash'.", "Purchased 40 shares of mutual fund MF1 for $40.", "Purchased 40 shares of mutual fund MF1 for $40."])
    def test_bmf2(self): #proper function, buying fractions
        a = Portfolio()
        mf = MutualFund('MF1')
        a.addCash(100)
        a.buyMutualFund(mf, 40.5)
        self.assertEqual(a.id['Cash'], 59.5)
        self.assertEqual(a.id['Mutual Funds'], {'MF1': 40.5})
        self.assertTrue(a.log == ["Added $100 to 'Cash'.", "Purchased 40.5 shares of mutual fund MF1 for $40.5."])
    def test_bmf3(self): #no overdraw
        a = Portfolio()
        mf = MutualFund('MF1')
        a.addCash(100)
        a.buyMutualFund(mf, 120) #buying too much mutual fund - overdrawing
        self.assertEqual(a.id['Cash'], 100)
        self.assertEqual(a.id['Mutual Funds'], {})
        self.assertTrue(a.log == ["Added $100 to 'Cash'."])
    def test_bmf4(self): #ensuring number of shares entered correctly
        a = Portfolio()
        mf = MutualFund('MF1')
        a.addCash(100)
        a.buyMutualFund(mf, 'string') #purchasing string amount
        self.assertEqual(a.id['Cash'], 100)
        self.assertEqual(a.id['Mutual Funds'], {})
        self.assertTrue(a.log == ["Added $100 to 'Cash'."])
    def test_bmf5(self): #ensuring asset entered
        a = Portfolio()
        mf = MutualFund('MF1')
        a.addCash(100)
        a.buyMutualFund(a, 50) #buying non-asset
        self.assertEqual(a.id['Cash'], 100)
        self.assertEqual(a.id['Mutual Funds'], {})
        self.assertTrue(a.log == ["Added $100 to 'Cash'."])

#sellMutualFund
    def test_smf(self): #proper function, complete sales
        a = Portfolio()
        mf = MutualFund('MF1')
        a.addCash(100)
        a.buyMutualFund(mf, 40)
        a.sellMutualFund(mf, 40) #complete sale
        self.assertEqual(a.id['Mutual Funds'], {})
    def test_smf1(self): #proper function, partial sales
        a = Portfolio()
        mf = MutualFund('MF1')
        a.addCash(100)
        a.buyMutualFund(mf, 40)
        a.sellMutualFund(mf, 30) #partial sale
        self.assertEqual(a.id['Mutual Funds'], {'MF1': 10})
    def test_smf2(self): #no overdraw
        a = Portfolio()
        mf = MutualFund('MF1')
        a.addCash(100)
        a.buyMutualFund(mf, 40)
        a.sellMutualFund(mf, 50) #overdrawing
        self.assertEqual(a.id['Cash'], 60)
        self.assertEqual(a.id['Mutual Funds'], {'MF1': 40})
        self.assertTrue(a.log == ["Added $100 to 'Cash'.", "Purchased 40 shares of mutual fund MF1 for $40."])
    def test_smf3(self): #ensuring number of shares entered correctly
        a = Portfolio()
        mf = MutualFund('MF1')
        a.addCash(100)
        a.buyMutualFund(mf, 40)
        a.sellMutualFund(mf, 'string') #purchasing string
        self.assertEqual(a.id['Cash'], 60)
        self.assertEqual(a.id['Mutual Funds'], {'MF1': 40})
        self.assertTrue(a.log == ["Added $100 to 'Cash'.", "Purchased 40 shares of mutual fund MF1 for $40."])
    def test_smf4(self): #ensuring asset sell
        a = Portfolio()
        mf = MutualFund('MF1')
        a.addCash(100)
        a.buyMutualFund(mf, 40)
        a.sellMutualFund(a, 30) #selling non-asset
        self.assertEqual(a.id['Cash'], 60)
        self.assertEqual(a.id['Mutual Funds'], {'MF1': 40})
        self.assertTrue(a.log == ["Added $100 to 'Cash'.", "Purchased 40 shares of mutual fund MF1 for $40."])
    def test_smf5(self): #no selling MF not in portfolio
        a = Portfolio()
        mf = MutualFund('MF1')
        mf1 = MutualFund('MF2')
        a.addCash(100)
        a.buyMutualFund(mf, 40)
        a.sellMutualFund(mf1, 20) #selling MF not in portfolio
        self.assertEqual(a.id['Cash'], 60)
        self.assertEqual(a.id['Mutual Funds'], {'MF1': 40})
        self.assertTrue(a.log == ["Added $100 to 'Cash'.", "Purchased 40 shares of mutual fund MF1 for $40."])

#go back and check that it adds it to the log for both add and withdraw cash
#buyStock:
#    taking from cash
#    adding to port
#    adding to log
#    check:
#        insufficient funds (raises custom exception)
#        whole number buys (raise custom exception)
#        inserting strings for numbers
#        loading a 'not' stock
#        adding to an existing port entry (double add)


if __name__ == '__main__':
    unittest.main()



#pdflatex [filename]
#biber [filename]
#pdflatex [filename]
