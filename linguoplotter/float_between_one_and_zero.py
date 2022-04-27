from typing import Union


class FloatBetweenOneAndZero(float):
    def __new__(cls, number: Union[float, int]):
        number = min(number, 1.0)
        number = max(number, 0.0)
        return float.__new__(cls, number)
