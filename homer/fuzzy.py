def NOT(a: float) -> float:
    return 1.0 - a


def AND(a: float, b: float) -> float:
    return a * b


def OR(a: float, b: float) -> float:
    return a + b - a * b


def NAND(a: float, b: float) -> float:
    return NOT(AND(a, b))


def NOR(a: float, b: float) -> float:
    return NOT(OR(a, b))


def XOR(a: float, b: float) -> float:
    return AND(OR(a, b), NAND(a, b))


def XNOR(a: float, b: float) -> float:
    return NOT(XOR(a, b))
