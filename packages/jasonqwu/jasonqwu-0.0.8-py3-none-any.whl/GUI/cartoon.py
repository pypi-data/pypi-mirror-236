from tkinter import *
import time
import sched


root = Tk()
root.title('卡通图片')
root.geometry('800x600')
w = Canvas(root, width=400, height=400, bg='white')
w.place(x=200, y=100)
# 设置作品名称的Label
l1 = Label(text='作品名称：', font=('楷体', 15), fg='black').place(x=200, y=25)
l1 = Label(text='修改此处为作品名称', font=('楷体', 15), fg='black').place(x=300, y=25)
l1 = Label(text='学生姓名：XXX', font=('楷体', 15), fg='black').place(x=200, y=60)
l1 = Label(text='个人班级：XXXX', font=('楷体', 15), fg='black').place(x=400, y=60)


# 定义1函数清空画布
def cv_white():
    w.create_rectangle((0, 0, 500, 500), fill='white')  # 重新放置新画布


# 定义画原始人物的函数
def bt1_age():
    # 画虚线
    line1 = w.create_line(0, 200, 400, 200,
                          fill="black",
                          dash=(4, 4))    # 设置横向坐标线
    line2 = w.create_line(200, 0, 200, 400,
                          fill="black",
                          dash=(4, 4))    # 设置纵向坐标线

    # 画圆脸
    w.create_oval((125, 70, 275, 220), fill='blue')

    # 画圆脸
    w.create_oval((140, 100, 260, 220), fill='white')

    # 画椭圆
    w.create_oval((200, 80, 230, 120), fill='white')

    # 画椭圆
    w.create_oval((170, 80, 200, 120), fill='white')

    # 画椭圆眼睛
    w.create_oval((203, 92, 215, 108), fill='black')

    # 画椭圆眼睛
    w.create_oval((185, 92, 197, 108), fill='black')

    # 画椭圆眼睛
    w.create_oval((206, 95, 212, 105), fill='white')

    # 画椭圆眼睛
    w.create_oval((188, 95, 194, 105), fill='white')

    # 画圆鼻子
    w.create_oval((193, 115, 207, 130), fill='red')

    # 嘴
    w.create_arc((140, 60, 260, 180),
                 style='arc',
                 start=240,
                 extent=60)    # 画弧线

    w.create_line(200, 130, 200, 180, fill="black")    # 竖线

    # 胡须
    w.create_line(215, 150, 245, 150, fill="black")    # 横线
    w.create_line(155, 150, 185, 150, fill="black")    # 横线

    w.create_line(158, 127, 185, 137, fill="black")
    w.create_line(215, 137, 242, 127, fill="black")

    w.create_line(158, 170, 185, 163, fill="black")
    w.create_line(215, 163, 242, 168, fill="black")

    # 身体
    w.create_rectangle(150, 200, 250, 285, fill="blue")     # 身体正前方

    w.create_arc((160, 190, 240, 270),
                 style='chord',
                 start=135,
                 extent=270,
                 fill='white')    # 画弧线

    w.create_line((150, 200, 250, 200),
                  fill="red",
                  width=10,
                  capstyle='round')    # 圆滑轮廓线

    w.create_arc((185, 270, 215, 300),
                 style='chord',
                 start=0,
                 extent=180,
                 fill='white')    # 画弧线
    w.create_line(185, 285, 215, 285, fill="white")
    # 画脚
    # 画椭圆
    w.create_oval((140, 275, 190, 295), fill='white')     # 左脚
    w.create_oval((210, 275, 260, 295), fill='white')     # 右脚

    # 画手
    w.create_polygon([150, 205, 150, 235, 120, 250, 120, 235],
                     outline="black",
                     fill="blue")    # 手臂多边形
    w.create_polygon([250, 205, 250, 235, 280, 250, 280, 235],
                     outline="black",
                     fill="blue")

    w.create_oval((110, 230, 135, 255), fill='white')     # 左圆形手掌
    w.create_oval((265, 230, 290, 255), fill='white')     # 右圆形手掌

    # 画铃铛
    w.create_oval((190, 200, 210, 220), fill='yellow')    # 铃铛中心圆
    w.create_line((191, 210, 209, 210),
                  fill="black",
                  width=5,
                  capstyle='round')    # 圆滑轮廓线
    w.create_line((192, 210, 208, 210),
                  fill="yellow",
                  width=3,
                  capstyle='round')    # 圆滑轮廓线

    w.create_oval((198, 213, 202, 217), fill='red')   # 中心小红点
    w.create_line(200, 218, 200, 220, fill="black")

    # 画口袋
    w.create_arc((170, 200, 230, 260),
                 style='chord',
                 start=180,
                 extent=180,
                 fill='white')    # 画弧线


# 定义函数实现人物眨眼
def bt1_later():
    # w = Canvas(root, width=400, height=400, bg='white').place(x=200, y=100)
    # 画虚线
    line1 = w.create_line(0, 200, 400, 200,
                          fill="black",
                          dash=(4, 4))
    line2 = w.create_line(200, 0, 200, 400,
                          fill="black",
                          dash=(4, 4))

    # 画圆脸
    w.create_oval((125, 70, 275, 220), fill='blue')

    # 画圆脸
    w.create_oval((140, 100, 260, 220), fill='white')

    # 画椭圆
    w.create_oval((200, 80, 230, 120), fill='white')

    # 画椭圆
    w.create_oval((170, 80, 200, 120), fill='white')

    # 闭左眼
    w.create_line((185, 100, 195, 105), fill='black')   # 闭左眼
    w.create_line((185, 105, 195, 105), fill='black')   # 闭左眼
    w.create_line((185, 110, 195, 105), fill='black')   # 闭左眼

    # 闭右眼
    w.create_line((205, 105, 215, 100), fill='black')   # 闭右眼
    w.create_line((205, 105, 215, 105), fill='black')   # 闭右眼
    w.create_line((205, 105, 215, 110), fill='black')   # 闭右眼

    # 画圆鼻子
    w.create_oval((193, 115, 207, 130), fill='red')

    # 嘴
    w.create_arc((140, 60, 260, 180),
                 style='arc',
                 start=240,
                 extent=60)    # 画弧线

    w.create_line(200, 130, 200, 180, fill="black")    # 竖线

    # 胡须
    w.create_line(215, 150, 245, 150, fill="black")    # 横线
    w.create_line(155, 150, 185, 150, fill="black")    # 横线

    w.create_line(158, 127, 185, 137, fill="black")
    w.create_line(215, 137, 242, 127, fill="black")

    w.create_line(158, 170, 185, 163, fill="black")
    w.create_line(215, 163, 242, 168, fill="black")

    # 身体
    w.create_rectangle(150, 200, 250, 285, fill="blue")

    w.create_arc((160, 190, 240, 270),
                 style='chord',
                 start=135,
                 extent=270,
                 fill='white')    # 画弧线

    # w.create_rectangle(150,195,250,205,fill='red')capstyle='round'

    w.create_line((150, 200, 250, 200),
                  fill="red",
                  width=10,
                  capstyle='round')    # 圆滑轮廓线

    w.create_arc((185, 270, 215, 300),
                 style='chord',
                 start=0,
                 extent=180,
                 fill='white')    # 画弧线
    w.create_line(185, 285, 215, 285, fill="white")
    # 画脚
    # 画椭圆
    w.create_oval((140, 275, 190, 295), fill='white')
    w.create_oval((210, 275, 260, 295), fill='white')

    # 画手
    w.create_polygon([150, 205, 150, 235, 120, 250, 120, 235],
                     outline="black",
                     fill="blue")    # 手臂多边形
    w.create_polygon([250, 205, 250, 235, 280, 250, 280, 235],
                     outline="black",
                     fill="blue")

    w.create_oval((110, 230, 135, 255), fill='white')
    w.create_oval((265, 230, 290, 255), fill='white')

    # 画铃铛
    w.create_oval((190, 200, 210, 220), fill='yellow')
    w.create_line((191, 210, 209, 210),
                  fill="black",
                  width=5,
                  capstyle='round')    # 圆滑轮廓线
    w.create_line((192, 210, 208, 210),
                  fill="yellow",
                  width=3,
                  capstyle='round')    # 圆滑轮廓线

    w.create_oval((198, 213, 202, 217), fill='red')
    w.create_line(200, 218, 200, 220, fill="black")

    # 画口袋
    w.create_arc((170, 200, 230, 260),
                 style='chord',
                 start=180,
                 extent=180,
                 fill='white')    # 画弧线
    # time.sleep(2)


# 定义函数实现四肢运动
def bt2_later():
    # w = Canvas(root, width=400, height=400, bg='white').place(x=200, y=100)
    # 画虚线
    line1 = w.create_line(0, 200, 400, 200, fill="black", dash=(4, 4))
    line2 = w.create_line(200, 0, 200, 400, fill="black", dash=(4, 4))
    w.create_rectangle((198, 50, 202, 70), fill='black')
    w.create_rectangle((180, 45, 220, 50), fill='yellow')
    # 画圆脸
    w.create_oval((125, 70, 275, 220), fill='blue')

    # 画圆脸
    w.create_oval((140, 100, 260, 220), fill='white')

    # 画椭圆
    w.create_oval((200, 80, 230, 120), fill='white')

    # 画椭圆
    w.create_oval((170, 80, 200, 120), fill='white')

    # 画椭圆眼睛
    w.create_oval((203, 92, 215, 108), fill='black')

    # 画椭圆眼睛
    w.create_oval((185, 92, 197, 108), fill='black')

    # 画椭圆眼睛
    w.create_oval((206, 95, 212, 105), fill='white')

    # 画椭圆眼睛
    w.create_oval((188, 95, 194, 105), fill='white')

    # 画圆鼻子
    w.create_oval((193, 115, 207, 130), fill='red')

    # 嘴
    w.create_arc((140, 60, 260, 180),
                 style='arc',
                 start=240,
                 extent=60)    # 画弧线
    w.create_rectangle((190, 180, 210, 200), fill='red')   # 实现伸舌头动作
    w.create_line(200, 130, 200, 180, fill="black")    # 竖线

    # 胡须
    w.create_line(215, 150, 245, 150, fill="black")    # 横线
    w.create_line(155, 150, 185, 150, fill="black")    # 横线

    w.create_line(158, 127, 185, 137, fill="black")
    w.create_line(215, 137, 242, 127, fill="black")

    w.create_line(158, 170, 185, 163, fill="black")
    w.create_line(215, 163, 242, 168, fill="black")

    # 身体
    # 修改参数实现四肢运动
    w.create_rectangle(150, 200, 250, 285, fill="blue")     # 身体正前方

    w.create_arc((160, 190, 240, 270),
                 style='chord',
                 start=135,
                 extent=270,
                 fill='white')    # 画弧线

    w.create_line((150, 200, 250, 200),
                  fill="red",
                  width=10,
                  capstyle='round')    # 圆滑轮廓线

    w.create_arc((170, 270, 230, 300),
                 style='chord',
                 start=0,
                 extent=180,
                 fill='white',
                 outline='white')    # 画弧线使双腿张开
    w.create_line(185, 285, 215, 285, fill="white")
    # 画脚
    # 画椭圆
    w.create_oval((130, 275, 170, 295), fill='white')
    w.create_oval((230, 275, 270, 295), fill='white')

    # 画手
    # 修改参数实现抬手
    w.create_polygon([150, 205, 150, 235, 120, 220, 120, 200],
                     outline="black",
                     fill="blue")    # 手臂多边形
    w.create_polygon([250, 205, 250, 235, 280, 220, 280, 200],
                     outline="black",
                     fill="blue")    # 右胳膊

    w.create_oval((100, 195, 125, 220), fill='white')
    w.create_oval((275, 193, 300, 220), fill='white')

    # 画铃铛
    w.create_oval((190, 200, 210, 220), fill='yellow')
    w.create_line((191, 210, 209, 210),
                  fill="black",
                  width=5,
                  capstyle='round')    # 圆滑轮廓线
    w.create_line((192, 210, 208, 210),
                  fill="yellow",
                  width=3,
                  capstyle='round')    # 圆滑轮廓线

    w.create_oval((198, 213, 202, 217), fill='red')
    w.create_line(200, 218, 200, 220, fill="black")

    # 画口袋
    w.create_arc((170, 200, 230, 260),
                 style='chord',
                 start=180,
                 extent=180,
                 fill='white')    # 画弧线


# 定义函数使人物颜色变化为黄色
def bt3_later():
    # 更改
    # 画虚线
    line1 = w.create_line(0, 200, 400, 200, fill="black", dash=(4, 4))
    line2 = w.create_line(200, 0, 200, 400, fill="black", dash=(4, 4))

    # 画圆脸
    w.create_oval((125, 70, 275, 220), fill='yellow')

    # 画圆脸
    w.create_oval((140, 100, 260, 220), fill='white')

    # 画椭圆
    w.create_oval((200, 80, 230, 120), fill='white')

    # 画椭圆
    w.create_oval((170, 80, 200, 120), fill='white')

    #  画椭圆眼睛
    w.create_oval((203, 92, 215, 108), fill='black')

    #  画椭圆眼睛
    w.create_oval((185, 92, 197, 108), fill='black')

    #  画椭圆眼睛
    w.create_oval((206, 95, 212, 105), fill='white')

    #  画椭圆眼睛
    w.create_oval((188, 95, 194, 105), fill='white')

    # 画圆鼻子
    w.create_oval((193, 115, 207, 130), fill='red')

    # 嘴
    w.create_arc((140, 60, 260, 180),
                 style='arc',
                 start=240,
                 extent=60)    # 画弧线

    w.create_line(200, 130, 200, 180, fill="black")    # 竖线

    # 胡须
    w.create_line(215, 150, 245, 150, fill="black")    # 横线
    w.create_line(155, 150, 185, 150, fill="black")    # 横线

    w.create_line(158, 127, 185, 137, fill="black")
    w.create_line(215, 137, 242, 127, fill="black")

    w.create_line(158, 170, 185, 163, fill="black")
    w.create_line(215, 163, 242, 168, fill="black")

    # 身体
    w.create_rectangle(150, 200, 250, 285, fill="yellow")

    w.create_arc((160, 190, 240, 270),
                 style='chord',
                 start=135,
                 extent=270,
                 fill='white')    # 画弧线

    # w.create_rectangle(150,195,250,205,fill='red')capstyle='round'

    w.create_line((150, 200, 250, 200),
                  fill="red",
                  width=10,
                  capstyle='round')    # 圆滑轮廓线

    w.create_arc((185, 270, 215, 300),
                 style='chord',
                 start=0,
                 extent=180,
                 fill='white')    # 画弧线
    w.create_line(185, 285, 215, 285, fill="white")
    # 画脚
    # 画椭圆
    w.create_oval((140, 275, 190, 295), fill='white')
    w.create_oval((210, 275, 260, 295), fill='white')

    # 画手
    w.create_polygon([150, 205, 150, 235, 120, 250, 120, 235],
                     outline="black",
                     fill="yellow")    # 手臂多边形
    w.create_polygon([250, 205, 250, 235, 280, 250, 280, 235],
                     outline="black",
                     fill="yellow")

    w.create_oval((110, 230, 135, 255), fill='white')
    w.create_oval((265, 230, 290, 255), fill='white')

    # 画铃铛
    w.create_oval((190, 200, 210, 220), fill='yellow')
    w.create_line((191, 210, 209, 210),
                  fill="black",
                  width=5,
                  capstyle='round')    # 圆滑轮廓线
    w.create_line((192, 210, 208, 210),
                  fill="yellow",
                  width=3,
                  capstyle='round')    # 圆滑轮廓线

    w.create_oval((198, 213, 202, 217), fill='red')
    w.create_line(200, 218, 200, 220, fill="black")

    # 画口袋
    w.create_arc((170, 200, 230, 260),
                 style='chord',
                 start=180,
                 extent=180,
                 fill='white')    # 画弧线


s = sched.scheduler(time.time, time.sleep)


# 定义递归函数实现重新布局画布
def bt1_while():
    cv_white()  # 重新布局画布
    bt1_age()   # 设置为原始人物

    #  递归点击实现眨眼
    b1 = Button(root,
                text='点击眨眼',
                cursor='hand2',
                font=('楷体', 15),
                comman=bt1,
                bg='#E9F578').place(x=200, y=520)


# 眨眼
def bt1():
    cv_white()  # 重新布局画布
    bt1_later()     # 调用眨眼函数

    b1 = Button(root,
                text='点击眨眼',
                cursor='hand2',
                font=('楷体', 15),
                comman=bt1_while,
                bg='#E9F578').place(x=200, y=520)


# 定义递归函数实现重新布局画布
def bt2_while():
    cv_white()  # 重新布局画布
    bt1_age()   # 定义原始人物
    b2 = Button(root,
                text='运动四肢',
                cursor='hand2',
                font=('楷体', 15),
                comman=bt2,
                bg='#DC78F5').place(x=350, y=520)


# 运动四肢
def bt2():
    cv_white()  # 重新布局画布
    bt2_later()     # 调用运动函数
    b1 = Button(root,
                text='运动四肢',
                cursor='hand2',
                font=('楷体', 15),
                comman=bt2_while,
                bg='#DC78F5').place(x=350, y=520)


# 定义递归函数实现重新布局画布
def bt3_while():
    cv_white()  # 重新布局画布
    bt1_age()   # 定义原始人物
    b3 = Button(root,
                text='色彩装饰',
                cursor='hand2',
                font=('楷体', 15),
                comman=bt3,
                bg='#78B4F5').place(x=510, y=520)


# 色彩装饰
def bt3():
    cv_white()  # 重新布局画布
    bt3_later()     # 调用颜色改变函数
    b3 = Button(root,
                text='色彩装饰',
                cursor='hand2',
                font=('楷体', 15),
                comman=bt3_while,
                bg='#78B4F5').place(x=510, y=520)


bt1_age()   # 第一次界面打开时实现原始人物布局

# 定义点击眨眼按钮
b1 = Button(root,
            text='点击眨眼',
            cursor='hand2',
            font=('楷体', 15),
            comman=bt1,
            bg='#E9F578').place(x=200, y=520)

# 定义运动四肢按钮的
b2 = Button(root,
            text='运动四肢',
            cursor='hand2',
            font=('楷体', 15),
            comman=bt2,
            bg='#DC78F5').place(x=350, y=520)

# 定义色彩装饰按钮
b3 = Button(root,
            text='色彩装饰',
            cursor='hand2',
            font=('楷体', 15),
            comman=bt3,
            bg='#78B4F5').place(x=510, y=520)

# 页面窗口循环
mainloop()
