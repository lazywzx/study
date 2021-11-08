/***************************************
@function: 根据输入控制信号生成相位控制字
***************************************/
module pha_word_gen(
				input [1:0]p_count_in,
				input clk,
				input f_p_choose_in,
				input [11:0]ad_in,
				output [11:0]pha_word_out,
				output [11:0]pha_oled_out
				);

reg [11:0]Pword = 12'd0;
reg [8:0]pha_oled;
reg [11:0]pha_word_reg;

always@(posedge clk)
begin
// 当f_p_choose_in=1时修改相位，否则保持不变
	if(f_p_choose_in)
		begin// 相位控制字
			case(p_count_in)
				2'd0:  
					Pword <= 0;	//0~90
				2'd1:  
					Pword <= 1024;	//90~180
				2'd2:  
					Pword <= 2048;	//180~270
				2'd3:  
					Pword <= 3071;	//270~360
				default: 
					Pword <= Pword;
			endcase
			pha_word_reg <= Pword + 1024 * ad_in / 4095;
			pha_oled <= (Pword + 1024 * ad_in / 4095) * 90 / 1024;
		end
	else
		begin
			pha_word_reg <= pha_word_reg;
			pha_oled <= pha_oled;
		end
end

// 输出信号并调整为适合OLED显示的格式
assign pha_word_out = pha_word_reg;
assign pha_oled_out = {3'b000, pha_oled};

endmodule
