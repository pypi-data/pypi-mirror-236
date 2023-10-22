import numpy as np
import scipy.special

from src.functions.gamma import gamma
from tests.test_utils import TestHelper


class Test:
    def test_integer(self):
        TestHelper.config_test(gamma, scipy.special.gamma)
        TestHelper.assert_allclose(1)
        TestHelper.assert_allclose(2)
        TestHelper.assert_allclose(4)
        TestHelper.assert_allclose(21)
        TestHelper.assert_allclose(np.asarray([3, 9, 14]))

    def test_real(self):
        TestHelper.config_test(gamma, scipy.special.gamma)
        TestHelper.assert_allclose(0.1)
        TestHelper.assert_allclose(0.7)
        TestHelper.assert_allclose(1.6)
        TestHelper.assert_allclose(25.8)
        TestHelper.assert_allclose(-0.4)
        TestHelper.assert_allclose(-42.64)
        TestHelper.assert_allclose(np.asarray([0.3, 1.9, -13.2, 21.5]))

    def test_complex(self):
        TestHelper.config_test(gamma, scipy.special.gamma)
        TestHelper.assert_allclose(1j)
        TestHelper.assert_allclose(0.3 + 4.5j)
        TestHelper.assert_allclose(2.4 - 1.2j)
        TestHelper.assert_allclose(9.4 + 21.7j)
        TestHelper.assert_allclose(-0.2 - 3.7j)
        TestHelper.assert_allclose(np.asarray([0.7 - 3.4j, -6.9 + 0.3j, 5.8 - 63.6j]))

    def test_performance(self):
        in_array = np.asarray([0.4 + 0.2j, 3.1 - 2.6j, -1.5 - 0.6j] * 100)
        TestHelper.compare_performance(gamma, scipy.special.gamma, in_array)
