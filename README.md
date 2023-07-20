Author: wecracy <wecracy@snu.ac.kr>
Date: 20/07/2023

*** INTRODUCTION ***

This package is for generating candidate task configurations 
for the example "Task Allocation Algorithm Simulation" at 
https://github.com/cap-lab/argos3-examples.

*** REQUIREMENT ***

Your computer should have Python 3.* to run this package.
The followings are the required python packages.
json, multiprocessing, math, random, PyYAML

*** HOW TO RUN ***

The default commands for running the package are the following.
```console
cd compile_time_selector
python3 main.py
```
With the above commands, you can generate the configuration, 
"output/group_seelction_candidate_info.json".

If you want to use another algorithm for a candidate selector,
you can specify the new algorith with "-a" option.
```console
python main.py -a static
```

If you want to use another test configuration, specify it with 
"-t" option.
```console
python main.py -t new_test.yml
```

If you want to use another name for the output result, specify it 
with "-o" option.
```console
python main.py -o new_output_file_name
```

*** HOW TO ADD A NEW COMPILE-TIME CANDIDIATE SELLECTOR ***

You can add a new compile-time selector by making a new class.
The new class should have a "compile_time_allocate(self, 
robot_list, task_list)" method. This method should return the 
threshold and selection result. The threshold is the floating 
value, which will be used during the run-time allocation. The 
allocation result should follow the following format.
```json
{
   "0": [
        {
          "name": 1,
          "load": 1,
          "requ": 1,
          "weigh": 1,
          "min": 1
       },
       ...
   ],
   ...
}
```
The key is the id of the robot in the decimal format from 0 to
(number of robots - 1). And the value is the list of candidate
tasks. The task info can be automatically inserted by just appending
the task elements of "task_list" input. After you create the new
selector you can register it by appending the new case in the 
"allocate" method in the "main.py".
