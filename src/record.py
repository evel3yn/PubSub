import sys
import zmq

#  Socket to talk to server
context = zmq.Context()

# Since we are the subscriber, we use the SUB type of the socket
socket = context.socket(zmq.SUB)

connect_str = "tcp://" + "10.0.0.1" + ":5550"

print("Collecting updates from weather server...")
socket.connect(connect_str)

socket.setsockopt(zmq.SUBSCRIBE, '')
print "ready to receive"
string = socket.recv_string()
print "message received"
