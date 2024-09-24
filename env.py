import functools
import random
from typing import Union

from pettingzoo.utils import agent_selector, wrappers
from pettingzoo.utils.conversions import parallel_wrapper_fn
from pettingzoo import AECEnv
from gymnasium import spaces
import numpy as np
from entities import Empty, Fish

__all__ = ["env", "parallel_env", "raw_env"]

ref = 'jetbrains://pycharm/navigate/reference?project=Fish&path=.venv/Lib/site-packages/pettingzoo/butterfly/knights_archers_zombies/knights_archers_zombies.py'


def env(**kwargs):
    env = raw_env(**kwargs)
    env = wrappers.AssertOutOfBoundsWrapper(env)
    env = wrappers.OrderEnforcingWrapper(env)
    return env


parallel_env = parallel_wrapper_fn(env)


class raw_env(AECEnv):
    metadata = {
        "render_modes": ["human", "ascii"],
        "name": "fish",
        "is_parallelizable": True,  # Add this line to indicate the environment is parallelizable
    }

    def __init__(self, rows=10, cols=10, render_mode="ansi"):
        super().__init__()
        self._agent_selector = None
        self.field = None
        self.frame = 0
        self.rows = rows
        self.cols = cols
        self.render_mode = render_mode

        self.possible_agents = [str(i) for i in range(self.rows * self.cols)]
        self.agents = self.possible_agents.copy()
        self.empty = Empty(self)

    def reset(self, seed=None, options=None):
        self.field: dict[str, Union[Empty, Fish]] = {str(i): self.empty for i in self.possible_agents}

        self.truncations = {a: False for a in self.agents}
        self.spawn()
        self._agent_selector = agent_selector(self.ready_agents())
        self.agent_selection = self._agent_selector.next()

        self.infos = {agent: {} for agent in self.agents}
        print(self.field[self.agent_selection].observe())

    def step(self, action):
        if self.terminations[self.agent_selection] or self.truncations[self.agent_selection]:
            self._was_dead_step(action)
            return

        self.field[self.agent_selection].act(action)

    def observe(self, agent):
        return self.field[agent].observe()

    def spawn(self, count=2):
        spawned = 0
        while spawned < count:
            i = str(random.randint(0, len(self.possible_agents)))
            if self.field[i] == self.empty:
                self.field[i] = Fish(self, int(i) // self.cols, int(i) % self.cols)
                spawned += 1

    def ready_agents(self):
        agents = []
        self.terminations = {a: True for a in self.agents}
        for key, agent in self.field.items():
            if agent.alive:
                self.terminations[key] = False
                if self.frame % agent.value == 0:
                    agents.append(key)
        return agents

    @functools.lru_cache(maxsize=None)
    def observation_space(self, agent):
        return spaces.Box(low=0, high=255, shape=(self.rows * self.cols * 2,), dtype=np.uint8)

    @functools.lru_cache(maxsize=None)
    def action_space(self, agent):
        return spaces.MultiDiscrete([self.rows, self.cols])
