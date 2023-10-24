"Utilities for lists"
from typing import Generator, Callable, Iterable


def cast(dtype: type):
    """Allows dynamic cast for generators

    Args:
        dtype (type): a data type
    """
    def funchandler(func: Callable):
        def funcwrapper(*args: list, **kwargs: dict):
            return dtype(func(*args, **kwargs))
        return funcwrapper
    return funchandler


@cast(list)
def flatten(list_to_flatten: list) -> Generator:
    """Flattens a potentially multi-level list

    Args:
        list_to_flatten (list): a list eventually containing other lists and elts

    Yields:
        Generator: series of elements, converted by decorator to a list
    """
    for elt in list_to_flatten:
        if isinstance(elt, list):
            yield from flatten(elt)
        else:
            yield elt


def boolean_reverse(list_to_reverse: list, cond: bool) -> list:
    """If boolean condition is true, reverses the list.
    Otherwise, keeps it as it is.

    Args:
        list_to_reverse (list): candidate for reversal
        cond (bool): if the list should be reversed

    Returns:
        list: the list or it's reverse
    """
    list_to_reverse[::-cond or 1]


def grouper(iterable: Iterable, n: int = 2, m: int = 1) -> list:
    """Collect data into possibly overlapping fixed-length chunks or blocks

    Args:
        iterable (Iterable): the iterable you want to pack
        n (int, optional): size of the chunks. Defaults to 2.
        m (int, optional): overlaps of the chunks. Defaults to 1.

    Returns:
        list: a list of n-sized chunks with an overlap of m
    """
    return [iterable[i:i+n] for i in range(0, len(iterable)-1, n-m)]


@cast(list)
def common_members(*elements: set) -> list:
    """given a series of sets, returns common members

    Args:
        *elements (set): a series of sets

    Returns:
        list: common elements between all the sets
    """
    return elements[0].intersection(*elements[1:])
