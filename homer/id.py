from collections import defaultdict


class ID:
    COUNTS = defaultdict(int)

    @classmethod
    def new(cls, typ: type, qualifier: str = None) -> str:
        qualifier = qualifier if qualifier is not None else ""
        type_name = qualifier + typ.__name__
        cls.COUNTS[type_name] += 1
        return type_name + str(cls.COUNTS[type_name])
