Implements a collection of `scipy.special` functions with support for complex arguments during the Numba `nopython`
mode.

# Functions

| Function Name |                                                          scipy                                                           |  
|:--------------|:------------------------------------------------------------------------------------------------------------------------:|
| gamma         | [scipy.special.gamma](https://docs.scipy.org/doc/scipy/reference/generated/scipy.special.gamma.html#scipy.special.gamma) |

# Performance

Scipy is already optimized well, so using Numba likely will not improve the speed of the mathematical function in itself
and these implementations might even be less optimized. The advantage of these function comes from allowing much larger
blocks of `nopython` mode, which can profit much better from parallelization.

Consider the following example:

```python
from numba import njit, prange


@njit(parallel=True)
def prange_test(A):
    s = 0
    for i in prange(A.shape[0]):
        s += my_func(A[i])
    return s
```

The function `prange_test` contains a `prange` loop that may be parallelized with Numba. However, if it contains
functions that are not supported by Numba, this is no longer possible. As a result, having a Numba compatible `my_func`
function can be benefitial, even if it may be slower than an equivalent function from an existing library.