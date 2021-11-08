/*********************************
@function: 延时器，防止OLED刷屏过快
**********************************/
module delay500ms(
			input clk,
			input [31:0]data_in,
			output [31:0]data_out
			);

// 50MHz下0.5秒参量	
parameter T500MS = 32'd24_999_999;

reg [31:0]out_reg;
reg [31:0]count;

always@(posedge clk)
begin
	if(count == T500MS)
		begin	
			count <= 32'd0; 
			out_reg <= data_in; 
		end
	else
		begin	
			count <= count + 1'b1; 
			out_reg <= out_reg; 
		end
end

assign data_out = out_reg;

endmodule
						