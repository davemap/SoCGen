from enum import Enum, auto

class InterfaceType(Enum):
    LOGIC       = auto()
    SVINTERFACE = auto()
    
def InterfaceInit(self, name, description):
    self.name           = name
    self.description    = description
    # TODO: Move this check to Connection
    # if self.interface_type == InterfaceType.SVINTERFACE:
    #     if modport in self.interface_modports:
    #         self.modport = modport
    #     else:
    #         raise ValueError(f"Error: {modport} is not in Avaliable Modports list")

class Interface:
    name                  = "name"
    description           = ""
    interface_description = ""
    interface_type        = InterfaceType.LOGIC
    interface_modports    = []
    modport               = None
    parameters            = []
    connections           = []
    bit_width             = 1
    sv_input_ports        = []
    sv_interface_file     = ""
    
    
    def __init__(self,name, description):
        InterfaceInit(self, name, description)
    
    @property
    def bit_width(self):
        if self.interface_type == InterfaceType.LOGIC:
            return self.bit_width
        else:
            return 0
    
    @property
    def input_ports(self):
        if self.interface_type == InterfaceType.SVINTERFACE:
            return self.sv_input_ports
        else:
            return None
    
    @property
    def modports(self):
        if self.interface_type == InterfaceType.SVINTERFACE:
            return self.sv_modports
        else:
            return None
    
    @property
    def interface_file(self):
        if self.interface_type == InterfaceType.SVINTERFACE:
            return self.sv_interface_file
        else:
            return None
    
    @property
    def port_width_string(self):
        string = ""
        if self.bit_width > 1:
            string = f"[{self.bit_width - 1}:0] "
        return string
    
    @property
    def interface_base(self):
        return self.__class__.__name__
    
    @property
    def description_str(self):
        if self.description != "":
            return f" // {self.description}"
        else:
            return ""
    
    @property
    def input_declr(self):
        if self.interface_type == InterfaceType.LOGIC:
            return f"input {self.port_width_string}{self.name},{self.description_str}"
        else:
            return ""

    @property
    def output_declr(self):
        if self.interface_type == InterfaceType.LOGIC:
            return f"output {self.port_width_string}{self.name},{self.description_str}"
        else:
            return ""

    @property
    def inout_declr(self):
        if self.interface_type == InterfaceType.LOGIC:
            return f"inout {self.port_width_string}{self.name},{self.description_str}"
        else:
            return ""

    @property
    def internal_declr(self):
        if self.interface_type == InterfaceType.LOGIC:
            return f"logic {self.port_width_string}{self.name};{self.description_str}"
        else:
            return f"{self.interface_base} {self.name};{self.description_str}"
    
    def sv_if_port_declr(self,modport = None):
        if self.interface_type == InterfaceType.SVINTERFACE:
            if modport == None:
                return f"{self.interface_base} {self.name},{self.description_str}"
            else:
                return f"{self.interface_base}.{modport} {self.name},{self.description_str}"
        else:
            return ""
    
    def find_connection(self,modinst,sub_module):
        valid_list = [connection for connection in modinst.connections if ((connection.sub_module == sub_module) and (connection.connect == self))]
        if len(valid_list) == 0:
            return None
        else:
            return valid_list[0]
        
def createBaseInterface (interface_name, 
                         interface_description = "",
                         interface_type = InterfaceType.LOGIC,
                         parameters = [],
                         bit_width = 1,
                         interface_file = "",
                         modports = [],
                         input_ports = []):
    NewInterface = type(interface_name, (Interface, ), {
        # Constructor
        "__init__": InterfaceInit,
        # Interface Description
        "interface_description": interface_description,
        # Interface Type
        "interface_type": interface_type,
        # Parameters
        "parameters": parameters,
        # Logic Bit Width
        "bit_width": (bit_width if interface_type == InterfaceType.LOGIC else 0),
        # Interface File
        "sv_interface_file": interface_file,
        # Modports
        "interface_modports": (modports if interface_type == InterfaceType.SVINTERFACE else []) ,
        # Input Ports
        "sv_input_ports": input_ports
    })
    return NewInterface