from draw_board_class import board_class
from field_class import Field

import numpy as np
import time
import random

import turtle

class Q_Learning():

    def __init__(self, size, agent_position, evil_man_position, castle_position, randomize):
        self.size = size
        self.agent_position = agent_position
        self.evil_man_position = evil_man_position
        self.castle_position =castle_position

        self.randomize = randomize

    def random_position(self):
        self.agent_position = (random.randint(0, 9), random.randint(0, 9))

        numbers_x = list(range(0,10))
        numbers_y = list(range(0,10))
        numbers_x.remove(self.agent_position[0])
        numbers_y.remove(self.agent_position[1])
        self.evil_man_position = (random.choice(numbers_x), random.choice(numbers_y))

    # implementing q-learning algorithm
    def train_q_learning(self):

        self.field = Field(self.size, self.agent_position, self.evil_man_position, self.castle_position)
        done = False

        number_of_states = self.field.get_number_of_states()
        number_of_actions = 7

        # q_table ogrenmenin gerceklestigi yerdir, buradaki her bir durum-aksiyon elemani icin agirlik hesaplanir
        self.q_table = np.zeros((number_of_states, number_of_actions))  # butun durumlar ve bu durumlara karsilik aksiyonlarin sayisi kadar
                                                                # boyutta bir q_table olusturulur, butun elemanlari 0 ile doldurulur

        self.epsilon = 0.2  # explore ve exploit'in secimi icin probability degeridir
                    # 0.1 ihtimal ile explore secilirse random bir secim yapar ve onceden gidilmeyen yollari acmaya yarar
                    # kalan ihtimallerde ise exploit secilmis olur, o anki duruma gore aksiyonlardan ek yuksek reward-degeri alinir, yani en yuksek rewardli aksiyon secilmis olur
        alpha = 0.1    # learning rate
        gamma = 0.6

        for i in range(1050):
            if i % 100 == 0:
                print("i: ", i)
            if i == 1000:
                np.save("C:/Users/sesle/Desktop/Workspace/ReinforcementLearning/Github/Project-2/q_table_10bin.npy", self.q_table) # egitilen q_table save edilir
            if self.randomize:
                self.random_position()
                self.field = Field(self.size, self.agent_position, self.evil_man_position, self.castle_position)
            else:
                self.field = Field(self.size, self.agent_position, self.evil_man_position, self.castle_position)  # her dongunun basinda butun herseyi sifirlamak icin field objesi bastan olusturulur
            if i >= 1000:
                self.epsilon = 0.2
                self.board = board_class(self.agent_position, self.evil_man_position, self.castle_position)      
            done =  False
            step_number = 0  # bir olayi bitirmek icin kac aksiyon alindigini tutar
            while not done:
                step_number += 1
                state = self.field.get_state()
                if random.uniform(0, 1) < self.epsilon:  # 0-1 arasi random sayi secilir, epsilon degeri ile kiyaslanir
                    action = random.randint(0, 6)  # random bir aksiyon secilir

                else:
                    action = np.argmax(self.q_table[state])  # bu ifade su demektir: q_table'dan o anki state column degerlerini al, yani o state'in aksiyon degerlerini al
                                                        # ilk dongu icin q_table[state] ifadesi = [0, 0, 0, 0, 0, 0] dizisini dondurur, yani her aksiyonun degerleridir
                                                        # np.argmax ile bu degerlerden en buyuk olan secilir ve o degerin aksiyonu alinir
                                                        # bu degerler her iterasyonda asagida guncellenecektir, boylece her seferinde optimum aksiyonlar secilmeye calisilir

                reward, movement, done = self.field.make_action(action)
                
                # q-learning'in ogrenme hesabi su sekilde yapilir -> Q[state, action] = (1 - alpha) * Q[state, action] + alpha * (reward + gamma * max(Q[new_state]) - Q[state, action])
                new_state = self.field.get_state()
                new_state_max = np.max(self.q_table[new_state])

                self.q_table[state, action] = (1 - alpha) * self.q_table[state, action] + alpha*(reward + gamma * new_state_max - self.q_table[state, action])

                if step_number % 30000 == 0:
                    print("step_number: ", step_number)
                # if i % 3 == 0 and i != 0:
                if i >= 1000:
                    print("i: ", i, "step_number: ", step_number)
                    self.evaluate_rl_while_training(i, step_number, action, movement)
            if i>= 1000:
                self.board.reset()

    def evaluate_rl_while_training(self, i, step_number, action, movement):  
        self.board.write_info(i, step_number, action)
        self.board.make_action(action, movement, self.field.agent_position, self.field.evil_man_position, self.field.castle_position)

        return step_number
    
    def evaluate_rl(self, trained_q_table, random_position, random_movement):
        if random_position:
            self.random_position()
        self.field = Field(self.size, self.agent_position, self.evil_man_position, self.castle_position)
        self.board = board_class(self.agent_position, self.evil_man_position, self.castle_position)
        
        done = False
        step_number = 0  # olayi kac adimda tamamladigini tutar
        i = 0

        epsilon = 0.2
        while not done:
            step_number = step_number + 1
            state = self.field.get_state()

            if random_movement:
                if random.uniform(0, 1) < epsilon:  # 0-1 arasi random sayi secilir, epsilon degeri ile kiyaslanir
                    action = random.randint(0, 6)  # random bir aksiyon secilir
                else:
                    action = np.argmax(trained_q_table[state])
            else:
                action = np.argmax(trained_q_table[state])
                if step_number >= 130:  # algoritmanin takili kalmasini onlemek icin, yoksa sonsuz kadar hep ayni hareketi tekrarliyor
                    print("fail")
                    done = True

            reward, movement, done = self.field.make_action(action)

            self.evaluate_rl_while_training(i, step_number, action, movement)
            time.sleep(0.1)

        self.board.reset()
        return step_number

    def manual_test(self):
        self.field = Field(self.size, self.agent_position, self.evil_man_position, self.castle_position)  # her dongunun basinda butun herseyi sifirlamak icin field objesi bastan olusturulur
        self.board = board_class(self.agent_position, self.evil_man_position, self.castle_position)      

        action = 0
        for i in range(3):
            reward, movement, done = self.field.make_action(action)
            self.evaluate_rl_while_training()
        
        action = 3
        for i in range(5):
            reward, movement, done = self.field.make_action(action)
            self.evaluate_rl_while_training()

        action = 4
        reward, movement, done = self.field.make_action(action)
        self.evaluate_rl_while_training()

        action = 0
        reward, movement, done = self.field.make_action(action)
        self.evaluate_rl_while_training()

        action = 5
        reward, movement, done = self.field.make_action(action)
        self.evaluate_rl_while_training()

        action = 3
        for i in range(7):
            reward, movement, done = self.field.make_action(action)
            self.evaluate_rl_while_training()

        action = 6
        reward, movement, done = self.field.make_action(action)
        self.evaluate_rl_while_training()

        turtle.done()