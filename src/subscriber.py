from array import array

import zmq
import sys

context = zmq.Context()
socket = context.socket(zmq.SUB)
srv_addr = sys.argv[1] if len(sys.argv) > 1 else "localhost"
connect_str = "tcp://" + srv_addr + ":5556"
print("Collecting updates from weather server...")
socket.connect(connect_str)
zip_filter = sys.argv[2] if len(sys.argv) > 2 else "10001"
if isinstance(zip_filter, bytes):
    zip_filter = zip_filter.decode('ascii')
socket.setsockopt_string(zmq.SUBSCRIBE, zip_filter)

while True:
    zip = array('s', ['0', '0', '0', '0', '0'])
    tem = array('s', ['0', '0', '0', '0', '0'])
    rel = array('s', ['0', '0', '0', '0', '0'])

    zipInt = array('i', [0, 0, 0, 0, 0])
    temInt = array('i', [0, 0, 0, 0, 0])
    relInt = array('i', [0, 0, 0, 0, 0])

    i = 0

    string = socket.recv_string()
    zipcodeStr, temperatureStr, relhumidityStr, strengthStr, zipHisStr, temHisStr, relHisStr = string.split()
    # receive history
    zip[0], zip[1], zip[2], zip[3], zip[4] = zipHisStr.split("/")
    tem[0], tem[1], tem[2], tem[3], tem[4] = temHisStr.split("/")
    rel[0], rel[1], rel[2], rel[3], rel[4] = relHisStr.split("/")

    # turn the string to int
    for k in range(5):
        zipInt[k] = int(zip[k])
        temInt[k] = int(tem[k])
        relInt[k] = int(rel[k])

    print("This is history")
    for l in range(0, 5):
        if zipInt[l] == int(zip_filter):
            print("tem %i" % temInt[l])
            print("rel %i" % relInt[l])

    print('This is received message')
    print("Topic: %s, Temperature: %s, Humidity: %s, Strength: %s" % (
    zipcodeStr, temperatureStr, relhumidityStr, strengthStr))
