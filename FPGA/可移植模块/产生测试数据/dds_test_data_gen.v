module dds_test_data_gen(
							input clk,
							input rst_n,
							input [3:0]key_value,
							output [15:0]fre_data,
							output [15:0]pha_data
							);

reg [15:0]fre_data_reg = 16'd500;
reg [15:0]pha_data_reg = 16'd0;

parameter [15:0]fre_add = 16'd50;
parameter [15:0]pha_add = 16'd1000;

always@(posedge clk or negedge rst_n)
begin
	if(!rst_n)
		begin	fre_data_reg <= 16'd0; pha_data_reg <= 16'd0; end
	else
		begin
			case(key_value)
				4'd1: fre_data_reg <= fre_data_reg + fre_add;
				4'd2: fre_data_reg <= fre_data_reg - fre_add;
				4'd3: pha_data_reg <= pha_data_reg + pha_add;
				4'd4: pha_data_reg <= pha_data_reg - pha_add;
				default;
			endcase
		end
end

assign fre_data = fre_data_reg;
assign pha_data = pha_data_reg;

endmodule
