Benchmarking
============

Benchmarking consists of two steps:

1. The run step where each input model is processed with AMPL to generate
   a problem instance which is then sent to a solver. Solver runtime is
   measured and written to the log together with solver output, final
   objective value and other information.

2. The formatting step where logs obtained in the previous step are formatted
   for presentation.

The reason for such arrangement is that the run step can be very time
consuming so it is beneficial to do it separately. Once solution logs are
obtained the formatting can be done multiple times, possibly with different
settings and on another machine.

The time to process AMPL model and data is not included in the reported
solution time, but the time it took solver to read a problem instance is.

Each benchmark is described by a Python module that specifies

* inputs - collection of AMPL models
* timeout - solver timeout in seconds
* configs - benchmark configurations with solver names and options

Input models can be either taken from the repository or generated
automatically.

Example of a Python benchmark module:

.. code:: python

  import couenne, lgo
  from util import Config, load_index

  inputs = load_index('casado', 'hansen')

  # Timeout in seconds
  timeout = 60

  configs = [
    Config('minos'),
    Config('baron'),
    Config('couenne', couenne.options()),
    Config('lgo', {'opmode': lgo.LOCAL_SEARCH_MODE}, suffix='local-search'),
    Config('lgo', {'opmode': lgo.MULTISTART_MODE}, suffix='multistart')
  ]

The `load_index` method returns the list of all models from the
[casado](https://github.com/ampl/global-optimization/tree/master/casado)
and [hansen](https://github.com/ampl/global-optimization/tree/master/hansen)
collections.

Note that the `lgo` solver is included in two configurations.
The `suffix` argument specifies a suffix to be added to the log name.

Running benchmarks
------------------



