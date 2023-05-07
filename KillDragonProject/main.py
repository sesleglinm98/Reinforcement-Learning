from rl_q_learning_scratch import Q_Learning
import numpy as np

_size = 10
_item_start = (0, 0)
_start_position = (0, 9)
_item_drop_off = (9, 9)

train_q = Q_Learning(_size, _item_start, _start_position, _item_drop_off, True)

# train_q.train_q_learning()

q_table = np.load("C:/Users/sesle/Desktop/Workspace/ReinforcementLearning/Github/Project-2/q_table_500bin.npy")  # loading q_table which is trained before

train_q.evaluate_rl(q_table, True, True)
train_q.evaluate_rl(q_table, True, True)
train_q.evaluate_rl(q_table, True, True)