/*******************************
@function: 计时闸门，截取输入信号
********************************/
module gate(
			input clk,
			output gate_en
			);

reg[20:0]count;

always @(posedge clk)
begin
   count<=count+1;
end

assign gate_en = count[20];

endmodule 
