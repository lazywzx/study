/****************************************************
@function: 防止除0错误，当输入0时输出保持上一个时钟的值
*****************************************************/
module data_choose(
						input [31:0]result_in,
						input clk,
						output [31:0]result_out
						);

reg [31:0]temp;

always@(posedge clk)
begin
	if(result_in)// 非0时更新
		temp <= result_in;
	else
		temp <= temp;
end

assign result_out	= temp;

endmodule
						