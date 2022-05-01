import numpy as np 

param1 = {
    "param_name": "rho", 
    "min": 5,
    "max": 10, 
    "parts": 10
}

param2 = {
    "param_name": "theta", 
    "min": 4,
    "max": 5, 
    "parts": 10
}


params = [param1, param2]

matrix = list( np.array_split(
                        range(params[0]['min'],params[0]['max']), 
                        params[0]['parts'] ))
min = params[0]['min']
max = params[0]['max']
parts =  params[0]['parts']
print(list(np.linspace(min,max, parts)))