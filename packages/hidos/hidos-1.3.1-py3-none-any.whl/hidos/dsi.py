import functools
from typing import cast, Any, Iterable, Iterator, Optional, Union


@functools.total_ordering
class EditionId:
    def __init__(self, value: Union[str, 'EditionId', Iterable[int]] = tuple()):
        self._tuple: tuple[int]
        if isinstance(value, EditionId):
            self._tuple = value._tuple
        else:
            if isinstance(value, str):
                value = (int(s) for s in value.split("."))
            else:
                if any(type(i) != int for i in value):
                    raise ValueError("EditionId components must all be int")
            self._tuple = cast(tuple[int], tuple(value))
            if any(i < 0 for i in self._tuple):
                raise ValueError("EditionId component integers must be non-negative")

    def sub(self, num: int) -> 'EditionId':
        return EditionId((*self._tuple, num))

    @property
    def listed(self) -> bool:
        return not self.unlisted

    @property
    def unlisted(self) -> bool:
        return 0 in self._tuple

    def __getitem__(self, i: int) -> int:
        return self._tuple[i]

    def __len__(self) -> int:
        return len(self._tuple)

    def __str__(self) -> str:
        return ".".join((str(i) for i in self._tuple))

    def __hash__(self) -> int:
        return hash(self._tuple)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, EditionId):
            return self._tuple == other._tuple
        return False

    def __ge__(self, other: Any) -> bool:
        if isinstance(other, EditionId):
            return self._tuple >= other._tuple
        raise TypeError("Must compare a EditionId to a EditionId")

    def __repr__(self) -> str:
        return str(self)

    def __iter__(self) -> Iterator[int]:
        return iter(self._tuple)


class Dsi:
    def __init__(self, value: Union['Dsi', str], edition: Optional[EditionId] = None):
        self.base: str
        self.edid: EditionId
        if isinstance(value, Dsi):
            self.base = value.base
            self.edid = value.edid
        else:
            parts = value.split("/", 1)
            if len(parts) > 2:
                raise ValueError(f"Invalid DSI: {value}")
            self.base = parts[0]
            try:
                self.edid = EditionId(parts[1])
            except IndexError:
                self.edid = EditionId()
        if edition is not None:
            edid = EditionId(edition)
            if self.edid != EditionId() and self.edid != edition:
                raise ValueError(f"Conflicting edition: {value} vs {edition}")
            self.edid = edid

    def __str__(self) -> str:
        eds = str(self.edid)
        return self.base if not eds else self.base + "/" + eds

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Dsi):
            return self.base == other.base and self.edid == self.edid
        return False

    def __hash__(self) -> int:
        return hash((self.base, self.edid))
