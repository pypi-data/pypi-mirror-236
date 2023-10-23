import multiprocessing
import typing

A = typing.TypeVar("A")


def run(fun: typing.Callable[[A], typing.Any], arg_lst: list[A], *, max_concurrency: int):
    semaphore = multiprocessing.Semaphore(max_concurrency)

    def _target(arg: A):
        with semaphore:
            fun(arg)

    all_processes: list[multiprocessing.Process] = []

    for arg in arg_lst:
        all_processes.append(multiprocessing.Process(target=_target, args=(arg,)))
        all_processes[-1].start()

    for proc in all_processes:
        proc.join()
