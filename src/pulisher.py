from time import sleep
import zmq
import sys
from random import randrange

context = zmq.Context()

socket = context.socket(zmq.PUB)

srv_addr = sys.argv[1] if len(sys.argv) > 1 else "localhost"
connect_str = "tcp://" + srv_addr + ":5556"

socket.connect(connect_str)

zipcode = 37215
# second argument is strength of pub, 0~...
strength = int(sys.argv[2]) if len(sys.argv) > 2 else 0

while True:
    temperature = randrange(-80, 135)
    relhumidity = randrange(10, 60)

    socket.send_string("%i %i %i %i" % (zipcode, temperature, relhumidity, strength))
    # print "send messages"
    sleep(1)
