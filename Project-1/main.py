from rl_from_scratch_3 import Q_Learning
import numpy as np

_size = 10
_item_start = (0, 0)
_start_position = (0, 9)
_item_drop_off = (9, 9)

train_q = Q_Learning(_size, _item_start, _start_position, _item_drop_off, True)

# train_q.train_q_learning()

q_table = np.load("C:/Users/sesle/Desktop/Workspace/ReinforcementLearning/Github/q-learning/trained_q_tables/q_table_3milyon.npy")  # onceden egitilen q_table load edilir

train_q.evaluate_rl(q_table, True, True)
train_q.evaluate_rl(q_table, True, True)
train_q.evaluate_rl(q_table, True, True)

# print(evaluate_new_reinforcement_learning())
# print(evaluate_reinforcement_learning())