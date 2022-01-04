

class SystemDB:
    __instance = None

    def __init__(self, id):

        if SystemDB.__instance != None:
            raise Exception('This class is a singleton!')
        else:
            SystemDB.__instance = self

        self.dataSet = {'id1': ['Savings Account', '1', 2000],
                        'id2': ['Savings Account', '2', 5000],
                        'id3': ['Current Account', '3', 0, 1000, 10000],
                        'id4': ['Current Account', '4', 5000, 0, 20000]}
                                # negative balance, positive balance, overdraft
        self.id = id
        if id not in self.dataSet:
            raise Exception('Account Not Found')

    def withdraw(self, amount):
        idName = self.dataSet[self.id]  # getting the dictionary key
        if idName[0] == 'Savings Account':
            idName[2] = SavingsAccount(idName[2]).withdraw(amount)
        else:
            idName[2], idName[3] = CurrentAccount(idName[2], idName[3], idName[4]).withdraw(amount)
        print(self.dataSet)

    def deposit(self, amount):
        idName = self.dataSet[self.id]
        if idName[0] == 'Savings Account':
            idName[2] = SavingsAccount(idName[2]).deposit(amount)
        else:
            idName[2], idName[3] = CurrentAccount(idName[2], idName[3], idName[4]).deposit(amount)
        print(self.dataSet)

class SavingsAccount:
    def __init__(self, balance):
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        if self.balance - amount > 1000:    # min balance in Savings are 1000
            self.balance -= amount
            return self.balance
            # print(self.balance, '-=', amount)
        else:
            raise Exception('Withdrawal Amount Too Large')


class CurrentAccount:
    def __init__(self, negativeBalance, positiveBalance, overdraft):
        self.negativeBalance = negativeBalance
        self.positiveBalance = positiveBalance
        self.overdraft = overdraft

    def deposit(self, amount):
        if self.positiveBalance == 0:
            if self.negativeBalance >= amount:
                self.negativeBalance -= amount
                return self.negativeBalance, self.positiveBalance
            else:
                self.positiveBalance += amount - self.negativeBalance
                self.negativeBalance = 0
                return self.negativeBalance, self.positiveBalance
        else:
            self.positiveBalance += amount
            return self.negativeBalance, self.positiveBalance

    def withdraw(self, amount):
        if self.positiveBalance == 0:
            if self.overdraft - self.negativeBalance < amount:
                raise Exception('Withdrawal Amount Too Large')
            else:
                self.negativeBalance += amount
                return self.negativeBalance, self.positiveBalance
        else:
            if self.overdraft + self.positiveBalance < amount:
                raise Exception('Withdrawal Amount Too Large')
            elif self.positiveBalance < amount:
                self.negativeBalance += amount - self.positiveBalance
                self.positiveBalance = 0
                return self.negativeBalance, self.positiveBalance
            else:
                self.positiveBalance -= amount
                return self.negativeBalance, self.positiveBalance


# SystemDB('id4').deposit(7300)   # to make 7300 deposite in account 'id4'
# SystemDB('id2').withdraw(1850)  # to make 1850 withdraw from account 'id2'

