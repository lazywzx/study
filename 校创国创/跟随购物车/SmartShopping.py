import tkinter as tk  # 使用Tkinter前需要先导入
import tkinter.messagebox  # 要使用messagebox先要导入模块
import time
import color_deceted
import rfid_deceted


# 第1步，实例化object，建立窗口window
window = tk.Tk()

# 第2步，给窗口的可视化起名字
window.title('My Window')

# 第3步，设定窗口的大小(长 * 宽)
window.geometry('1920x1080')  # 这里的乘是小x

# 第4步，在图形界面上创建 500 * 200 大小的画布并放置各种元素
canvas = tk.Canvas(window, height=600, width=800)
# 说明图片位置，并导入图片到画布上
image_file = tk.PhotoImage(file='qrcode.png')  # 图片位置（相对路径，与.py文件同一文件夹下，也可以用绝对路径，需要给定图片具体绝对路径）
image = canvas.create_image(300, 0, anchor='n',image=image_file)        # 图片锚定点（n图片顶端的中间点位置）放在画布（250,0）坐标处


# 第5步，定义触发函数功能
def hit_me():
    total_money = 0
    chosen_goods = []
    counter = 0
    if tkinter.messagebox.askokcancel(title="SmartShopping", message="开始购物？"):
        while True:
            print('ok')
            color_deceted.color_follow()
            color_deceted.color_follow()
            color_deceted.color_follow()
            color_deceted.color_follow()
            rfid_data = rfid_deceted.rfid_read()
            color_deceted.color_follow()
            color_deceted.color_follow()
            color_deceted.color_follow()
            color_deceted.color_follow()
            if rfid_data != 'none':
                chosen_goods.append(rfid_data)
                total_money = total_money + chosen_goods[counter][1]
                tk.Label(window, text=str(counter + 1) + '. \t' + chosen_goods[counter][0] + '\t\t\t\t￥' + str(chosen_goods[counter][1]), font=('Arial', 30), ).place(
                    x=60, y=100 + 50 * counter, anchor='nw')
                tk.Label(window, text='￥' + str(total_money), font=('Arial', 30), ).place(x=1600, y=50, anchor='nw')
                counter = counter + 1
                window.update()
                time.sleep(1)



# 第4步，在图形界面上创建一个标签用以显示内容并放置
tk.Button(window, text='SmartShopping', bg='green', font=('Arial', 30), command=hit_me).pack()
tk.Label(window, text='  名称：\t\t\t\t价格：\t\t\t\t总价：', font=('Arial', 30), ).place(x=30, y=50, anchor='nw')
tk.Label(window, text='￥付款码￥', font=('Arial', 40), ).place(x=1400, y=300, anchor='nw')
canvas.place(x=2030, y=1000, anchor='se')

# 第6步，主窗口循环显示
window.mainloop()
