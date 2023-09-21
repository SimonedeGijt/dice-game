from stable_baselines3 import PPO

from run import setup_logger
from service.yahtzeeenv import YahtzeeEnv

if __name__ == '__main__':
    setup_logger()
    env = DummyVecEnv([lambda: YahtzeeEnv()])  # Vectorize the environment
    model = PPO("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=1000000)

    obs = env.reset()
    for _ in range(1000):
        action, _states = model.predict(obs)
        obs, rewards, dones, info = env.step(action)
        env.render()
