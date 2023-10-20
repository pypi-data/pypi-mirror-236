#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randint
from sys import argv


def run_cli():
    from lossy_mpi.pool import Pool, Status
    from mpi4py import MPI

    verbose = False
    if len(argv) > 1:
        if argv[1].strip() == "verbose":
            verbose = True

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    root = 0

    pool = Pool(comm, root, timeout=2, n_tries=10)
    pool.ready()

    n_data = randint(1, 10)

    while True:
        # simulate graceful failure: if no more work, drop rank from pool
        # decide on current status (i.e. if current rank has data to send)
        if n_data <= 0:
            pool.drop()

        # update mask -- this is not necessary, but it does speeding things up
        pool.sync_mask()

        # decide to break (root checks if all done) + root: print mask
        if rank == root:
            if verbose:
                print(pool.mask, flush=True)

            if pool.done:
                break
        else:
            # if done, break out of loop
            if pool.status is Status.DONE:
                break

        # Update what we expect the reference mask to be: after each iteration
        # we drop a random Status.READY rank
        if n_data > 0:
            n_data -= 1

        print(f"{rank=} is at the barrier", flush=True)
        pool.barrier()

    print(f"{rank=} has left the loop", flush=True)
    last_n_data = comm.gather(n_data, root=root)

    if rank == root:
        print(f"{last_n_data=}")

    comm.barrier()


if __name__ == "__main__":
    run_cli()
