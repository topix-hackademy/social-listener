import multiprocessing as mp

class ProcessManager(object):

    def __init__(self, data_file):
        self.data_file = data_file
        self.jobs = []

    def create_process(self, target):
        try:
            self.jobs.append(mp.Process(target=target))
            self.update_process_list()
        except Exception as e:
            return False
        return True

    def update_process_list(self):
        pass

