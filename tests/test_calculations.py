import pytest
from app.calculations import BankAccount, InsufficientFunds
from app.calculations import add, subtract, multiply, divide

@pytest.fixture
def zero_bank_account():
    print("Creating empty bank account!")
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)

@pytest.mark.parametrize("num1, num2, expected", [
    (3, 2, 5),
    (3, 3, 6),
    (3, 6, 9),
])
def test_add(num1, num2, expected):
    sum = add(num1, num2)

    # assert True
    # assert 1 == 1
    # assert sum == 5
    assert sum == expected


def test_subtract():
    subtraction = subtract(9, 8)

    assert subtraction == 1


def test_multiply():
    multiplication = multiply(40, 20)

    assert multiplication == 800


def test_divide():
    division = divide(50, 10)

    assert division == 5


def test_bank_set_initial_amount(bank_account):

    assert bank_account.balance == 50

#
def test_bank_default_amount(zero_bank_account):
    print("Testing my bank account!")

    assert zero_bank_account.balance == 0

#
def test_withdraw(bank_account):
    bank_account.withdraw(30)
    
    assert bank_account.balance == 20

#
def test_deposit(bank_account):
    bank_account.deposit(30)
    
    assert bank_account.balance == 80

#
def test_collect_interest(bank_account):
    bank_account.collecting_interest()

    assert round(bank_account.balance, 6) == 55

#
@pytest.mark.parametrize("deposited, withdrew, expected", [
    (500, 200, 300),
    (20, 10, 10),
    (1200,200, 1000),
    # (20,200, 1000),
])
def test_bank_transaction(zero_bank_account, deposited, withdrew, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)

    assert zero_bank_account.balance == expected

#
def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(200)