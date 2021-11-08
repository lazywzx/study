module dds_test(

	input sys_clk ,
	input sys_rst_n ,
	input [22:0]freq_word,
	input [9:0]phase_word,
	output[7:0]  wave_out
);


		                     
reg   [31:0] freq_word_reg  ;
reg   [9:0] phase_word_reg ;
reg   [31:0] phase_adder    ;   //相位累加器
reg   [9:0]  rom_address    ;   //存储深度2^10

/*
parameter freq_word = 32'd2100;
parameter phase_word = 12'd0 ;
*/

/*** 频率设置 ***/
always @(posedge sys_clk or negedge sys_rst_n) begin 
	if (sys_rst_n ==1'b0) begin 
		freq_word_reg <= 32'h0000;
	end	
	else 
		freq_word_reg <= freq_word * 10000;
end

/*** 相位设置 ***/
always @(posedge sys_clk or negedge sys_rst_n) begin 
	if (sys_rst_n ==1'b0) begin 
		phase_word_reg <= 9'd0;
	end
	
	else  
		phase_word_reg <= phase_word;
end

/*** 相位变化量设置 ***/
always @(posedge sys_clk or negedge sys_rst_n) begin 
	if (sys_rst_n ==1'b0) begin 
		phase_adder <= 32'h0000;
	end
	else begin
		if(phase_adder > 32'd4_284_000_000)
			phase_adder <= 32'd0;
		phase_adder <= phase_adder + freq_word_reg;        //对频率控制字进行累加
	end
end

/*** 正弦输出 ***/
always @(posedge sys_clk or negedge sys_rst_n) begin 
	if (sys_rst_n ==1'b0) begin 
		rom_address <= 10'd0;
	end
	else  
		rom_address <= phase_adder[29:20] + phase_word_reg;       
	end

	
wave_rom u_wave_rom(
	.address (rom_address) ,
	.clock   (sys_clk)  ,  
	.q       (wave_out)
);
		
endmodule 
