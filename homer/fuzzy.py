def NOT(a):
    return 1 - a


def AND(a, b):
    return a * b


def OR(a, b):
    return a + b - a * b


def NAND(a, b):
    return NOT(AND(a, b))


def NOR(a, b):
    return NOT(OR(a, b))


def XOR(a, b):
    return AND(OR(a, b), NAND(a, b))
