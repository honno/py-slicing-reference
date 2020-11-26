from typing import Iterable
from typing import Sequence
from typing import Union
from typing import Optional
from typing import Any
from collections import OrderedDict
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
            if abs(key) > n:
                raise IndexError("list index out of range")

            i = key if key >= 0 else len(self) + key

            return self._dict[i]

        elif isinstance(key, slice):
            srange = range(n)[key]
            return listy(self._dict[i] for i in srange)

        else:
            name = type(key).__name__
            raise TypeError(f"listy indices must be integers or slices, not {name}")

    def __setitem__(self, key: Union[int, slice], value: Any):
        n = len(self)

        if isinstance(key, int):
            if abs(key) > n:
                raise IndexError("list index out of range")

            i = key if key >= 0 else n + key

            self._dict[i] = value

        elif isinstance(key, slice):
            keys = self._dict.keys()

            values = list(value) if isinstance(value, Iterable) else [value]
            nvalues = len(values)

            start, stop, step = key.indices(n)

            # determine slice range

            dstart, dstop = start, stop

            try:
                if (dstop - dstart) / step < 0:
                    if step >= 1:
                        dstop = dstart
                    else:
                        dstart = dstop
            except ZeroDivisionError:
                pass

            srange = range(dstart, dstop, step)

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
            name = type(key).__name__
            raise TypeError(f"listy indices must be integers or slices, not {name}")

    def __delitem__(self, key: Union[int, slice]):
        n = len(self)

        if isinstance(key, int):
            if abs(key) > n:
                raise IndexError("list index out of range")

            del self._dict[key]

            larger_keys = [k for k in self._dict.keys() if k > key]
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

            for k in [k for k in keys if k in srange]:
                del self._dict[k]

            if srange:
                srange_min = min(srange[0], srange[-1])

                larger_keys = sorted([k for k in keys if k > srange_min])

                if larger_keys:
                    larger_values = [self._dict[k] for k in larger_keys]

                    reindexed_subdict = {}
                    rstart = srange_min
                    rstop = rstart + len(larger_keys)
                    for k, v in zip(range(rstart, rstop), larger_values):
                        reindexed_subdict[k] = v

                    for k in larger_keys:
                        del self._dict[k]
                    self._dict.update(reindexed_subdict)

        else:
            name = type(key).__name__
            raise TypeError(f"listy indices must be integers or slices, not {name}")


    def __len__(self):
        return len(self._dict)

    def __iter__(self):
        for i in range(len(self)):
            yield self[i]

    def insert(self, i: int, value: Any):
        larger_keys = [k for k in self._dict.keys() if k >= i]
        reindexed_subdict = {k + 1: self._dict[k] for k in larger_keys}
        for k in larger_keys:
            del self._dict[k]
        self._dict.update(reindexed_subdict)

        self._dict[i] = value

    def __eq__(self, other):
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
