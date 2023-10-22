from numpy.testing import assert_allclose
from time import time
from numba import njit, prange
from typing import Callable


class TestHelper:
    @staticmethod
    def actual(x):
        return x

    desired = actual

    @staticmethod
    def config_test(actual: Callable, desired: Callable) -> None:
        TestHelper.actual = actual
        TestHelper.desired = desired

    @staticmethod
    def assert_allclose(x):
        a = TestHelper.actual(x)
        b = TestHelper.desired(x)
        print(a, b)
        assert_allclose(a, b)

    @staticmethod
    def compare_performance(numba, comp, arg, parallel_repeats=1000, repeats=20):
        @njit(parallel=True)
        def numba_loop():
            for _ in prange(parallel_repeats):
                numba(arg)

        def regular_loop():
            for _ in range(parallel_repeats):
                comp(arg)

        numba_loop()

        start = time()
        for _ in range(repeats):
            numba_loop()
        numba_time = time() - start

        start = time()
        for _ in range(repeats):
            regular_loop()
        scipy_time = time() - start
        if numba_time < scipy_time:
            speed_up = int(((scipy_time / numba_time) - 1) * 100)
            print("This implementation was " + str(speed_up) + "% faster.")
        else:
            slow_down = int((1 - (scipy_time / numba_time)) * 100)
            assert False, "This implementation was " + str(slow_down) + "% slower."
