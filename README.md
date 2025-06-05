# domp_recovery
DOMP Recovery models

- domp_f.py is the file with the required models
- domp_main.py is the main source file. One can solve the model by:
    
## Loading data and parameters from a file:

domp_solver = DOMP(file, method, time_limit, relax, p, alpha)

where:

    - file: file of data, each row represent the coordinates of an observation.
    - method: "sum", "cent", "ksum", "decreasing". 
    - alpha: for "cent", is the parameter alpha, for "ksum", alpha represent the percent of first observations that are accounted.
    - p: number of clusters to be computed.
    - time_limit: time_limit for solving the model
    - relax: True if the LP is solved, False if the IP.

## Solve the model

    domp_solver.solve_BEP()


## Extract Results:
    
    domp_solver.solution_info

## Example

    

```python

    from domp_f import *


    file = "synth_data/synth_data/instance_n10_m2_s0_d2_o00_0.txt"
    method = "cent"
    alpha=0.5
    p=2
    time_limit=3600
    relax=False

    domp_solver = DOMP(file, method, time_limit, relax, p, alpha)
    domp_solver.solve_BEP()
    domp_solver.solution_info
````

**Example Output:**



