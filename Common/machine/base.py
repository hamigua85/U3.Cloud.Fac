class State:
    Ready = 'ready'
    Preoperation = 'preoperation'
    Working = 'working'
    Done = 'done'
    Fault = 'fault'


class Type:
    FDM = 'FDM'
    SLM = 'SLM'


class Color:
    White = 'white'
    Black = 'black'
    Yellow = 'yellow'
    Blue = 'blue'


class Material:
    ABS = 'ABS'
    PLA = 'PLA'


class Machine:
    def __init__(self):
        self.material = None
        self.x_size = None
        self.y_size = None
        self.z_size = None
        pass
