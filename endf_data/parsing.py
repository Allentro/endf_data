import json
import os
import numpy as np

def isotope_info(isotope):
    if ')' and '(' in isotope: 
        state = isotope.split('(')[1].split(')')[0]
        if state != 'gs': 
            state = str(int(float(state)))
        isotope = isotope.split('(')[0]
    else: 
        state = 'gs'
    mass = ""
    element = ""
    for d in isotope:
        if d.isdigit():
            mass = mass + d
        else: 
            element = element + d
    return element, mass, state

def decay_dict(isotope):
    def extract_json(element, mass, state): 
        inner_dic = {}
        JSON_PATH = f'{os.path.dirname(__file__)}/decay_data/{element}.json'
        with open(JSON_PATH) as json_file:
            data = json.load(json_file)[mass][state]
            if data['nucleus']['stability'] == 'non-stable':
                dic = {}
                decays = data['decay_data']['decays'].keys()
                for product in decays: 
                    if product == 'fission': 
                        inner_dic[product] = 'fission'
                    else:
                        half_life = data['decay_data']['decays'][product]['half_life']
                        branching = data['decay_data']['decays'][product]['Branching_factor']
                        rad_type = data['decay_data']['decays'][product]['radiation_type']
                        de, dm, ds = isotope_info(product)
                        inner_dic[product] = {'half_life':half_life,
                                             'branching':branching, 
                                             'decays': extract_json(de, dm, ds), 
                                             'rad_type':rad_type}
                #print(decays)
                return inner_dic
            else: 
                return 'Stable'
    element, mass, state = isotope_info(isotope)
    dic = {} 
    decay_dict = extract_json(element, mass, state)
    JSON_PATH = f'{os.path.dirname(__file__)}/decay_data/{element}.json'
    with open(JSON_PATH) as json_file:
        data = json.load(json_file)[mass][state]
    half_life = data['decay_data']['half_life']
    dic[f'{mass}{element}({state})'] =  {'half_life':half_life, 
                                         'branching':1,
                                        'decays':decay_dict, 
                                        'rad_type':None}
    
    extract_json(element, mass, state)
    return dic