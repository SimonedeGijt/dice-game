import gym
import numpy as np

class QLearningAgent:
    def __init__(self, action_space_size, observation_space_size, learning_rate=0.1, discount_factor=0.9, exploration_prob=0.1):
        self.action_space_size = action_space_size
        self.observation_space_size = observation_space_size
        self.q_table = np.zeros((observation_space_size, action_space_size))
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_prob = exploration_prob

    def select_action(self, state):
        if np.random.uniform(0, 1) < self.exploration_prob:
            return np.random.choice(self.action_space_size)
        else:
            return np.argmax(self.q_table[state, :])

    def learn(self, state, action, reward, next_state):
        old_value = self.q_table[state, action]
        next_max = np.max(self.q_table[next_state, :])
        new_value = (1 - self.learning_rate) * old_value + self.learning_rate * (reward + self.discount_factor * next_max)
        self.q_table[state, action] = new_value
