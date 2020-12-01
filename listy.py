"""Reference implementation of Python's list

A dictionary is used to map indices to their respective elements.
"""
from typing import Iterable, Sequence, Union, Optional, Any, Type
from collections.abc import MutableSequence

__all__ = ["listy"]

class listy(MutableSequence):
    def __init__(self, sequence: Optional[Iterable] = None):
        self._dict = {}

        if sequence:
            self[:] = sequence

    def __getitem__(self, key: Union[int, slice]):
        n = len(self)

        if isinstance(key, int):
            if key >= n or key < -n:
                raise IndexError("list index out of range")
            i = key if key >= 0 else len(self) + key
            return self._dict[i]

        elif isinstance(key, slice):
            srange = range(n)[key]
            return listy(self._dict[i] for i in srange)

        else:
            listy._raise_type_error(type(key))

    def __setitem__(self, key: Union[int, slice], value: Any):
        n = len(self)

        if isinstance(key, int):
            if key >= n or key < -n:
                raise IndexError("list index out of range")
            i = key if key >= 0 else n + key
            self._dict[i] = value

        elif isinstance(key, slice):
            keys = self._dict.keys()

            values = list(value) if isinstance(value, Iterable) else [value]
            nvalues = len(values)

            start, stop, step = key.indices(n)

            # determine slice range

            sstart, sstop = start, stop
            try:
                if (sstop - sstart) / step < 0:
                    if step >= 1:
                        sstop = sstart
                    else:
                        sstart = sstop
            except ZeroDivisionError:
                pass
            srange = range(sstart, sstop, step)

            # del keys in slice range

            for k in [k for k in keys if k in srange]:
                del self._dict[k]

            # update keys above slice range

            diff = nvalues - len(srange)
            if diff:
                try:
                    srange_max = max(srange[0], srange[-1])
                except IndexError:
                    srange_max = srange.start

                larger_keys = [k for k in keys if k >= srange_max]
                reindexed_subdict = {k + diff: self._dict[k] for k in larger_keys}

                for k in larger_keys:
                    del self._dict[k]
                self._dict.update(reindexed_subdict)

            # finally, insert value(s) safely

            istop = start + step * nvalues
            insert_range = range(start, istop, step)
            for k, v in zip(insert_range, values):
                self._dict[k] = v

        else:
            listy._raise_type_error(type(key))

    def __delitem__(self, key: Union[int, slice]):
        n = len(self)

        if isinstance(key, int):
            if abs(key) > n:
                raise IndexError("list index out of range")
            i = key if key >= 0 else n + key
            del self._dict[key]

            larger_keys = [k for k in self._dict.keys() if k > i]
            reindexed_subdict = {k - 1: self._dict[k] for k in larger_keys}
            for k in larger_keys:
                del self._dict[k]
            self._dict.update(reindexed_subdict)

        elif isinstance(key, slice):
            keys = self._dict.keys()

            start, stop, step = key.indices(n)
            try:
                if (stop - start) / step < 0:
                    if step >= 1:
                        stop = start
                    else:
                        start = stop
            except ZeroDivisionError:
                pass
            srange = range(start, stop, step)

            if srange:
                for k in [k for k in keys if k in srange]:
                    del self._dict[k]

                srange_min = min(srange[0], srange[-1])
                larger_keys = [k for k in keys if k > srange_min]

                if larger_keys:
                    reindexed_subdict = {}
                    rstart = srange_min
                    rstop = rstart + len(larger_keys)
                    for k, lk in zip(range(rstart, rstop), sorted(larger_keys)):
                        larger_value = self._dict[lk]
                        reindexed_subdict[k] = larger_value

                    for k in larger_keys:
                        del self._dict[k]
                    self._dict.update(reindexed_subdict)

        else:
            listy._raise_type_error(type(key))

    def __len__(self):
        return len(self._dict)

    def insert(self, i: int, value: Any):
        larger_keys = [k for k in self._dict.keys() if k >= i]
        reindexed_subdict = {k + 1: self._dict[k] for k in larger_keys}
        for k in larger_keys:
            del self._dict[k]
        self._dict.update(reindexed_subdict)

        self._dict[i] = value

    def __eq__(self, other: Any):
        if isinstance(other, Sequence):
            if len(self) != len(other):
                return False
            return all(a == b for a, b in zip(self, other))
        else:
            return False

    def __repr__(self):
        list_ = list(self[:len(self)])
        return repr(list_)

    def __str__(self):
        return f"listy({repr(self)})"

    @staticmethod
    def _raise_type_error(type_: Type):
        name = type_.__name__
        raise TypeError(f"listy indices must be integers or slices, not {name}")


