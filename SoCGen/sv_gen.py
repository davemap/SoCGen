from SoCGen.module import *
from SoCGen.interface import *
from SoCGen.parameter import *
from pprint import pprint
from mako.template import Template
import os

def gen_mako_sv(modinst, file_location):
    for template in modinst.templates:
        myTemplate = Template(filename = template)
        lint(modinst)
        mod_file = open(file_location+"/"+modinst.name+get_tpl_type(template),"w")
        mod_file.write(myTemplate.render(modinst = modinst))
        mod_file.close()

def get_tpl_type(path):
    """ Strips Template Extension from filename and returns template 
        extension type """
    return os.path.splitext(os.path.splitext(path)[0])[1]
    
def lint(module):
    return 0