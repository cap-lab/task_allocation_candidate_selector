class Robot:
    def __init__(self, index, location, robot_info, task_info):
        self.index = index
        self.location = location 
        self.stop = False
        self.robot_info = robot_info 
        self.task_info = task_info
        self.db = dict()
        self.old_db = dict()
        self.iteration = 0

    def set_task_candidate(self, task_dict):
        self.candidate_task_dict = task_dict

    def get_capa(self):
        return self.robot_info['capa']

    def set_cons(self, cons):
        self.robot_info['cons'] = cons

    def get_cons(self):
        return self.robot_info['cons']

    def get_candidates(self):
        return self.candidate_task_dict

    def get_task(self):
        return self.db[self.index]['task']

    def change_my_table(self, table):
        self.db[self.index] = table

    def get_db(self):
        return self.db

    def cache_current_db(self):
        for index, table in self.db.items():
            self.old_db[index] = table

    def send(self):
        return self.old_db

    def receive(self, sender_db):
        for index, table in sender_db.items():
            if index in self.db.keys():
                if self.db[index]['count'] < table['count']:
                    self.db[index] = table
            else:
                self.stop = False
                self.iteration = 0
                self.db[index] = table

    def allocate(self, allocator):
        if self.stop is False:
            allocator.run_time_allocate(robot=self, task_dict=self.candidate_task_dict)
            self.iteration = self.iteration + 1

