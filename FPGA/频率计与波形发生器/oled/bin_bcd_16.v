/***************************************************
@function: 将输入的16位二进制数以bcd码的形式输出各数位
****************************************************/
`timescale 1ns / 1ps
module bin_bcd_16(
		clk,
		rst_n,
		bin,
		bcd
    );
	 
input  clk,rst_n;
input  [15:0] bin;
output [19:0] bcd;

reg    [3:0] one,ten,hun,tho,wan;
integer I;
reg    [35:0]shift_reg=36'b0;

/*-----------------二-BCD转换器-----------------*/
always @ (posedge clk or negedge rst_n )
begin
shift_reg={19'b0, bin};
	if ( !rst_n )// 复位后寄存器归零
		  begin
			 one<=0;
			 ten<=0;
			 hun<=0;
			 tho<=0;
			 wan<=0; 
		  end
   else 
	begin 
		// 移位加三算法
	   for (I=1; I<=15; I=I+1)
		  begin
				  shift_reg=shift_reg << 1; 
				  
				  if (shift_reg[19:16]+4'b0011>4'b0111)
					  begin
						 shift_reg[19:16]=shift_reg[19:16]+4'b0011;
					  end 
				  if (shift_reg[23:20]+4'b0011>4'b0111)
					  begin
						 shift_reg[23:20]=shift_reg[23:20]+4'b0011;
					  end 
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
		   end
		// 取出各个数位的BCD值
		shift_reg=shift_reg << 1; 
		wan <= shift_reg[35:32];
		tho <= shift_reg[31:28];
		hun <= shift_reg[27:24];
		ten <= shift_reg[23:20];
		one <= shift_reg[19:16];
	end
end

// 输出各个数位
assign bcd[19:16] = wan;
assign bcd[15:12] = tho;
assign bcd[11:8] = hun;
assign bcd[7:4] = ten;
assign bcd[3:0] = one;

endmodule
