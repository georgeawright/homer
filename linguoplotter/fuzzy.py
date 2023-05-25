from functools import reduce


def NOT(a: float) -> float:
    return 1.0 - a


def AND(*args):
    operation = lambda a, b: a * b
    return reduce(operation, args, 1.0)


def OR(*args):
    operation = lambda a, b: a + b - a * b
    return reduce(operation, args, 0.0)


def NAND(*args):
    return NOT(AND(args))


def NOR(*args):
    return NOT(OR(args))
