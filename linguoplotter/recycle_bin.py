class RecycleBin:
    def __init__(self):
        self._items = []

    @property
    def is_empty(self):
        return len(self._items) == 0

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return (item for item in self._items)

    def add(self, item):
        self._items.append(item)

    def remove_oldest(self):
        return self._items.pop(0)
