/******************************************
@function: 采样4x4键盘输入，并转换为控制信号
******************************************/
`timescale 1ns / 1ps
module key(
				input clk,	//开发板上输入时钟：50Mhz
				input [3:0]key_in,	//输入按键信号Reset, KEY1~KEY3
				output [2:0]wave_type_out,
				output f_p_choose_out,
				output [3:0]f_count_out,
				output [1:0]p_count_out
							);

reg [19:0] count;
reg [3:0] key_scan;	//按键扫描值

//采样按键值，20ms扫描一次采样频率小于按键毛刺频率，相当于消除掉了高频毛刺信号
always@(posedge clk)	//检测时钟的上升沿和复位的下降沿
begin
	if(count == 20'd999_999)	//20ms扫描一次按键
		begin
			count <= 20'b0;	//计数器计到20ms，计数器清零
			key_scan <= key_in;	//采样按键输入电平
		end
	else
		count <= count + 20'b1;	//计数器加1
end

//按键信号锁存一个时钟节拍
reg [3:0] key_scan_r;
always@(posedge clk)
	key_scan_r <= key_scan;

//当检测到按键有下降沿变化时，代表该按键被按下，按键有效
wire [3:0] flag_key = key_scan_r [3:0] & (~key_scan [3:0]);

// 初始化寄存器
reg [2:0]wave_type = 3'd0;
reg f_p_choose = 1'b0;
reg [3:0]f_count = 4'h0;
reg [1:0]p_count = 2'd0;

always@(posedge clk)
begin
	case(flag_key)
		4'b0001: //频率或相位减小
			begin
				if(!f_p_choose)
					if(f_count == 4'h0)
						f_count <= 4'hB;
					else
						f_count <= f_count - 1'b1;
				else
					if(p_count == 2'd0)
						p_count <= 2'd3;
					else
						p_count <= p_count - 1'b1;
			end
		4'b0010: //频率或相位增加
			begin
				if(!f_p_choose)
					if(f_count == 4'hB)
						f_count <= 4'h0;
					else
						f_count <= f_count + 1'b1;
				else
					if(p_count == 4'd3)
						p_count <= 4'd0;
					else
						p_count <= p_count + 1'b1;
			end
		4'b0100: f_p_choose <= !f_p_choose;	//更改频率或相位选择
		4'b1000: //波形切换
			begin
				if(wave_type == 3'd4)
					wave_type <= 3'd0;
				else
					wave_type <= wave_type + 1'b1;
			end
			default: // 默认保持不变
			begin
				wave_type <= wave_type;
				f_p_choose <= f_p_choose;
				f_count <= f_count;
				p_count <= p_count;
			end
	endcase
end

// 输出信号
assign wave_type_out = wave_type;
assign f_p_choose_out = f_p_choose;
assign f_count_out = f_count;
assign p_count_out = p_count;

endmodule
