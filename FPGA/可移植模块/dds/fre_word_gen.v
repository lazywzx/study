module fre_word_gen(
				input [3:0]key_data,
				input clk,
				input rst_n,
				output [31:0]fre_word_out
				);

reg [31:0]Fword;
			
always@(posedge clk or negedge rst_n)
begin
	if(!rst_n)
		Fword <= 32'd0;
	else
		case(key_data)
			4'h0:  Fword <= 34;	//1Hz
			4'h1:  Fword <= 1718;	//50Hz
			4'h2:  Fword <= 3436;	//100Hz
			4'h3:  Fword <= 17180;	//500Hz
			4'h4:  Fword <= 34360;	//1KHz
			4'h5:  Fword <= 171799;	//5KHz
			4'h6:  Fword <= 343597;	//10KHz
			4'h7:  Fword <= 1717987;	//50KHz
			4'h8:  Fword <= 3435974;	//100KHz
			4'h9:  Fword <= 17179869;	//500KHz
			4'hA: Fword <= 34359738;	//1MHz
			4'hB: Fword <= 68719477;	//2MHz
			4'hC: Fword <= 103079215;	//3MHz
			4'hD: Fword <= 137438953;	//4MHz
			4'hE: Fword <= 171798692;	//5MHz
			//4'hF: Fword <= 343597384;	//10MHz
			default: Fword <= Fword;
		endcase
end

assign fre_word_out = Fword;

endmodule
		