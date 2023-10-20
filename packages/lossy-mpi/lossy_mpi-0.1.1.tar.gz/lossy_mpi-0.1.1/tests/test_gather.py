#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from random import randint
from sys import argv


def check_vec(a, b):
    for x, y in zip(a, b):
        assert x == y


@pytest.mark.mpi(min_size=4)
def test_timeout_gather():
    # from lossy_mpi import getLogger
    from lossy_mpi.pool import Pool, Status
    from mpi4py import MPI

    # logger = getLogger(__name__)

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    root = 0

    pool = Pool(comm, root, timeout=2, n_tries=10)
    pool.advance_transaction_counter(600)
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

        # generate data, and update what we expect the reference mask and data
        # to be: after each iteration we drop the highest Status.READY rank
        n_iter += 1
        mask_ref[-n_iter] = Status.TIMEOUT
        data = rank + n_iter

        all_data = pool.gather(data)
        if rank == root:
            data_ref = [i + n_iter for i in range(size)]
            for i, m in zip(range(size), pool.mask):
                if m != Status.READY:
                    data_ref[i] = None
            check_vec(all_data, data_ref)

        # decreate the local counter => this will be used to decide if a rank
        # is to be dropped from the communicator
        if n_data > 0:
            n_data -= 1

    # Ensure that prior tests don't overlap with the next text
    comm.barrier()


@pytest.mark.mpi(min_size=4)
def test_dropout_gather():
    from lossy_mpi.pool import Pool, Status
    from mpi4py import MPI

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    root = 0

    pool = Pool(comm, root, timeout=2, n_tries=10)
    pool.advance_transaction_counter(200)
    pool.ready()

    # high-numbered ranks will "drop out" first
    n_data = size - rank
    n_iter = 0
    mask_ref = [Status.READY]*size

    while True:
        # simulate graceful failure: if no more work, drop rank from pool
        # decide on current status (i.e. if current rank has data to send)
        if n_data <= 0:
            pool.drop()

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
        mask_ref[-n_iter] = Status.DONE
        data = rank + n_iter

        all_data = pool.gather(data)
        if rank == root:
            data_ref = [i + n_iter for i in range(size)]
            for i, m in zip(range(size), pool.mask):
                if m != Status.READY:
                    data_ref[i] = None
            check_vec(all_data, data_ref)

        # decreate the local counter => this will be used to decide if a rank
        # is to be dropped from the communicator
        if n_data > 0:
            n_data -= 1

    # Ensure that prior tests don't overlap with the next text
    comm.barrier()


if __name__ == "__main__":
    test_dropout_gather()
    test_timeout_gather()
