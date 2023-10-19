from hello_pypigit.who import my_name, who, plus

def test_my_name():
    print("my name is TOM")

def test_my_name():
    my_name()
    
def test_who():
    who()
    
def test_plus():
    r = plus(1, 3)
    assert r ==  4
