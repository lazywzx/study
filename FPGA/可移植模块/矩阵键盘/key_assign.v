module key_assign(
						input clk,
						input rst_n,
						input [3:0]key_val_in,
						output [19:0]fre_out,
						output [19:0]pha_out,
						output [19:0]smg_out
						);
						
reg [19:0]fre_reg;
reg [19:0]pha_reg;
reg [19:0]key_val;

always@(posedge clk or negedge rst_n)
begin
	if(!rst_n)
		key_val <= 20'd0;
	else
		begin
			case(key_val_in)
				4'hE: key_val <= 20'd0;
				4'h0, 4'h1, 4'h2, 4'h3, 4'h4, 4'h5, 4'h6, 4'h7, 4'h8, 4'h9: key_val <= key_val * 10 + key_val_in;
				4'hA: fre_reg <= key_val;
				4'hB: pha_reg <= key_val;
				default: begin key_val <= key_val; fre_reg <= fre_reg; pha_reg <= pha_reg; end
			endcase
		end
end

assign smg_out = key_val;
assign fre_out = fre_reg;
assign pha_out = pha_reg;

endmodule				
