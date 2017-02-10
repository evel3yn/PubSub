import zmq
import sys
from array import *

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5556")
# subscribe all incoming topic
socket.setsockopt(zmq.SUBSCRIBE, "")

zipcodeArrayHis = array('i', [0, 0, 0, 0, 0])
temperatureArrayHis = array('i', [0, 0, 0, 0, 0])
relhumidityArrayHis = array('i', [0, 0, 0, 0, 0])
while True:
    i = 0
    while (i < 5):
        # blocking is default
        string = socket.recv_string()
        zipcode, temperature, relhumidity, strength = string.split()
        i = i + 1

        zipcodeArrayHis[i] = zipcode
        temperatureArrayHis[i] = temperature
        relhumidityArrayHis[i] = relhumidity

        # History
        tempt = zipcodeArrayHis.tolist()
        zipHis = '/'.join(str(e) for e in tempt)
        tempt = temperatureArrayHis.tolist()
        temHis = '/'.join(str(e) for e in tempt)
        tempt = relhumidityArrayHis.tolist()
        relHis = '/'.join(str(e) for e in tempt)

        # only need one context
        socket2 = context.socket(zmq.PUB)
        socket.bind("tcp://*:5556")
        # send these 5 information in one time
        # send last 5 infor as history
        socket.send_string(
            "%i %i %i %i %s %s %s" % (zipcode, temperature, relhumidity, strength, zipHis, temHis, relHis))

        i = i + 1
        if i == 5:
            i = 0
