module shrink_10bits(
					input [47:0]consult_in,
					output [31:0]consult_out
					);

wire [47:0]out_reg;
assign out_reg = consult_in >> 10;
assign consult_out = out_reg[31:0];

endmodule
					