# PyDebug

This is a simple set of utilities which makes it easier to debug Python objects.
Pydebug respects Django's config. It checks if the decorator is running within a Django
project and `DEBUG` is set to `True`. If it's set to `False`, it simply returns the function.

## Installing

You can install by cloning this repository and running `pip install .` within this directory, or
you can install through Pypi, by running `pip install python-pydebug`.

## Requirements

Although Pydebug uses Python's standard library, it tried to import `Django` to make sure you are not
within a Django project.

| Library       | Defaults |
|---------------|----------|
| Cython        | -        |
| IPDB          | PDB      |
| Line-profiler | -        |

`Line-profiler` requires `Cython` to work, if `IPDB` is not found, it fallsback to Python's standard `PBD` library.

# Usage

### `PDBDebugger`

``` python
from pydebug import PDBDebugger

@PDBDebugger()
def hello_world(a, b):
    x = a + b
    return (a, b)
```

You may tell `PDBdebugger` to drop a `IPDB` shell only when an error occurs

``` python
from pydebug import PDBDebugger

@PDBDebugger(on_error=True)
def hello_world(a, b):
    x = a + b
    return (a, b)
```

### `DisassembleDebug`

You may disassemble a Python function by using the `Disassembledebug` decorator.

``` python
from pydebug import Disassembledebug

@DisassembleDebug()
def hello_world(a, b):
    x = a + b
    return (a, b)
```

### `Profilerdebug`

`Profilerdebug` uses Python's default `cProfile` library.

``` python
from pydebug import ProfilerDebug

@ProfilerDebug()
def hello_world(a, b):
    x = a + b
    return (a, b)
```

### `LineProfilerDebug`

`LineProfilerDebug` requires `line-profile` library to work, which also requires `Cython`.

``` python
from pydebug import LineProfilerDebug

@LineProfilerDebug()
def hello_world(a, b):
    x = a + b
    return (a, b)
```

### `ObjectInfoDebug`

`ObjectInfoDebug` prints the arguments which were passed to the function, the `performace` counter (in minutes), the
`process` time (in minutes) and the returned objects by the function.

``` python
from pydebug import ObjectInfoDebug

@ObjectInfoDebug()
def hello_world(a, b):
    x = a + b
    return (a, b)
```

# TODOs

1. Allow developer to use multiple decorators instead of one decorating the other
2. Show better profile metrics
3. Plot metrics to an image
