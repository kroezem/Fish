import numpy as np


class Entity:
    def __init__(self, env, row, col):
        self.value = 1
        self.alive = True
        self.row = row
        self.col = col
        self.env = env

    def pos(self, row=None, col=None):
        if row is None:
            row = self.row
        if col is None:
            col = self.col

        return str(row * self.env.cols + col)

    def act(self, action):
        row = action[0]
        col = action[1]

        distance = [abs(self.row - row), abs(self.col - col)]
        if all(distance) < 2:
            self_pos = self.pos()
            target_pos = self.pos(row, col)
            target = self.env.field[target_pos]

            if target == self.env.empty:
                self.env.field[self_pos] = self.env.empty
                self.env.field[target_pos] = self
                self.row = row
                self.col = col
                return self.value

            elif target != self:
                if self.value >= target.value:
                    self.value += target.value
                    self.env.field[self_pos] = self.env.empty
                    self.env.field[target_pos] = self
                    return self.value + target.value
        return 0

    def observe(self):
        isolated = np.zeros_like(self.env.agents,dtype=np.uint8)
        isolated[int(self.pos())] = self.value

        field = [self.env.field[agent].value for agent in self.env.agents]
        return np.concatenate((isolated, field))


class Empty(Entity):
    def __init__(self, env, row=0, col=0):
        super().__init__(env, row, col)
        self.alive = False
        self.value = 0

    def act(self, action):
        return 0

    def observe(self):
        obs =
        return


class Fish(Entity):
    def __init__(self, env, row, col):
        super().__init__(env, row, col)
