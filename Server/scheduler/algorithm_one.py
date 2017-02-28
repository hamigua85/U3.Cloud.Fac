import base, json
from app import task_redis
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
        for machine_addr in task_redis.keys():
            data = task_redis.get(machine_addr)
            online_machine = fdm.FDM()
            index += 1
            temp = online_machine.parse_data_to_bootstrap_table(index, machine_addr, json.loads(data))
            machines_info.append(temp)
        return machines_info
