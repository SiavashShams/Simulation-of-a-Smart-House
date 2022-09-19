
import paho.mqtt.client as mqtt
import time,json,random


button_state = {"enabled": False}
def on_log(client, userdata, level, buf):
   print(buf)
def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True #set flag
        #client.subscribe('v1/devices/me/rpc/request/+')
        print("connected OK")
    else:
        print("Bad connection Returned code=",rc)
        client.loop_stop()
def on_disconnect(client, userdata, rc):
   print("client disconnected ok")
def setValue(params):
    button_state['enabled'] = params
    print("Rx setValue is : ", button_state)
def on_publish(client, userdata, mid):
    print("In on_pub callback mid= "  ,mid)
def on_message(client, userdata, msg):
    print('Topic: ' + msg.topic + '\nMessage: ' + str(msg.payload))
    if msg.topic.startswith('v1/devices/me/rpc/request/'):
        requestId = msg.topic[len('v1/devices/me/rpc/request/'):len(msg.topic)]
        print("requestId : ", requestId)
        data = json.loads(msg.payload)
        if data['method'] == 'getValue':
            print("getvalue request\n")
            print("sent getValue : ", button_state)
            client.publish('v1/devices/me/rpc/response/' + requestId, json.dumps(button_state), 1)
        if data['method'] == 'setValue':
            print("setvalue request\n")
            params = data['params']
            setValue(params)
            client.publish('v1/devices/me/attributes', json.dumps(button_state), 1)
        if data['method']=='rpcCommand':
            data_outt=data['params']
            client.publish('v1/devices/me/telemetry', json.dumps(data_outt), 1)

class Sensor:
    def __init__(self, client, topic, qos, change, interval, direction, \
                 start_value, min_value, max_value):
        self.client = client
        self.change_up = change
        self.change_down = -change
        self.change = change
        self.interval = interval
        self.temp = start_value
        self.max_value = max_value
        self.min_value = min_value
        self.direction = direction
        self.topic = topic
        self.qos = qos

    def random_change(self):
        a = random.randint(0, 10)
        b = random.randint(0, 25)
        print("direction =", self.direction)
        if b == 6 and self.direction == "up":
            self.direction = "down"
            # print("Reversing")
        elif b == 6 and self.direction == "down":  # decreasing temperature
            self.direction = "up"
            # print("Reversing")
        if self.direction == "up":
            self.change = self.change_up
        else:
            self.change = self.change_down
        if a == 5 and self.direction == "up":
            self.change = self.change_down
        elif a == 5 and self.direction == "down":
            self.change = self.change_up

    def publish(self, data_out):
        print("data out=", data_out)
        self.client.publish(self.topic, data_out, self.qos)  # publish

    def update(self):
        self.random_change()
        self.temp = self.temp + self.change

    def start(self):
            self.update()
            self.client.loop(0.01)
            if self.temp >= self.max_value:
                self.temp = self.max_value
            if self.temp <= self.min_value:
                self.temp = self.min_value

            # print("temp =",self.temp)
            if json_data_flag:
                data = dict()
                data["room-temp"] = self.temp
                data_out = json.dumps(data)
            else:
                data_out = self.temp
            self.publish(data_out)
            # print("change is ",self.change)
            time.sleep(self.interval)

count=0
mqtt.Client.connected_flag=False        #create flag in class
mqtt.Client.suppress_puback_flag=False
client = mqtt.Client("python1")             #create new instance
#client.on_log=on_log
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_publish = on_publish
client.on_message=on_message
broker="demo.thingsboard.io"
port =1883
topic="v1/devices/me/telemetry"
#need to edit user name
username="Your Token"
password=""
if username !="":
   pass
client.username_pw_set(username, password)
client.connect(broker,port)           #establish connection
while not client.connected_flag: #wait in loop
   client.loop()
   time.sleep(1)
time.sleep(3)
data=dict()
json_data_flag = True
qos = 0
change = 0.5
interval = 2
direction = "up"
min_value = 0
max_value = 30
start_value = 20
s = Sensor(client, topic, qos, change, interval, direction, start_value, min_value, max_value)
for i in range(100):
    data["Lights"]="ON"
    data["Door"]="OPEN"
    data_out=json.dumps(data)
    print("publish topic",topic, "data out= ",data_out)
    ret=client.publish(topic,data_out,0)
    s.start()
    time.sleep(2)
    client.loop()
    data["Lights"]="OFF"
    data["Door"]="CLOSED"
    data_out=json.dumps(data)
    print("publish topic",topic, "data out= ",data_out)
    ret=client.publish(topic,data_out,0)
    s.start()
    time.sleep(2)
    client.loop()

client.disconnect()



