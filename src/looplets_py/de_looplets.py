"""
All the looplet definitions
"""

import typing as tp


class Expression:
    """
    Base class for all subexpr
    """

    def __getitem__(self, idx):
        """
        Get the item at index idx
        """
        raise NotImplementedError("Subclasses must implement __getitem__")

    def __iter__(self):
        """
        Get an iterator over the expression
        """
        raise NotImplementedError("Subclasses must implement __iter__")


class Run(Expression):
    """
    A sequence of same repeated body. Note that
    it may be something other than a scaler
    """

    def __init__(self, body: tp.Any):
        self.body = body

    def __getitem__(self, idx):
        return self.body  # possible rep exposure

    def __iter__(self):
        while True:
            yield self.body


class Phase:
    """
    Limits the extent of the "body" upto stride.
    """

    def __init__(self, body: Expression, stride: int | None = None):
        self.body = body
        self.stride = stride

    def __getitem__(self, idx):
        if self.stride is None or idx < self.stride:
            return self.body[idx]

        raise IndexError("Index out of range")

    def __iter__(self):
        if self.stride is None:
            while True:
                yield self.body
        # if self.stride is not None:
        for i in range(self.stride):
            yield self.body[i]

class Pipeline(Expression):
    """
    Connects multiple bodies together
    """
    def __init__(self, *bodies: Phase):
        self.bodies = bodies
        self.boundaries = [body.stride for body in bodies]

    def __getitem__(self, idx):
        for i, boundary in enumerate(self.boundaries):
            if boundary is None or idx < boundary:
                return self.bodies[i][idx]
            idx -= boundary
        raise IndexError("Index out of range")

    def __iter__(self):
        for i, _ in enumerate(self.boundaries):
            yield from self.bodies[i]

class Lookup(Expression):
    """
    More generalized version of Run. Can take in a sequence often just a 
    lookup of an array. But can also by something like (i) -> sin(i)
    """

    def __init__(self, body: tp.Callable[[int], tp.Any]):
        self.body = body

    def __getitem__(self, idx):
        return self.body(idx)

    def __iter__(self):
        i = 0
        while True:
            yield self.body(i)
            i += 1
