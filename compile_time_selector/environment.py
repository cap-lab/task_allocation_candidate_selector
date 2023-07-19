from robot import Robot
from math import ceil
import copy
from functools import reduce

class Environment:
    def __init__(self, robot, task_list, neighbor_range, allocator, dst_dir):
        self.allocator = allocator
        self.neighbor_range = neighbor_range
        self.task_list = list(None for _ in range(len(task_list)))
        self.dst_dir = dst_dir
        for index, task in enumerate(task_list):
            self.task_list[index] = task
            self.task_list[index]['min'] = ceil(task['load']/task['requ'])
        self.robot_list = list()
        for index in range(robot['num']):
            self.robot_list.append(Robot(index, index, copy.deepcopy(robot), self.task_list))

    def compile_time_allocate(self):
        self.allocator.compile_time_allocate(self.robot_list, self.task_list, self.dst_dir)
