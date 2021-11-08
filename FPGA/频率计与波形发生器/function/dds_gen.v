/*************************************************************
@function: 根据频率和相位控制字，计算波形查找表地址并输出波形数据
**************************************************************/
// 包含必要的ROM文件
`include "../rom/sine_ddsrom.v"
`include "../rom/sawt_ddsrom.v"
`include "../rom/squa_ddsrom.v"
`include "../rom/tria_ddsrom.v"
`include "../rom/diy_ddsrom.v"

module dds_gen(
				input Clk,
				input [31:0]Fword,
				input [11:0]Pword,
				input [2:0]wave_type_in,
				output DA_Clk,
				output DA_Wrt,
				output [13:0]DA_Data
);

reg [13:0]DA_Data_reg;

reg [31:0]Fre_acc = 0;	
reg [13:0]Rom_Addr = 0;

wire[13:0]Wave_Data_sine;	
wire[13:0]Wave_Data_sawt;
wire[13:0]Wave_Data_squa;
wire[13:0]Wave_Data_tria;
wire[13:0]Wave_Data_diy;

/*---------------相位累加器------------------*/	
always @(posedge Clk)
	Fre_acc <= Fre_acc + Fword;

/*----------生成查找表地址---------------------*/		
always @(posedge Clk)
	Rom_Addr <= Fre_acc[31:18] + Pword;	

/*----------例化查找表ROM-------*/
// 正弦波
sine_ddsrom ddsrom_sine(
	.address(Rom_Addr[13:2]),
	.clock(Clk),
	.q(Wave_Data_sine)
);

// 锯齿波
sawt_ddsrom ddsrom_sawt(
	.address(Rom_Addr[13:2]),
	.clock(Clk),
	.q(Wave_Data_sawt)
);

// 方波
squa_ddsrom ddsrom_squa(
	.address(Rom_Addr[13:2]),
	.clock(Clk),
	.q(Wave_Data_squa)
);

// 三角波
tria_ddsrom ddsrom_tria(
	.address(Rom_Addr[13:2]),
	.clock(Clk),
	.q(Wave_Data_tria)
);

// 自定义手绘波形
diy_ddsrom ddsrom_diy(
	.address(Rom_Addr[13:2]),
	.clock(Clk),
	.q(Wave_Data_diy)
);

/*----------波形选择器-------*/
always@(posedge Clk)
begin
	case(wave_type_in)
		3'd0: DA_Data_reg <= Wave_Data_sine;
		3'd1: DA_Data_reg <= Wave_Data_sawt;
		3'd2: DA_Data_reg <= Wave_Data_squa;
		3'd3: DA_Data_reg <= Wave_Data_tria;
		3'd4: DA_Data_reg <= Wave_Data_diy;
		default: DA_Data_reg <= DA_Data_reg;
	endcase
end

/*----------输出DA时钟----------*/
assign DA_Clk = Clk;
assign DA_Wrt = Clk;
assign DA_Data = DA_Data_reg;

endmodule
