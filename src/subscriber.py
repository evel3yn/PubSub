import zmq
import sys

context = zmq.Context()
socket = context.socket(zmq.SUB)
# ip
srv_addr = sys.argv[1] if len(sys.argv) > 1 else "localhost"
connect_str = "tcp://" + srv_addr + ":5550"

print("Collecting updates from weather server...")
socket.connect(connect_str)
#filter
zip_filter = sys.argv[2] if len(sys.argv) > 2 else "10001"
if isinstance(zip_filter, bytes):
    zip_filter = zip_filter.decode('ascii')
socket.setsockopt_string(zmq.SUBSCRIBE, zip_filter)

while True:
    zip = tem = rel = ['', '', '', '', '']
    zipInt = temInt = relInt = [0, 0, 0, 0, 0]

    i = 0
    print("ready to receive")
    string = socket.recv_string()
    print("message received")
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

    print("This is received history")
    a = 1
    for l in range(0, 5):
        # if zipInt[l] == int(zip_filter):
        print("%ith temperature is %i" % (a, temInt[l]))
        print("%ith relhumidity is %i" % (a, relInt[l]))
        a += 1

    print('This is received message')
    print("Topic: %s, Temperature: %s, Humidity: %s, Strength: %s" % (
        zipcodeStr, temperatureStr, relhumidityStr, strengthStr))
