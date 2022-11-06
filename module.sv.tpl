module ${modinst.name}
% if modinst.parameter_count:
### Parmater Declaration
#(
)
% endif
### Port Declaration
(
% if modinst.port_count:
    % for interface in modinst.input_ports:
    ${interface.input_declr}
    % endfor
    % for interface in list(modinst.inout_ports):
    ${interface.inout_declr}
    % endfor
    % for interface in list(modinst.output_ports):
    ${interface.output_declr}
    % endfor
    % for interface in list(modinst.sv_if_ports):
    ${interface[0].sv_if_port_declr(interface[1])}
    % endfor
% endif
);

% if modinst.internal_count:
### Internal Logic Declarations
    % for interface in modinst.internals:
    ${interface.internal_declr};
    % endfor
% endif

% if modinst.sub_module_count:
### Sub-module Instatiations
    % for sub_module in modinst.sub_modules:
    ${sub_module.module_base} ${sub_module.name} (
        % for interface in sub_module.ports:
<% connection = interface.find_connection(modinst,sub_module) %>\
        ### Connect Up Each Port
        .${interface.name} (${connection.connection_declr if connection != None else ""}),
        % endfor
        );

    % endfor
% endif

endmodule