`timescale 1ns / 1ps

module oled_test_data(
			input clk_in,
			input rst_n_in,
			input [3:0]key_data,
			output [19:0]fre_out,
			output [19:0]am_out,
			output [19:0]phase_out,
			output [19:0]smg_out
			);
			
	

reg [19:0]fre_value;
reg [19:0]am_value;
reg [19:0]phase_value;
reg [19:0]smg_value;
reg [3:0]i = 4'd0;

always@(posedge clk_in or negedge rst_n_in)
begin
	if(!rst_n_in) begin fre_value <= 20'd0; am_value <= 20'd0; phase_value <= 20'd0; i <= 4'd0; smg_value <= 20'd0; end
	else
		begin
			case(key_data)
				4'h0: begin	fre_value <= 20'd686009; am_value <= 20'd456; phase_value <= 20'd0; smg_value <= 20'd123456; end
				4'h1: begin	fre_value <= 20'd686889; am_value <= 20'd456; phase_value <= 20'd0; smg_value <= 20'd123456; end
				4'h2: begin	fre_value <= 20'd975633; am_value <= 20'd600; phase_value <= 20'd100; smg_value <= 20'd6; end
				4'h3: begin	fre_value <= 20'd25081; am_value <= 20'd3; phase_value <= 20'd128940; smg_value <= 20'd6689; end
				4'h4: begin	fre_value <= 20'd2501; am_value <= 20'd30; phase_value <= 20'd18940; smg_value <= 20'd668; end
				4'h5: begin	fre_value <= 20'd25090; am_value <= 20'd320; phase_value <= 20'd1940; smg_value <= 20'd68; end
				4'h6: begin	fre_value <= 20'd290; am_value <= 20'd39; phase_value <= 20'd19402; smg_value <= 20'd681; end
				4'h7: begin	fre_value <= 20'd20; am_value <= 20'd3669; phase_value <= 20'd402; smg_value <= 20'd68231; end
				4'h8: begin	fre_value <= 20'd6869; am_value <= 20'd456; phase_value <= 20'd0; smg_value <= 20'd123456; end
				4'h9: begin	fre_value <= 20'd17633; am_value <= 20'd600; phase_value <= 20'd100; smg_value <= 20'd6; end
				4'hA: begin	fre_value <= 20'd2081; am_value <= 20'd3; phase_value <= 20'd128940; smg_value <= 20'd6689; end
				4'hB: begin	fre_value <= 20'd25015; am_value <= 20'd30; phase_value <= 20'd18940; smg_value <= 20'd668; end
				4'hC: begin	fre_value <= 20'd2500; am_value <= 20'd320; phase_value <= 20'd1940; smg_value <= 20'd68; end
				4'hD: begin	fre_value <= 20'd29; am_value <= 20'd39; phase_value <= 20'd19402; smg_value <= 20'd681; end
				4'hE: begin	fre_value <= 20'd7789; am_value <= 20'd3669; phase_value <= 20'd402; smg_value <= 20'd68231; end
				4'hF: begin	fre_value <= 20'd10; am_value <= 20'd3669; phase_value <= 20'd402; smg_value <= 20'd68231; end
				default: begin	fre_value <= fre_value; am_value <= am_value; phase_value <= phase_value; smg_value <= smg_value; end
			endcase
		end
end

/*
parameter T1MS = 32'd19_999_999;
reg [31:0]C1;
 
always @ (posedge clk_in or negedge rst_n_in)
	if( !rst_n_in )
		C1 <= 32'd0;
	else if( C1 == T1MS )
		C1 <= 32'd0;
	else
		C1 <= C1 + 1'b1;


always@(posedge clk_in or negedge rst_n_in)
begin
	if(!rst_n_in) begin fre_value <= 20'd0; am_value <= 20'd0; phase_value <= 20'd0; i <= 4'd0; smg_value <= 20'd0; end
	else
		begin
			case(i)
				4'd0: 
					if(C1 == T1MS)
						i <= i +1'b1;
					else
						begin	fre_value <= 20'd686889; am_value <= 20'd456; phase_value <= 20'd0; smg_value <= 20'd123456; end
				4'd1: 
					if(C1 == T1MS)
						i <= i + 1'b1;
					else
						begin	fre_value <= 20'd975633; am_value <= 20'd600; phase_value <= 20'd100; smg_value <= 20'd6; end
				4'd2: 
					if(C1 == T1MS)
						i <= 4'd0;
					else
						begin	fre_value <= 20'd25081; am_value <= 20'd3; phase_value <= 20'd128940; smg_value <= 20'd6689; end
			endcase
		end
end
*/

assign fre_out = fre_value;
assign am_out = am_value;
assign phase_out = phase_value;
assign smg_out = smg_value;

endmodule
