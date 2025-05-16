from typing import Any, Union


class Secret:
    def __init__(self, value: Union[str, bytes]):
        if isinstance(value, str):
            value = value.encode("utf-8")
        self._secret = value

    def getSecret(self) -> bytes:
        return self._secret

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, self.__class__) and self._secret == other

    def __repr__(self) -> str:
        return "<Secret>"

    def __str__(self) -> str:
        if self._secret:
            return "*******"
        return ""

    def __len__(self) -> int:
        return len(self._secret)

    def __hash__(self) -> int:
        return hash(self._secret)
