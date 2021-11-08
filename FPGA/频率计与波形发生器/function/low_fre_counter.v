/************************************************************
@function: 按低频输入信号方式计数，信号周期内计算高频时钟周期数
************************************************************/
module low_fre_counter(
						input sys_count_clk,
						input rst_n,
						input f_in_gate,
						output [31:0]result
						);
						
reg [31:0]result_reg = 32'd0;
reg [31:0]out_reg = 32'd0;
reg flag = 0;

//==========闸门上升/下降沿检测==========
reg en_scan;
always@(posedge sys_count_clk)
begin
	en_scan <= f_in_gate;
end

reg en_scan_r;
always@(posedge sys_count_clk)
begin
	en_scan_r <= en_scan;
end

//上升沿
wire flag_en_pos = (!en_scan_r) & en_scan;
//下降沿
wire flag_en_neg = en_scan_r & (!en_scan);

/*---------------------计数器------------------*/
always@(posedge sys_count_clk )
begin
	case (flag)
		1: 
			result_reg <= 32'd0;
		0: 
			result_reg <= result_reg + 1'b1;
		default;
   endcase 
end

/*------------------输出缓冲器---------------------*/
always@(posedge flag_en_pos)
begin
	out_reg <= result_reg;
	flag <= !flag;
end

assign result = out_reg;

endmodule
