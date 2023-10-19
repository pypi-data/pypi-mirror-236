from typing import Any, Dict, List
import numpy as np
from math import *
from lcapy import Circuit

NetlistObject = object

def get_unknonws_from_elements(elements_list: List[str]) -> List[str]:

    elements = [x for x in elements_list if x[0] not in ['W', 'X']]

    unknonws = []

    for element in elements:
        
        if element[0] == 'V':
            unknonws += [f"I{element}"]  
        elif element[0] == 'I':
            unknonws += [f"V{element}"]  
        else:
            unknonws += [f"I{element}", f"V{element}"]  
    
    return unknonws

def generate_equations(schematic: NetlistObject) -> Dict[str, str]: 

    equations = {}

    unknowns = get_unknonws_from_elements(schematic.elements.keys())

    for x in unknowns:
        unknown_type = x[0]
        element = x[1:]
        equations[x] = str(eval(f"schematic.{element}.{unknown_type}.expr['t']"))

    return equations

def evaluate_equations(equations: Dict[str, str], variables: Dict[str, float]) -> Dict[str, float]:

    # assign variables in working memory : 
    for y,x in variables.items():
        equation = f"{y} = {x}"
        eval(compile(equation, filename="equation", mode="exec"))

    # execute equations : 
    for y,x in equations.items():
        equation = f"{y} = {x}"
        eval(compile(equation, filename="equation", mode="exec"))
        variables[y] = eval(y)

    return variables

def solve(task: Dict[str, Any], draw: bool=False) -> Dict[str, float]:

    schematic = Circuit(task["netlist"])

    equations = generate_equations(schematic)
    solutions = evaluate_equations(equations=equations, variables=task["variables"])

    if draw:
        schematic.draw(task["insert_figpaths"][0], style="european")

    return solutions

