module cut_comp(
					input [7:0]data_in,
					output [31:0]data_out
					);

assign data_out = {24'b0000_0000_0000_0000_0000_0000, data_in};

endmodule
