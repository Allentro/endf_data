import argparse
import numpy as np
from . import parsing
from . import printing

def main():
  
    parser = argparse.ArgumentParser(prog ='endf_data',
                                     description ='ENDF Nucleus and Decay data package.')
  
    parser.add_argument('isotope', type = str, help ='Isotope of interest.')
    
    parser.add_argument('-data', default = True, type =bool, 
                    dest ='data', help ="Output of nucleus and decay data.")
        
    parser.add_argument('-chain', default = True, type =argparse.FileType('w', encoding='latin-1'), 
                        dest ='chain', help ="Calculate full decay chain.")
    
    parser.add_argument('-max_hl', default = np.inf, type =float, dest ='max_hl', 
                        help ="Maximum half-life cutoff before treating istope as stable in the decay chain.")
    
    parser.add_argument('-min_branch', default = 0, type =float, 
                        dest ='min_branch', help ="Minimum branching ratio to include in the decay chain.")
    
    parser.add_argument('-plot', type=bool, dest ='plot', default = True,
                        help ='Plot decay chain')
    
    parser.add_argument('-save',type=bool, dest='save', default = False, 
                        help='Directory to save data.')
  
    args = parser.parse_args()
    printing.initial_print() 
    if args.data == True: 
        printing.nuclear_data(args.isotope)
    if args.chain == True: 
        if args.plot == True:
            dic = parsing.decay_dict(args.isotope)
            printing.printing_decay_data(dic, args.max_hl, args.min_branch)
        