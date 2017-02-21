# -*- coding:utf-8 -*-
machine_state = {1: "ready", 2: "preoperation", 3: "working", 4: "done", 5: "fault"}
machine_type = {1: "fdm"}
color = {1: "white", 2: "black", 3: "yellow", 4: "blue"}


def fdm_data_parser(index, addr, data):
    state = dict()
    state["id"] = index
    state["address"] = addr
    state["state"] = machine_state[data[1]]
    state["temperature"] = 'nozzle:{0}℃, Bed:{1}℃'.format(data[2]*100 + data[3], data[6]*100 + data[7])
    state["progress"] = '{0}%'.format(data[8])
    state["worked_time"] = data[9]*100 + data[10]
    state["type"] = machine_type[data[11]]
    state["xyz_size"] = '{0}*{1}*{2}'.format(data[12]*100 + data[13], data[14]*100 + data[15], data[16]*100 + data[17])
    state["color"] = color[data[18]]
    state["nozzle_size"] = data[19]/10.0
    state["task"] = ""
    for d in data[20:len(data)]:
        state["task"] += chr(d)
    return state
