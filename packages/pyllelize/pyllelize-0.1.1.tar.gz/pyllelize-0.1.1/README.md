# Pyllelize

Easily parallelize your Python functions with `pyllelize`. Whether you're dealing with CPU-bound tasks or I/O-bound asynchronous functions, `pyllelize` offers a simple interface to distribute your workload efficiently.

## Key Features

- **Thread-based Parallelization**: Distribute CPU-bound tasks across multiple threads with ease.
  
- **Process-based Parallelization**: Harness the full power of multi-core processors by distributing tasks across separate processes, bypassing Python's Global Interpreter Lock.
  
- **Asynchronous Execution**: Seamlessly parallelize I/O-bound asynchronous tasks.
  
- **Error Handling**: Safely capture and report errors without halting the execution of other tasks.

## Installation

```bash
pip install pyllelize
```

## Quick Start

### Thread-based Execution

```python
from pyllelize import parallel_execute_threads

def multiply(a, b):
    return a * b

arguments = [(1, 2), (3, 4), (5, 6)]
results = parallel_execute_threads(multiply, arguments)
print(results)  # Possible output: [2, 12, 30]
```

### Process-based Execution

```python
from pyllelize import parallel_execute_processes

def add(a, b):
    return a + b

arguments = [(1, 2), (3, 4), (5, 6)]
results = parallel_execute_processes(add, arguments)
print(results)  # Possible output: [3, 7, 11]
```

### Asynchronous Execution

```python
import asyncio
from pyllelize import parallel_execute_threads_async

async def fetch_data(a, b):
    await asyncio.sleep(1)  # Simulating async I/O operation
    return a + b

arguments = [(1, 2), (3, 4), (5, 6)]
results = parallel_execute_threads_async(fetch_data, arguments)
print(results)  # Possible output after 1 second: [3, 7, 11]
```

## License

This project is licensed under the [MIT License](link-to-license-file).
