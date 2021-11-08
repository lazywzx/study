module expend(
			input [31:0]sys_count,
			output [31:0]sys_out
			);
			
assign sys_out = sys_count << 10;

endmodule
			