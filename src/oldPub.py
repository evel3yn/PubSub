import zmq
from random import randrange

context = zmq.Context()

# The difference here is that this is a publisher and its aim in life is
# to just publish some value. The binding is as before.
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5556")

# keep publishing
while True:
    zipcode = randrange(1, 100000)
    temperature = randrange(-80, 135)
    relhumidity = randrange(10, 60)

    socket.send_string("%i %i %i" % (zipcode, temperature, relhumidity))
