from . import parsing 
import numpy as np
import os
import json 

def initial_print(): 
    print('  ______ _   _ _____  ______   _____        _        ')
    print(' |  ____| \ | |  __ \|  ____| |  __ \      | |       ')
    print(' | |__  |  \| | |  | | |__    | |  | | __ _| |_ __ _ ')
    print(' |  __| | . ` | |  | |  __|   | |  | |/ _` | __/ _` |')
    print(' | |____| |\  | |__| | |      | |__| | (_| | || (_| |')
    print(' |______|_| \_|_____/|_|      |_____/ \__,_|\__\__,_|')

def print_branch(dic):
    branch = round(100*float(dic['branching']),4)
    return f'{branch}%'

def nuclear_hl(hl, dhl=None):
    def convert_error(value, error):
        decimals = 0
        while value != int(value):
            value *= 10
            decimals += 1
        return error / 10**decimals
    
    mul = [1,'s']
    if hl > 31557600: 
        mul_unit = [31557600, 'y']
    elif hl > 86400:
        mul = [86400, 'd']
    elif hl >3600: 
        mul = [3600, 'h']
    elif hl >60:
        mul = [60, 'm']
    elif hl <1e-3:
        mul = [1e-3, 'ms']
    elif hl <1e-6:
        mul = [1e-6, 'us']
    elif hl <1e-9:
        mul = [1e-9, 'ns']
    elif hl <1e-12:
        mul = [1e-12, 'ps']
    if dhl == None: 
        return f'{round(hl/mul[0],2)} {mul[1]}'
    else: 
        return f'({round(hl/mul[0],3)}+/-{round(dhl/mul[0],3)}) {mul[1]}'

def print_radtype(dic):
    rtyp = dic['rad_type']
    decay = {0:'\u03B3',
         1:'\u03B2-', 
         2:'\u03B2+',
         3:'IT',
         4:'\u03B1', 
         5:'n', 
         6:'SF', 
         7:'p', 
         8:'e-',
         9:'X-rays', 
         10:'Unknown'}
    return decay[rtyp]

def printing_decay_data(dic, max_time=np.inf, min_branch=0): 
    def run_dic_inner(inner_dic, parent,max_time, min_branch, counter=0): 
        mul = 10
        if isinstance(inner_dic, dict):
            for key in inner_dic.keys():
                if isinstance(inner_dic[key], dict): 
                    #print(inner_dic[key])
                    if inner_dic[key]['branching'] < min_branch: 
                        continue
                    elif inner_dic[key]['decays'] == 'Stable':# or inner_dic[key]['half_life'] > max_time:
                        if key != parent:
                            print(' '*((counter-1)*mul) +'|')
                            print(' '*((counter-1)*mul) + f'{print_radtype(inner_dic[key])}')
                            print(' '*((counter-1)*mul) +'|')
                            print(' '*((counter-1)*mul) +f'---{print_branch(inner_dic[key])}----> ' +f'{key}   [stable]')
                        else: 
                            print(f'{key}  [stable]')
                        counter -= 1
                    else: 
                        if key != parent:
                            print(' '*((counter-1)*mul) +'|')
                            print(' '*((counter-1)*mul) +f'{print_radtype(inner_dic[key])}')
                            print(' '*((counter-1)*mul) +'|')
                            print(' '*((counter-1)*mul) +f"---{print_branch(inner_dic[key])}----> " +f"{key}  [{nuclear_hl(inner_dic[key]['half_life'])}]")
                        else: 
                            print(f"{key}   [{nuclear_hl(inner_dic[key]['half_life'])}]")
                        counter += 1
                        counter = run_dic_inner(inner_dic[key]['decays'], parent,max_time,min_branch, counter)
        return counter

    counter = 0
    print('')
    print('----------------------DECAY CHAIN ------------------------')
    print('')
    parent = next(iter(dic))
    counter = run_dic_inner(dic, parent,max_time, min_branch, counter)
    print('')
    print('-----------------------------------------------------------')
    return
                                                     
def nuclear_data(isotope): 
    print('')
    print('----------------------NUCLEAR DATA------------------------')
    print('')
    element, mass, state = parsing.isotope_info(isotope)
    JSON_PATH = f'{os.path.dirname(__file__)}/decay_data/{element}.json'
    with open(JSON_PATH) as json_file:
        data = json.load(json_file)[mass][state]
        spin = float.as_integer_ratio(data['nucleus']['spin'])
        if spin[1] == 1: 
            spin = spin[0] 
        else: 
            spin = f'{spin[0]}/{spin[1]}'
        parity = data['nucleus']['parity']
        print(f'J\u03C0 = {spin}{parity}')
        if data['nucleus']['stability'] == 'stable': 
            print('Stable nucleus')
        else: 
            print(f"Half life = {nuclear_hl(data['decay_data']['half_life'], data['decay_data']['Error(half_life)'])}")
            print('Direct daughter(s):')
            for decay in data['decay_data']['decays']: 
                inner_data = data['decay_data']['decays'][decay]
                print(f'    ---------{decay}------------')
                print(f"    Branching = ({round(inner_data['Branching_factor']*100)}\u00B1{round(inner_data['Error(Branching_factor)']*100)})%")
                print(f"    Q-value   = ({round(inner_data['Q-value'])}\u00B1{round(inner_data['Error(Q-value)'])})keV")
                print(f"    Half-life = {round(inner_data['half_life'])}")
                print('')
    return