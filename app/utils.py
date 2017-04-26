def depth(x):
    # type: (dict) -> int
    if isinstance(x, dict) and x:
        return 1 + max(depth(i) for i in x.values())
    else:
        return 0


assert depth({}) == 0
assert depth({"a": "a"}) == 1
assert depth({"a": {"a": "b"}}) == 2
assert depth({"a": {"a": "b"}, "b": {"a": {"b": "c"}}}) == 3
