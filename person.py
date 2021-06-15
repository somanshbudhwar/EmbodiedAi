import random

import numpy as np
import pygame

from experiments.covid.config import config
from simulation.agent import Agent
from simulation.utils import *


class Person(Agent):
    """ """
    def __init__(
            self, pos, v, population, index: int, mode: str , image: str = "experiments/covid/images/susceptible.png"
    ) -> None:
        super(Person, self).__init__(
            pos,
            v,
            color = 'blue',
            max_speed=config["agent"]["max_speed"],
            min_speed=config["agent"]["min_speed"],
            mass=config["agent"]["mass"],
            width=config["agent"]["width"],
            height=config["agent"]["height"],
            dT=config["agent"]["dt"],
            index=index
        )
        base_image, rect = image_with_rect(image, [10, 10])
        self.image = base_image
        self.rect = rect
        self.mode = 'susceptible'
        self.population = population
        self.radius = config['person']['radius_view']
        self.timer = 0
        self.p_infection = 0.7
        self.change_mode(mode)




    def update_actions(self) -> None:
        # if self.population.datapoints:
        #     print(self.population.points_to_plot)
        self.timer += 1
        for obstacle in self.population.objects.obstacles:
            collide = pygame.sprite.collide_mask(self, obstacle)
            if bool(collide):
                self.avoid_obstacle()
        neighbours = self.population.find_neighbors(self, self.radius)
        if self.timer % 50 == 0:
            for neighbour in neighbours:
                if neighbour.mode == 'infected' \
                        and self.mode == 'susceptible' \
                        and self.p_infection < np.random.rand():
                    self.change_mode('infected')
                    self.data_update()
                    self.timer = 0
        if self.timer > 300 and self.mode == 'infected':
            self.change_mode('removed')
            self.data_update()
            self.timer = 0

        # if self.timer > 300 and self.mode == 'removed':
        #     self.change_mode('susceptible')
        #     self.data_update()
        #     self.timer = 0



    def change_mode(self, mode='susceptible'):
        if mode == 'infected':
            self.mode = 'infected'
            image = "experiments/covid/images/infected.png"
        elif mode == 'removed':
            self.mode = 'removed'
            image = "experiments/covid/images/removed.png"
        else:
            self.mode = 'susceptible'
            image = "experiments/covid/images/susceptible.png"

        width = config["agent"]["width"]
        height = config["agent"]["height"]
        base_image, rect = image_with_rect(image, [width, height])
        self.image = base_image

    def data_update(self):
        self.population.datapoints = []
        for person in self.population.agents:
            if person.mode == 'susceptible':
                self.population.datapoints.append('S')
            elif person.mode == 'infected':
                self.population.datapoints.append('I')
            elif person.mode == 'removed':
                self.population.datapoints.append('R')
        print(self.population.datapoints)
