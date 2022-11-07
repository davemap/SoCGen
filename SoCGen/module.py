from SoCGen.connection import ConnectPort
from enum import Enum, auto

class ModuleType(Enum):
    DEVICE  = auto()
    WRAPPER = auto()
    REGBANK = auto()
    BUS     = auto()
    
def ModuleInit(self, name, description):
    self.name         = name
    self.description  = description

class Module:
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
        port_connections = [connection.interfaces for connection in self.connections if connection.connect.__class__ == ConnectPort]
        return [interface[0][0] for interface in port_connections if interface[0][0] in self.interfaces]
        
    @property
    def internals(self):
        return [interface for interface in self.interfaces if interface not in self.ports]
    
    @property
    def input_ports(self):
        port_connections = [connection.interfaces for connection in self.connections if connection.connect == ConnectPort.INPUT]
        return [interface[0][0] for interface in port_connections if interface[0][0] in self.interfaces]
  
    @property
    def inout_ports(self):
        port_connections = [connection.interfaces for connection in self.connections if connection.connect == ConnectPort.INOUT]
        return [interface[0][0] for interface in port_connections if interface[0][0] in self.interfaces]
  
    @property
    def output_ports(self):
        port_connections = [connection.interfaces for connection in self.connections if connection.connect == ConnectPort.OUTPUT]
        return [interface[0][0] for interface in port_connections if interface[0][0] in self.interfaces]
  
    @property
    def sv_if_ports(self):
        port_connections = [connection.interfaces for connection in self.connections if connection.connect == ConnectPort.SV_IF]
        return [(interface[0][0],interface[0][1] if len(interface[0]) > 1 else None) for interface in port_connections if interface[0][0] in self.interfaces]
  
    @property
    def port_count(self):
        return len(self.ports)
    
    @property
    def internal_count(self):
        return len(self.internals)
    
    @property
    def parameter_count(self):
        return len(self.parameters)
        
    @property
    def sub_module_count(self):
        return len(self.sub_modules)
    
    @property
    def module_base(self):
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
    