import random

class Allocator:
    def __parameter_init(self, task_list):
        max_ratio = 0
        min_ratio = 1
        for task in task_list:
            task_ratio = 1/task['min']
            if max_ratio < task_ratio:
                max_ratio = task_ratio
            if min_ratio > task_ratio:
                min_ratio = task_ratio
        threshold = (max_ratio + min_ratio)
        return threshold

    def compile_time_allocate(self, robot_list, task_list):
        threshold = self.__parameter_init(task_list)
        robot_task_list = {str(r.index): list() for r in robot_list}
        task_status = [{'h':0,'c':t['min'],'t':t, 'k':random.random()} for t in task_list]
        task_status = sorted(task_status, key=lambda e: (e['h'], e['k']))
        cons_list = [robot.get_cons() for robot in robot_list]
        changed = True
        while changed is True:
            changed = False
            for robot in robot_list:
                for task in task_status:
                     if (not task['t'] in robot_task_list[str(robot.index)]) and cons_list[robot.index] >= task['t']['weig']:
                        robot_task_list[str(robot.index)].append(task['t'])
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
        return threshold, robot_task_list
                    
