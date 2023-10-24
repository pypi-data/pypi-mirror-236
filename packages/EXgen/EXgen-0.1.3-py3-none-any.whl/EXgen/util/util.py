import numpy as np
from typing import Dict, Any

# command generator functions : 
latex_command_win = lambda filename: f"pdflatex {filename}"
latex_command_unix = lambda filename, logfile: f"pdflatex {filename} > {logfile}"

# variable initialization utilities : 
def init_var(var_def: Dict[str, Any], precision: int=4) -> np.ndarray[np.float64]:

    dim = var_def.get("dim", 1)

    if var_def["dist"] == "uniform":
        val = np.random.rand(dim)*(var_def["max"]-var_def["min"]) + var_def["min"]
    elif var_def["dist"] == "normal": #! Implement with mean and std
        val = np.random.randn(dim)*(var_def["max"]-var_def["min"]) + var_def["min"]
    elif var_def["dist"] == "exact":
        val = np.array([var_def["val"]])

    if "round" in var_def.keys() and var_def["round"]:
        val = np.round(val, precision)

    if dim == 1:
        val = val[0]

    return val

def init_var_vals(var_defs: Dict[str,Dict[str, int]], precision: int=4) -> Dict[str, float]:
    var_vals = {}
    for var in var_defs.keys():
        
        nelems = var_defs[var].get("nelems", 1)

        if nelems == 1:
            val = init_var(var_defs[var], precision)
            var_vals[var] = val
        else:
            for ind in range(nelems):
                varname = f"{var}{ind+1}"
                val = init_var(var_defs[var], precision)
                var_vals[varname] = val
                
    return var_vals