from hypothesis import assume
from hypothesis import reject
from hypothesis import strategies as st
from hypothesis.stateful import RuleBasedStateMachine
from hypothesis.stateful import initialize
from hypothesis.stateful import rule

from listy import listy

ints = st.lists(st.integers())
chars = st.from_regex(r"[a-z]*", fullmatch=True)


# TODO test extended slices (ugh)
class DefaultListStateMachine(RuleBasedStateMachine):
    @initialize(ints=ints)
    def init_lists(self, ints):
        self.list_ = ints

        self.listy = listy(ints)

        assert self.listy == self.list_

    @property
    def n(self):
        return len(self.list_)

    @rule(data=st.data())
    def get(self, data):
        assume(self.n > 0)
        i = data.draw(st.integers(min_value=0, max_value=self.n - 1))

        assert self.listy[i] == self.list_[i]

    @rule(data=st.data(), chars=chars)
    def set(self, data, chars):
        assume(self.n > 0)
        i = data.draw(st.integers(min_value=0, max_value=self.n - 1))

        self.list_[i] = chars
        self.listy[i] = chars

        assert self.listy == self.list_

    @rule(chars=chars)
    def append(self, chars):
        self.list_.append(chars)
        self.listy.append(chars)

        assert self.listy == self.list_

    @rule(ints=ints)
    def concat(self, ints):
        self.list_ += ints
        self.listy += ints

        assert self.listy == self.list_

    @rule(data=st.data())
    def slice_get(self, data):
        slice_ = data.draw(st.slices(self.n))

        assert self.listy[slice_] == self.list_[slice_]

    @rule(data=st.data(), chars_or_ints=st.one_of(chars, ints))
    def slice_set(self, data, chars_or_ints):
        slice_ = data.draw(st.slices(self.n))

        try:
            self.list_[slice_] = chars_or_ints
        except ValueError:
            # lists don't support extended slice when their length differs from
            # the length of the inserted values
            reject()
        self.listy[slice_] = chars_or_ints

        assert self.listy == self.list_

    @rule(data=st.data())
    def del_(self, data):
        assume(self.n > 0)
        i = data.draw(st.integers(min_value=0, max_value=self.n - 1))

        del self.list_[i]
        del self.listy[i]

        assert self.listy == self.list_

    @rule(data=st.data())
    def del_slice(self, data):
        slice_ = data.draw(st.slices(self.n))

        del self.list_[slice_]
        del self.listy[slice_]

        assert self.listy == self.list_


TestDefaultListStateMachine = DefaultListStateMachine.TestCase
