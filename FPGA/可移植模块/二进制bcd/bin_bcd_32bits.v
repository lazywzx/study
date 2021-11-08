`timescale 1ns / 1ps
module bin_bcd(
clk,rst_n,bin,bcd
    );
	 
input  clk,rst_n;
input  [31:0] bin;
output [35:0] bcd;

reg    [3:0] one,ten,hun,tho,wan,sw,m,sm,bm;
integer I;
reg    [67:0]shift_reg=67'b0;

////////////////////// 二进制转换为十进制 /////////////////
always @ (posedge clk or negedge rst_n )
begin
shift_reg={35'b0, bin};
	if ( !rst_n )
		  begin
			 one<=0;
			 ten<=0;
			 hun<=0;
			 tho<=0;
			 wan<=0;
			 sw<=0;
			 m <= 0;
			 sm <= 0;
			 bm <= 0; 
		  end
   else 
	begin 
	   for (I=1; I<=31; I=I+1)
		  begin
				  shift_reg=shift_reg << 1; 
				  
				  if (shift_reg[35:32]+4'b0011>4'b0111)
					  begin
						 shift_reg[35:32]=shift_reg[35:32]+4'b0011; // >7则加3
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
				  if (shift_reg[55:52]+4'b0011>4'b0111)
					  begin
						 shift_reg[55:52]=shift_reg[55:52]+4'b0011;
					  end 	
				  if (shift_reg[59:56]+4'b0011>4'b0111)
					  begin
						 shift_reg[59:56]=shift_reg[59:56]+4'b0011;
					  end 					  
				  if (shift_reg[63:60]+4'b0011>4'b0111)
					  begin
						 shift_reg[63:60]=shift_reg[63:60]+4'b0011;
					  end
				  if (shift_reg[67:64]+4'b0011>4'b0111)
					  begin
						 shift_reg[67:64]=shift_reg[67:64]+4'b0011;
					  end 					  
		   end
	shift_reg=shift_reg << 1; 
	bm <= shift_reg[67:64];
	sm <= shift_reg[63:60];
	m <= shift_reg[59:56];	
	sw <= shift_reg[55:52];
	wan <= shift_reg[51:48];
	tho <= shift_reg[47:44];
	hun <= shift_reg[43:40];
	ten <= shift_reg[39:36];
	one <= shift_reg[35:32];
	end

end

assign bcd[35:32] = bm;
assign bcd[31:28] = sm;
assign bcd[27:24] = m;
assign bcd[23:20] = sw;
assign bcd[19:16] = wan;
assign bcd[15:12] = tho;
assign bcd[11:8] = hun;
assign bcd[7:4] = ten;
assign bcd[3:0] = one;

endmodule
