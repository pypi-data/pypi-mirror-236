import importlib
from contextlib import contextmanager
from cProfile import Profile
from pstats import SortKey, Stats


@contextmanager
def profiled():
    with Profile() as profiler:
        yield
        stats = Stats(profiler)
        stats.sort_stats(SortKey.CUMULATIVE)
        stats.print_stats()
        stats.dump_stats("profile")


def load_code():
    return importlib.import_module("tests.data.code")
