module dds_14bits(

	input sys_clk ,
	input sys_rst_n ,
	input [15:0]freq_word,
	input [15:0]phase_word,
	output [13:0]wave_out
);
	                     
reg   [15:0]freq_word_reg;
reg   [15:0]phase_word_reg;
reg   [15:0]phase_adder;   //相位累加�?
reg   [15:0]rom_address;   //存储深度2^16

/*** 频率设置 ***/
always @(posedge sys_clk or negedge sys_rst_n) begin 
	if (sys_rst_n ==1'b0)
		freq_word_reg <= 16'd0;
	else 
		freq_word_reg <= freq_word;
end

/*** 相位设置 ***/
always @(posedge sys_clk or negedge sys_rst_n) begin 
	if (sys_rst_n ==1'b0)
		phase_word_reg <= 16'd0;
	else  
		phase_word_reg <= phase_word;
end

/*** 相位变化量设�?***/
always @(posedge sys_clk or negedge sys_rst_n) begin 
	if (sys_rst_n ==1'b0) begin 
		phase_adder <= 20'd0;
	end
	else begin
		if(phase_adder > 20'd65535)
			phase_adder <= 20'd0;
		phase_adder <= phase_adder + freq_word_reg;        //对频率控制字进行累加
	end
end

/*** 正弦输出 ***/
always @(posedge sys_clk or negedge sys_rst_n) begin 
	if (sys_rst_n ==1'b0) begin 
		rom_address <= 16'd0;
	end
	else  
		rom_address <= phase_adder[15:0] + phase_word_reg;       
	end

wave_rom u_wave_rom(
	.address (rom_address) ,
	.clock   (sys_clk)  ,  
	.q       (wave_out)
);
		
endmodule 
