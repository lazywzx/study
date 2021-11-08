module keypad
(
		clk,
		rst_n,
		col,
		row,                              
		key_val              
);

input clk;
input rst_n;
input [3:0] row;                 // 矩阵键盘 行
output reg [3:0] col;            // 矩阵键盘 列
output [3:0]key_val;        // 键盘值  

reg [3:0]key_val_reg;
//++++++++++++++++++++++++++++++++++++++
// 状态机部分 开始
//++++++++++++++++++++++++++++++++++++++
// 状态编码
parameter NO_KEY_PRESSED = 6'b000_001;  // 没有按键按下   
parameter SCAN_COL0      = 6'b000_010;  // 扫描第0列  
parameter SCAN_COL1      = 6'b000_100;  // 扫描第1列  
parameter SCAN_COL2      = 6'b001_000;  // 扫描第2列  
parameter SCAN_COL3      = 6'b010_000;  // 扫描第3列  
parameter KEY_PRESSED    = 6'b100_000;  // 有按键按下
reg [5:0] current_state, next_state;    // 现态、次态
reg  key_pressed_flag;              // 键盘按下标志
reg [3:0] col_reg, row_reg;             // 列值、行值
reg [20:0]cnt;
reg clk0;

always@(posedge clk or negedge rst_n)
begin
   if(!rst_n)
      current_state<=NO_KEY_PRESSED;
   else
      current_state<=next_state;  
end

always@(posedge clk)
begin
   if(cnt<200_0000)
		cnt<=cnt+1;
	else
	  begin
		cnt<=0;
		clk0<=~clk0;
	  end
end

always@(posedge clk0)
begin
	case(current_state)
		NO_KEY_PRESSED:
			if(row!=4'b1111)  
				next_state<=SCAN_COL0;
         else
					begin
						next_state<=NO_KEY_PRESSED;
					end
      SCAN_COL0:
         begin
            if(row!=4'b1111)
					next_state<=KEY_PRESSED;
            else
					next_state<=SCAN_COL1;               
         end
      SCAN_COL1:
         begin
            if(row!=4'b1111)
               next_state<=KEY_PRESSED;
            else  
					next_state<=SCAN_COL2;
         end
      SCAN_COL2:
         begin
				if(row!=4'b1111)
               next_state<=KEY_PRESSED;
            else  
					next_state<=SCAN_COL3;
         end
      SCAN_COL3:
         begin
            if(row!=4'b1111)
               next_state<=KEY_PRESSED;
            else
					next_state<=NO_KEY_PRESSED;
         end
      KEY_PRESSED:
         if(row!=4'b1111)
            next_state<=KEY_PRESSED;
         else
				next_state<=NO_KEY_PRESSED;
      default:
				next_state<=NO_KEY_PRESSED;
endcase
end  

always@(posedge clk or negedge rst_n)
begin
   if(!rst_n)
		begin
			col<= 4'b0000;
			key_pressed_flag<=0;
		end
   else
		case(next_state)
			NO_KEY_PRESSED:
				begin
					col<=4'b0000;
					key_pressed_flag<=0;
				end   
			SCAN_COL0:  
				col<=4'b1110;
			SCAN_COL1:  
				col<=4'b1101;
			SCAN_COL2:  
				col<=4'b1011;
			SCAN_COL3:  
				col<=4'b0111;
			KEY_PRESSED:
				begin
					col_reg<=col;
					row_reg<=row;
					key_pressed_flag<=1;
				end
		endcase  
end

always@(posedge clk0 or negedge rst_n)
begin
	if(!rst_n)
	  key_val_reg<=4'h0;
	else if(key_pressed_flag)
	  begin
		case({col_reg,row_reg})
		 8'b1110_1110: key_val_reg<=4'h1; //显示"1"
		 8'b1110_1101: key_val_reg<=4'h2; //显示"2"
		 8'b1110_1011: key_val_reg<=4'h3; //显示"3"
		 8'b1110_0111: key_val_reg<=4'hA; //显示"A"
		
		 8'b1101_1110: key_val_reg<=4'h4; //显示"4"
		 8'b1101_1101: key_val_reg<=4'h5; //显示"5"
		 8'b1101_1011: key_val_reg<=4'h6; //显示"6"
		 8'b1101_0111: key_val_reg<=4'hB; //显示"B"
		
		 8'b1011_1110: key_val_reg<=4'h7; //显示"7"
		 8'b1011_1101: key_val_reg<=4'h8; //显示"8"
		 8'b1011_1011: key_val_reg<=4'h9; //显示"9"
		 8'b1011_0111: key_val_reg<=4'hC; //显示"C"
		
		 8'b0111_1110: key_val_reg<=4'hE; //显示"E"
		 8'b0111_1101: key_val_reg<=4'h0; //显示"0"
		 8'b0111_1011: key_val_reg<=4'hF; //显示"F"
		 8'b0111_0111: key_val_reg<=4'hD; //显示"D"
		 
		 default: key_val_reg<=4'hF;	//默认保持F无效值
		endcase
	  end
end  

//只在上升沿将按下的值更新到输出端口
//按住和放开的时间中输出F

reg [3:0]key_val_out_reg;
always@(posedge clk)
begin
	key_val_out_reg <= key_val_reg;
end

reg [3:0]key_val_out = 4'hF;
always@(posedge clk)
begin
	if(!rst_n)
		key_val_out <= 4'hF;
	else
		begin
			if(key_val_reg == 4'hF)
				key_val_out <= key_val_out_reg;
			else
				key_val_out <= 4'hF;
		end
end


assign key_val = key_val_out;

endmodule

