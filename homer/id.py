class ID:
    COUNT = 0

    @classmethod
    def new(cls, item) -> str:
        cls.COUNT += 1
        return type(item).__name__ + str(cls.COUNT)
