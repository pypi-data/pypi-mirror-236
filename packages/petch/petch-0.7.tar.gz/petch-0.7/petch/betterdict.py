from typing import Any, Callable, TypeVar
from petch.betterlist import BetterList

K = TypeVar("K")
V = TypeVar("V")
M = TypeVar("M")
N = TypeVar("N")


class BetterDict(dict[K, V]):
    """
    This Dict Class allows you todo javascript styled continuous operation.
    ex.
    x = BetterDict({'a':1,'b':2,'c':3,'d':4})
    y = x.filter_key(func1).filter_value(func2).map_key(func3).foreach_value(print)
    """

    @property
    def keys_list(self):
        return BetterList(self.keys())

    @property
    def values_list(self):
        return BetterList(self.values())

    @property
    def length(self):
        return len(self)

    def sort(self, func: Callable[[K], Any] = lambda x: x[1]) -> "BetterDict[K,V]":
        """
        Sort your key
        Input : {"e": 3, "d": 2, "a": 4, "b": 6, "c": 1}
        Output: {'a': 4, 'b': 6, 'c': 1, 'd': 2, 'e': 3}
        """
        return BetterDict(sorted(self.items(), key=func))

    def max(
        self, n_largest: int = 1, func: Callable[[K], Any] = lambda x: x[1]
    ) -> "BetterList[K]":
        """
        BetterDict({"a":1,"b":2,"c":3,"d":4})
        Return key list that looks like this
        ['d', 'c']
        """
        return BetterList(self.sort(func).keys_list[-n_largest:][::-1])

    def min(
        self, n_smallest: int = 1, func: Callable[[K], Any] = lambda x: x[1]
    ) -> "BetterList[K]":
        """
        BetterDict({"a":1,"b":2,"c":3,"d":4})
        Return key list that looks like this
        ['a', 'b']
        """
        return BetterList(self.sort(func).keys_list[:n_smallest])

    def sort_keys(self, func: Callable[[K], Any] = lambda x: x) -> "BetterDict[K,V]":
        """
        Input   : {"e": 3.1, "d": 2.3, "a": 4.5, "b": 6.0, "c": 1.2}
        Output  : {'a': 4.5, 'b': 6.0, 'c': 1.2, 'd': 2.3, 'e': 3.1}
        """
        return self.sort(func)

    def sort_values(self, func: Callable[[V], Any] = lambda x: x) -> "BetterDict[K,V]":
        """
        Input   : {"e": 3.1, "d": 2.3, "a": 4.5, "b": 6.0, "c": 1.2}
        Output  : {'c': 1.2, 'd': 2.3, 'e': 3.1, 'a': 4.5, 'b': 6.0}
        """
        return self.sort(lambda t: func(self[t[0]]))

    def min_by_keys(
        self, n_smallest: int = 1, func: Callable[[K], Any] = lambda x: x
    ) -> "BetterDict[K,V]":
        """
        Input   : {"e": 3.1, "d": 2.3, "a": 4.5, "b": 6.0, "c": 1.2}
        Output  : {'a': 4.5, 'b': 6.0}
        """
        return BetterDict(BetterList(self.sort_keys(func).items())[:n_smallest])

    def max_by_keys(
        self, n_largest: int = 1, func: Callable[[K], Any] = lambda x: x
    ) -> "BetterDict[K,V]":
        """
        Input   : {"e": 3.1, "d": 2.3, "a": 4.5, "b": 6.0, "c": 1.2}
        Output  : {'e': 3.1, 'd': 2.3}
        """
        return BetterDict(BetterList(self.sort_keys(func).items())[-n_largest:][::-1])

    def min_by_values(
        self, n_smallest: int = 1, func: Callable[[V], Any] = lambda x: x
    ) -> "BetterDict[K,V]":
        """
        Input   : {"e": 3.1, "d": 2.3, "a": 4.5, "b": 6.0, "c": 1.2}
        Output  : {'c': 1.2, 'd': 2.3}
        """
        return BetterDict(BetterList(self.sort_values(func).items())[:n_smallest])

    def max_by_values(
        self, n_largest: int = 1, func: Callable[[V], Any] = lambda x: x
    ) -> "BetterDict[K,V]":
        """
        Input   : {"e": 3.1, "d": 2.3, "a": 4.5, "b": 6.0, "c": 1.2}
        Output  : {'b': 6.0, 'a': 4.5}
        """
        return BetterDict(BetterList(self.sort_values(func).items())[-n_largest:][::-1])

    def foreach(self, func: Callable[[K, V], Any]) -> None:
        for key, value in self.items():
            func(key, value)

    def foreach_key(self, func: Callable[[K], Any]) -> None:
        for key, _ in self.items():
            func(key)

    def foreach_value(self, func: Callable[[V], Any]) -> None:
        for _, value in self.items():
            func(value)

    def filter_key(self, func: Callable[[K], bool]) -> "BetterDict[K,V]":
        return BetterDict({key: value for key, value in self.items() if func(key)})

    def filter_out_key(self, func: Callable[[K], bool]) -> "BetterDict[K,V]":
        return BetterDict({key: value for key, value in self.items() if not func(key)})

    def filter_value(self, func: Callable[[V], bool]) -> "BetterDict[K,V]":
        return BetterDict({key: value for key, value in self.items() if func(value)})

    def filter_out_value(self, func: Callable[[V], bool]) -> "BetterDict[K,V]":
        return BetterDict(
            {key: value for key, value in self.items() if not func(value)}
        )

    def map(self, func: Callable[[K, V], N]) -> "BetterDict[K,N]":
        return BetterDict({key: func(key, value) for key, value in self.items()})

    def map_key(self, func: Callable[[K], N]) -> "BetterDict[N,V]":
        return BetterDict({func(key): value for key, value in self.items()})

    def map_value(self, func: Callable[[V], N]) -> "BetterDict[K,N]":
        return BetterDict({key: func(value) for key, value in self.items()})
