from multiprocessing import Process, Queue, Lock
import yaml
from environment import Environment
import copy

def allocate(robot, tasks, allocator_type, output_file):
    if allocator_type == "default":
        from default_allocator import Allocator
    elif allocator_type == "static":
        from static_allocator import Allocator
    allocator = Allocator()
    environment = Environment(robot, tasks, robot['comm'], allocator, output_file)
    environment.compile_time_allocate()

def tester(data, test_file, allocator_type, output_file):
    allocate(copy.deepcopy(data['robot']), copy.deepcopy(data['task']), allocator_type, output_file)

def argument_init():
    import argparse
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-t', '--test', type=str, default='../input/dynamic_test.yml', help='Test Scenario')
    parser.add_argument('-o', '--output_file', type=str, default='../output/group_selection_candidate_info.json', help='Output File')
    parser.add_argument('-a', '--allocator', type=str, default='default', help='Allocator Type')
    return parser.parse_args()

def process(test_name, testcase, process_list, allocator_type, output_file):
    lock = Lock()
    with open(testcase['file'], 'r') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    if 'change' in testcase.keys():
        change = testcase['change']
        keys = list(change.keys())
        change_set = [[keys[0], change[keys[0]][0], 1]]
        while len(change_set)!=0:
            item = change_set.pop()
            data['robot'][item[0]] = item[1]
            item[1] = item[1] + change[item[0]][2]
            if item[1] <= change[item[0]][1]:
                change_set.append(item)
            if item[2] == len(keys):
                proc = Process(target=tester, args=(data, testcase['file'], allocator_type, output_file))
                proc.start()
                while len(process_list) >= 13:
                    joined_list = list()
                    for index, old_proc in enumerate(process_list):
                        if old_proc.is_alive() is False:
                            old_proc.join()
                            joined_list.append(index)
                    for index in sorted(joined_list, reverse=True):
                        process_list.pop(index)
                process_list.append(proc)
            else:
                change_set.append([keys[item[2]], change[keys[item[2]]][0], item[2] + 1])
    else:
        proc = Process(target=tester, args=(data, testcase['file'], allocator_type, output_file))
        proc.start()
        proc.join()

if __name__ == "__main__":
    args = argument_init()
    with open(args.test, 'r') as f:
        test = yaml.load(f, Loader=yaml.FullLoader)
    process_list = []
    for testcase in test['testcase']:
        process(test['name'], testcase, process_list, args.allocator, args.output_file)
    for proc in process_list:
        proc.join()
