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

## Solve the model

    domp_solver.solve_BEP()


## Extract Results:
    
    domp_solver.solution_info])
