class State:
    Ready = 1
    Preoperation = 2
    Working = 3
    Done = 4
    Fault = 5


class Type:
    FDM = 1
    SLM = 2


class Color:
    White = 1
    Black = 2
    Yellow = 3
    Blue = 4


class Material:
    ABS = 1
    PLA = 2


class Machine:
    def __init__(self):
        self.material = None
        self.x_size = None
        self.y_size = None
        self.z_size = None
        pass
