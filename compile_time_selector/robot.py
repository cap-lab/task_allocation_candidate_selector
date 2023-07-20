class Robot:
    def __init__(self, index, robot_info):
        self.index = index
        self.robot_info = robot_info 

    def get_cons(self):
        return self.robot_info['cons']
