import gym
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env.base_vec_env import VecEnvWrapper
from reinforcementlearning.agent import QLearningAgent
from reinforcementlearning.yahtzeeenv import YahtzeeEnv
from run import setup_logger

if __name__ == '__main__':
    setup_logger()
    env = YahtzeeEnv()
    envs = gym.make('yahtzeeenv')
    vec_env = VecEnvWrapper.wrap_envs(envs, VecEnvWrapper)
    agent = QLearningAgent(vec_env.action_space, vec_env.observation_space)
    model = PPO("MlpPolicy", vec_env, verbose=1)
    model.learn(total_timesteps=1000000)

    for episode in range(1000):
        state = env.reset()
        done = False

        while not done:
            action = agent.select_action(state)
            next_state, reward, done, _ = vec_env.step(action)
            agent.learn(state, action, reward, next_state)
            state = next_state

    vec_env.close()
