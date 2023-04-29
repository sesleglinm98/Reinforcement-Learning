from draw_board_class import board_class
import time

class Field:
    def __init__(self, size, item_pickup, start_position, item_drop_off):
        self.size = size
        self.item_pickup = item_pickup
        self.item_drop_off = item_drop_off
        self.position = start_position
        self.item_in_car = False  # esyanin alinip alinmadigini tutar

        # self.board = board_class()

    def get_number_of_states(self):  # toplam kac tane durumun oldugunu dondurur
        return self.size*self.size*self.size*self.size*2 # 2 tane self.size tasiyicinin bulunabilecegi durumlar, 2 tane self.size itemin bulunabilecegi durumlar
        # carpi 2 ise itemin alinip alinmama durumu icin
        # birakilacak alanin durumlari carpima alinmadi, sebebi sanirim bu alan hareket edemiyor sabit bir yer oldugu icin
        # ama bu alaninda hesaba katildigi hesaplama yapilip sonuclari gozlenebilir

    def get_state(self):
        # burada yapilan islem belli bir zamanda hangi durumda oldugunun hesaplanmasidir
        # durumun hesaplanmasi bire bir mapping gibi dusunulebilir, her bir durum her bir sayi ile ifade ediliyor
        # bu mapping islemi icinde asagidaki gibi bir hesaplama yapiliyor ve boylece her durumun bir sayi karsiligi oluyor
        state = self.position[0] * self.size * self.size * self.size * 2
        state = state + self.position[1] * self.size * self.size * 2
        state = state + self.item_pickup[0] * self.size * 2
        state = state + self.item_pickup[1] * 2
        if self.item_in_car:  # itemin alinmis olmasi durumu icin
            state = state + 1
        # alinmamasi durumunu yazmaya gerek yok cunku 0 ile toplayip birsey degismeyecekti
        return state

    def make_action(self, action):
        (x, y) = self.position
        if action == 0: # go south - go down
            if y == self.size - 1:  # en assagida iken assagi inme eylemi durumu
                return -10, False
            else:
                self.position = (x, y + 1)
                return -1, False
        elif action == 1:  # go north - go up
            if y == 0:  # en yukarida iken yukari cikma eylemi durumu
                return -10, False
            else:
                self.position = (x, y - 1)
                return -1, False
        elif action == 2:  # go east - go left
            if x == 0:  # en solda iken sola gitme eylemi durumu
                return -10, False
            else:
                self.position = (x - 1, y)
                return -1, False
        elif action == 3:  # go west - go right
            if x == self.size - 1:  # en sagda iken saga gitme eylemi durumu
                return -10, False
            else:
                self.position = (x + 1, y)
                return -1, False
        elif action == 4:  # pickup item
            if self.item_in_car:  # item onceden alinmissa ve tekrar pickup eylemi secilirse
                return -10, False
            elif self.item_pickup != (x, y):  # item bulundugumuz konumda degil ve alma eylemi secilirse
                return -10, False
            else:
                self.item_in_car = True  # itemin bizde oldugunu belirtmek icin
                return 20, False
        elif action == 5: # drop off item
            if not self.item_in_car:  # item bizde degilse ve drop off eylemi secilirse
                return -10, False
            elif self.item_drop_off != (x, y):  # item bizdeyse ve drop off eylemi secilirse
                self.item_pickup = (x, y)  # itemi bulundugumuz konuma birakiriz
                self.item_in_car = False  # itemin bizde olmadigini belirtmek icin
                return -10, False
            else:
                return 20, True  # True ifadesi ile olayin tamamlandigi belirtilir


class Q_Learning():

    def __init__(self, size, item_start, start_position, item_drop_off, randomize):
        self.size = size
        self.item_start = item_start
        self.start_position = start_position
        self.item_drop_off = item_drop_off

        self.randomize = randomize

    def random_position(self):
        # self.item_start = rd.randint(9, size=(2))
        self.item_start = (random.randint(0, 9), random.randint(0, 9))
        self.start_position = (random.randint(0, 9), random.randint(0, 9))

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

        for i in range(200000):
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

            if i % 5000 == 0 and i != 0:
                print("i: ", i, "step_number: ", step_number)
                print("field.position coordinates: ", field.position)
                # self.evaluate_rl_while_training(i)

        np.save("C:/Users/sesle/Desktop/Workspace/ReinforcementLearning/Scratch-Tutorials/Learn-Python-with-Rune/q_table_200bin.npy", self.q_table) # egitilen q_table save edilir

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
            time.sleep(0.1)
            if step_number >= 30:  # algoritmanin takili kalmasini onlemek icin, yoksa sonsuz kadar hep ayni hareketi tekrarliyor
                done = True

        self.board.reset()
        return step_number
    
    def evaluate_rl(self, trained_q_table, randomize):
        if randomize:
            self.random_position()
        field = Field(self.size, self.item_start, self.start_position, self.item_drop_off)
        self.board = board_class(self.item_start, self.start_position, self.item_drop_off)
        
        done = False
        step_number = 0  # olayi kac adimda tamamladigini tutar
        i = 0

        while not done:
            step_number = step_number + 1

            state = field.get_state()

            # print("q_table[state]: ", q_table[0])
            action = np.argmax(trained_q_table[state])

            reward, done = field.make_action(action)

            self.board.write_info(i, step_number, action)
            self.board.move_carrier_upgraded(action, field.item_in_car, field.position[0], field.position[1])
            time.sleep(0.1)
            if step_number >= 100:  # algoritmanin takili kalmasini onlemek icin, yoksa sonsuz kadar hep ayni hareketi tekrarliyor
                print("fail")
                done = True

        self.board.reset()
        return step_number
    
    def evaluate_rl_with_epsilon_factor(self):
        pass # buraya epsilon faktörü eklenicek, yani explore edebilecek. Original train epsilonundan daha dusuk bir deger kullanilabilir

import numpy as np
from numpy import random as rd
import random

_size = 10
_item_start = (0, 0)
_start_position = (0, 9)
_item_drop_off = (9, 9)

train_q = Q_Learning(_size, _item_start, _start_position, _item_drop_off, True)

# train_q.train_q_learning()

q_table = np.load("C:/Users/sesle/Desktop/Workspace/ReinforcementLearning/Scratch-Tutorials/Learn-Python-with-Rune/q_table_200bin.npy")  # onceden egitilen q_table load edilir
train_q.evaluate_rl(q_table, True)

train_q.evaluate_rl(q_table, True)
train_q.evaluate_rl(q_table, True)

# print(evaluate_new_reinforcement_learning())
# print(evaluate_reinforcement_learning())

