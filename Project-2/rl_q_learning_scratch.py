from draw_board_class import board_class
from field_class import Field

import numpy as np
import time
import random

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

        # q_table is where the learning happens
        self.q_table = np.zeros((number_of_states, number_of_actions))  # q_table initialization

        self.epsilon = 0.2  # exploration and exploitation probability value
        alpha = 0.1    # learning rate
        gamma = 0.6    # discount factor

        for i in range(100000):
            if i % 100 == 0:
                print("iteration: ", i)

            if self.randomize:
                self.random_position()
                self.field = Field(self.size, self.agent_position, self.evil_man_position, self.castle_position)
            else:
                self.field = Field(self.size, self.agent_position, self.evil_man_position, self.castle_position)
            
            if i % 2000 == 0 and i != 0:
                self.board = board_class(self.agent_position, self.evil_man_position, self.castle_position)

            done =  False
            step_number = 0  # number of actions to end an event
            while not done:
                step_number += 1
                state = self.field.get_state()
                if random.uniform(0, 1) < self.epsilon:  # random number between 0-1 is selected and compared with the epsilon value.
                    action = random.randint(0, 6)  # random action is chosen

                else:
                    action = np.argmax(self.q_table[state])  # the highest value action of the state is selected from q_table

                reward, movement, done = self.field.make_action(action)
                
                # q-learning formula -> Q[state, action] = (1 - alpha) * Q[state, action] + alpha * (reward + gamma * max(Q[new_state]) - Q[state, action])
                new_state = self.field.get_state()
                new_state_max = np.max(self.q_table[new_state])

                self.q_table[state, action] = (1 - alpha) * self.q_table[state, action] + alpha*(reward + gamma * new_state_max - self.q_table[state, action])

                # evaluation model while training
                if i % 2000 == 0 and i != 0:
                    print("i: ", i, "step_number: ", step_number)
                    self.evaluation_in_board(i, step_number, action, movement)
                    if step_number >= 150:
                        self.board.reset()
                        done = True

                # save the model
                if i == 2000:
                    np.save("C:/Users/sesle/Desktop/Workspace/ReinforcementLearning/Github/Project-2/q_table_2bin.npy", self.q_table)
                elif i == 10000:
                    np.save("C:/Users/sesle/Desktop/Workspace/ReinforcementLearning/Github/Project-2/q_table_10bin.npy", self.q_table)
                elif i == 50000:
                    np.save("C:/Users/sesle/Desktop/Workspace/ReinforcementLearning/Github/Project-2/q_table_50bin.npy", self.q_table)

    def evaluation_in_board(self, i, step_number, action, movement):
        self.board.write_info(i, step_number, action)
        self.board.make_action(action, movement, self.field.agent_position, self.field.evil_man_position, self.field.castle_position)

        return step_number
    
    def evaluate_rl(self, trained_q_table, random_position, random_movement):
        if random_position:
            self.random_position()
        self.field = Field(self.size, self.agent_position, self.evil_man_position, self.castle_position)
        self.board = board_class(self.agent_position, self.evil_man_position, self.castle_position)
        
        done = False
        step_number = 0
        i = 0

        epsilon = 0.2
        while not done:
            step_number = step_number + 1
            state = self.field.get_state()

            if random_movement:
                if random.uniform(0, 1) < epsilon:
                    action = random.randint(0, 6)
                else:
                    action = np.argmax(trained_q_table[state])
            else:
                action = np.argmax(trained_q_table[state])
                if step_number >= 150:  # terminates event
                    print("fail")
                    done = True

            reward, movement, done = self.field.make_action(action)

            self.evaluation_in_board(i, step_number, action, movement)
            time.sleep(0.1)

        self.board.reset()
        return step_number

    def manual_test(self):
        self.field = Field(self.size, self.agent_position, self.evil_man_position, self.castle_position)
        self.board = board_class(self.agent_position, self.evil_man_position, self.castle_position)      

        action = 0
        for i in range(3):
            reward, movement, done = self.field.make_action(action)
            self.evaluation_in_board()
        
        action = 3
        for i in range(5):
            reward, movement, done = self.field.make_action(action)
            self.evaluation_in_board()

        action = 4
        reward, movement, done = self.field.make_action(action)
        self.evaluation_in_board()

        action = 0
        reward, movement, done = self.field.make_action(action)
        self.evaluation_in_board()

        action = 5
        reward, movement, done = self.field.make_action(action)
        self.evaluation_in_board()

        action = 3
        for i in range(7):
            reward, movement, done = self.field.make_action(action)
            self.evaluation_in_board()

        action = 6
        reward, movement, done = self.field.make_action(action)
        self.evaluation_in_board()