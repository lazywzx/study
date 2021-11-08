/*********************************************************
@function: 计算输入信号赋值Vpp，并将输入信号赋值二值化为0和1
**********************************************************/
module ad_caclu(
			input clk,
			input [11:0]ad_data_in,
			output f_in,
			output [15:0]vol_out
			);

// 50M频率下1s计数
parameter T1S = 26'd49_999_999;
reg [15:0]vol_max = 16'd2048;
reg [15:0]vol_min = 16'd2048;
reg [15:0]vol_out_reg = 16'd0;
reg [15:0]vol_in = 16'd0;
reg [25:0]counter = 26'd0;

always@(posedge clk)
begin
	if(counter == T1S)// 每隔一秒计算一次
		begin
			counter <= 26'd0;
			vol_out_reg <= vol_max - vol_min;
			vol_max <= 16'd2048;
			vol_min <= 16'd2048;
		end
		else// 一秒时间内不断更新最大最小值
		begin
			vol_in <= ad_data_in * 5000 / 4096;
			if(vol_max < vol_in)
				vol_max <= vol_in;
			else
				vol_max <= vol_max;
			if(vol_min > vol_in)
				vol_min <= vol_in;
			else
				vol_min <= vol_min;
			vol_out_reg <= vol_out_reg;
			counter <= counter + 1;
		end
end

// 与ADC数字半量程比较，二值化输入信号
assign f_in = (ad_data_in > 2048) ? 1:0;
assign vol_out = vol_out_reg;

endmodule
