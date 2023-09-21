import gym
import logging
from stable_baselines3 import PPO
from reinforcementlearning.agent import QLearningAgent
from run import setup_logger

if __name__ == '__main__':
    setup_logger()
    logging.info(f'Start the trainer')
    gym.envs.register(
        id='YahtzeeEnv',
        entry_point='yahtzeeenv:YahtzeeEnv',
    )
    env = gym.make('YahtzeeEnv')
    agent = QLearningAgent(env.action_space.n, env.observation_space.shape[0])
    model = PPO("MlpPolicy", env, verbose=1)
    logging.info(f'LEARN MODEL')
    logging.info(f'----------')
    model.learn(total_timesteps=10)
    logging.info(f'----------')
    logging.info(f'LEARNING DONE')
    training_loop = 1000

    for episode in range(training_loop):
        logging.info(f'\n\nNEW GAME, nr: {episode / training_loop * 100:2f}')
        logging.info(f'----------')

        state = env.reset()
        count = 1
        while count <= 13:
            logging.info(f'ROUND {count}')
            action = agent.select_action(state)
            next_state, reward, done, _, _ = env.step(action)
            agent.learn(state, action, reward, next_state)
            state = next_state
            count += 1
            logging.info('ROUND FINISHED')

    logging.info(f'----------')
    logging.info('GAME DONE')

    agent.pickle_table()

    logging.info('\n\nSTART VALIDATING')

    state = env.reset()
    count = 1
    total_reward = 0
    while count <= 13:
        logging.info(f'ROUND {count}')
        action = agent.select_action(state, False)
        next_state, reward, done, _, _ = env.step(action)
        total_reward += reward
        state = next_state
        count += 1
        logging.info(f'ROUND FINISHED WITH TOTAL SCORE OF {total_reward}')

    logging.info('Close the trainer')
    env.close()
