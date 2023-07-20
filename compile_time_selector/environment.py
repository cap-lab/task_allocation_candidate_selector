from robot import Robot
from math import ceil
import copy
import json

class Environment:
    def __init__(self, robot, task_list, neighbor_range, allocator, output_file):
        self.allocator = allocator
        self.neighbor_range = neighbor_range
        self.task_list = list(None for _ in range(len(task_list)))
        self.output_file = output_file
        for index, task in enumerate(task_list):
            self.task_list[index] = task
            self.task_list[index]['min'] = ceil(task['load']/task['requ'])
        self.robot_list = list()
        for index in range(robot['num']):
            self.robot_list.append(Robot(index, copy.deepcopy(robot)))
        self.workload_sum = 0
        for task in task_list:
            self.workload_sum = self.workload_sum + task['load']
        

    def compile_time_allocate(self):
        threshold, alloc_result = self.allocator.compile_time_allocate(self.robot_list, self.task_list)
        data = {"threshold": threshold, 
                "workload_sum": self.workload_sum, 
                "num_of_group": len(self.task_list), 
                "num_of_robots": len(self.robot_list)}
        data.update(alloc_result)
        with open(self.output_file, 'w') as f:
            json.dump(data, f, indent=4)


