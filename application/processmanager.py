import json
import logging
import multiprocessing as mp
import os
import psutil
from application.utils.helpers import what_time_is_it
from application.utils import globals


class ProcessManager(object):

    def __init__(self, data_file):
        """
        Process Manager Constructor
        :param data_file: position of json status file.
        :param data_file:
        """
        self.data_file = data_file
        self.create_structure()

    def create_structure(self):
        """
        Check if exixts status file, if does not -> Create
        :return:
        """
        if not os.path.isfile(self.data_file):
            self.init_configuration()

    def init_configuration(self):
        """
        Create the init status file
        :return:
        """
        self.dump_new_process_list({"data": [],
                                    "last_update": what_time_is_it()})

    def read_json_return_dict(self):
        """
        Read from json source the process status list
        :return:
        """
        with open(self.data_file, 'r') as fp:
            return json.load(fp)

    def create_process(self, target, name, ptype):
        """
        Create new process
        :param target: target function
        :param name: Name of the new process
        :param ptype: Name of the Process type ['twitter_listener', 'twitter_collector']
        :return: True / False
        """
        try:
            p = mp.Process(target=target, name=name)
            p.daemon = True
            p.start()
            self.update_process_list(p, ptype)
        except Exception as e:
            logging.error(e)
            raise Exception(e)

    def update_process_list(self, new_process, ptype):
        """
        Add new process to process List.
        Then create new process json status file.
        :param new_process: Process object
        :param ptype: Process type
        :return:
        """
        what_time_is_now = what_time_is_it()
        data = self.read_json_return_dict()
        data['data'].append({"name": new_process.name,
                             "ptype": ptype,
                             "pid": new_process.pid,
                             "is_alive": new_process.is_alive(),
                             "created": what_time_is_now,
                             "terminated": False,
                             "last_update": what_time_is_now})
        data['last_update'] = what_time_is_now
        self.dump_new_process_list(data)

    def dump_new_process_list(self, data):
        """
        Create a new json status file.
        :param data: Dictionary with two keys 'data' / 'last_update'
        :return:
        """
        with open(self.data_file, 'w') as fp:
            json.dump(data, fp)

    def refresh_status(self):
        """
        Refresh process status reading from json status file.
        If a process is dead or in zombie status a flag 'is_alive' will be setted to False
        :return:
        """
        data = self.read_json_return_dict()
        what_time_is_now = what_time_is_it()
        for entry in data['data']:
            if (not psutil.pid_exists(entry['pid']) and entry['is_alive']) or \
                    (psutil.pid_exists(entry['pid']) and
                     psutil.Process(entry['pid']).status() == psutil.STATUS_ZOMBIE and
                     entry['is_alive']):
                entry['is_alive'] = False
                entry['last_update'] = what_time_is_now

        data['last_update'] = what_time_is_now
        self.dump_new_process_list(data)

    def stop_process(self, pid):
        """
        Stop a child process
        :param pid: Process ID
        :return: True/False, MESSAGE_TO_PRINT
        """
        try:
            pid = int(pid)
            data = self.read_json_return_dict()
            if not any(entry['pid'] == pid for entry in data['data']):
                return False, 'Process Not In List'
            psutil.Process(pid).terminate()
        except Exception as e:
            logging.error(e)
            return False, 'Process does not exists'
        return True, 'Process Stopped'

    @staticmethod
    def update_process(pid, new_status):
        """
        Update the "terminated" of a singe process
        :param pid:
        :param pid:
        :return:
        """
        with open(globals.configuration.pm_data['data_file'], 'r') as fp:
            data = json.load(fp)
        for process in data['data']:
            if str(process['pid']) == str(pid):
                process['terminated'] = new_status
                process['last_update'] = what_time_is_it()
                break
        data['last_update'] = what_time_is_it()
        with open(globals.configuration.pm_data['data_file'], 'w') as fp:
            json.dump(data, fp)
