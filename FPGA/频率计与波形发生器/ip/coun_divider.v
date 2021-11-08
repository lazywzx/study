/********************
@function: 定义除法器
@build: LPM_DIVIDE
*********************/
`timescale 1 ps / 1 ps
module coun_divider (
	denom,
	numer,
	quotient,
	remain);

	input	[31:0]  denom;
	input	[31:0]  numer;
	output	[31:0]  quotient;
	output	[31:0]  remain;

	wire [31:0] sub_wire0;
	wire [31:0] sub_wire1;
	wire [31:0] quotient = sub_wire0[31:0];
	wire [31:0] remain = sub_wire1[31:0];

	lpm_divide	LPM_DIVIDE_component (
				.denom (denom),
				.numer (numer),
				.quotient (sub_wire0),
				.remain (sub_wire1),
				.aclr (1'b0),
				.clken (1'b1),
				.clock (1'b0));
	defparam
		LPM_DIVIDE_component.lpm_drepresentation = "UNSIGNED",
		LPM_DIVIDE_component.lpm_hint = "LPM_REMAINDERPOSITIVE=TRUE",
		LPM_DIVIDE_component.lpm_nrepresentation = "UNSIGNED",
		LPM_DIVIDE_component.lpm_type = "LPM_DIVIDE",
		LPM_DIVIDE_component.lpm_widthd = 32,
		LPM_DIVIDE_component.lpm_widthn = 32;

endmodule
