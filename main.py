import supersuit as ss
from stable_baselines3 import PPO
from stable_baselines3.ppo import CnnPolicy, MlpPolicy
import env

env = env.parallel_env()
env = ss.black_death_v3(env)
env.reset()
env = ss.pettingzoo_env_to_vec_env_v1(env)
env = ss.concat_vec_envs_v1(env, 1, num_cpus=1, base_class="stable_baselines3")

model = PPO(
    MlpPolicy,
    env,
    verbose=3,
    batch_size=256,
)

model.learn(total_timesteps=10_000)

# for agent in env.agent_iter():
#     observation, reward, termination, truncation, info = env.last()
#
#     if termination or truncation:
#         action = None
#     else:
#         # this is where you would insert your policy
#         action = env.action_space(agent).sample()
#
#     env.step(action)
# env.close()
