module dds_gen(
				input Clk,
				input Rst_n,
				input [31:0]Fword,
				input [11:0]Pword,
				output DA_Clk,
				output DA_Wrt,
				output [13:0]DA_Data
);

	reg [13:0]DA_Data_reg;/*D输出输出A*/
	
	reg [31:0]Fre_acc;	
	reg [13:0]Rom_Addr;

	wire[13:0]Wave_Data;	
/*---------------相位累加器------------------*/	
	always @(posedge Clk or negedge Rst_n)
	if(!Rst_n)  
		Fre_acc <= 32'd0;
	else 
		Fre_acc <= Fre_acc + Fword;

/*----------生成查找表地址---------------------*/		
	always @(posedge Clk or negedge Rst_n)
	if(!Rst_n)
		Rom_Addr <= 14'd0;
	else
		Rom_Addr <= Fre_acc[31:18] + Pword;	

/*----------例化查找表ROM-------*/		
	ddsrom ddsrom_sine(
		.address(Rom_Addr[13:2]),
		.clock(Clk),
		.q(Wave_Data)
	);

always@(posedge Clk)
begin
	DA_Data_reg <= Wave_Data;
end
	
/*----------输出DA时钟----------*/
assign DA_Clk = Clk;
assign DA_Wrt = Clk;
assign DA_Data = DA_Data_reg;

endmodule
