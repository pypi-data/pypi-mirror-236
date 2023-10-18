import concurrent.futures
from typing import Callable, List, Any, Tuple


def parallel_execute_processes(
    function: Callable[..., Any], arguments: List[Tuple], process_count: int = 4
) -> List[Any]:
    """
    Executes the given function in parallel using multiple processes.

    This function distributes the work across multiple processes and collects
    the results in the order they finish.

    Parameters:
    - function (Callable[..., Any]):
        The function to be executed. It should accept as many arguments as there
        are elements in each tuple of the 'arguments' list.

    - arguments (List[Tuple]):
        A list of tuples, where each tuple contains the arguments for the 'function'.
        Example:
        If the function is defined as `def foo(a, b, c)`,
        the arguments list should be like [(a1, b1, c1), (a2, b2, c2), ...].

    - process_count (int, optional):
        The number of processes to use for parallel execution.
        Default is 4.

    Returns:
    - List[Any]:
        A list of results from each execution of 'function'. The results are
        returned in the order they finish, which may not necessarily be the
        same order as in the 'arguments' list.

    Example:
        def add(a, b):
            return a + b

        arguments = [(1, 2), (3, 4), (5, 6)]
        results = parallel_execute_processes(add, arguments)
        print(results)  # Possible output: [3, 7, 11]
    """

    with concurrent.futures.ProcessPoolExecutor(max_workers=process_count) as executor:
        futures = {executor.submit(function, *args): args for args in arguments}

        results = []
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
        return results
