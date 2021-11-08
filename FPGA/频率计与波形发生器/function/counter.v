/******************************************************
@function: 按高频输入信号方式计数，闸门期内计算信号周期数
*******************************************************/
module counter(
						input sys_clk,
						input count_clk,
						input rst_n,
						input cou_en,
						output [31:0]result
						);
						
reg [31:0]result_reg;
reg [31:0]out_reg;

//==========闸门上升/下降沿检测==========
reg en_scan;
always@(posedge sys_clk)
begin
	en_scan <= cou_en;
end

reg en_scan_r;
always@(posedge sys_clk)
begin
	en_scan_r <= en_scan;
end

//上升沿
wire flag_en_pos = (!en_scan_r) & en_scan;
//下降沿
wire flag_en_neg = en_scan_r & (!en_scan);

/*------------------计数器--------------------*/
always@(posedge count_clk or negedge rst_n or posedge flag_en_pos)
begin
	if(!rst_n)
		result_reg <= 32'd0;
	else if(flag_en_pos)
		result_reg <= 32'd0;
	else if(cou_en)
		result_reg <= result_reg + 1;
end

/*--------------输出缓冲器--------------------*/
always@(posedge flag_en_neg)
begin
		out_reg <= result_reg;
end

assign result = out_reg;

endmodule
						