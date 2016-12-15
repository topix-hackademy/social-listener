import multiprocessing as mp
import logging
import json
import os
import psutil
from datetime import datetime as dt


class ProcessManager(object):

    def __init__(self, data_file):
        self.data_file = data_file
        self.jobs = []
        self.status = []
        self.create_structure()

    def create_structure(self):
        if not os.path.isfile(self.data_file):
            self.init_configuration()

    def init_configuration(self):
        self.dump_new_process_list({"data": [], "last_update": dt.now().strftime("%Y/%m/%d-%H:%M:%S")})

    def read_json_return_dict(self):
        with open(self.data_file, 'r') as fp:
            return json.load(fp)

    def create_process(self, target, name):
        try:
            p = mp.Process(target=target, name=name)
            p.start()
            self.jobs.append(p)
            self.update_process_list(p)
        except Exception as e:
            logging.error(e)
            return False
        return True

    def update_process_list(self, new_process):
        data = self.read_json_return_dict()
        data['data'].append({"name": new_process.name,
                             "pid": new_process.pid,
                             "is_alive": new_process.is_alive(),
                             "created": dt.now().strftime("%Y/%m/%d-%H:%M:%S"),
                             "last_update": dt.now().strftime("%Y/%m/%d-%H:%M:%S")})
        data['last_update'] = dt.now().strftime("%Y/%m/%d-%H:%M:%S")
        self.dump_new_process_list(data)

    def dump_new_process_list(self, data):
        with open(self.data_file, 'w') as fp:
            json.dump(data, fp)

    def refersh_status(self):
        data = self.read_json_return_dict()
        what_time_is_now = dt.now().strftime("%Y/%m/%d-%H:%M:%S")
        for entry in data['data']:
            if not psutil.pid_exists(entry['pid']) and entry['is_alive']:
                entry['is_alive'] = False
                entry['last_update'] = what_time_is_now
        data['last_update'] = what_time_is_now
        self.dump_new_process_list(data)
