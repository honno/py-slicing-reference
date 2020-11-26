## Python Slicing Reference

Python's builtin `list` type allows one to pass in slices
to get, set or delete a range of elements.

```python
>>> my_list = ['a', 'b','c']
>>> my_list[0:2]
['a', 'b']
>>> my_list[0:3:2]
['a', 'b']
>>> my_list[1:3] = [1, 2]
>>> my_list
['a', 1, 2]
>>> my_list[::-1] = ['z', 'y', 'x']
>>> my_list
['x', 'y', 'z']
```

The slice notation using colons is infact a `slice` builtin,
where `start:stop:step` is equivalent to `slice(start, stop, step)`.
This looks an awful lot like the `range(start, stop, step)` builtin,
but 1-to-1 translating slices to ranges is not always appropiate.

I have created this package as a reference implementation of `list`,
specifically to educate on how it deals with slices.
I use [Hypothesis](https://hypothesis.readthedocs.io/en/latest/) 
to test my custom class `listy` against Python's very own `list`,
hopefully ensuring that all situations where slicing is involved
is perfectly emulated.
