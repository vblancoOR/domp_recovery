from domp_f import *


import numpy as np
import pandas as pd
import sys, getopt, os
import re

def main(argv):

    file="synth_data/"+"instance_n10_m2_s6_d3_o05_1.txt"

    estring = 'python3 domp_main.py -f  <file>\n'
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:f:",["help"])
    except getopt.GetoptError:
        print(estring)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("h", "--help"):
            print(estring)
            sys.exit()
        elif opt=='-f':
            file=arg

    match = re.search(r"m(\d+)", file)
    if match:
        p = int(match.group(1))
        
    ALP=[0, 0.25, 0.5, 0.75, 1]
    METHODS=["sum", "cent", "ksum", "decreasing"]
    RELAX=[True, False]

    results_df = pd.DataFrame()

    for method in METHODS:
        if method=="cent":
            ALP=[0,0.25, 0.5, 0.75, 1]
        elif method=="ksum":
            ALP=[0.25, 0.5, 0.75]
        else:
            ALP=[1]
        for alpha in ALP:
            for relax in RELAX:
                domp_solver = DOMP(file, method, 7200, relax, p, alpha)
                domp_solver.solve_BEP()
                new_row = pd.DataFrame([domp_solver.solution_info])
                # Append result to the main DataFrame
                results_df = pd.concat([results_df, new_row], ignore_index=True)
                new_row.to_csv(
                    f"results/res_{file[11:]}", 
                    mode='a', 
                    header=not os.path.exists(f"results/res_{file[11:]}"), 
                    index=False
                )

if __name__ == "__main__":
    main(sys.argv)
