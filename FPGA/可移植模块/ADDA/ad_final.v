module ad_final(
       clk,
		 AD1_CLK,
		 AD1_IN,
		 AD1_OUT
);
input clk;
input [11:0] AD1_IN;
output AD1_CLK;
output [11:0] AD1_OUT;

wire clk1;
wire clk2;
pll_65M PLL_50M (
	.inclk0(clk),
	.c0(clk1),		//130MHZ
	.c1(AD1_CLK)
	);

fenpin fenpin(
   .fin(clk1),
	.fout(clk2)
	);
ad9226 ad9266(
    .date_in(AD1_IN),
	 .date_out(AD1_OUT),
	 .clk(clk2)
	 );

endmodule