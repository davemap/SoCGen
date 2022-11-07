import SoCGen.module as module, SoCGen.interface as interface, SoCGen.parameter as parameter
from SoCGen.module import *
from SoCGen.interface import *
from SoCGen.parameter import *
from pprint import pprint
from mako.template import Template

def gen_mako_sv(modinst, file_location):
    moduleTemplate = "module.sv.tpl"
    myTemplate = Template(filename = moduleTemplate)
    lint(modinst)
    mod_file = open(modinst.name+".sv","w")
    mod_file.write(myTemplate.render(modinst = modinst))
    mod_file.close()

def lint(module):
    return 0