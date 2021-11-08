/********************
@function: 定义乘法器
@build: lpm_mult
********************/
`timescale 1 ps / 1 ps
module f_count_mult_constant (
	dataa,
	result);
	
	input	[31:0]  dataa;
	output	[47:0]  result;

	wire [47:0] sub_wire0;
	wire [15:0] sub_wire1 = 16'hbebb;
	wire [47:0] result = sub_wire0[47:0];

	lpm_mult	lpm_mult_component (
				.dataa (dataa),
				.datab (sub_wire1),
				.result (sub_wire0),
				.aclr (1'b0),
				.clken (1'b1),
				.clock (1'b0),
				.sum (1'b0));
	defparam
		lpm_mult_component.lpm_hint = "INPUT_B_IS_CONSTANT=YES,MAXIMIZE_SPEED=5",
		lpm_mult_component.lpm_representation = "UNSIGNED",
		lpm_mult_component.lpm_type = "LPM_MULT",
		lpm_mult_component.lpm_widtha = 32,
		lpm_mult_component.lpm_widthb = 16,
		lpm_mult_component.lpm_widthp = 48;

endmodule
