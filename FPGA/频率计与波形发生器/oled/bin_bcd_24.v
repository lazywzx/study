/***************************************************
@function: 将输入的24位二进制数以bcd码的形式输出各数位
****************************************************/
`timescale 1ns / 1ps
module bin_bcd_24(
			clk,
			rst_n,
			bin,
			bcd
			);
	 
input  clk,rst_n;
input  [23:0] bin;
output [27:0] bcd;

reg    [3:0] one,ten,hun,tho,wan,sw,m;
reg    [51:0]shift_reg=51'b0;
integer I;

/*-----------------二-BCD转换器-----------------*/
always @ (posedge clk or negedge rst_n )
begin
	shift_reg={27'b0, bin};
	if ( !rst_n )// 复位后寄存器归零
		  begin
			 one<=0;
			 ten<=0;
			 hun<=0;
			 tho<=0;
			 wan<=0;
			 sw<=0;
			 m <= 0;
		  end
   else 
	begin 
		// 移位加三算法
	   for (I=1; I<=23; I=I+1)
		  begin
				  shift_reg=shift_reg << 1; 
				  
				  if (shift_reg[27:24]+4'b0011>4'b0111)
					  begin
						 shift_reg[27:24]=shift_reg[27:24]+4'b0011;
					  end 
				  if (shift_reg[31:28]+4'b0011>4'b0111)
					  begin
						 shift_reg[31:28]=shift_reg[31:28]+4'b0011;
					  end 
				  if (shift_reg[35:32]+4'b0011>4'b0111)
					  begin
						 shift_reg[35:32]=shift_reg[35:32]+4'b0011;
					  end 
				  if (shift_reg[39:36]+4'b0011>4'b0111)
					  begin
						 shift_reg[39:36]=shift_reg[39:36]+4'b0011;
					  end 
				  if (shift_reg[43:40]+4'b0011>4'b0111)
					  begin
						 shift_reg[43:40]=shift_reg[43:40]+4'b0011;
					  end 
				  if (shift_reg[47:44]+4'b0011>4'b0111)
					  begin
						 shift_reg[47:44]=shift_reg[47:44]+4'b0011;
					  end 	
				  if (shift_reg[51:48]+4'b0011>4'b0111)
					  begin
						 shift_reg[51:48]=shift_reg[51:48]+4'b0011;
					  end 					  
		   end
		// 取出各个数位的BCD值
		shift_reg=shift_reg << 1; 
		m <= shift_reg[51:48];	
		sw <= shift_reg[47:44];
		wan <= shift_reg[43:40];
		tho <= shift_reg[39:36];
		hun <= shift_reg[35:32];
		ten <= shift_reg[31:28];
		one <= shift_reg[27:24];
	end
end

// 输出各个数位
assign bcd[27:24] = m;
assign bcd[23:20] = sw;
assign bcd[19:16] = wan;
assign bcd[15:12] = tho;
assign bcd[11:8] = hun;
assign bcd[7:4] = ten;
assign bcd[3:0] = one;

endmodule
