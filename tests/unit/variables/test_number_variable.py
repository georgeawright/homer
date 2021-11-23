from homer.variables import NumberVariable


def test_subsumes():
    variable = NumberVariable(10, 20)

    assert variable.subsumes(10)
    assert variable.subsumes(20)
    assert variable.subsumes(15)
    assert not variable.subsumes(9.999)
    assert not variable.subsumes(20.001)

    small_variable = NumberVariable(5, 9)
    big_variable = NumberVariable(21, 25)
    broad_variable = NumberVariable(9, 21)

    assert not variable.subsumes(small_variable)
    assert not variable.subsumes(big_variable)
    assert not variable.subsumes(broad_variable)

    narrow_variable_1 = NumberVariable(15, 17)
    narrow_variable_2 = NumberVariable(15, 20)
    narrow_variable_3 = NumberVariable(10, 15)

    assert variable.subsumes(narrow_variable_1)
    assert variable.subsumes(narrow_variable_2)
    assert variable.subsumes(narrow_variable_3)
