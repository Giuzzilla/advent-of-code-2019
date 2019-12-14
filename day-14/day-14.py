#https://adventofcode.com/2019/day/14
import math
import re

def clean_input(path = "./input.txt"):
    input_f = open(path).readlines()
    arr = [re.split(" => |, ",line.strip()) for line in input_f]
    production = dict()

    for formula in arr:
        requirements_dict = dict()
        for item in formula[:-1]:
            quantity, name = item.split(" ")
            requirements_dict[name] = int(quantity)

        tpl = tuple(formula[-1].split(" "))
        produce_qnt = int(tpl[0])
        produce_name = tpl[1]
        production[produce_name] = [produce_qnt, requirements_dict]

    set_of_materials = set()

    for l in arr:
        for item in l:
            set_of_materials.add(item.split(" ")[1])

    return production, set_of_materials

def check(available, to_produce):
    if to_produce['FUEL'] > 1:
        return True
    
    for key in to_produce:
        if key != 'ORE' and to_produce[key] != 0:
            return True
    return False


def check2(available):
    if available['ORE'] > 0:
        return True
    return False

def inner_loop(available, to_produce, production):
    while check(available, to_produce):
        for name in to_produce.keys():
            qnt = max(to_produce[name] - available[name], 0)
            available[name] = max(available[name] - to_produce[name], 0)
            if qnt == 0:
                to_produce[name] = 0
                continue
            
            if name == 'ORE':
                continue

            producable_qnt = production[name][0]        
            to_produce[name] = 0
            multiplier = math.ceil(float(qnt) / producable_qnt)
            available[name] += multiplier * producable_qnt - qnt
            
            for key in production[name][1]:
                to_produce[key] += multiplier*production[name][1][key]
    
    return available, to_produce

def first_star(production, set_of_materials):
    initial_ore = 1000000000000
    to_produce = dict()
    available = dict()

    for material in set_of_materials:
        to_produce[material] = 0
        available[material] = 0

    to_produce['FUEL'] = 1
    available['ORE'] = initial_ore 

    available, _ = inner_loop(available, to_produce, production)
    
    return initial_ore - available['ORE']

def second_star(production, set_of_materials): # Bruteforce
    i = 0
    initial_ore = 1000000000000
    to_produce = dict()
    available = dict()
    for material in set_of_materials:
        to_produce[material] = 0
        available[material] = 0
    available['ORE'] = initial_ore 

    while check2(available):
        to_produce['FUEL'] = 1
        available, to_produce = inner_loop(available, to_produce, production)
        i += 1

    return i - 1  # Exclude last iteration with negative Ore

if __name__ == "__main__":
    production, set_of_materials = clean_input()

    print(f"First star answer: {str(first_star(production, set_of_materials))}")
    print(f"Second star answer: {str(second_star(production, set_of_materials))}")

