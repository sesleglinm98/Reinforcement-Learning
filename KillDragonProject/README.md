In this project, there is an agent, an enemy, an award and an area where the award is left to be constructed on the field. The aim of the agent is to travel around the field to find the enemy and kill him. Afterwards, it is to take the prize falling from the enemy and leave it in the designated area. The agent has to complete these tasks with the least action, every action done is written as a penalty point in the learning algorithm. The agent can only kill the enemy while he is one square away, and if he comes to the square where the enemy is located without killing, the enemy will kill the agent and the mission will fail. After the agent kills the enemy, the reward appears at the enemy's location. In order to train the Reinforcement learning algorithm, specific rewards and punishments and their amount were determined for each situation.

**Rewards and Penalties**

**1)** The more steps the agent takes, the more penalty points (-1) <br />
**2)** If the agent tries to go out of the field, penalty points are taken  (-10) <br />
**3)** If the agent hits the enemy, reward points are taken (+10) <br />
**4)** If the enemy hits the agent, penalty points are taken  (-20) <br />
**5)** If the agent attacks but fails to hit the enemy, penalty points are taken (-1) <br />
**6)** If the enemy has been killed before and the attack is made again, penalty points are taken (-1) <br />
**7)** If the agent takes the prize from the field after killing the enemy, the reward points are received (+20) <br />
**8)** If the agent drops the reward in the designated area, the reward points are taken (+20) <br />
**9)** If the agent drops the bounty in the wrong place, penalty points are taken  (-10) <br />
**10)** If the reward has already been taken and the action is pick up again, penalty points are taken  (-10) <br />
**11)** If the pick up action is taken while the agent is not above the bounty, penalty points are taken  (-10) <br />
**12)** If the drop off action is chosen before the reward is already received, penalty points will be charged  (-10) <br />
**13)** If the prize is left in a place other than the designated place, penalty points are taken (-10) <br />

 $~~~~~~~~~~~~~~~~~$ ![board-description_1](https://user-images.githubusercontent.com/64321774/236818876-7691c098-fff6-474e-8d3e-1a959c1674d9.png)
 
 $~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~$ ***figure 1) Overview of the Graphical Design***
 <br />
 <br />
 <br />
 <br />

$~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~$ ![agent-attacked-enemy](https://user-images.githubusercontent.com/64321774/236809726-2aa0578d-4789-4b44-84a7-2fd038ff4d5f.png)

$~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~$ ***figure 2) Agent Attacking the Enemy***
<br />
<br />
<br />
<br />
$~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~$ ![agent-pickup-reward](https://user-images.githubusercontent.com/64321774/236809750-f3c4e997-4995-435e-b41b-4fa2f6fc43e2.png)

$~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~$ ***figure 3) Agent Receiving Award***

<br />
<br />
<br />
<br />

**draw_board_class.py** <br />
The graphical drawing of the project is performed using the python turtle module in the draw_board_class.py code. Coordinate and event information is passed to the board_class class from the rl_q_learning_scratch.py code. Drawings are constantly updated according to this information transmitted.

**field_class.py** <br />
In the field_class.py code, the states of the algorithm are calculated. According to these states, the q_table table of the reinforcement learning algorithm is created. In addition, rewards and penalties are calculated according to the actions taken.

**rl_q_learning_scratch.py** <br />
In the rl_q_learning_scratch.py code, the q learning algorithm is created using the numpy module. Board_class() and Field() classes are also used in the code. In addition to the reinforcement learning training, the evaluation of the training can be done. Also, the trained models are saved with numpy.save.

**main.py** <br />
An object of the Q_Learning class is created in the main.py code and training is started with that object. In addition, the evaluation function can be run by loading the pre-trained model.
