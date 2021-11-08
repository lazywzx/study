module gate(
				input clk,
				output gate_en
				);

parameter T2S = 27'd99_999_999;
parameter T3S = 28'd149_999_999;

reg [27:0]count_en;
reg gate_reg;
				
always@(posedge clk)
begin
	if(count_en == T2S)
		gate_reg <= 0;
	else if(count_en == T3S)
		begin
			gate_reg <= 1;
			count_en <= 28'd0;
		end
	else
		count_en <= count_en + 1'b1;
end

assign gate_en = gate_reg;

endmodule
