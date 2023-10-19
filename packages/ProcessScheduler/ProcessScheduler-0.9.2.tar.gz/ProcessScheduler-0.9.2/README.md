[![Codacy Badge](https://app.codacy.com/project/badge/Grade/7221205f866145bfa4f18c08bd96e71f)](https://www.codacy.com/gh/tpaviot/ProcessScheduler/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=tpaviot/ProcessScheduler&amp;utm_campaign=Badge_Grade)
[![codecov](https://codecov.io/gh/tpaviot/ProcessScheduler/branch/master/graph/badge.svg?token=9HI1FPJUDL)](https://codecov.io/gh/tpaviot/ProcessScheduler)
[![Azure Build Status](https://dev.azure.com/tpaviot/ProcessScheduler/_apis/build/status/tpaviot.ProcessScheduler?branchName=master)](https://dev.azure.com/tpaviot/ProcessScheduler/_build?definitionId=9)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/tpaviot/ProcessScheduler/HEAD?filepath=examples-notebooks)
[![Documentation Status](https://readthedocs.org/projects/processscheduler/badge/?version=latest)](https://processscheduler.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/ProcessScheduler.svg)](https://badge.fury.io/py/ProcessScheduler)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4480745.svg)](https://doi.org/10.5281/zenodo.4480745)
[![slack](https://img.shields.io/badge/slack-ProcessScheduler-brightgreen)](https://join.slack.com/t/processscheduler/shared_invite/zt-pa152rki-126YyMsuLNxhOv_suqKtkQ)

# ProcessScheduler
A python library to compute resource-constrained task schedules. Express your scheduling problem in terms of tasks, resources and constraints, ProcessScheduler computes one/the best schedule that satisfies the requirements.

The computation is based on a set of constraints expressed under the form of first-order logic assertions. Problem solving is performed by the SAT/SMT [Z3 Theorem Prover](https://github.com/Z3Prover/z3).

## Documentation

User-end documentation available at https://processscheduler.readthedocs.io/

## Features

*   tasks: zero duration task, fixed duration task, variable duration task, work amount, optional task,
*   resources: worker, cumulative workers, workers selection, productivity attribute,
*   advanced cost functions,
*   buffer: NonConcurrentBuffer,
*   task constraints: precedence, start synced, end synced, start at, end at, start after, end before,
*   resource constraints: AllSameSelected, AllDifferentSelected,
*   everything can be set as optional (tasks, resources, constraints),
*   first-order-logic operations (not, or, xor, and, implies, if/then/else) between task or resource constraints,
*   builtin and customized indicators (resource utilization, resource cost),
*   single and multiobjective optimization (makespan, flowtime, earliest, latest, resource cost, etc.),
*   exporters: excel, smtlib2.0, json
*   Gantt chart rendering using matplotlib or plotly

## Install

Install with pip.

```bash
pip install ProcessScheduler
```

The Z3 theorem prover is the only required dependency.

Optional dependencies (install either with pip or conda):

*   matplotlib (Gantt chart rendering),
*   plotly (Gantt chart rendering),
*   numpy

## Try online

There are some Jupypter notebooks that can be executed online at [myBinder.org](https://mybinder.org/v2/gh/tpaviot/ProcessScheduler/HEAD?filepath=examples-notebooks)

## Helloworld

```python
import processscheduler as ps
# a simple problem, without horizon (solver will find it)
pb = ps.SchedulingProblem('HelloWorldProcessScheduler')

# add two tasks
task_hello = ps.FixedDurationTask('Process', duration=2)
task_world = ps.FixedDurationTask('Scheduler', duration=2)

# precedence constraint: task_world must be scheduled
# after task_hello
c1 = ps.TaskPrecedence(task_hello, task_world, offset=0)
pb.add_constraint(c1) # explicitly add this constraint to the problem

# solve
solver = ps.SchedulingSolver(pb)
solution = solver.solve()

# display solution, ascii or matplotlib gantt diagram
solution.render_gantt_matplotlib()
```

![png](examples-notebooks/pics/hello_world_gantt.svg)

## Code quality

ProcessScheduler uses the following tools to ensure code quality:

*   unittests,
*   code coverage (coverage.py, codecov.io),
*   continuous-integration at MS azure,
*   static code analysis (codacy),
*   spelling mistakes tracking (codespell),
*   code formatting using the black python formatter

## License/Author

ProcessScheduler is distributed under the terms of the GNU General Public License v3 or (at your option) any later version. It is currently developed and maintained by Thomas Paviot (tpaviot@gmail.com).
