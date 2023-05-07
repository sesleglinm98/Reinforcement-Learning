from draw_board_class import board_class
from field_class import Field

import numpy as np
import time
import random

class Q_Learning():

    def __init__(self, size, item_start, start_position, item_drop_off, randomize):
        self.size = size
        self.item_start = item_start
        self.start_position = start_position
        self.item_drop_off = item_drop_off

        self.randomize = randomize

    def random_position(self):
        self.item_start = (random.randint(0, 9), random.randint(0, 9))
        self.start_position = (random.randint(0, 9), random.randint(0, 9))

        # self.item_drop_off = (random.randint(0, 9), random.randint(0, 9))

    # implementing q-learning algorithm
    def train_q_learning(self):

        field = Field(self.size, self.item_start, self.start_position, self.item_drop_off)
        done = False

        number_of_states = field.get_number_of_states()
        number_of_actions = 6

        # q_table ogrenmenin gerceklestigi yerdir, buradaki her bir durum-aksiyon elemani icin agirlik hesaplanir
        self.q_table = np.zeros((number_of_states, number_of_actions))  # butun durumlar ve bu durumlara karsilik aksiyonlarin sayisi kadar
                                                                # boyutta bir q_table olusturulur, butun elemanlari 0 ile doldurulur

        epsilon = 0.1  # explore ve exploit'in secimi icin probability degeridir
                    # 0.1 ihtimal ile explore secilirse random bir secim yapar ve onceden gidilmeyen yollari acmaya yarar
                    # kalan ihtimallerde ise exploit secilmis olur, o anki duruma gore aksiyonlardan ek yuksek reward-degeri alinir, yani en yuksek rewardli aksiyon secilmis olur
        alpha = 0.1    # learning rate
        gamma = 0.6

        for i in range(3000000):
            if self.randomize:
                self.random_position()
                # print("item_start:: ", self.item_start)
                field = Field(self.size, self.item_start, self.start_position, self.item_drop_off)
            else:
                field = Field(self.size, self.item_start, self.start_position, self.item_drop_off)  # her dongunun basinda butun herseyi sifirlamak icin field objesi bastan olusturulur
            done =  False
            step_number = 0  # bir olayi bitirmek icin kac aksiyon alindigini tutar
            while not done:
                step_number += 1
                state = field.get_state()
                if random.uniform(0, 1) < epsilon:  # 0-1 arasi random sayi secilir, epsilon degeri ile kiyaslanir
                    action = random.randint(0, 5)  # random bir aksiyon secilir

                else:
                    # print("q_table[state]: ", q_table[0])
                    action = np.argmax(self.q_table[state])  # bu ifade su demektir: q_table'dan o anki state column degerlerini al, yani o state'in aksiyon degerlerini al
                                                        # ilk dongu icin q_table[state] ifadesi = [0, 0, 0, 0, 0, 0] dizisini dondurur, yani her aksiyonun degerleridir
                                                        # np.argmax ile bu degerlerden en buyuk olan secilir ve o degerin aksiyonu alinir
                                                        # bu degerler her iterasyonda asagida guncellenecektir, boylece her seferinde optimum aksiyonlar secilmeye calisilir


                reward, done = field.make_action(action)

                # q-learning'in ogrenme hesabi su sekilde yapilir -> Q[state, action] = (1 - alpha) * Q[state, action] + alpha * (reward + gamma * max(Q[new_state]) - Q[state, action])
                new_state = field.get_state()
                new_state_max = np.max(self.q_table[new_state])

                self.q_table[state, action] = (1 - alpha) * self.q_table[state, action] + alpha*(reward + gamma * new_state_max - self.q_table[state, action])
                
            
                # if i % 500 == 0 and i != 0:
                    # print("i: ", i, "step_number: ", step_number)
                    # print("field.position coordinates: ", field.position)
                    # self.board.write_info(i, step_number, action)
                    # self.board.move_carrier_upgraded(action, field.item_in_car, field.position[0], field.position[1])
                    # time.sleep(0.5)
                    # self.evaluate_new_reinforcement_learning(i)

            if i % 1000 == 0 and i != 0:
                print("i: ", i, "step_number: ", step_number)
                print("field.position coordinates: ", field.position)
                # self.evaluate_rl_while_training(i)

        np.save("C:/Users/sesle/Desktop/Workspace/ReinforcementLearning/Github/q-learning/trained_q_tables/q_table_3milyon.npy", self.q_table) # egitilen q_table save edilir

    def evaluate_rl_while_training(self, i):  # onceki evaluate fonksiyonunun egitim kisimlarinin ve random ilerlemesinin cikarilmis hali
        
        field = Field(self.size, self.item_start, self.start_position, self.item_drop_off)
        self.board = board_class(self.item_start, self.start_position, self.item_drop_off)
        
        done = False
        step_number = 0  # olayi kac adimda tamamladigini tutar

        while not done:
            step_number = step_number + 1

            state = field.get_state()

            # print("q_table[state]: ", q_table[0])
            action = np.argmax(self.q_table[state])

            reward, done = field.make_action(action)

            self.board.write_info(i, step_number, action)
            self.board.move_carrier_upgraded(action, field.item_in_car, field.position[0], field.position[1])
            # time.sleep(0.1)
            if step_number >= 30:  # algoritmanin takili kalmasini onlemek icin, yoksa sonsuz kadar hep ayni hareketi tekrarliyor
                done = True

        self.board.reset()
        return step_number
    
    def evaluate_rl(self, trained_q_table, random_position, random_movement):
        if random_position:
            self.random_position()
        field = Field(self.size, self.item_start, self.start_position, self.item_drop_off)
        self.board = board_class(self.item_start, self.start_position, self.item_drop_off)
        
        done = False
        step_number = 0  # olayi kac adimda tamamladigini tutar
        i = 0

        epsilon = 0.2
        while not done:
            step_number = step_number + 1
            state = field.get_state()

            if random_movement:
                if random.uniform(0, 1) < epsilon:  # 0-1 arasi random sayi secilir, epsilon degeri ile kiyaslanir
                    action = random.randint(0, 5)  # random bir aksiyon secilir
                else:
                    action = np.argmax(trained_q_table[state])
            else:
                action = np.argmax(trained_q_table[state])
                if step_number >= 100:  # algoritmanin takili kalmasini onlemek icin, yoksa sonsuz kadar hep ayni hareketi tekrarliyor
                    print("fail")
                    done = True

            reward, done = field.make_action(action)
            if action == 4:
                self.board.pickup_acion()
            elif action == 5:
                self.board.drop_off_action()

            self.board.write_info(i, step_number, action)
            self.board.move_carrier_upgraded(action, field.item_in_car, field.position[0], field.position[1])
            time.sleep(0.1)

        self.board.reset()
        return step_number
