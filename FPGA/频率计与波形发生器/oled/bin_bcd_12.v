/***************************************************
@function: 将输入的12位二进制数以bcd码的形式输出各数位
****************************************************/
`timescale 1ns / 1ps
module bin_bcd_12(
			clk,
			rst_n,
			bin,
			bcd
			);
	 
input  clk,rst_n;
input  [11:0] bin;
output [15:0] bcd;

reg    [3:0] one,ten,hun,tho,wan,sw,m;
integer I;
reg    [27:0]shift_reg=27'b0;

/*-----------------二-BCD转换器-----------------*/
always @ (posedge clk or negedge rst_n )
begin
	shift_reg={15'b0, bin};
	if ( !rst_n )
		  begin// 复位后寄存器归零
			 one<=0;
			 ten<=0;
			 hun<=0;
			 tho<=0;
		  end
   else 
	begin 
		// 移位加三算法
	   for (I=1; I<=11; I=I+1)
		  begin
				  shift_reg=shift_reg << 1; 
				  
				  if (shift_reg[15:12]+4'b0011>4'b0111)
					  begin
						 shift_reg[15:12]=shift_reg[15:12]+4'b0011; 
					  end 
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
		   end
		// 取出各个数位的BCD值
		shift_reg=shift_reg << 1; 
		tho <= shift_reg[27:24];
		hun <= shift_reg[23:20];
		ten <= shift_reg[19:16];
		one <= shift_reg[15:12];
	end

end

// 输出各个数位
assign bcd[15:12] = tho;
assign bcd[11:8] = hun;
assign bcd[7:4] = ten;
assign bcd[3:0] = one;

endmodule
