class Node:
    def __init__(self, data: dict):
        for key, value in data.items():
            setattr(self, key, value)

    def __getattribute__(self, attr: str):
        value = super().__getattribute__(attr)
        if isinstance(value, dict):
            value = Node(value)
        return value
