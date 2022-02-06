from app.calculations import *


def test_add():
    print("testing add function")
    assert add(3,4) == 7

def test_subtract():
    print("testing subtract function")
    assert subtract(4,3) == 1

def test_divide():
    print("testing divide function")
    assert divide(16,4) == 4 

def test_multiply():
    print("testing multiply function")
    assert multiply(3,4) == 12
