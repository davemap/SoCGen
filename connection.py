from interface import *

class ConnectPort(Enum):
    INPUT   = auto() # Input Port
    OUTPUT  = auto() # Output Port
    INOUT   = auto() # Inout Port
    SV_IF   = auto() # SV Interface Port

class Connection:
    def __init__(self, interfaces, connect, sub_module = None, modport = None):
        self.sub_module        = None if connect.__class__ == ConnectPort else sub_module
        self.connect           = connect
        self.interfaces        = interfaces
        self.interface_inst    = [interface[0] for interface in interfaces]
        self.interface_bits    = []
        self.interface_modport = []
        for interface in interfaces:
            if interface[0].interface_type == InterfaceType.LOGIC:
                self.interface_bits.append(list(range(interface[0].bit_width)) if len(interface) == 1 else list(range(interface[1][0],interface[1][1]+1)))
            elif interface[0].interface_type == InterfaceType.SVINTERFACE:
                self.interface_modport.append(interface[1] if len(interface) > 1 else "")
    
    @property
    def interface_width(self):
        return [len(self.interface_bits) for interface in self.interface_bits]
    
    @property
    def interface_bitslice_string(self):
        bs_string_list = []
        for if_idx, interface_width in enumerate(self.interface_width):
            sub_if_string = ""
            if interface_width < self.interface_inst[if_idx].bit_width:
                if interface_width == 1:
                    sub_if_string = f" [{self.interface_bits[if_idx][0]}]"
                else:
                    sub_if_string = f" [{self.interface_bits[if_idx][-1]}:{self.interface_bits[if_idx][0]}]"
            bs_string_list.append(sub_if_string)
        return bs_string_list
    
    @property
    def connection_declr(self):
        if len(self.interfaces) == 1:
            return f"{self.interface_inst[0].name}{self.interface_bitslice_string[0]}"
        else:
            connection_string = "{"
            for if_idx, interface in enumerate(self.interfaces):
                connection_string += f"{self.interface_inst[if_idx].name}{self.interface_bitslice_string[if_idx]}, "
            connection_string = connection_string[:-2] + "}"
            return connection_string