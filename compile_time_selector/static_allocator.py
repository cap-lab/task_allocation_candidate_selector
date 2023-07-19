import random
import numpy as np
import decimal
from math import inf
from statistics import stdev
import json

class Allocator:
    def __parameter_init(self, task_list):
        max_ratio = 0
        min_ratio = 1
        workload_sum = 0
        for task in task_list:
            task_ratio = 1/task['min']
            workload_sum = workload_sum + task['load']
            if max_ratio < task_ratio:
                max_ratio = task_ratio
            if min_ratio > task_ratio:
                min_ratio = task_ratio
        threshold = (max_ratio + min_ratio)
        return workload_sum, threshold

    def compile_time_allocate(self, robot_list, task_list):
        workload_sum, threshold = self.__parameter_init(task_list)
        task_count = [9,3,9,29]
        task_info = [t for t in task_list]
        robot_i = 0 
        robot_task_list = [list() for _ in range(len(robot_list))]
        for ti in range(4):
            for _ in range(task_count[ti]):
                robot_task_list[robot_i].append(task_info[ti])
                robot_i = robot_i + 1
        print(robot_task_list)
        for robot in robot_list:
            data = {"candidate":robot_task_list[robot.index], "threshold": threshold, "workload_sum": workload_sum, "num_of_group": len(task_list), "num_of_robots": len(robot_list)}
            with open("../compile_time/group_selection_info_"+str(robot.index)+".json", 'w') as f:
                json.dump(data, f)
            
