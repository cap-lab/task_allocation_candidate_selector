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

    def compile_time_allocate(self, robot_list, task_list, dst_dir):
        workload_sum, threshold = self.__parameter_init(task_list)
        robot_task_list = [list() for _ in range(len(robot_list))]
        task_status = [{'h':0,'c':t['min'],'t':t, 'k':random.random()} for t in task_list]
        task_status = sorted(task_status, key=lambda e: (e['h'], e['k']))
        cons_list = [robot.get_cons() for robot in robot_list]
        changed = True
        while changed is True:
            changed = False
            for robot in robot_list:
                for task in task_status:
                     if (not task['t'] in robot_task_list[robot.index]) and cons_list[robot.index] >= task['t']['weig']:
                        robot_task_list[robot.index].append(task['t'])
                        cons_list[robot.index] = cons_list[robot.index]-task['t']['weig']
                        task['c'] = task['c'] - 1
                        if task['c'] == 0:
                            task['h'] = task['h'] + 1
                            task['c'] = task['t']['min']
                        changed = True
                        break
                for task in task_status:
                    task['k'] = random.random()
                task_status = sorted(task_status, key=lambda e: (e['h'], e['k']))
        print(robot_task_list)
        data = {"threshold": threshold, 
                "workload_sum": workload_sum, 
                "num_of_group": len(task_list), 
                "num_of_robots": len(robot_list)}
        for robot in robot_list:
            data[str(robot.index)] = robot_task_list[robot.index]
        with open(dst_dir+"/group_selection_candidate_info.json", 'w') as f:
            json.dump(data, f, indent=4)
            
