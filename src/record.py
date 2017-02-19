import zmq
import sys
from random import randrange

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5556")

print("Sending information to whether server...")

zipcode = randrange(1, 100000)
# second argument is strength of pub, 0~...
strength = int(sys.argv[2]) if len(sys.argv) > 2 else 0

while True:
    temperature = randrange(-80, 135)
    relhumidity = randrange(10, 60)

    socket.send_string("%i %i %i %i" % (zipcode, temperature, relhumidity, strength))
