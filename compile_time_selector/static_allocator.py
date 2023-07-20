import random
import numpy as np
import decimal
from math import inf
from statistics import stdev
import json

class Allocator:
    def compile_time_allocate(self, robot_list, task_list):
        task_count = [9,3,9,29]
        task_info = [t for t in task_list]
        robot_i = 0 
        robot_task_list = {str(r.index): list() for r in robot_list}
        for ti in range(4):
            for _ in range(task_count[ti]):
                robot_task_list[str(robot_i)].append(task_info[ti])
                robot_i = robot_i + 1
        print(robot_task_list)
        return 0.0, robot_task_list
            
