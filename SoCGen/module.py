from SoCGen.connection import ConnectPort
from enum import Enum, auto

class ModuleType(Enum):
    """ 
    Enumerated Type for Type of Module a Design-file is
    """
    DEVICE  = auto()
    WRAPPER = auto()
    REGBANK = auto()
    BUS     = auto()
    
def ModuleInit(self, name, description):
    """ 
    Module Constructor Function
    """
    self.name         = name
    self.description  = description

class Module:
    """ 
    - Module Base Class. Dervied classes are generated on the fly and 
    inherit from this base class. 

    - Each Yaml Module File Creates its own class and is then instanced 
    by other Classes. This allows for Modules to contain multiple of the
    same sub-modules, each with different parameters, names and descriptions
    if they are overloaded. 
    """
    name               = "name"
    description        = ""
    module_description = ""
    module_type        = ModuleType.DEVICE
    size               = 0x0
    parameters         = []
    include_files      = []
    templates          = []
    sub_modules        = []
    interfaces         = []
    connections        = []
    
    def __init__(self, name):
        ModuleInit(self, name)
    
    @property
    def ports(self):
        """ List of All Ports """
        port_connections = [connection.interfaces for connection in self.connections if connection.connect.__class__ == ConnectPort]
        return [interface[0][0] for interface in port_connections if interface[0][0] in self.interfaces]
        
    @property
    def internals(self):
        """ List of Internal Logic Instances """
        return [interface for interface in self.interfaces if interface not in self.ports]
    
    @property
    def input_ports(self):
        """ List of Input Ports """
        port_connections = [connection.interfaces for connection in self.connections if connection.connect == ConnectPort.INPUT]
        return [interface[0][0] for interface in port_connections if interface[0][0] in self.interfaces]
  
    @property
    def inout_ports(self):
        """ List of Inout Ports """
        port_connections = [connection.interfaces for connection in self.connections if connection.connect == ConnectPort.INOUT]
        return [interface[0][0] for interface in port_connections if interface[0][0] in self.interfaces]
  
    @property
    def output_ports(self):
        """ List of Output Ports """
        port_connections = [connection.interfaces for connection in self.connections if connection.connect == ConnectPort.OUTPUT]
        return [interface[0][0] for interface in port_connections if interface[0][0] in self.interfaces]
  
    @property
    def sv_if_ports(self):
        """ List of SystemVerilog Interface Ports """
        port_connections = [connection.interfaces for connection in self.connections if connection.connect == ConnectPort.SV_IF]
        return [(interface[0][0],interface[0][1] if len(interface[0]) > 1 else None) for interface in port_connections if interface[0][0] in self.interfaces]
  
    @property
    def port_count(self):
        """ Total Number of Ports """
        return len(self.ports)
    
    @property
    def internal_count(self):
        """ Total Number of Internal Logic Instances """
        return len(self.internals)
    
    @property
    def parameter_count(self):
        """ Number of Unqiue Paramaters """
        return len(self.parameters)
        
    @property
    def sub_module_count(self):
        """ Number of Instantiated Sub-modules """
        return len(self.sub_modules)
    
    @property
    def module_base(self):
        """ Returns Name of Module Class """
        return self.__class__.__name__

def createBaseModule   (module_name, 
                        module_description = "",
                        module_type = ModuleType.DEVICE,
                        size = 0x0,
                        parameters = [],
                        include_files = [],
                        templates = ["Templates/SystemVerilog/module.sv.tpl"],
                        sub_modules = [],
                        interfaces = [],
                        connections = []):
    """
    Function used to create a new Module Class
    - When a Yaml Module file is pased, this function will be populated
      and a new Module Class will be created.
    """
    NewModule = type(module_name, (Module, ), {
        # Constructor
        "__init__": ModuleInit,
        # Module Description
        "module_description": module_description,
        # Type
        "module_type": module_type,
        # Size
        "size": size,
        # Parameters
        "parameters": parameters,
        # Include Files
        "include_files": include_files,
        # Templates
        "templates": templates,
        # Sub-Devices
        "sub_modules": sub_modules,
        # Interfaces
        "interfaces": interfaces,
        # Connections
        "connections": connections
    })
    return NewModule
    