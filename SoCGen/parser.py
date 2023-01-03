import yaml
import sys
sys.path.append(".")

from SoCGen.module import *
from SoCGen.interface import *
from SoCGen.parameter import *
from SoCGen.sv_gen import *
from SoCGen.connection import *
from pprint import pprint

def gen_sv():
    # Instance a Top-level Module
    top_mod = BaseTopModule("top_mod", "Top-Level Module Instance")
    
    # Generate an SV file from Top-level Module Instance
    gen_mako_sv(top_mod, "Test")
    
def parse_yaml(file):
    """ Parses a Yaml File and Creates Required Objects """
    # Open the Top-Level Yaml File
    with open(file) as yaml_file:
        # Yaml Read
        data_map = yaml.safe_load(yaml_file)
        pprint(data_map)
        
def yaml_test():
    parse_yaml("Test_Yaml/top_mod.yaml")
    
if __name__ == "__main__":
    yaml_test()