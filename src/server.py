import copy
import zmq
import Queue

# False if no same zipcode
# return all zipcode if it has same element
def checksame(zlist):
    retlist = []
    for temp in zlist:
        # how many element have this value
        flag = zipList.count(temp)
        if flag > 1:
            if retlist.count(temp) == 0:
                retlist.append(temp)
    return retlist


# return the index of element who has the max strength
def getmax(indexList, strengList):
    a = []
    for index in indexList:
        a.append(strengList[index])
    return a.index(max(a))


#connext the socket
context = zmq.Context()
# socket = context.socket(zmq.PUB)
# socket.bind("tcp://*:5556")

socket = context.socket(zmq.SUB)
socket.bind("tcp://*:5556")


# subscribe all incoming topic
socket.setsockopt(zmq.SUBSCRIBE, '')

# send them seperately
# only need one context
socket2 = context.socket(zmq.PUB)
socket2.bind("tcp://*:5550")


zipcodeArrayHis = Queue.Queue()
temperatureArrayHis = Queue.Queue()
relhumidityArrayHis = Queue.Queue()
zipcodeArrayHisT = Queue.Queue()
temperatureArrayHisT = Queue.Queue()
relhumidityArrayHisT = Queue.Queue()

# initialize history
for x in range(0, 5):
    zipcodeArrayHis.put(0)
    temperatureArrayHis.put(0)
    relhumidityArrayHis.put(0)

# initialize new history
zipNewHis = 0
temNewHis = 0
relNewHis = 0


# store 5 messages in a class
class History:

    def __init__(self, zipc, tem, rel, stren, zipH, temH, relH):
        self.zipcode = int(zipc)
        self.temperature = int(tem)
        self.relhumidity = int(rel)
        self.strength = int(stren)
        self.zipHis = zipH
        self.temHis = temH
        self.relHis = relH


while True:
    i = 0
    # assume it will receive 5 messages at the same time

    # 5 History object
    hisList = []

    while (i < 5):
        print ("ready to receive")
        # blocking is default
        string = socket.recv_string()
        print ("received message")
        # receive the message
        zipcode, temperature, relhumidity, strength = string.split()

        print (zipcode)

        # push in the new history
        zipcodeArrayHis.put(zipNewHis)
        temperatureArrayHis.put(temNewHis)
        relhumidityArrayHis.put(relNewHis)

        # pop up the old history
        zipcodeArrayHis.get()
        temperatureArrayHis.get()
        relhumidityArrayHis.get()

        # next time this should be pushed in history queue
        zipNewHis = int(zipcode)
        temNewHis = int(temperature)
        relNewHis = int(relhumidity)

        # copy queue
        zipcodeArrayHisT.queue = copy.deepcopy(zipcodeArrayHis.queue)
        temperatureArrayHisT.queue = copy.deepcopy(temperatureArrayHis.queue)
        relhumidityArrayHisT.queue = copy.deepcopy(relhumidityArrayHis.queue)

        # History
        # change to list and then use '/' as delimiter to make a string
        tempt = [zipcodeArrayHisT.get(), zipcodeArrayHisT.get(), zipcodeArrayHisT.get(), zipcodeArrayHisT.get(),
                 zipcodeArrayHisT.get()]
        zipHis = '/'.join(str(e) for e in tempt)
        tempt = [temperatureArrayHisT.get(), temperatureArrayHisT.get(), temperatureArrayHisT.get(),
                 temperatureArrayHisT.get(), temperatureArrayHisT.get()]
        temHis = '/'.join(str(e) for e in tempt)
        tempt = [relhumidityArrayHisT.get(), relhumidityArrayHisT.get(), relhumidityArrayHisT.get(),
                 relhumidityArrayHisT.get(), relhumidityArrayHisT.get()]
        relHis = '/'.join(str(e) for e in tempt)

        # store the message in class array
        hisList.append(History(zipcode, temperature, relhumidity, int(strength), zipHis, temHis, relHis))

        i += 1

    # get rid of the repeated topic hisList elements.
    # get all the zipcode
    zipList = [hisList[0].zipcode, hisList[1].zipcode, hisList[2].zipcode, hisList[3].zipcode, hisList[4].zipcode]
    # get all the strength
    strengList = [hisList[0].strength, hisList[1].strength, hisList[2].strength, hisList[3].strength,
                  hisList[4].strength]
    # if there is any element same
    # if not empty, that means there are same element
    retZipList = checksame(zipList)
    if retZipList:
        # for every repeated element
        for zip in retZipList:
            indexList = []
            i = 0
            for ziporigin in zipList:
                if zip == ziporigin:
                    indexList.append(i)
                i += 1
            # index of max strength element
            maxindex = getmax(indexList, strengList)
            # indexs of other repeated elemtns
            indexList.pop(maxindex)
            # pop up these repeated hisList elemtents
            # sort the index reversely
            reverseIndexList = reversed(sorted(indexList))
            for index in reverseIndexList:
                hisList.pop(index)

    # send all history
    for his in hisList:
        # send last 5 infor (if repeated, not send)
        socket2.send_string("%i %i %i %i %s %s %s" % (
            his.zipcode, his.temperature, his.relhumidity, his.strength, his.zipHis, his.temHis, his.relHis))
        print ("send message")
