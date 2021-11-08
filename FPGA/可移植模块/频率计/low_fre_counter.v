module low_fre_counter(
						input sys_count_clk,
						//input count_clk,
						input rst_n,
						input f_in_gate,
						output [31:0]result
						);
						
reg [31:0]result_reg;
reg [31:0]out_reg;

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
//====================================

always@(posedge sys_count_clk or negedge rst_n or posedge flag_en_pos)
begin
	if(!rst_n)
		result_reg <= 32'd0;
	else if(flag_en_pos)
		result_reg <= 32'd0;
	result_reg <= result_reg + 1;
end

reg [31:0]temp;
always@(posedge sys_count_clk)
begin
	temp <= result_reg;
end

always@(posedge flag_en_pos)
begin
		out_reg <= temp;
end

assign result = out_reg;

endmodule
						