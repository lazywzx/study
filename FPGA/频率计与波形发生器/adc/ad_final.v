/****************************************
@function: 分别采样两路ADC输入，供后续处理
*****************************************/
// 包含必要文件
`include "../pll/pll_65M.v"
`include "./fenpin.v"
`include "./ad9226.v"

module ad_final(
       clk,
		 AD_CLK,
		 AD1_IN,
		 AD1_OUT,
		 AD2_IN,
		 AD2_OUT
);

input clk;
input [11:0] AD1_IN;
input [11:0] AD2_IN;
output [11:0] AD1_OUT;
output [11:0] AD2_OUT;
output AD_CLK;

wire clk1;
wire clk2;

// 实例化65M时钟
pll_65M PLL65M (
	.inclk0(clk),
	.c0(clk1),		//130MHZ
	.c1(AD_CLK)
	);

// 时钟二分频
fenpin fenpin(
   .fin(clk1),
	.fout(clk2)
	);

// 信号发生器采样旋钮电位器电压输入
ad9226 sampling_resistance(
    .date_in(AD1_IN),
	 .date_out(AD1_OUT),
	 .clk(clk2)
	 );

// 波频鉴定器采样信号输入
ad9226 sampling_signal(
    .date_in(AD2_IN),
	 .date_out(AD2_OUT),
	 .clk(clk2)
	 );

endmodule
