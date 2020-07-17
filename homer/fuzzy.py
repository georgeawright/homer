from functools import reduce


def NOT(a: float) -> float:
    return 1.0 - a


def AND(*arg):
    return reduce(_AND, arg)


def OR(*arg):
    return reduce(_OR, arg)


def NAND(*arg):
    return reduce(_NAND, arg)


def NOR(*arg):
    return reduce(_NOR, arg)


def XOR(*arg):
    return reduce(_XOR, arg)


def XNOR(*arg):
    return reduce(_XNOR, arg)


def _AND(a: float, b: float) -> float:
    return a * b


def _OR(a: float, b: float) -> float:
    return a + b - a * b


def _NAND(a: float, b: float) -> float:
    return NOT(_AND(a, b))


def _NOR(a: float, b: float) -> float:
    return NOT(_OR(a, b))


def _XOR(a: float, b: float) -> float:
    return AND(_OR(a, b), _NAND(a, b))


def _XNOR(a: float, b: float) -> float:
    return NOT(_XOR(a, b))
