Benchmarking
============

Benchmarking consists of two steps:

1. The run step where each input model is processed with AMPL_ to generate
   a problem instance which is then sent to a solver. Solver runtime is
   measured and written to the log together with solver output, final
   objective value and other information.

2. The formatting step where logs obtained in the previous step are formatted
   for presentation.

.. _AMPL: http://www.ampl.com/
   
The reason for such arrangement is that the run step can be very time
consuming so it is beneficial to do it separately. Once solution logs are
obtained formatting can be done multiple times, possibly with different
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

The ``load_index`` method returns the list of all models from the casado_
and hansen_ collections.

.. _casado: https://github.com/ampl/global-optimization/tree/master/casado
.. _hansen: https://github.com/ampl/global-optimization/tree/master/hansen

Note that the ``lgo`` solver is included in two configurations.
The ``suffix`` argument specifies a suffix to be added to the log name.

Requirements
------------

The benchmark script is written in Python and uses the following modules:

* `PyYAML <http://pyyaml.org/>`_: YAML implementations for Python
* `Pandas <http://pandas.pydata.org/>`_: Python Data Analysis Library

Running benchmarks
------------------

Command: ``benchmark run <path>``

where ``<path>`` is a path to the Python benchmark module. Example:

.. code::

  benchmark run montreal2015/casado-hansen.py

This will run the ``casado-hansen`` benchmark and write log files such as
``casado-hansen-minos.yaml``, one for each configuration. Logs are written in
the YAML_ format and here is a sample log entry:

.. code:: yaml

  - model: casado/casado01.mod
    sha: d83bc5f2a89421d937b9d2ea8f9053d822231d4d
    solver: minos
    start: 2015-06-05 17:53:01.772361
    time: 0.00385594367981
    timeout: False
    obj: -0.99113461363
    solve_result: solved
    solve_message: |
      MINOS 5.51: optimal solution found.
      3 iterations, objective -0.9911346136299205
      Nonlin evals: obj = 9, grad = 8.
    output: |
      MINOS 5.51: 

.. _YAML: http://yaml.org/

Formatting results
------------------

Command: ``benchmark format <path>``

where ``<path>`` is a path to the Python benchmark module. The current directory
should contain log files generated during the run step.

Example:

.. code::

  benchmark format montreal2015/casado-hansen.py

This will read log files, process them and write the formatted results to text
files such as ``casado-hansen-minos.txt``, one for each log file.
