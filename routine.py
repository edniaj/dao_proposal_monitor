import time
from typing import List

class IRoutineTask:
    def run_task(self):
        pass

class IRoutineController:
    def add_routine_task(self, task: IRoutineTask):
        pass
        
    def run_controller(self):
        pass

class RoutineTask:
    def __init__(self, _callback, _interval):

        self.timestamp = 0
        self.interval = _interval
        self.callback = _callback

    def run_task(self):

        timestamp_now = time.time()
        '''
        04/02/2023 @ jd
        i.e. 
        8am + 5 mins interval < 8.04
        if true then we should run the callback function

        if false then we should respect the interval

        '''
        if self.timestamp + self.interval < timestamp_now:

            self.callback()

            '''
            Update timestamp
            '''
            timestamp_now = time.time()           
            self.timestamp = timestamp_now + self.interval

class RoutineController:
    
    def __init__(self):
        self.task_list : List[RoutineTask] = []
    
    def add_routine_task(self, _callback, _interval):
        
        new_task = RoutineTask(_callback, _interval)
        self.task_list.append(new_task)

    def run_controller(self):
        
        while 1:
            for each_task in self.task_list:
                try:
                    each_task.run_task()
                except Exception as e:
                    print(f"Error running task: {e}")

        


controller = RoutineController()
'''

'''
# c.add_routine_task( lambda:print('hello3'), 3)
# c.add_routine_task( lambda:print('hello1'), 1)

controller.run_controller()