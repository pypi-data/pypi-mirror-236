import asyncio
import concurrent.futures
from typing import Callable, List, Any, Tuple


def parallel_execute_threads(
    function: Callable[..., Any], arguments: List[Tuple], thread_count: int = 4
) -> List[Any]:
    """
    Executes the given function in parallel using multiple threads.

    This function distributes the work across multiple threads and collects
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

    - thread_count (int, optional):
        The number of threads to use for parallel execution.
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
        results = parallel_execute(add, arguments)
        print(results)  # Possible output: [3, 7, 11]
    """

    with concurrent.futures.ThreadPoolExecutor(max_workers=thread_count) as executor:
        futures = {executor.submit(function, *args): args for args in arguments}

        results = []
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
        return results


def run_async_fn(loop: asyncio.AbstractEventLoop, coro) -> Any:
    """
    Runs a coroutine in the provided event loop and returns the result.

    Parameters:
    - loop (asyncio.AbstractEventLoop): The event loop in which the coroutine is to be executed.
    - coro: The coroutine to be executed.

    Returns:
    - Any: Result of the executed coroutine.
    """
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)


def parallel_execute_threads_async(
    function: Callable[..., Any], arguments: List[Tuple], thread_count: int = 4
) -> List[Any]:
    """
    Executes asynchronous coroutine functions in parallel using multiple threads.

    This function distributes the coroutine execution across multiple threads.

    Parameters:
    - function (Callable[..., Any]):
        The coroutine function to be executed. It should accept as many arguments as there
        are elements in each tuple of the 'arguments' list.

    - arguments (List[Tuple]):
        A list of tuples, where each tuple contains the arguments for the 'function'.
        Example:
        If the function is defined as `async def foo(a, b, c)`,
        the arguments list should be like [(a1, b1, c1), (a2, b2, c2), ...].

    - thread_count (int, optional):
        The number of threads to use for parallel execution.
        Default is 4.

    Returns:
    - List[Any]:
        A list of results from each execution of 'function'. The results are
        returned in the order they finish.

    Raises:
    - ValueError: If the provided function is not a coroutine function.

    Example:
        async def fetch_data(a, b):
            await asyncio.sleep(1)
            return a + b

        arguments = [(1, 2), (3, 4), (5, 6)]
        results = parallel_execute_threads_async(fetch_data, arguments)
        print(results)  # Possible output: [3, 7, 11]
    """

    with concurrent.futures.ThreadPoolExecutor(max_workers=thread_count) as executor:
        futures = []
        for args in arguments:
            if asyncio.iscoroutinefunction(function):
                new_loop = asyncio.new_event_loop()
                futures.append(executor.submit(run_async_fn, new_loop, function(*args)))
            else:
                raise ValueError("Provided function is not a coroutine function")

        return [future.result() for future in concurrent.futures.as_completed(futures)]
