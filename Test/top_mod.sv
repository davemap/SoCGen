module top_mod
(
    input [2:0] clk, // Clock Input
    input rst, // Reset Input
    apb_if.slave apb, // Apb Interface
);

    apb_if apb2; // Apb Interface;
    logic a; // Wire a;
    logic b; // Wire b;
    logic c; // Wire c;

    a_module a_mod (
        .clk ({clk [2], clk [1:0]}),
        .rst (),
        );

    a_module ab_mod (
        .clk (),
        .rst (),
        );


endmodule