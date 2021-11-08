/***********************
@function: 定义50M常数值
@build: LPM_CONSTANT
************************/
`timescale 1 ps / 1 ps
module  constant_50M_lpm_constant_269
	( 
	result) ;
	output   [31:0]  result;


	assign
		result = 32'b00000010111110101111000010000000;
endmodule //constant_50M_lpm_constant_269

`timescale 1 ps / 1 ps
module constant_50M (
	result);

	output	[31:0]  result;

	wire [31:0] sub_wire0;
	wire [31:0] result = sub_wire0[31:0];

	constant_50M_lpm_constant_269	constant_50M_lpm_constant_269_component (
				.result (sub_wire0));

endmodule
