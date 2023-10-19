#!/usr/bin/env python
# -*- coding: utf-8 -*-

def zero_constructor(ref):
    import numpy as np

    if isinstance(ref, np.ndarray):
        return np.zeros_like(ref)

    return list_zero_constructor(ref)


def list_zero_constructor(ref):
    return [0]*len(ref)


def reduce_sum(result, data):
    f = [d for d in data if d is not None]
    for d in f:
        assert d.shape == result.shape, f"{d.shape} != {result.shape}"
        result += d


def reduce_sub(result, data):
    f = [d for d in data if d is not None]
    for d in f:
        assert d.shape == result.shape, f"{d.shape} != {result.shape}"
        result -= d


def reduce_mul(result, data):
    f = [d for d in data if d is not None]
    for d in f:
        assert d.shape == result.shape, f"{d.shape} != {result.shape}"
        result *= d


def reduce_div(result, data):
    f = [d for d in data if d is not None]
    for d in f:
        assert d.shape == result.shape, f"{d.shape} != {result.shape}"
        result *= d
