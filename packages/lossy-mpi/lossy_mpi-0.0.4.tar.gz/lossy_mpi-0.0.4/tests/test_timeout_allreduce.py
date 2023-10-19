#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import numpy


def check_vec(a, b):
    for x, y in zip(a, b):
        if isinstance(x, numpy.ndarray):
            assert numpy.array_equal(x, y)
        else:
            assert x == y
 

def reduce_sum(result, data):
    f = [d for d in data if d is not None]
    for d in f:
        assert d.shape == result.shape
        result += d


@pytest.mark.mpi(min_size=4)
def test_timeout_allreduce():
    from lossy_mpi.pool import Pool, Status
    from lossy_mpi.util import reduce_sum, zero_constructor
    from mpi4py import MPI

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    root = 0

    pool = Pool(comm, root, timeout=2, n_tries=10)
    pool.advance_transaction_counter(400)
    pool.ready()

    # high-numbered ranks will "drop out" first
    n_data = size - rank
    n_iter = 0
    mask_ref = [Status.READY]*size

    while True:
        # simulate unexpected failure: if no more work, then stop responding
        # decide on current status (i.e. if current rank has data to send)
        # assume that rank 0 does not fail
        if n_data <= 0 and rank != root:
            break

        # update mask -- this is not necessary, but it does speeding things up
        pool.sync_mask()

        # decide to break (root checks if all done) + root: print mask
        if rank == root:
            check_vec(pool.mask, mask_ref)

            if pool.done:
                break
        else:
            # if done, break out of loop
            if pool.status is Status.DONE:
                break

        # generate data, and update what we expect the reference mask and data
        # to be: after each iteration we drop the highest Status.READY rank
        n_iter += 1

        # mask reference
        mask_ref[-n_iter] = Status.TIMEOUT

        # data reference
        data_ref = [numpy.zeros(10) + i + n_iter for i in range(size)]
        for i, m in zip(range(size), pool.mask):
            if m != Status.READY:
                data_ref[i] = None

        # sum of data reference
        sum_ref = sum([d for d in data_ref if d is not None])

        data = numpy.zeros(10) + rank + n_iter
        # allreduce!
        # all_data = pool.gather(data)
        # if rank == root:
        #     reduced = numpy.zeros_like(data)
        #     reduce_sum(reduced, all_data)
        # else:
        #     reduced = None
        # reduced = pool.bcast(reduced)
        reduced = pool.allreduce(data, zero_constructor, reduce_sum)

        if rank == root:
            check_vec(reduced, sum_ref)

        # decreate the local counter => this will be used to decide if a rank
        # is to be dropped from the communicator
        if n_data > 0:
            n_data -= 1

    # Ensure that prior tests don't overlap with the next text
    comm.barrier()

if __name__ == "__main__":
    test_timeout_allreduce()
