from stable_baselines3 import PPO

from reinforcementlearning.agent import QLearningAgent
from reinforcementlearning.yahtzeeenv import YahtzeeEnv
from run import setup_logger

if __name__ == '__main__':
    setup_logger()
    env = YahtzeeEnv()
    agent = QLearningAgent()
    # env = DummyVecEnv([lambda: YahtzeeEnv()])  # Vectorize the environment
    model = PPO("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=1000000)

    obs = env.reset()

    for episode in range(1000):
        state = env.reset()
        done = False

        while not done:
            action = agent.select_action(state)
            next_state, reward, done, _ = env.step(action)
            agent.learn(state, action, reward, next_state)
            state = next_state