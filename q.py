import random


def pretty(d, indent=0):
    for key,value in d.items():
        print('\t' * indent + str(key))
        if isinstance(value, dict):
            pretty(value, indent+1)
        else:
            print('\t'*(indent+1) + str(value))

ammo_limit = 3

states = []

for i in range(0,ammo_limit+1):
    for j in range(0,ammo_limit+1):
        states.append((i,j))

states.append('w')
states.append('l')
states.append('d')

def reward(state):
    if state == 'w':
        return 1
    elif state == 'l':
        return -1
    else:
        return 0


def get_next_state(state, action_1, action_2):

    if action_1 == 'fire' and action_2 == 'fire':
        return 'd'
    if action_1 == 'fire' and action_2 == 'load':
        return 'w'
    if action_1 == 'fire' and action_2 == 'block' and state[0] == ammo_limit:
        return 'w'

    if action_1 == 'load' and action_2 == 'fire':
        return 'l'
    if action_1 == 'block' and action_2 == 'fire' and state[1] == ammo_limit:
        return 'l'

    next_state = [state[0], state[1]]

    if action_1 == 'fire':
        next_state[0] -= 1
    elif action_1 == 'load':
        next_state[0] = min(ammo_limit, state[0]+1)
    if action_2 == 'fire':
        next_state[1] -= 1
    elif action_2 == 'load':
        next_state[1] = min(ammo_limit, state[1]+1)

    return tuple(next_state)

class agent():
    def __init__(self):
        self.states = states
        self.q_table = {}

        self.gamma = 0.6

        self.state = (0,0)

        for state in states:
            self.q_table[state] = {}
            self.q_table[state]['load'] = random.random()
            self.q_table[state]['block'] = random.random()
            if state[0] != 0:
                self.q_table[state]['fire'] = random.random()

    def get_action(self, epsilon):
        if random.random() < epsilon:
            next_action = None
            for i, action in enumerate(self.q_table[self.state]):
                if random.random() < 1.0/(1+i):
                    next_action = action
            return next_action
        else:
            next_action = None
            max_value = -1e9
            for action in self.q_table[self.state]:
                if self.q_table[self.state][action] > max_value:
                    next_action = action
                    max_value = self.q_table[self.state][action]

            return next_action

    def update_action_table(self, state, action_1, action_2, alpha):
        next_state = get_next_state(state, action_1, action_2)

        max_next_q = -1e9
        for q in self.q_table[next_state]:
            max_next_q = max(max_next_q, self.q_table[next_state][q])

        self.q_table[state][action_1] += alpha*(reward(next_state) + 
                                                self.gamma*max_next_q - 
                                                self.q_table[state][action_1])

agent_1 = agent()
agent_2 = agent()

epochs = 1000

agent_1_win = 0
agent_1_loss = 0
draw = 0
for i in range(0, epochs):
    epsilon = (epochs-i)/epochs

    agent_1.state = (0,0)
    agent_2.state = (0,0)

    while True:

        agent_1_action = agent_1.get_action(epsilon)
        agent_2_action = agent_2.get_action(epsilon)

        #print(agent_1.state, agent_2.state, agent_1_action, agent_2.state, agent_2_action)


        agent_1.update_action_table(agent_1.state, agent_1_action, agent_2_action, alpha=0.9)
        agent_2.update_action_table(agent_2.state, agent_2_action, agent_1_action, alpha=0.9)

        agent_1.state = get_next_state(agent_1.state, agent_1_action, agent_2_action)
        agent_2.state = get_next_state(agent_2.state, agent_2_action, agent_1_action)

        if agent_1.state in ['w', 'l', 'd']:
            if agent_1.state == 'w':
                agent_1_win +=1 
            elif agent_1.state == 'l':
                agent_1_loss += 1
            else:
                draw += 1
            break



pretty(agent_1.q_table)

print(agent_1_win, agent_1_loss, draw)




