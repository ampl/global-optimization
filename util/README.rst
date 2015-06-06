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

  - model: /tmp/tmpkOJSRH/01-01-10.mod
    sha: 5aad7f30608601641bc2869a07dc5b8315584e5f
    solver: minos
    start: 2015-06-03 14:58:43.972498
    time: 0.0059061050415
    timeout: False
    obj: 0.0157685012892
    solve_result: solved
    solve_message: |
      MINOS 5.51: optimal solution found.
      11 iterations, objective 0.015768501289210177
      Nonlin evals: obj = 39, grad = 38.
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
