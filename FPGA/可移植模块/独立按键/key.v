`timescale 1ns / 1ps
module key(
				input clk,	//开发板上输入时钟：50Mhz
				input [3:0]key_in,	//输入按键信号Reset, KEY1~KEY3
				output [3:0]key_out
							);

wire rst_n = 1'b1;

reg [19:0] count;
reg [3:0] key_scan;	//按键扫描值

//采样按键值，20ms扫描一次采样频率小于按键毛刺频率，相当于消除掉了高频毛刺信号
always@(posedge clk or negedge rst_n)	//检测时钟的上升沿和复位的下降沿
	begin
		if(!rst_n)
			count <= 20'd0;
		else
			begin
				if(count == 20'd999_999)	//20ms扫描一次按键
					begin
						count <= 20'b0;	//计数器计到20ms，计数器清零
						key_scan <= key_in;	//采样按键输入电平
					end
				else
					count <= count + 20'b1;	//计数器加1
			end
	end

//按键信号锁存一个时钟节拍
reg [3:0] key_scan_r;
always@(posedge clk)
	key_scan_r <= key_scan;

//当检测到按键有下降沿变化时，代表该按键被按下，按键有效
wire [3:0] flag_key = key_scan_r [3:0] & (~key_scan [3:0]);

reg [3:0]temp;
always@(posedge clk or negedge rst_n)
	begin
		if(!rst_n)
			temp <= 4'b1111;
		else
			begin
				case(flag_key)
					4'b0001: temp <= 4'd1;
					4'b0010: temp <= 4'd2;
					4'b0100: temp <= 4'd3;
					4'b1000: temp <= 4'd4;
					default: temp <= 4'd0;
				endcase
			end
	end

assign key_out = temp;

endmodule

