/*************************************
@function: 比较器，调整高频、低频分界线
**************************************/
module compare(
				input [31:0]data_in1,
				input [31:0]data_in2,
				output [31:0]fre_out
				);
				
assign fre_out = (data_in1 > 32'd300_000) ? data_in1 : data_in2;

endmodule
				