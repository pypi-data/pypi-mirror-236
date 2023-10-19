#
# @author Jason Q. Wu
# @create 2021-04-21 14:19
#
import turtle
import random


class Picture:
    def __init__(self, width=1200, height=846, x=0, y=0, speed=0, size=1):
        self.__pen = turtle.Turtle()
        self.__screen = self.pen.screen
        self.__range = (420, 220)
        self.__color = (random.random(), random.random(), random.random())
        self.screen.setup(width=width, height=height+2, startx=x, starty=y)
        self.pen.speed(speed)
        self.pen.pensize(size)

    def random_range(min, max):
        return min + (max - min) * r.random()

    @property
    def screen(self):
        return self.__screen

    @screen.setter
    def screen(self, value):
        self.__screen = value

    @property
    def pen(self):
        return self.__pen

    @pen.setter
    def pen(self, value):
        self.__pen = value

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(value):
        self.__color = value

    def title(self, title):
        self.screen.title(title)

    def bgcolor(self, bgcolor):
        self.screen.bgcolor(bgcolor)

    def hideturtle(self):
        self.__window.hideturtle()

    def showturtle(self):
        self.__window.showturtle()

    def move_to(self, x, y):
        self.pen.up()
        self.pen.goto(x, y)
        self.pen.down()

    def draw_to(self, x, y):
        self.pen.down()
        self.pen.goto(x, y)

    def circle(self, radius, x, y):
        pos_x, pos_y = self.pen.pos()
        self.move_to(x, y)
        self.pen.circle(radius)
        self.move_to(pos_x, pos_x)

    def rectangle(self, x, y, width, height):
        pos_x, pos_y = self.pen.pos()
        self.move_to(x, y)
        self.pen.forward(width)
        self.pen.left(90)
        self.pen.forward(height)
        self.pen.left(90)
        self.pen.forward(width)
        self.pen.left(90)
        self.pen.forward(height)
        self.pen.left(90)
        self.move_to(pos_x, pos_x)

    def triangle(self, x1, y1, x2, y2, x3, y3):
        pos_x, pos_y = self.pen.pos()
        self.move_to(x1, y1)
        self.draw_to(x2, y2)
        self.pen.left(135)
        self.draw_to(x3, y3)
        self.pen.left(135)
        self.draw_to(x1, y1)
        self.pen.left(90)
        self.move_to(pos_x, pos_x)

    def polygon(self, color, edges):
        self.pen.begin_fill()
        self.pen.fillcolor(color)
        for i in range(edges):
            self.pen.forward(20)
            self.pen.left(180 * (edges - 1) / edges)
        self.pen.end_fill()

    def tree(self, pen_size, length, num):
        pen_size = pen_size * 3 / 4
        length = length * 3 / 4
        self.pen.pensize(pen_size)
        self.pen.pencolor(random.randint(0, 255),
                          random.randint(0, 255),
                          random.randint(0, 255))
        self.pen.left(45)
        self.pen.forward(length)

        if (num < 14):
            draw_tree(pen_size, length, num + 1)

        self.pen.backward(length)
        self.pen.right(90)
        self.pen.forward(length)

        if (num < 14):
            draw_tree(pen_size, length, num + 1)

        self.pen.backward(length)
        self.pen.left(45)
        self.pen.pensize(pen_size)

        # for i in range(4):
        #     self.pen.forward(50)
        #     self.pen.left(90)
        # self.pen.left(2)
        #


if __name__ == '__main__':
    window = Picture(420, 300)
    window.pen.hideturtle()
    window.screen.tracer(False)
    window.title("Jason 的海龟图")
    window.bgcolor("orange")
    window.circle(40, 120, 40)
    window.rectangle(-50, -50, 50, 50)
    window.triangle(-50, 0, 0, 0, -25, 50)
    window.circle(25, 0, -75)
    window.move_to(-220, -55)
    window.pen.forward(400)
    window.screen.tracer(True)
    window.screen.mainloop()
