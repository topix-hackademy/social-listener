import logging
import multiprocessing as mp
import psutil
from application.utils.helpers import what_time_is_it
from application.mongo import Connection


class ProcessManager(object):

    @staticmethod
    def get_single_process(pid):
        """
        Get a Single Process given the PID
        :param pid:  Process ID
        :return:
        """
        return Connection.Instance().db.manager.find_one({'pid': pid})

    @staticmethod
    def get_all_processes():
        """
        Return the list of the processes
        :return:
        """
        return list(Connection.Instance().db.manager.find().sort([('last_update', -1)]))

    @staticmethod
    def get_all_processes_with_condition(condition):
        """
        Return the list of the processes
        :return:
        """
        return list(Connection.Instance().db.manager.find(condition).sort([('last_update', -1)]))

    @staticmethod
    def update_process(pid, newobj):
        """
        Update a single process
        :param pid: PID
        :param newobj: New Object to Set
        :return:
        """
        return Connection.Instance().db.manager.update({'pid': pid}, {'$set': newobj})

    @staticmethod
    def insert_process(process):
        """
        Insert new process
        :param process: Process object
        :return:
        """
        return Connection.Instance().db.manager.insert_one(process)

    @staticmethod
    def terminate_process(pid, new_status):
        """
        Update the "terminated" of a singe process
        :param pid: Process ID
        :param new_status: True / False
        :return:
        """
        ProcessManager.update_process(pid, {
            'terminated': new_status, 'last_update': what_time_is_it()
        })

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
        :param new_process: Process object
        :param ptype: Process type
        :return:
        """
        what_time_is_now = what_time_is_it()
        self.insert_process({
            "name": new_process.name,
            "ptype": ptype,
            "pid": new_process.pid,
            "is_alive": new_process.is_alive(),
            "created": what_time_is_now,
            "terminated": False,
            "last_update": what_time_is_now
        })

    def refresh_status(self):
        """
        Refresh process status.
        If a process is dead or in zombie status a flag 'is_alive' will be setted to False
        :return:
        """
        what_time_is_now = what_time_is_it()
        for process in Connection.Instance().db.manager.find({}):
            if (not psutil.pid_exists(process['pid']) and process['is_alive']) or \
                    (psutil.pid_exists(process['pid']) and psutil.Process(process['pid']).status() ==
                        psutil.STATUS_ZOMBIE and process['is_alive']):
                self.update_process(process['pid'], {
                        'is_alive': False,
                        'last_update': what_time_is_now
                    })
            elif psutil.pid_exists(process['pid']) and process['is_alive']:
                self.update_process(process['pid'], {'last_update': what_time_is_now})
        logging.info('Refresh Done!')

    def stop_process(self, pid):
        """
        Stop a child process
        :param pid: Process ID
        :return: True/False, MESSAGE_TO_PRINT
        """
        try:
            process = self.get_single_process(int(pid))
            if not process:
                return False, 'Process Not In List'
            psutil.Process(process['pid']).terminate()
        except Exception as e:
            logging.error(e)
            return False, 'Process does not exists'
        return True, 'Process Stopped'
