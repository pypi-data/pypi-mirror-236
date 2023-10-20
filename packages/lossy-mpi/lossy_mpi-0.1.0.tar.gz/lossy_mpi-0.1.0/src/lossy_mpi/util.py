#!/usr/bin/env python
# -*- coding: utf-8 -*-

#_______________________________________________________________________________
# Constructors for reduction sink

def zero_constructor(ref):
    import numpy as np

    if isinstance(ref, np.ndarray):
        return np.zeros_like(ref)

    if isinstance(ref, list):
        return list_zero_constructor(ref)

    return 0

def list_zero_constructor(ref):
    return [0]*len(ref)

#-------------------------------------------------------------------------------

#_______________________________________________________________________________
# Generic reduction operators

def reduce_sum(result, data):
    import numpy as np

    f = [d for d in data if d is not None]

    if isinstance(result, np.ndarray):
        return reduce_sum_numpy(result, f)

    if isinstance(result, list):
        return reduce_sum_list(result, f)

    return reduce_sum_scalar(result, f)

def reduce_sub(result, data):
    import numpy as np

    f = [d for d in data if d is not None]

    if isinstance(result, np.ndarray):
        return reduce_sub_numpy(result, f)

    if isinstance(result, list):
        return reduce_sub_list(result, f)

    return reduce_sub_scalar(result, f)

def reduce_mul(result, data):
    import numpy as np

    f = [d for d in data if d is not None]

    if isinstance(result, np.ndarray):
        return reduce_mul_numpy(result, f)

    if isinstance(result, list):
        return reduce_mul_list(result, f)

    return reduce_mul_scalar(result, f)

def reduce_div(result, data):
    import numpy as np

    f = [d for d in data if d is not None]

    if isinstance(result, np.ndarray):
        return reduce_div_numpy(result, f)

    if isinstance(result, list):
        return reduce_div_list(result, f)

    return reduce_div_scalar(result, f)


def reduce_lambda(result, data, op):
    for i, v in enumerate([d for d in data if d is not None]):
        result = op(result, v, i)
    return result


#-------------------------------------------------------------------------------

#_______________________________________________________________________________
# Numpy reduction operators

def reduce_sum_numpy(result, data):
    for d in data:
        assert d.shape == result.shape, f"{d.shape} != {result.shape}"
        result += d
    return result

def reduce_sub_numpy(result, data):
    for d in data:
        assert d.shape == result.shape, f"{d.shape} != {result.shape}"
        result -= d
    return result

def reduce_mul_numpy(result, data):
    for d in data:
        assert d.shape == result.shape, f"{d.shape} != {result.shape}"
        result *= d
    return result

def reduce_div_numpy(result, data):
    for d in data:
        assert d.shape == result.shape, f"{d.shape} != {result.shape}"
        result /= d
    return result

#-------------------------------------------------------------------------------

#_______________________________________________________________________________
# list reduction operators

def reduce_sum_list(result, data):
    for d in data:
        assert len(d) == len(result), f"{len(d)} != {len(result)}"
        for i in range(len(d)):
            result[i] = result[i] + d[i]
    return result

def reduce_sub_list(result, data):
    for d in data:
        assert len(d) == len(result), f"{len(d)} != {len(result)}"
        for i in range(len(d)):
            result[i] = result[i] - d[i]
    return result

def reduce_mul_list(result, data):
    for d in data:
        assert len(d) == len(result), f"{len(d)} != {len(result)}"
        for i in range(len(d)):
            result[i] = result[i] * d[i]
    return result

def reduce_div_list(result, data):
    for d in data:
        assert len(d) == len(result), f"{len(d)} != {len(result)}"
        for i in range(len(d)):
            result[i] = result[i] / d[i]
    return result

#-------------------------------------------------------------------------------

#_______________________________________________________________________________
# scalar reduction operators

def reduce_sum_scalar(result, data):
    for d in data:
        result = result + d
    return result

def reduce_sub_scalar(result, data):
    for d in data:
        result = result - d
    return result

def reduce_mul_scalar(result, data):
    for d in data:
        result = result * d
    return result

def reduce_div_scalar(result, data):
    for d in data:
        result = result / d
    return result

#-------------------------------------------------------------------------------
