import sys
sys.path.append(".")

from SoCGen.module import *
from SoCGen.interface import *
from SoCGen.parameter import *
from SoCGen.sv_gen import *
from SoCGen.connection import *
from pprint import pprint

def test():
    # Create Base Interface Classes which can be instanced in multiple Modules
    BaseClkIf = createBaseInterface("clk_if", interface_type = InterfaceType.LOGIC, bit_width = 3)
    BaseRstIf = createBaseInterface("rst_if", interface_type = InterfaceType.LOGIC, bit_width = 1)
    BaseWireIf = createBaseInterface("wire_if", interface_type = InterfaceType.LOGIC, bit_width = 1)
    BaseApbIf = createBaseInterface("apb_if", interface_type = InterfaceType.SVINTERFACE, modports = ["master", "slave"])
    
    # Create Interface Instances
    clk_inst = BaseClkIf("clk", "Clock Input")
    rst_inst = BaseRstIf("rst", "Reset Input")
    apb_inst = BaseApbIf("apb", "Apb Interface")
    apb2_inst = BaseApbIf("apb2", "Apb Interface")
    wire_a_inst = BaseWireIf("a", "Wire a")
    wire_b_inst = BaseWireIf("b", "Wire b")
    wire_c_inst = BaseWireIf("c", "Wire c")
    
    # Create a Sub Module Class which can be instanced by the Top-Level Module
    BaseAModule = createBaseModule("a_module",
        interfaces = [
            clk_inst, rst_inst
        ],
        connections = [
            Connection([(clk_inst,)], ConnectPort.INPUT),
            Connection([(rst_inst,)], ConnectPort.INPUT)
        ]
    )
    
    # Create Sub-Module Instances
    a_mod_inst = BaseAModule("a_mod", "Sub-Module A Instance")
    ab_mod_inst = BaseAModule("ab_mod", "Sub-Module AB Instance")

    # Create a Base Top Module Class which can be instanced to generate an SV file
    BaseTopModule = createBaseModule("top_module",
        interfaces = [
            clk_inst, rst_inst, apb_inst, apb2_inst,
            wire_a_inst, wire_b_inst, wire_c_inst
        ],
        sub_modules = [
            a_mod_inst,
            ab_mod_inst
        ],
        connections = [
            Connection([(clk_inst,)], ConnectPort.INPUT),
            Connection([(clk_inst,(2,2)),(clk_inst,(1,0))], clk_inst, sub_module = a_mod_inst),
            Connection([(rst_inst,)], ConnectPort.INPUT),
            Connection([(apb_inst,"slave")], ConnectPort.SV_IF)
        ]
    )
    
    # Instance a Top-level Module
    top_mod = BaseTopModule("top_mod", "Top-Level Module Instance")
    
    # Generate an SV file from Top-level Module Instance
    gen_mako_sv(top_mod, "Test")

if __name__ == "__main__":
    test()