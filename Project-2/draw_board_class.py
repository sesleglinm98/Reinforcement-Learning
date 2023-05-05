import turtle
import time

class board_class():

    def __init__(self, agent_position, evil_man_position, castle_position):
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
        
        agent_x_pos = agent_position[0]
        agent_y_pos = agent_position[1]
        self.agent_x = self.start_x + self.square_size/2 + (agent_x_pos * self.square_size)
        self.agent_y = self.start_y - self.square_size/2 - (agent_y_pos * self.square_size)
        
        evil_man_x_pos = evil_man_position[0]
        evil_man_y_pos = evil_man_position[1]
        self.evil_man_x = self.start_x + self.square_size/2 + (evil_man_x_pos * self.square_size)
        self.evil_man_y = self.start_y - self.square_size/2 - (evil_man_y_pos * self.square_size)
        
        castle_x_pos = castle_position[0]
        castle_y_pos = castle_position[1]
        self.castle_x = self.start_x + self.square_size/2 + (castle_x_pos * self.square_size)
        self.castle_y = self.start_y - self.square_size/2 - (castle_y_pos * self.square_size)

        self.reward_x = self.evil_man_x
        self.reward_y = self.evil_man_y

        self.agent_turtle = turtle.Turtle()
        self.evil_man_turtle = turtle.Turtle()
        self.castle_turtle = turtle.Turtle()
        self.reward_turtle = turtle.Turtle()

        self.write_turtle = turtle.Turtle()
        self.write_turtle.hideturtle()

        # adding images on board
        path = "C:/Users/sesle/Desktop/Workspace/ReinforcementLearning/Github/Project-2/draw_board_gifs/"
        turtle.addshape(path + "edited-diamond.gif")
        turtle.addshape(path + "edited-hero.gif")
        turtle.addshape(path + "castle.gif")
        turtle.addshape(path + "edited-diamonded-hero.gif")
        turtle.addshape(path + "winner-home.gif")
        turtle.addshape(path + "edited-dragon.gif")

        # animation frames
        # frame_path = "C:/Users/sesle/Desktop/Workspace/ReinforcementLearning/Github/q-learning/animation/funny-cat-frames/"
        # turtle.addshape(frame_path + "frame_0.gif")
        # turtle.addshape(frame_path + "frame_1.gif")
        # turtle.addshape(frame_path + "frame_2.gif")
        # turtle.addshape(frame_path + "frame_3.gif")
        # turtle.addshape(frame_path + "frame_4.gif")

        self.animation_counter = 0

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

        self.agent_turtle.speed(2)
        self.agent_turtle.shape(path + "edited-hero.gif")
        self.agent_turtle.color('black')
        self.agent_turtle.penup()
        self.agent_turtle.goto(self.agent_x, self.agent_y)
        self.agent_turtle.shapesize(2, 2)

        self.evil_man_turtle.speed(0)
        self.evil_man_turtle.shape(path + "edited-dragon.gif")
        self.evil_man_turtle.color('red')
        self.evil_man_turtle.penup()
        self.evil_man_turtle.goto(self.evil_man_x, self.evil_man_y)
        self.evil_man_turtle.shapesize(2, 2)
        
        self.castle_turtle.speed(0)
        self.castle_turtle.shape(path + "castle.gif")
        self.castle_turtle.color('green')
        self.castle_turtle.penup()
        self.castle_turtle.goto(self.castle_x, self.castle_y)
        self.castle_turtle.shapesize(2, 2)

        self.reward_turtle.speed(0)
        self.reward_turtle.shape(path + "edited-diamond.gif")
        self.reward_turtle.color('green')
        self.reward_turtle.penup()
        self.reward_turtle.goto(self.reward_x, self.reward_y)
        self.reward_turtle.shapesize(2, 2)
        self.reward_turtle.hideturtle()

        self.reward_taken = False # itemin alinip alinmadigi tutulur
        self.evil_man_dead = False  # kotu adamin olup olmedigi tutulur

        turtle.update() # tracer ile animasyon devre disi birakildigi icin, ekranin guncellenmesini saglar
        turtle.tracer(1)

    def make_action(self, action, movement, agent_position, evil_man_position, castle_position):
        self.agent_x = self.start_x + self.square_size/2 + (agent_position[0] * self.square_size)
        self.agent_y = self.start_y - self.square_size/2 - (agent_position[1] * self.square_size)
        self.evil_man_x = self.start_x + self.square_size/2 + (evil_man_position[0] * self.square_size)
        self.evil_man_y = self.start_y - self.square_size/2 - (evil_man_position[1] * self.square_size)
        self.castle_x = self.start_x + self.square_size/2 + (castle_position[0] * self.square_size)
        self.castle_y = self.start_y - self.square_size/2 - (castle_position[1] * self.square_size)

        path = "C:/Users/sesle/Desktop/Workspace/ReinforcementLearning/Github/Project-2/draw_board_gifs/"
        if movement == 0:
            self.agent_turtle.setx(self.agent_x)
            self.agent_turtle.sety(self.agent_y)
            self.evil_man_turtle.setx(self.evil_man_x)
            self.evil_man_turtle.sety(self.evil_man_y)
            self.castle_turtle.setx(self.castle_x)
            self.castle_turtle.sety(self.castle_y)
        elif movement == 1:  # evil oldurulmesi
            self.evil_man_turtle.hideturtle()
            self.reward_turtle.showturtle()
        elif movement == 2:  # reward alinmasi
            self.reward_turtle.hideturtle()
            self.agent_turtle.shape(path + "edited-diamonded-hero.gif")
        elif movement == 3:  # rewardin sahaya birakilmasi
            self.reward_turtle.setx(self.agent_x)
            self.reward_turtle.sety(self.agent_y)
            self.reward_turtle.showturtle()
            self.agent_turtle.shape(path + "edited-hero.gif")
        elif movement == 4:  # basarili reward castle'a konmasi
            print("wonnnn")
            self.write_turtle.setposition(0, 350)
            self.write_turtle.write("WON", align="center", font=('Courier', 24, 'normal'))
            time.sleep(1)
            # self.item_turtle.setx(self.started_item_pos_x)
            # self.item_turtle.sety(self.started_item_pos_y)
            self.reward_turtle.shapesize(2, 2)

    def move_x_axis(self, direction):
        if direction == "right":
            self.agent_turtle.setx(self.agent_turtle.position()[0] + 50)
            if self.reward_taken: # item alinmis ise carrier ile beraber hareket etmesi icin
                self.reward_turtle.setx(self.reward_turtle.position()[0] + 50)
        elif direction == "left":
            self.agent_turtle.setx(self.agent_turtle.position()[0] - 50)
            if self.reward_taken: # item alinmis ise carrier ile beraber hareket etmesi icin
                self.reward_turtle.setx(self.reward_turtle.position()[0] - 50)
                
    def move_y_axis(self, direction):
        if direction == "up":
            self.agent_turtle.sety(self.agent_turtle.position()[1] + 50)
            if self.reward_taken: # item alinmis ise hareket etmesi icin
                self.reward_turtle.sety(self.reward_turtle.position()[1] + 50)
        elif direction == "down":
            self.agent_turtle.sety(self.agent_turtle.position()[1] - 50)
            if self.reward_taken: # item alinmis ise hareket etmesi icin
                self.reward_turtle.sety(self.reward_turtle.position()[1] - 50)

    def picked_up_animation(self):
        frame_path = "C:/Users/sesle/Desktop/Workspace/ReinforcementLearning/Github/q-learning/animation/funny-cat-frames/"
        cnt = self.animation_counter
        self.agent_turtle.shape(frame_path + "frame_" + str(cnt) + ".gif")
        self.animation_counter += 1
        if self.animation_counter == 4:
            self.animation_counter = 0

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
            str_action = "pull trigger"
        elif action == 5:
            str_action = "pickup"
        elif action == 6:
            str_action = "dropoff"
        else:
            str_action = "unknown"

        self.write_turtle.write("action: {}".format(str_action), align="center", font=('Courier', 24, 'normal'))

    def reset(self):
        turtle.resetscreen()