# Name: Quan Pham
# Login:cs61a-sy
# TA:Sharad Vikram
# Section:19
# Q1.

# Mutable rlist
def mutable_rlist():
    """A mutable rlist that supports push, pop, and setitem operations.

    >>> a = mutable_rlist()
    >>> a('push', 3)
    >>> a('push', 2)
    >>> a('push', 1)
    >>> a('setitem', 1, 4)
    >>> a('str')
    '<rlist (1, 4, 3)>'
    """
    contents = empty_rlist

    def setitem(index, value):
        nonlocal contents
        tmp = []
        i = 0
        poppin = 0
        while i <= index:
            poppin = dispatch('pop')
            tmp.append(poppin)
            i +=1
        dispatch('push',value)
        tmp = tmp[:-1]
        for i in range(1,len(tmp)+1):
            poppin = dispatch('push',tmp[:-i])
    def dispatch(message, value=None, value1=None):
        nonlocal contents
        if message == 'first':
            return first(contents)
        if message == 'rest':
            return rest(contents)
        if message == 'len':
            return len_rlist(contents)
        if message == 'getitem':
            return getitem_rlist(contents, value)
        if message == 'str':
            return str_rlist(contents)
        if message == 'pop':
            item = first(contents)
            contents = rest(contents)
            return item
        if message == 'push':
            contents = rlist(value, contents)
        if message == 'setitem':
            contents = setitem(value, value1)
    return dispatch

def pair(x, y):
    def dispatch(m):
        if m == 0:
            return x
        elif m == 1:
            return y
    return dispatch

empty_rlist = None

def rlist(first, rest):
    return pair(first, rest)

def first(s):
    return s(0)

def rest(s):
    return s(1)

def len_rlist(s):
    if s == empty_rlist:
        return 0
    return 1 + len_rlist(rest(s))

def getitem_rlist(s, k):
    if k == 0:
        return first(s)
    return getitem_rlist(rest(s), k - 1)

def rlist_to_tuple(s):
    if s == empty_rlist:
        return ()
    return (first(s),) + rlist_to_tuple(rest(s))

def str_rlist(s):
    return '<rlist ' + str(rlist_to_tuple(s)) + '>'

# Q2.

class VendingMachine(object):
    """A vending machine that vends some product for some price.

    >>> v = VendingMachine('crab', 10)
    >>> v.vend()
    'Machine is out of stock.'
    >>> v.restock(2)
    'Current crab stock: 2'
    >>> v.vend()
    'You must deposit $10 more.'
    >>> v.deposit(7)
    'Current balance: $7'
    >>> v.vend()
    'You must deposit $3 more.'
    >>> v.deposit(5)
    'Current balance: $12'
    >>> v.vend()
    'Here is your crab and $2 change.'
    >>> v.deposit(10)
    'Current balance: $10'
    >>> v.vend()
    'Here is your crab.'
    >>> v.deposit(15)
    'Machine is out of stock. Here is your $15.'
    """
    "*** YOUR CODE HERE ***"
    def __init__ (self, product, dollar):
        self.price = dollar
        self.unit = 0
        self.type = product
        self.balance = 0
    def deposit(self,amount):
        if self.unit > 0:
            self.balance = self.balance + amount
            return print('Current balance: $',self.balance,'.')
        else:
            return print('Machine is out of stock. Here is your $',amount,'.')
    def restock(self,amount):
        self.unit = self.unit + amount
        return print('Current',self.type,'stock:',self.unit,'.')
    def vend(self):
        if self.unit == 0:
            return print('Machine is out of stock.')
        if self.unit > 0:
            if self.balance < self.price:
                return print('You must deposit $',self.price - self.balance,'more.')
            if self.balance == self.price:
                self.unit = self.unit - 1
                self.balance = 0
                return print('Here is your crab.')
            if self.balance > self.price:
                change = self.balance - self.price
                self.balance = 0
                self.unit = self.unit - 1
                return print('Here is your crab and $',change,'change.')

# Q3.

class MissManners(object):
    """A container class that only forward messages that say please.

    >>> v = VendingMachine('teaspoon', 10)
    >>> v.restock(2)
    'Current teaspoon stock: 2'
    >>> m = MissManners(v)
    >>> m.ask('vend')
    'You must learn to say please.'
    >>> m.ask('please vend')
    'You must deposit $10 more.'
    >>> m.ask('please deposit', 20)
    'Current balance: $20'
    >>> m.ask('now will you vend?')
    'You must learn to say please.'
    >>> m.ask('please give up a teaspoon')
    'Thanks for asking, but I know not how to give up a teaspoon'
    >>> m.ask('please vend')
    'Here is your teaspoon and $10 change.'
    """
    "*** YOUR CODE HERE ***"
    def __init__(self, object):
        self.object = object
    def ask(self,*arg):
        wordlst = arg[0].split()
        if any(word in 'please' for word in wordlst):
            if any(word in 'vend' for word in wordlst):
                self.object.vend()
            elif any(word in 'deposit' for word in wordlst):
                self.object.deposit(arg[1])
            elif any(word in 'restock' for word in wordlst):
                self.object.restock(arg[1])
            else:
                wordlst.remove('please')
                return print('Thanks for asking, but I know not'," ".join(wordlst),'.')
        else:
            return print('You must learn to say please')
# Q4.

class Account(object):
    """A bank account that allows deposits and withdrawals.

    >>> john = Account('John')
    >>> jack = Account('Jack')
    >>> john.deposit(10)
    10
    >>> john.deposit(5)
    15
    >>> john.interest
    0.02
    >>> jack.deposit(7)
    7
    >>> jack.deposit(5)
    12
    """

    interest = 0.02

    def __init__(self, account_holder):
        self.balance = 0
        self.holder = account_holder

    def deposit(self, amount):
        """Increase the account balance by amount and return the new balance."""
        self.balance = self.balance + amount
        return self.balance

    def withdraw(self, amount):
        """Decrease the account balance by amount and return the new balance."""
        if amount > self.balance:
            return 'Insufficient funds'
        self.balance = self.balance - amount
        return self.balance

"*** YOUR CODE HERE ***"
class SecureAccount(Account):
    def __init__(self,account_holder,account_password):
        self.balance = 0
        self.holder = account_holder
        self.password = account_password
        self.invalidcount = 0
    def secure_withdraw(self, amount, pinput):
        if self.invalidcount == 3:
            return print('This account is locked')
        if pinput != self.password:
            self.invalidcount = self.invalidcount + 1
            return print('Incorrect password')
        if pinput == self.password:
            return Account.withdraw(self,amount)
    def withdraw(self, amount):
        return print('This account requires a password to withdraw')

import unittest

class SecureAccountTest(unittest.TestCase):
    """Test the SecureAccount class."""

    def setUp(self):
        self.account = SecureAccount('Alyssa P. Hacker', 'p4ssw0rd')

    def test_secure(self):
        acc = self.account
        acc.deposit(1000)
        self.assertEqual(acc.balance, 1000, 'Bank error! Incorrect balance')
        self.assertEqual(acc.withdraw(100),
                         'This account requires a password to withdraw')
        self.assertEqual(acc.secure_withdraw(100, 'p4ssw0rd'), 900,
                         "Didn't withdraw 100")
        self.assertEqual(acc.secure_withdraw(100, 'h4x0r'), 'Incorrect password')
        self.assertEqual(acc.secure_withdraw(100, 'n00b'), 'Incorrect password')
        self.assertEqual(acc.secure_withdraw(100, '1337'), 'Incorrect password')
        self.assertEqual(acc.balance, 900, 'Withdrew with bad password')
        self.assertEqual(acc.secure_withdraw(100, 'p4ssw0rd'),
                         'This account is locked')
        self.assertEqual(acc.balance, 900, 'Withdrew from locked account')

# Q5.

"*** YOUR CODE HERE ***"

"""class MoreSecureAccountTest(SecureAccountTest):
    Test the MoreSecureAccount class.

    def setUp(self):
        self.account = MoreSecureAccount('Alyssa P. Hacker', 'p4ssw0rd')

"""