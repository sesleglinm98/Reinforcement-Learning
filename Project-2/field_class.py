class Field:
    def __init__(self, size, agent_position, evil_man_position, castle_position):
        self.size = size
        self.agent_position = agent_position
        self.evil_man_position = evil_man_position
        self.reward_position = evil_man_position 
        self.castle_position = castle_position
        self.reward_taken = False  # status of receiving the award
        self.evil_man_dead = False  # whether the evil man dies or not

    def get_number_of_states(self):  # calculates how many states there are in total
        return self.size*self.size*self.size*self.size*self.size*self.size*2*2 + 1

    def get_state(self): # find out what state it is in the algorithm
        state = self.agent_position[0] * self.size * self.size * self.size * self.size * self.size * 2 * 2
        state = state + self.agent_position[1] * self.size * self.size * self.size * self.size * 2 * 2
        state = state + self.evil_man_position[0] * self.size * self.size * self.size * 2 * 2
        state = state + self.evil_man_position[1] * self.size * self.size * 2 * 2
        state = state + self.reward_position[0] * self.size * 2 * 2
        state = state + self.reward_position[1] * 2 * 2
        if self.evil_man_dead:
            state = state + 3
        else:
            state = state + 2
        if self.reward_taken:
            state = state + 1
        return state

    def make_action(self, action):
        (x, y) = self.agent_position
        if action == 0: # go down
            if y == self.size - 1:  # action of going down while at the bottom
                return -10, 0, False
            else:
                self.agent_position = (x, y + 1)
                if self.agent_position[0] == self.evil_man_position[0] and self.agent_position[1] == self.evil_man_position[1]:  # if the agent comes near the evil position, he will receive penalty points and fail the task
                    if not self.evil_man_dead:
                        return -20, 0, True
                return -1, 0, False
        elif action == 1:  # go up
            if y == 0:  # action of going up while at the top
                return -10, 0, False
            else:
                self.agent_position = (x, y - 1)
                if self.agent_position[0] == self.evil_man_position[0] and self.agent_position[1] == self.evil_man_position[1]:  # if the agent comes near the evil position, he will receive penalty points and fail the task
                    if not self.evil_man_dead:
                        return -20, 0, True
                return -1, 0, False
        elif action == 2:  # go left
            if x == 0:  # action of going left while on the far left
                return -10, 0, False
            else:
                self.agent_position = (x - 1, y)
                if self.agent_position[0] == self.evil_man_position[0] and self.agent_position[1] == self.evil_man_position[1]:  # if the agent comes near the evil position, he will receive penalty points and fail the task
                    if not self.evil_man_dead:
                        return -20, 0, True
                return -1, 0, False
        elif action == 3:  # go right
            if x == self.size - 1:  # action of going right while on the far right
                return -10, 0, False
            else:
                self.agent_position = (x + 1, y)
                if self.agent_position[0] == self.evil_man_position[0] and self.agent_position[1] == self.evil_man_position[1]:  # if the agent comes near the evil position, he will receive penalty points and fail the task 
                    if not self.evil_man_dead:
                        return -20, 0, True
                return -1, 0, False
        elif action == 4:  # attack action
            if self.evil_man_dead:
                return -1, 0, False
            elif abs(self.evil_man_position[0] - x) == 1 and abs(self.evil_man_position[1] - y) == 1:
                self.evil_man_dead = True
                return 10, 1, False
            elif abs(self.evil_man_position[0] - x) == 0 and abs(self.evil_man_position[1] - y) == 1:
                self.evil_man_dead = True
                return 10, 1, False
            elif abs(self.evil_man_position[0] - x) == 1 and abs(self.evil_man_position[1] - y) == 0:
                self.evil_man_dead = True
                return 10, 1, False
            else:
                return -1, 0, False
        elif action == 5:  # pickup reward
            if self.reward_taken:  # if item is already taken and the pickup action is selected again
                return -10, 0, False
            elif self.reward_position != (x, y):  # if item is not in the agent's location and the pickup action is selected
                return -10, 0, False
            else:
                self.reward_taken = True  # to indicate that the agent has item
                return 20, 2, False
        elif action == 6: # drop off reward
            if not self.reward_taken:  # if item is not in agent and drop off action is selected
                return -10, 0, False
            elif self.castle_position != (x, y):  # if item is in agent and agent is not in castle position
                self.reward_position = (x, y)  # item is dropped at the agent's location
                self.reward_taken = False  # to indicate that item is not in the agent
                return -10, 3, False
            else:
                return 20, 4, True  # A true statement indicates that the event has been completed