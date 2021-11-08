/***************************************
@function: 根据输入控制信号生成频率控制字
***************************************/
module fre_word_gen(
				input [3:0]f_count_in,
				input clk,
				input f_p_choose_in,
				input [11:0]ad_in,
				output [31:0]fre_word_out,
				output [23:0]fre_oled_out
				);

reg [31:0]Fword = 32'd0;
reg [22:0]fre_oled;
reg [31:0]fre_word_reg;
reg [19:0]grad = 0;

// 根据键盘值选择频率控制字范围的最小值
// 例如：Fword=3436，则频率范围为100Hz~500Hz
always@(posedge clk)
begin
// 判断当前调整的是频率还是相位
// 当f_p_choose_in=1时，修改频率，否则频率保持不变
	if(!f_p_choose_in)
		begin
			case(f_count_in)	//50Hz梯度对应字梯度为1718
				4'h0:  
					begin Fword <= 0; grad <= 1718; end	//0Hz
				4'h1:  
					begin Fword <= 1718; grad <= 1718; end	//50Hz
				4'h2:  
					begin Fword <= 3436; grad <= 13744; end	//100Hz
				4'h3:  
					begin Fword <= 17180; grad <= 17180; end	//500Hz
				4'h4:  
					begin Fword <= 34360; grad <= 137439; end	//1KHz
				4'h5:  
					begin Fword <= 171799; grad <= 171798; end	//5KHz
				4'h6:  
					begin Fword <= 343597; grad <= 1374290; end	//10KHz
				4'h7:  
					begin Fword <= 1717987; grad <= 1717987; end	//50KHz
				4'h8:  
					begin Fword <= 3435974; grad <= 13743895; end	//100KHz
				4'h9:  
					begin Fword <= 17179869; grad <= 17179869; end	//500KHz
				4'hA:  
					begin Fword <= 34359738; grad <= 34359739; end	//1MHz
				4'hB:  
					begin Fword <= 68719477; grad <= 34359738; end//2MHz
				default: 
					begin Fword <= Fword; grad <= grad; end
			endcase
			// 计算总的频率控制字 = 范围下限 + 电位器输入量
			fre_word_reg <= Fword + grad * ad_in / 4095;
			fre_oled <= (Fword + grad * ad_in / 4095) * 50 / 1718;
		end
	else
		begin
			fre_word_reg <= fre_word_reg;
			fre_oled <= fre_oled;
		end
end

// 输出信号并调整为适合OLED显示的格式
assign fre_word_out = fre_word_reg;
assign fre_oled_out = {1'b0, fre_oled};

endmodule
		