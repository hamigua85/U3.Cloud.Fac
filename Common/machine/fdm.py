import base


class FDM(base.Machine):
    def __init__(self, index=None, address=None, x_size=None, y_size=None, z_size=None, material=None, state=None,
                 temp_nozzle=None, temp_bed=None, worked_time=None, color=None, nozzle_size=None, task_info=None):
        self.index = index
        self.address = address
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

    def parse_data_to_bootstrap_table(self, index, addr, data):
        for item in self.__dict__:
            if hasattr(self, item):
                setattr(self, item, data[item])
        self.index = index
        self.address = addr
        return self.__dict__
