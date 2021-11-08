/**************************************************
module: OledDriver
author: wanganran
description: drive Oled Xplained Pro display with fpga/cpld
input: clk_in,rst_n_in
output: rclk_out,sclk_out,sdio_out
date: 2015.10.23
**************************************************/
module OledDriver
(
input clk_in,  //clk_in = 25mhz
input rst_n_in,  //rst_n_in, active low
//output reg run_flag,
output reg oled_rst_n_out,  //nokia5110 reset, active low
output reg oled_cs_n_out,  //nokia5110 chip select, active low
output reg oled_dc_out,  //nokia5110 data or command control
output oled_clk_out,  //nokia5110 clock
output reg oled_data_out,  //nokia5110 data
//输入各种信号数据
input [35:0]fre_bcd_in,
input [23:0]am_bcd_in,
input [23:0]phase_bcd_in
);


parameter CLK_DIV_PERIOD=20; //related with clk_div's frequency
parameter DELAY_PERIOD=25000;  //related with delay time and refresh frequency

parameter CLK_L=2'd0;
parameter CLK_H=2'd1;
parameter CLK_RISING_DEGE=2'd2;
parameter CLK_FALLING_DEGE=2'd3;

parameter IDLE=3'd0;
parameter SHIFT=3'd1;
parameter CLEAR=3'd2;
parameter SETXY=3'd3;
parameter DISPLAY=3'd4;
parameter DELAY=3'd5;

parameter LOW =1'b0;
parameter HIGH =1'b1;
parameter CMD =1'b0;
parameter DATA =1'b1;

//parameter div_num_data = 4'd2345;

//assign oled_rst_n_out = 1;  //active low level, set 1 for normal
//assign oled_dc_out = 1;
assign oled_clk_out = clk_div;

//initial for memory register
reg [47:0] cmd_r [9:0];
initial
	begin
		cmd_r[0]= {8'hae, 8'h00, 8'h10, 8'h00, 8'hb0, 8'h81};   // command for initial
		cmd_r[1]= {8'hff, 8'ha1, 8'ha6, 8'ha8, 8'h1f, 8'hc8};   // command for initial
		cmd_r[2]= {8'hd3, 8'h00, 8'hd5, 8'h80, 8'hd9, 8'h1f};   // command for initial
		cmd_r[3]= {8'hda, 8'h00, 8'hdb, 8'h40, 8'h8d, 8'h14};   // command for initial
		cmd_r[4]= {8'haf, 8'he3, 8'he3, 8'he3, 8'he3, 8'he3};   // command for initial
		cmd_r[5]= {8'hb0, 8'h01, 8'h10, 8'hE3, 8'he3, 8'he3};   // command for set row1
		cmd_r[6]= {8'hb1, 8'h01, 8'h10, 8'hE3, 8'he3, 8'he3};   // command for set row2
		cmd_r[7]= {8'hb2, 8'h01, 8'h10, 8'hE3, 8'he3, 8'he3};   // command for set row3
		cmd_r[8]= {8'hb3, 8'h01, 8'h10, 8'hE3, 8'he3, 8'he3};   // command for set row4
	end

//initial for memory register
reg [47:0] mem [120:0];
reg [47:0] temp;
initial
	begin
	/*
		mem[0]= {8'h00, 8'h00, 8'h00, 8'h00, 8'h00, 8'h00};   // 0  sp 
		mem[1]= {8'h00, 8'h00, 8'h00, 8'h2f, 8'h00, 8'h00};   // 1  !  
		mem[2]= {8'h00, 8'h00, 8'h07, 8'h00, 8'h07, 8'h00};   // 2  
		mem[3]= {8'h00, 8'h14, 8'h7f, 8'h14, 8'h7f, 8'h14};   // 3  #
		mem[4]= {8'h00, 8'h24, 8'h2a, 8'h7f, 8'h2a, 8'h12};   // 4  $
		mem[5]= {8'h00, 8'h62, 8'h64, 8'h08, 8'h13, 8'h23};   // 5  %
		mem[6]= {8'h00, 8'h36, 8'h49, 8'h55, 8'h22, 8'h50};   // 6  &
		mem[7]= {8'h00, 8'h00, 8'h05, 8'h03, 8'h00, 8'h00};   // 7  '
		mem[8]= {8'h00, 8'h00, 8'h1c, 8'h22, 8'h41, 8'h00};   // 8  {
		mem[9]= {8'h00, 8'h00, 8'h41, 8'h22, 8'h1c, 8'h00};   // 9  )
		mem[10]= {8'h00, 8'h14, 8'h08, 8'h3E, 8'h08, 8'h14};   // 10 *
		mem[11]= {8'h00, 8'h08, 8'h08, 8'h3E, 8'h08, 8'h08};   // 11 +
		mem[12]= {8'h00, 8'h00, 8'h00, 8'hA0, 8'h60, 8'h00};   // 12 ,
		mem[13]= {8'h00, 8'h08, 8'h08, 8'h08, 8'h08, 8'h08};   // 13 -
		mem[14]= {8'h00, 8'h00, 8'h60, 8'h60, 8'h00, 8'h00};   // 14 .
		mem[15]= {8'h00, 8'h20, 8'h10, 8'h08, 8'h04, 8'h02};   // 15 /
		mem[16]= {8'h00, 8'h3E, 8'h51, 8'h49, 8'h45, 8'h3E};   // 16 0
		mem[17]= {8'h00, 8'h00, 8'h42, 8'h7F, 8'h40, 8'h00};   // 17 1
		mem[18]= {8'h00, 8'h42, 8'h61, 8'h51, 8'h49, 8'h46};   // 18 2
		mem[19]= {8'h00, 8'h21, 8'h41, 8'h45, 8'h4B, 8'h31};   // 19 3
		mem[20]= {8'h00, 8'h18, 8'h14, 8'h12, 8'h7F, 8'h10};   // 20 4
		mem[21]= {8'h00, 8'h27, 8'h45, 8'h45, 8'h45, 8'h39};   // 21 5
		mem[22]= {8'h00, 8'h3C, 8'h4A, 8'h49, 8'h49, 8'h30};   // 22 6
		mem[23]= {8'h00, 8'h01, 8'h71, 8'h09, 8'h05, 8'h03};   // 23 7
		mem[24]= {8'h00, 8'h36, 8'h49, 8'h49, 8'h49, 8'h36};   // 24 8
		mem[25]= {8'h00, 8'h06, 8'h49, 8'h49, 8'h29, 8'h1E};   // 25 9
		*/
		mem[0]= {8'h00, 8'h3E, 8'h51, 8'h49, 8'h45, 8'h3E};   // 16 0
		mem[1]= {8'h00, 8'h00, 8'h42, 8'h7F, 8'h40, 8'h00};   // 17 1
		mem[2]= {8'h00, 8'h42, 8'h61, 8'h51, 8'h49, 8'h46};   // 18 2
		mem[3]= {8'h00, 8'h21, 8'h41, 8'h45, 8'h4B, 8'h31};   // 19 3
		mem[4]= {8'h00, 8'h18, 8'h14, 8'h12, 8'h7F, 8'h10};   // 20 4
		mem[5]= {8'h00, 8'h27, 8'h45, 8'h45, 8'h45, 8'h39};   // 21 5
		mem[6]= {8'h00, 8'h3C, 8'h4A, 8'h49, 8'h49, 8'h30};   // 22 6
		mem[7]= {8'h00, 8'h01, 8'h71, 8'h09, 8'h05, 8'h03};   // 23 7
		mem[8]= {8'h00, 8'h36, 8'h49, 8'h49, 8'h49, 8'h36};   // 24 8
		mem[9]= {8'h00, 8'h06, 8'h49, 8'h49, 8'h29, 8'h1E};   // 25 9
		
		mem[26]= {8'h00, 8'h00, 8'h36, 8'h36, 8'h00, 8'h00};   // 26 :
		mem[27]= {8'h00, 8'h00, 8'h56, 8'h36, 8'h00, 8'h00};   // 27 ;
		mem[28]= {8'h00, 8'h08, 8'h14, 8'h22, 8'h41, 8'h00};   // 28 <
		mem[29]= {8'h00, 8'h14, 8'h14, 8'h14, 8'h14, 8'h14};   // 29 =
		mem[30]= {8'h00, 8'h00, 8'h41, 8'h22, 8'h14, 8'h08};   // 30 >
		mem[31]= {8'h00, 8'h02, 8'h01, 8'h51, 8'h09, 8'h06};   // 31 ?
		mem[32]= {8'h00, 8'h32, 8'h49, 8'h59, 8'h51, 8'h3E};   // 32 @
		mem[33]= {8'h00, 8'h7C, 8'h12, 8'h11, 8'h12, 8'h7C};   // 33 A
		mem[34]= {8'h00, 8'h7F, 8'h49, 8'h49, 8'h49, 8'h36};   // 34 B
		mem[35]= {8'h00, 8'h3E, 8'h41, 8'h41, 8'h41, 8'h22};   // 35 C
		mem[36]= {8'h00, 8'h7F, 8'h41, 8'h41, 8'h22, 8'h1C};   // 36 D
		mem[37]= {8'h00, 8'h7F, 8'h49, 8'h49, 8'h49, 8'h41};   // 37 E
		mem[38]= {8'h00, 8'h7F, 8'h09, 8'h09, 8'h09, 8'h01};   // 38 F
		mem[39]= {8'h00, 8'h3E, 8'h41, 8'h49, 8'h49, 8'h7A};   // 39 G
		mem[40]= {8'h00, 8'h7F, 8'h08, 8'h08, 8'h08, 8'h7F};   // 40 H
		mem[41]= {8'h00, 8'h00, 8'h41, 8'h7F, 8'h41, 8'h00};   // 41 I
		mem[42]= {8'h00, 8'h20, 8'h40, 8'h41, 8'h3F, 8'h01};   // 42 J
		mem[43]= {8'h00, 8'h7F, 8'h08, 8'h14, 8'h22, 8'h41};   // 43 K
		mem[44]= {8'h00, 8'h7F, 8'h40, 8'h40, 8'h40, 8'h40};   // 44 L
		mem[45]= {8'h00, 8'h7F, 8'h02, 8'h0C, 8'h02, 8'h7F};   // 45 M
		mem[46]= {8'h00, 8'h7F, 8'h04, 8'h08, 8'h10, 8'h7F};   // 46 N
		mem[47]= {8'h00, 8'h3E, 8'h41, 8'h41, 8'h41, 8'h3E};   // 47 O
		mem[48]= {8'h00, 8'h7F, 8'h09, 8'h09, 8'h09, 8'h06};   // 48 P
		mem[49]= {8'h00, 8'h3E, 8'h41, 8'h51, 8'h21, 8'h5E};   // 49 Q
		mem[50]= {8'h00, 8'h7F, 8'h09, 8'h19, 8'h29, 8'h46};   // 50 R
		mem[51]= {8'h00, 8'h46, 8'h49, 8'h49, 8'h49, 8'h31};   // 51 S
		mem[52]= {8'h00, 8'h01, 8'h01, 8'h7F, 8'h01, 8'h01};   // 52 T
		mem[53]= {8'h00, 8'h3F, 8'h40, 8'h40, 8'h40, 8'h3F};   // 53 U
		mem[54]= {8'h00, 8'h1F, 8'h20, 8'h40, 8'h20, 8'h1F};   // 54 V
		mem[55]= {8'h00, 8'h3F, 8'h40, 8'h38, 8'h40, 8'h3F};   // 55 W
		mem[56]= {8'h00, 8'h63, 8'h14, 8'h08, 8'h14, 8'h63};   // 56 X
		mem[57]= {8'h00, 8'h07, 8'h08, 8'h70, 8'h08, 8'h07};   // 57 Y
		mem[58]= {8'h00, 8'h61, 8'h51, 8'h49, 8'h45, 8'h43};   // 58 Z
		mem[59]= {8'h00, 8'h00, 8'h7F, 8'h41, 8'h41, 8'h00};   // 59 [
		mem[60]= {8'h00, 8'h55, 8'h2A, 8'h55, 8'h2A, 8'h55};   // 60 .
		mem[61]= {8'h00, 8'h00, 8'h41, 8'h41, 8'h7F, 8'h00};   // 61 ]
		mem[62]= {8'h00, 8'h04, 8'h02, 8'h01, 8'h02, 8'h04};   // 62 ^
		mem[63]= {8'h00, 8'h40, 8'h40, 8'h40, 8'h40, 8'h40};   // 63 _
		mem[64]= {8'h00, 8'h00, 8'h01, 8'h02, 8'h04, 8'h00};   // 64 '
		mem[65]= {8'h00, 8'h20, 8'h54, 8'h54, 8'h54, 8'h78};   // 65 a
		mem[66]= {8'h00, 8'h7F, 8'h48, 8'h44, 8'h44, 8'h38};   // 66 b
		mem[67]= {8'h00, 8'h38, 8'h44, 8'h44, 8'h44, 8'h20};   // 67 c
		mem[68]= {8'h00, 8'h38, 8'h44, 8'h44, 8'h48, 8'h7F};   // 68 d
		mem[69]= {8'h00, 8'h38, 8'h54, 8'h54, 8'h54, 8'h18};   // 69 e
		mem[70]= {8'h00, 8'h08, 8'h7E, 8'h09, 8'h01, 8'h02};   // 70 f
		mem[71]= {8'h00, 8'h18, 8'hA4, 8'hA4, 8'hA4, 8'h7C};   // 71 g
		mem[72]= {8'h00, 8'h7F, 8'h08, 8'h04, 8'h04, 8'h78};   // 72 h
		mem[73]= {8'h00, 8'h00, 8'h44, 8'h7D, 8'h40, 8'h00};   // 73 i
		mem[74]= {8'h00, 8'h40, 8'h80, 8'h84, 8'h7D, 8'h00};   // 74 j
		mem[75]= {8'h00, 8'h7F, 8'h10, 8'h28, 8'h44, 8'h00};   // 75 k
		mem[76]= {8'h00, 8'h00, 8'h41, 8'h7F, 8'h40, 8'h00};   // 76 l
		mem[77]= {8'h00, 8'h7C, 8'h04, 8'h18, 8'h04, 8'h78};   // 77 m
		mem[78]= {8'h00, 8'h7C, 8'h08, 8'h04, 8'h04, 8'h78};   // 78 n
		mem[79]= {8'h00, 8'h38, 8'h44, 8'h44, 8'h44, 8'h38};   // 79 o
		mem[80]= {8'h00, 8'hFC, 8'h24, 8'h24, 8'h24, 8'h18};   // 80 p
		mem[81]= {8'h00, 8'h18, 8'h24, 8'h24, 8'h18, 8'hFC};   // 81 q
		mem[82]= {8'h00, 8'h7C, 8'h08, 8'h04, 8'h04, 8'h08};   // 82 r
		mem[83]= {8'h00, 8'h48, 8'h54, 8'h54, 8'h54, 8'h20};   // 83 s
		mem[84]= {8'h00, 8'h04, 8'h3F, 8'h44, 8'h40, 8'h20};   // 84 t
		mem[85]= {8'h00, 8'h3C, 8'h40, 8'h40, 8'h20, 8'h7C};   // 85 u
		mem[86]= {8'h00, 8'h1C, 8'h20, 8'h40, 8'h20, 8'h1C};   // 86 v
		mem[87]= {8'h00, 8'h3C, 8'h40, 8'h30, 8'h40, 8'h3C};   // 87 w
		mem[88]= {8'h00, 8'h44, 8'h28, 8'h10, 8'h28, 8'h44};   // 88 x
		mem[89]= {8'h00, 8'h1C, 8'hA0, 8'hA0, 8'hA0, 8'h7C};   // 89 y
		mem[90]= {8'h00, 8'h44, 8'h64, 8'h54, 8'h4C, 8'h44};   // 90 z
		mem[91]= {8'h14, 8'h14, 8'h14, 8'h14, 8'h14, 8'h14};   // 91 horiz lines
		//chinese word xiao jiao ya
		mem[100]= {8'h00, 8'hC0, 8'h30, 8'h00, 8'h00, 8'hFF};   // 91 xiao
		mem[101]= {8'h00, 8'h00, 8'h10, 8'h60, 8'h80, 8'h00};   // 91 xiao
		mem[102]= {8'h01, 8'h00, 8'h00, 8'h08, 8'h08, 8'h0F};   // 91 xiao
		mem[103]= {8'h00, 8'h00, 8'h00, 8'h00, 8'h01, 8'h00};   // 91 xiao
		mem[104]= {8'hFE, 8'h92, 8'hFE, 8'h00, 8'hA4, 8'h7F};   // 91 jiao
		mem[105]= {8'h24, 8'h00, 8'hFE, 8'h02, 8'hFE, 8'h00};   // 91 jiao
		mem[106]= {8'h07, 8'h08, 8'h0F, 8'h00, 8'h03, 8'h02};   // 91 jiao
		mem[107]= {8'h03, 8'h00, 8'h0F, 8'h02, 8'h03, 8'h00};   // 91 jiao
		mem[108]= {8'h01, 8'h02, 8'h04, 8'h08, 8'h10, 8'hE0};   // 91 ya
		mem[109]= {8'h10, 8'h08, 8'h04, 8'h02, 8'h01, 8'h00};   // 91 ya
		mem[110]= {8'h00, 8'h00, 8'h00, 8'h00, 8'h00, 8'h0F};   // 91 ya
		mem[111]= {8'h00, 8'h00, 8'h00, 8'h00, 8'h00, 8'h00};   // 91 ya
	end
	
//clk_div = clk_in/CLK_DIV_PERIOD, 50% is high voltage
reg clk_div; 
reg[15:0] clk_cnt=0;
always@(posedge clk_in or negedge rst_n_in)
begin
	if(!rst_n_in) clk_cnt<=0;
	else begin
		clk_cnt<=clk_cnt+1;  
		if(clk_cnt==(CLK_DIV_PERIOD-1)) clk_cnt<=0;
		if(clk_cnt<(CLK_DIV_PERIOD/2)) clk_div<=0;
		else clk_div<=1;
	end
end


//divide clk_div 4 state, RISING and FALLING state is keeped one cycle of clk_in, like a pulse.
reg[1:0] clk_div_state=CLK_L;  
always@(posedge clk_in or negedge rst_n_in)
begin
	if(!rst_n_in) clk_div_state<=CLK_L;
    else 
		case(clk_div_state)
			CLK_L: begin
					if (clk_div) clk_div_state<=CLK_RISING_DEGE;  
					else clk_div_state<=CLK_L;
				end
			CLK_RISING_DEGE :clk_div_state<=CLK_H;  
			CLK_H:begin                 
					if (!clk_div) clk_div_state<=CLK_FALLING_DEGE;
					else clk_div_state<=CLK_H;
				end 
			CLK_FALLING_DEGE:clk_div_state<=CLK_L;  
			default;
		endcase
end


reg shift_flag = 0;
reg[6:0] x_reg;
reg[2:0] y_reg;   
reg[7:0] char_reg;
reg[8:0] temp_cnt;
reg[7:0] data_reg; 
reg[2:0] data_state=IDLE; 
reg[2:0] data_state_back; 
reg[7:0] data_state_cnt=0;  
reg[3:0] shift_cnt=0; 
reg[25:0] delay_cnt=0;  
//Finite State Machine, 
always@(posedge clk_in or negedge rst_n_in)      
begin
	if(!rst_n_in) 
		begin 
			data_state<=IDLE;
			//run_flag <= 1;
			data_state_cnt<=0;
			shift_flag <= 0;
			oled_cs_n_out<=HIGH;
		end
    else
		case (data_state)
			IDLE: begin
					oled_cs_n_out<=HIGH;
					data_state_cnt<=data_state_cnt+1;
					case(data_state_cnt)
						0: oled_rst_n_out <= 0;
						1: data_state<=DISPLAY;
						2: oled_rst_n_out <= 1;
						3: data_state<=DISPLAY;
						//display initial
						4: begin data_state<=DISPLAY;data_state_back<=DISPLAY;oled_dc_out<=CMD;char_reg<=0; end
						5: begin data_state<=DISPLAY;data_state_back<=DISPLAY;oled_dc_out<=CMD;char_reg<=1; end
						6: begin data_state<=DISPLAY;data_state_back<=DISPLAY;oled_dc_out<=CMD;char_reg<=2; end
						7: begin data_state<=DISPLAY;data_state_back<=DISPLAY;oled_dc_out<=CMD;char_reg<=3; end
						8: begin data_state<=DISPLAY;data_state_back<=DISPLAY;oled_dc_out<=CMD;char_reg<=4; end
						//clear display
						9: begin data_state<=DISPLAY;data_state_back<=DISPLAY;oled_dc_out<=CMD;char_reg<=5; end
						10: begin data_state<=CLEAR;data_state_back<=CLEAR; end
						11: begin data_state<=DISPLAY;data_state_back<=DISPLAY;oled_dc_out<=CMD;char_reg<=6; end
						12: begin data_state<=CLEAR;data_state_back<=CLEAR; end
						13: begin data_state<=DISPLAY;data_state_back<=DISPLAY;oled_dc_out<=CMD;char_reg<=7; end
						14: begin data_state<=CLEAR;data_state_back<=CLEAR; end
						15: begin data_state<=DISPLAY;data_state_back<=DISPLAY;oled_dc_out<=CMD;char_reg<=8; end
						16: begin data_state<=CLEAR;data_state_back<=CLEAR; end

						//设置起始行
						//fre显示
						17: begin data_state<=DISPLAY;data_state_back<=DISPLAY;oled_dc_out<=CMD;char_reg<=5; end
						//wite the word
						//固定的字符
						18: begin data_state<=DISPLAY;data_state_back<=DISPLAY;oled_dc_out<=DATA;char_reg<=70; end
						19: begin data_state<=DISPLAY;data_state_back<=DISPLAY;oled_dc_out<=DATA;char_reg<=82; end
						20: begin data_state<=DISPLAY;data_state_back<=DISPLAY;oled_dc_out<=DATA;char_reg<=69; end
						21: begin data_state<=DISPLAY;data_state_back<=DISPLAY;oled_dc_out<=DATA;char_reg<=26; end
						//传入的数据
						22: begin data_state<=DISPLAY;data_state_back<=DISPLAY;oled_dc_out<=DATA;char_reg<= fre_bcd_in[35:32]; end
						23: begin data_state<=DISPLAY;data_state_back<=DISPLAY;oled_dc_out<=DATA;char_reg<= fre_bcd_in[31:28]; end
						24: begin data_state<=DISPLAY;data_state_back<=DISPLAY;oled_dc_out<=DATA;char_reg<= fre_bcd_in[27:24]; end
						25: begin data_state<=DISPLAY;data_state_back<=DISPLAY;oled_dc_out<=DATA;char_reg<= fre_bcd_in[23:20]; end
						26: begin data_state<=DISPLAY;data_state_back<=DISPLAY;oled_dc_out<=DATA;char_reg<= fre_bcd_in[19:16]; end
						27: begin data_state<=DISPLAY;data_state_back<=DISPLAY;oled_dc_out<=DATA;char_reg<= fre_bcd_in[15:12]; end
						28: begin data_state<=DISPLAY;data_state_back<=DISPLAY;oled_dc_out<=DATA;char_reg<= fre_bcd_in[11:8]; end
						29: begin data_state<=DISPLAY;data_state_back<=DISPLAY;oled_dc_out<=DATA;char_reg<= fre_bcd_in[7:4]; end
						30: begin data_state<=DISPLAY;data_state_back<=DISPLAY;oled_dc_out<=DATA;char_reg<= fre_bcd_in[3:0]; end
						//固定的字符
						31: begin data_state<=DISPLAY;data_state_back<=DISPLAY;oled_dc_out<=DATA;char_reg<=40; end
						32: begin data_state<=DISPLAY;data_state_back<=DISPLAY;oled_dc_out<=DATA;char_reg<=58; end
						/*
						//am显示
						//设置起始行
						30: begin data_state<=DISPLAY;data_state_back<=DISPLAY;oled_dc_out<=CMD;char_reg<=6; end
						//wite the word
						//固定的字符
						31: begin data_state<=DISPLAY;data_state_back<=DISPLAY;oled_dc_out<=DATA;char_reg<=65; end
						32: begin data_state<=DISPLAY;data_state_back<=DISPLAY;oled_dc_out<=DATA;char_reg<=77; end
						33: begin data_state<=DISPLAY;data_state_back<=DISPLAY;oled_dc_out<=DATA;char_reg<=26; end
						//传入的数据
						34: begin data_state<=DISPLAY;data_state_back<=DISPLAY;oled_dc_out<=DATA;char_reg<= am_bcd_in[23:20]; end
						35: begin data_state<=DISPLAY;data_state_back<=DISPLAY;oled_dc_out<=DATA;char_reg<= am_bcd_in[19:16]; end
						36: begin data_state<=DISPLAY;data_state_back<=DISPLAY;oled_dc_out<=DATA;char_reg<= am_bcd_in[15:12]; end
						37: begin data_state<=DISPLAY;data_state_back<=DISPLAY;oled_dc_out<=DATA;char_reg<= am_bcd_in[11:8]; end
						38: begin data_state<=DISPLAY;data_state_back<=DISPLAY;oled_dc_out<=DATA;char_reg<= am_bcd_in[7:4]; end
						39: begin data_state<=DISPLAY;data_state_back<=DISPLAY;oled_dc_out<=DATA;char_reg<= am_bcd_in[3:0]; end
						//固定的字符
						40: begin data_state<=DISPLAY;data_state_back<=DISPLAY;oled_dc_out<=DATA;char_reg<=54; end

						//phase显示
						//设置起始行
						41: begin data_state<=DISPLAY;data_state_back<=DISPLAY;oled_dc_out<=CMD;char_reg<=7; end
						//wite the word
						//固定的字符
						42: begin data_state<=DISPLAY;data_state_back<=DISPLAY;oled_dc_out<=DATA;char_reg<=80; end
						43: begin data_state<=DISPLAY;data_state_back<=DISPLAY;oled_dc_out<=DATA;char_reg<=72; end
						44: begin data_state<=DISPLAY;data_state_back<=DISPLAY;oled_dc_out<=DATA;char_reg<=65; end
						45: begin data_state<=DISPLAY;data_state_back<=DISPLAY;oled_dc_out<=DATA;char_reg<=26; end
						//传入的数据
						46: begin data_state<=DISPLAY;data_state_back<=DISPLAY;oled_dc_out<=DATA;char_reg<= phase_bcd_in[23:20]; end
						47: begin data_state<=DISPLAY;data_state_back<=DISPLAY;oled_dc_out<=DATA;char_reg<= phase_bcd_in[19:16]; end
						48: begin data_state<=DISPLAY;data_state_back<=DISPLAY;oled_dc_out<=DATA;char_reg<= phase_bcd_in[15:12]; end
						49: begin data_state<=DISPLAY;data_state_back<=DISPLAY;oled_dc_out<=DATA;char_reg<= phase_bcd_in[11:8]; end
						50: begin data_state<=DISPLAY;data_state_back<=DISPLAY;oled_dc_out<=DATA;char_reg<= phase_bcd_in[7:4]; end
						51: begin data_state<=DISPLAY;data_state_back<=DISPLAY;oled_dc_out<=DATA;char_reg<= phase_bcd_in[3:0]; end
						//固定的字符
						52: begin data_state<=DISPLAY;data_state_back<=DISPLAY;oled_dc_out<=DATA;char_reg<=82; end
						53: begin data_state<=DISPLAY;data_state_back<=DISPLAY;oled_dc_out<=DATA;char_reg<=65; end
						54: begin data_state<=DISPLAY;data_state_back<=DISPLAY;oled_dc_out<=DATA;char_reg<=68; end
						*/
						
						55: 
						begin data_state_cnt <= 17; 
						//run_flag <= ~run_flag; 
						end
						default;
					endcase
				end
				
			SHIFT: begin
					if(!shift_flag)
						begin
							if (clk_div_state==CLK_FALLING_DEGE)  
								begin
									if (shift_cnt==8)  
										begin
											shift_cnt<=0;
											data_state<=data_state_back;
										end
									else begin
											oled_cs_n_out<=LOW;
											oled_data_out<=data_reg[7];   
											shift_flag <= 1;
										end
								end
						end
					else
						begin
							if (clk_div_state==CLK_RISING_DEGE)   
								begin  
									data_reg<={data_reg[6:0], data_reg[7]};  
									shift_cnt<=shift_cnt+1;
									shift_flag <= 0;
								end
						end
				end

			DISPLAY: begin
						temp_cnt<=temp_cnt+1;
						oled_cs_n_out<=HIGH;
						if (temp_cnt==6) 
							begin
								data_state<=IDLE;
								temp_cnt<=0; 
							end
						else 
							begin
								temp = (oled_dc_out==CMD)? cmd_r[char_reg]:mem[char_reg];
								case (temp_cnt)
									0 :  data_reg<=temp[47:40];
									1 :  data_reg<=temp[39:32];
									2 :  data_reg<=temp[31:24];
									3 :  data_reg<=temp[23:16];
									4 :  data_reg<=temp[15:8];
									5 :  data_reg<=temp[7:0];
									default;
								endcase
								data_state<=SHIFT;
							end
					end
			
			CLEAR: begin            
					data_reg<=8'h00;
					temp_cnt<=temp_cnt+1;
					oled_cs_n_out<=HIGH;
					oled_dc_out<=DATA;
					if (temp_cnt>=128) 
						begin
							temp_cnt<=0;
							data_state<=IDLE;
						end
					else data_state<=SHIFT;
				end
			
			DELAY: begin
					if(delay_cnt==DELAY_PERIOD)
						begin
							data_state<=IDLE; 
							delay_cnt<=0;
						end
					else delay_cnt<=delay_cnt+1;
				end
					   
			default;
		endcase
end

endmodule
