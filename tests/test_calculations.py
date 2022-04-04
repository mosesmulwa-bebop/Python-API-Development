import pytest
from app.calculations import *

@pytest.fixture
def zero_bank_account():
    return BankAccount()


@pytest.fixture
def bank_account():
    return BankAccount(50)


@pytest.mark.parametrize("num1, num2, expected_value",[
    (3,4,7),
    (6,5,11),
    (8,9,17)
])
def test_add(num1,num2,expected_value):
    print("testing add function")
    assert add(num1,num2) == expected_value

def test_subtract():
    print("testing subtract function")
    assert subtract(4,3) == 1

def test_divide():
    print("testing divide function")
    assert divide(16,4) == 4 

def test_multiply():
    print("testing multiply function")
    assert multiply(3,4) == 12





def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 50

def test_bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_bank_deposit(zero_bank_account):
    zero_bank_account.deposit(50)
    assert zero_bank_account.balance == 50


@pytest.mark.parametrize("deposited, withdrew, expected_value",[
    (70,70,55),
    (80,80,55),
    (90,90,55)
])


def test_bank_transaction(deposited, withdrew, expected_value, bank_account):
    bank_account.deposit(deposited)
    assert bank_account.balance == 50 + deposited
    bank_account.withdraw(withdrew)
    assert bank_account.balance == 50
    bank_account.collect_interest()
    assert round(bank_account.balance) == expected_value

def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(200)
