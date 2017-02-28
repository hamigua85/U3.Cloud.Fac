import base
from app import redis
from machine import fdm


class AlgorithmOne(base.Scheduler):
    def __init__(self):
        #thread.start_new_thread()
        pass

    def add_task_to_waiting_list(self, task):
        self.waiting_task[str(task.uuid)] = task

    @staticmethod
    def update_online_machines():
        machines_info = []
        index = 0
        for machine_addr in redis.keys():
            data = eval(redis.get(eval(machine_addr)))
            online_machine = fdm.FDM()
            online_machine.parse_data(data)
            index += 1
            temp = online_machine.parse_data_to_bootstrap_table(index, eval(machine_addr))
            machines_info.append(temp)
        return machines_info
