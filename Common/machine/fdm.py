import base


class FDM(base.Machine):
    def __init__(self, x_size=None, y_size=None, z_size=None, material=None, state=None, temp_nozzle=None, temp_bed=None,
                 worked_time=None, color=None, nozzle_size=None, task_info=None):
        self.type = base.Type.FDM
        self.x_size = x_size
        self.y_size = y_size
        self.z_size = z_size
        self.material = material
        self.state = state
        self.temp_nozzle = temp_nozzle
        self.temp_bed = temp_bed
        self.worked_time = worked_time
        self.color = color
        self.nozzle_size = nozzle_size
        self.task_info = task_info

    def parse_data(self, data):
        state = dict()
        self.state = data[1]
        self.temp_nozzle = data[2] * 100 + data[3]
        self.temp_bed = data[6] * 100 + data[7]
        self.worked_time = data[9] * 100 + data[10]
        self.type = data[11]
        self.x_size = data[12] * 100 + data[13]
        self.y_size = data[14] * 100 + data[15]
        self.z_size = data[16] * 100 + data[17]
        self.color = data[18]
        self.nozzle_size = data[19] / 10.0

    def parse_data_to_bootstrap_table(self, index, addr):
        state = dict()
        state["id"] = index
        state["address"] = addr
        state["state"] = self.state
        state["temp_nozzle"] = self.temp_nozzle
        state["temp_bed"] = self.temp_bed
        state["worked_time"] = self.worked_time
        state["type"] = self.type
        state["xyz_size"] = '{0}*{1}*{2}'.format(self.x, self.y, self.z)
        state["color"] = self.color
        state["nozzle_size"] = self.nozzle_size
        state["task"] = self.task_info
        return state
