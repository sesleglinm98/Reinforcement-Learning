import turtle
import time

class board_class():

    def __init__(self, item_start, carrier_start, drop_off_start):
    # def __init__(self):
        board_size = 10
        self.square_size = 50
        self.start_x = -250
        self.start_y = 250

        self.item_size = 40
        carrier_size = 40
        drop_region_size = 40

        # position[0]=0 -> -250 + 25  -> start_x + square_size/2 + 0 * square_size
        # position[0]=1 -> -250 + 75  -> start_x + square_size/2 + 1 * square_size
        # position[0]=2 -> -250 + 125 -> start_x + square_size/2 + 2 * square_size
        
        item_x_pos = item_start[0]
        item_y_pos = item_start[1]
        self.item_x = self.start_x + self.square_size/2 + (item_x_pos * self.square_size)
        self.item_y = self.start_y - self.square_size/2 - (item_y_pos * self.square_size)
        
        carrier_x_pos = carrier_start[0]
        carrier_y_pos = carrier_start[1]
        self.carrier_x = self.start_x + self.square_size/2 + (carrier_x_pos * self.square_size)
        self.carrier_y = self.start_y - self.square_size/2 - (carrier_y_pos * self.square_size)
        
        drop_region_x_pos = drop_off_start[0]
        drop_region_y_pos = drop_off_start[1]
        self.drop_region_x = self.start_x + self.square_size/2 + (drop_region_x_pos * self.square_size)
        self.drop_region_y = self.start_y - self.square_size/2 - (drop_region_y_pos * self.square_size)

        self.started_item_pos_x = self.item_x
        self.started_item_pos_y = self.item_y

        item_turtle = turtle.Turtle()
        carrier_turtle = turtle.Turtle()
        drop_region_turtle = turtle.Turtle()
        self.item_turtle = item_turtle
        self.carrier_turtle = carrier_turtle
        self.drop_region_turtle = drop_region_turtle

        self.write_turtle = turtle.Turtle()
        self.write_turtle.hideturtle()

        # adding images on board
        path = "C:/Users/sesle/Desktop/Workspace/ReinforcementLearning/Scratch-Tutorials/create-your-rl-environment/"
        turtle.addshape(path + "edited-apple.gif")
        turtle.addshape(path + "funny-cat-hug-edited.gif")
        turtle.addshape(path + "home2.gif")
        turtle.addshape(path + "applecatrun-apple-cat.gif")
        turtle.addshape(path + "winner-home.gif")

        turtle.speed(0)  # cizim hizini ayarlar, 0 en hizlisi
        turtle.hideturtle() # cizim okunu gorunmez yapar
        turtle.tracer(0) # bunun ile animasyon devre disi birakilir, bu olmadiginda tum cizimler animasyon seklinde cizilir

        for i in range(board_size):
            for j in range(board_size):
                if (i + j) % 2 == 0:
                    turtle.fillcolor("white")
                else:
                    turtle.fillcolor("gray")
                turtle.penup()
                turtle.goto(self.start_x + i * self.square_size, self.start_y - j * self.square_size)
                turtle.pendown()
                turtle.begin_fill()
                for k in range(4):
                    turtle.forward(self.square_size)
                    turtle.right(90)
                turtle.end_fill()

        self.carrier_turtle.speed(2)
        # self.carrier_turtle.shape('circle')
        self.carrier_turtle.shape(path + "funny-cat-hug-edited.gif")
        self.carrier_turtle.color('black')
        self.carrier_turtle.penup()
        self.carrier_turtle.goto(self.carrier_x, self.carrier_y)
        self.carrier_turtle.shapesize(2, 2)

        self.item_turtle.speed(0)
        # self.item_turtle.shape('circle')
        self.item_turtle.shape(path + "edited-apple.gif")
        self.item_turtle.color('red')
        self.item_turtle.penup()
        self.item_turtle.goto(self.item_x, self.item_y)
        self.item_turtle.shapesize(2, 2)
        
        self.drop_region_turtle.speed(0)
        # self.drop_region_turtle.shape('circle')
        self.drop_region_turtle.shape(path + "home2.gif")
        self.drop_region_turtle.color('green')
        self.drop_region_turtle.penup()
        self.drop_region_turtle.goto(self.drop_region_x, self.drop_region_y)
        self.drop_region_turtle.shapesize(2, 2)

        self.picked_up_item = False # itemin alinip alinmadigi tutulur

        turtle.update() # tracer ile animasyon devre disi birakildigi icin, ekranin guncellenmesini saglar
        turtle.tracer(1)

    def move_carrier(self, carrier_x_pos, carrier_y_pos):
        self.carrier_x = self.start_x + self.square_size/2 + (carrier_x_pos * self.square_size)
        self.carrier_y = self.start_y - self.square_size/2 - (carrier_y_pos * self.square_size)
        self.carrier_turtle.setx(self.carrier_x)
        self.carrier_turtle.sety(self.carrier_y)
        # self.carrier_turtle.goto(carrier_x, carrier_y)

        # turtle.update()
        # turtle.done()

    def move_carrier_upgraded(self, action, item_in_car, carrier_x_pos, carrier_y_pos):
        self.carrier_x = self.start_x + self.square_size/2 + (carrier_x_pos * self.square_size)
        self.carrier_y = self.start_y - self.square_size/2 - (carrier_y_pos * self.square_size)
        
        if action == 0 or action == 1 or action == 2 or action == 3:
            self.carrier_turtle.setx(self.carrier_x)
            self.carrier_turtle.sety(self.carrier_y)
            if item_in_car:
                self.item_turtle.setx(self.carrier_x)
                self.item_turtle.sety(self.carrier_y)
        elif action == 4:
            self.item_turtle.shapesize(1, 1)
        elif action == 5:
            if self.item_turtle.position() == self.drop_region_turtle.position():
                print("wonnnn")
                self.write_turtle.setposition(0, 350)
                self.write_turtle.write("WON", align="center", font=('Courier', 24, 'normal'))
                time.sleep(1)
                self.item_turtle.setx(self.started_item_pos_x)
                self.item_turtle.sety(self.started_item_pos_y)
                self.item_turtle.shapesize(2, 2)
            else:
                self.item_turtle.shapesize(2, 2)

    def move_x_axis(self, direction):
        if direction == "right":
            self.carrier_turtle.setx(self.carrier_turtle.position()[0] + 50)
            if self.picked_up_item: # item alinmis ise carrier ile beraber hareket etmesi icin
                self.item_turtle.setx(self.item_turtle.position()[0] + 50)
        elif direction == "left":
            self.carrier_turtle.setx(self.carrier_turtle.position()[0] - 50)
            if self.picked_up_item: # item alinmis ise carrier ile beraber hareket etmesi icin
                self.item_turtle.setx(self.item_turtle.position()[0] - 50)
                
    def move_y_axis(self, direction):
        if direction == "up":
            self.carrier_turtle.sety(self.carrier_turtle.position()[1] + 50)
            if self.picked_up_item: # item alinmis ise hareket etmesi icin
                self.item_turtle.sety(self.item_turtle.position()[1] + 50)
        elif direction == "down":
            self.carrier_turtle.sety(self.carrier_turtle.position()[1] - 50)
            if self.picked_up_item: # item alinmis ise hareket etmesi icin
                self.item_turtle.sety(self.item_turtle.position()[1] - 50)

    def pickup_acion(self):
        if self.item_turtle.position() == self.carrier_turtle.position():
            # self.item_turtle.shapesize(1, 1)
            path = "C:/Users/sesle/Desktop/Workspace/ReinforcementLearning/Scratch-Tutorials/create-your-rl-environment/"
            self.carrier_turtle.shape(path + "applecatrun-apple-cat.gif")
            self.picked_up_item = True
            self.item_turtle.hideturtle()

    def drop_off_action(self):
        path = "C:/Users/sesle/Desktop/Workspace/ReinforcementLearning/Scratch-Tutorials/create-your-rl-environment/"
        if self.item_turtle.position() == self.drop_region_turtle.position(): # itemin droppoff bolgesinde birakilmasi durumu
            self.carrier_turtle.hideturtle()
            self.item_turtle.hideturtle()
            self.drop_region_turtle.shape(path + "winner-home.gif")
            # turtle.done() # dikkat et bunun cikarilmasi gerekebilir
        else:
            self.picked_up_item = False
            # self.item_turtle.shapesize(2, 2)
            self.carrier_turtle.shape(path + "funny-cat-hug-edited.gif")
            self.item_turtle.showturtle()

    def write_info(self, iteration, step, action):
        # self.score.write("Hit: {}   Missed: {}".format(self.hit, self.miss), align='center', font=('Courier', 24, 'normal'))
        # turtle.backward((turtle.getscreen().window_width() / 2) - 10)
        self.write_turtle.clear()
        self.write_turtle.penup()
        self.write_turtle.setposition(0, 300)
        self.write_turtle.write("iteration i: {} Step: {}".format(iteration, step), align="center", font=('Courier', 24, 'normal'))
        self.write_turtle.setposition(0, 260)
        str_action = ""
        if action == 0:
            str_action = "down"
        elif action == 1:
            str_action = "up"
        elif action == 2:
            str_action = "left"
        elif action == 3:
            str_action = "right"
        elif action == 4:
            str_action = "pickup"
        elif action == 5:
            str_action = "dropoff"
        else:
            str_action = "unknown"

        self.write_turtle.write("action: {}".format(str_action), align="center", font=('Courier', 24, 'normal'))

    def reset(self):
        turtle.resetscreen()

# board = board_class((0, 0), (0, 0), (9, 9))

# board.pickup_acion()
# board.move_carrier(0, 0)
# board.move_carrier(9, 5)

# board.move_x_axis("left")
# board.move_y_axis("down")
# board.move_x_axis("left")
# board.write_info(1, 10, 0)

# turtle.done()


