module shrink(
					input [31:0]consult_in,
					output [31:0]consult_out
					);
					
assign consult_out = consult_in >> 10;

endmodule
					