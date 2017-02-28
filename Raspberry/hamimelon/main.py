import requests, time, json
from threading import Timer
from machine import fdm


current_machine = fdm.FDM()


def get_machine_state():
    return current_machine.__dict__


def send_machine_state():
    info = get_machine_state()
    try:
        print str(time.time())
        print info
        r = requests.post("http://192.168.0.99:5000/online_machine_state", data=json.dumps(info), timeout=5)
    except Exception, e:
        print e
    finally:
        t = Timer(5, send_machine_state)
        t.start()

if __name__ == "__main__":
    send_machine_state()
