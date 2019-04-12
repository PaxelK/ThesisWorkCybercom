import math
import gym
from gym import spaces, logger
from gym.utils import seeding
import numpy as np

import sys
sys.path.append("..")  # Adds higher directory to python modules path.

from setParams import *
from EnvironmentEngine import *

EE = EnvironmentEngine()

class WSN(gym.Env):
    '''
    # Observations:
    Type: Box(4)
    Observation         Min     Max
    X position          0       xSize
    Y position          0       ySize
    (CHstatus           0       1)
    PR                  0       3

    # Actions:
    Type: Discrete(6)
    0 = Move south
    1 = Move north
    2 = Move east
    3 = Move west
    4 = Increase packet rate
    5 = Decrease Packet rate
    '''
    def __init__(self):
        EE = EnvironmentEngine()

        self.xSize = xSize
        self.ySize = ySize

        self.rnd = 0
        self.numNodes = numNodes
        self.PRamount = 4 # Amount of values PR can be

        # By using a system grid size of 100x100 we get a step size of 2 m
        high = np.array([
            int(self.xSize/50),
            int(self.ySize/50),
            4])

        low = np.array([
            0,
            0,
            0])

        self.action_space = spaces.Discrete(6)
        self.observation_space = spaces.Box(low, high, dtype=np.float32)

        self.seed()
        self.done = False
        self.viewer = None
        self.state = EE.getStates()[0:2]  # Gets the first two elements in the list that's returned by getStates
        for i in range(numNodes):
            self.state.append(EE.nodes[i].PA)

        self.steps_beyond_done = None
    
    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        assert self.action_space.contains(action), "%r (%s) invalid"%(action, type(action))
        self.rnd += 1

        self.state = EE.getStates()[0:2]  # Gets the first two elements in the list that's returned by getStates
        for i in range(numNodes):
            self.state.append(EE.nodes[i].PA)

        print(self.state)
        xPos, yPos, PR = self.state
        PR = [PR]

        if len(EE.deadNodes) == numNodes:
            done = True

        if action == 0:
            yPos -= 1
            EE.updateEnv(xPos, yPos,PR)

        elif action == 1:
            yPos += 1
            EE.updateEnv(xPos, yPos,PR)

        elif action == 2:
            xPos += 1
            EE.updateEnv(xPos, yPos, PR)

        elif action == 3:
            yPos -= 1
            EE.updateEnv(xPos, yPos, PR)

        elif action == 4:
            EE.nodes[1].PA = min(self.PRamount-1, EE.nodes[1].PA+1)
            EE.updateEnv(xPos, yPos, PR)

        elif action == 1:
            EE.nodes[1].PA = max(0, EE.nodes[1].PA-1)
            EE.updateEnv(xPos, yPos, PR)

        return np.array(self.state), reward, done, {}



    '''
    def step(self, action):
        assert self.action_space.contains(action), "%r (%s) invalid" % (action, type(action))
        state = self.state
        x, x_dot, theta, theta_dot = state
        force = self.force_mag if action == 1 else -self.force_mag
        costheta = math.cos(theta)
        sintheta = math.sin(theta)
        temp = (force + self.polemass_length * theta_dot * theta_dot * sintheta) / self.total_mass
        thetaacc = (self.gravity * sintheta - costheta * temp) / (
                    self.length * (4.0 / 3.0 - self.masspole * costheta * costheta / self.total_mass))
        xacc = temp - self.polemass_length * thetaacc * costheta / self.total_mass
        if self.kinematics_integrator == 'euler':
            x = x + self.tau * x_dot
            x_dot = x_dot + self.tau * xacc
            theta = theta + self.tau * theta_dot
            theta_dot = theta_dot + self.tau * thetaacc
        else:  # semi-implicit euler
            x_dot = x_dot + self.tau * xacc
            x = x + self.tau * x_dot
            theta_dot = theta_dot + self.tau * thetaacc
            theta = theta + self.tau * theta_dot
        self.state = (x, x_dot, theta, theta_dot)
        done = x < -self.x_threshold \
               or x > self.x_threshold \
               or theta < -self.theta_threshold_radians \
               or theta > self.theta_threshold_radians
        done = bool(done)

        if not done:
            reward = 1.0
        elif self.steps_beyond_done is None:
            # Pole just fell!
            self.steps_beyond_done = 0
            reward = 1.0
        else:
            if self.steps_beyond_done == 0:
                logger.warn(
                    "You are calling 'step()' even though this environment has already returned done = True. You should always call 'reset()' once you receive 'done = True' -- any further steps are undefined behavior.")
            self.steps_beyond_done += 1
            reward = 0.0

        return np.array(self.state), reward, done, {}

    def reset(self):
        self.state = self.np_random.uniform(low=-0.05, high=0.05, size=(4,))
        self.steps_beyond_done = None
        return np.array(self.state)

    def render(self, mode='human'):
        screen_width = 600
        screen_height = 400

        world_width = self.x_threshold * 2
        scale = screen_width / world_width
        carty = 100  # TOP OF CART
        polewidth = 10.0
        polelen = scale * (2 * self.length)
        cartwidth = 50.0
        cartheight = 30.0

        if self.viewer is None:
            from gym.envs.classic_control import rendering
            self.viewer = rendering.Viewer(screen_width, screen_height)
            l, r, t, b = -cartwidth / 2, cartwidth / 2, cartheight / 2, -cartheight / 2
            axleoffset = cartheight / 4.0
            cart = rendering.FilledPolygon([(l, b), (l, t), (r, t), (r, b)])
            self.carttrans = rendering.Transform()
            cart.add_attr(self.carttrans)
            self.viewer.add_geom(cart)
            l, r, t, b = -polewidth / 2, polewidth / 2, polelen - polewidth / 2, -polewidth / 2
            pole = rendering.FilledPolygon([(l, b), (l, t), (r, t), (r, b)])
            pole.set_color(.8, .6, .4)
            self.poletrans = rendering.Transform(translation=(0, axleoffset))
            pole.add_attr(self.poletrans)
            pole.add_attr(self.carttrans)
            self.viewer.add_geom(pole)
            self.axle = rendering.make_circle(polewidth / 2)
            self.axle.add_attr(self.poletrans)
            self.axle.add_attr(self.carttrans)
            self.axle.set_color(.5, .5, .8)
            self.viewer.add_geom(self.axle)
            self.track = rendering.Line((0, carty), (screen_width, carty))
            self.track.set_color(0, 0, 0)
            self.viewer.add_geom(self.track)

            self._pole_geom = pole

        if self.state is None: return None

        # Edit the pole polygon vertex
        pole = self._pole_geom
        l, r, t, b = -polewidth / 2, polewidth / 2, polelen - polewidth / 2, -polewidth / 2
        pole.v = [(l, b), (l, t), (r, t), (r, b)]

        x = self.state
        cartx = x[0] * scale + screen_width / 2.0  # MIDDLE OF CART
        self.carttrans.set_translation(cartx, carty)
        self.poletrans.set_rotation(-x[2])

        return self.viewer.render(return_rgb_array=mode == 'rgb_array')

    def close(self):
        if self.viewer:
            self.viewer.close()
            self.viewer = None
    '''
