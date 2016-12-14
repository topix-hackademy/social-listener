import multiprocessing as mp
import json


class ProcessManager(object):

    def __init__(self, data_file):
        self.data_file = data_file
        self.jobs = []
        self.status = []

    def update_status(self):
        pass

    def create_process(self, target, name):
        try:
            p = mp.Process(target=target, name=name)
            p.start()
            self.jobs.append(p)
            self.update_process_list(p)
        except Exception as e:
            print e
            return False
        return True

    def update_process_list(self, new_process):
        pass

'''
PROCESS JSON FILE EXAMPLE
{
    "name":"",
    "pid":"",
    "is_alive":""
}

'''

