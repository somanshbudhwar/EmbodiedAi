from experiments.covid.config import config
from experiments.covid.person import Person
from simulation.swarm import Swarm
from simulation.utils import *


class Population(Swarm):
    """Class that represents the Population for the Covid experiment. TODO"""

    def __init__(self, screen_size) -> None:
        super(Population, self).__init__(screen_size)
        # self.object_loc = config["population"]["outside"]
        self.object_loc = config["population"]["outside"]

        # To do

    def initialize(self, num_agents: int) -> None:
        """
        Args:
            num_agents (int):

        """
        self.points_to_plot = {'S':[], 'I':[], 'R': []}
        filename = "experiments/covid/images/obs.png"
        object_loc = config["base"]["object_location"]
        scale = [800, 800]
        # To Do
        # code snipet (not complete) to avoid initializing agents on obstacles
        # given some coordinates and obstacles in the environment, this repositions the agent

        # if config["population"]["obstacles"]:  # you need to define this variable
        #     for obj in self.objects.obstacles:
        #         rel_coordinate = relative(
        #             coordinates, (obj.rect[0], obj.rect[1])
        #         )
        #
        #         try:
        #             while obj.mask.get_at(rel_coordinate):
        #                 coordinates = generate_coordinates(self.screen)
        #                 rel_coordinate = relative(
        #                     coordinates, (obj.rect[0], obj.rect[1])
        #                 )
        #         except IndexError:
        #             pass

        min_x, max_x = area(object_loc[0], scale[0])
        min_y, max_y = area(object_loc[1], scale[1])

        # add agents to the environment
        if config["population"]["obstacles"]:
            self.objects.add_object(
                file=filename, pos=object_loc, scale=scale, obj_type="obstacle"
            )
        for index, agent in enumerate(range(num_agents)):
            coordinates = generate_coordinates(self.screen)

            # if obstacles present re-estimate the corrdinates
            if config["population"]["obstacles"]:
                if config["population"]["outside"]:
                    while (
                            max_x >= coordinates[0] >= min_x
                            and max_y >= coordinates[1] >= min_y
                    ):
                        coordinates = generate_coordinates(self.screen)
                else:
                    while (
                            coordinates[0] >= max_x
                            or coordinates[0] <= min_x
                            or coordinates[1] >= max_y
                            or coordinates[1] <= min_y
                    ):
                        coordinates = generate_coordinates(self.screen)

            mode = 'infected' if index%10 == 0 else 'susceptible'
            self.add_agent(Person(pos=np.array(coordinates), v=None, population=self, index=index, mode = mode))
