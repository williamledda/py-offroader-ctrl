import paho.mqtt.client as mqtt
from PySide2.QtCore import QThread, Signal


class HubDataReceiver(QThread):
    def __init__(self):
        self.client = mqtt.Client(client_id="HubReceiver")

        self.status = 'Unknown'
        self.fw = 'Unknown'
        self.hw = 'Unknown'
        self.battery = 0

        self.client.subscribe("hub/status")
        self.client.subscribe("hub/fw")
        self.client.subscribe("hub/hw")
        self.client.subscribe("hub/battery")
        self.client.on_message = self.on_message
        self.statusReceived = Signal()

    def connectToHub(self):
        print("Connecting to Host...")
        self.client.connect(host="192.168.0.41")

    def disconnectFromHub(self):
        print("Disconnecting from Host...")
        self.client.disconnect()

    def run(self):
        self.client.loop_forever()

    def on_message(self, userdata, message):
        topic = message.topic

        if topic == 'hub/status':
            self.status = message.payload
        elif topic == 'hub/fw':
            self.fw = message.payload
        elif topic == 'hub/hw':
            self.hw = message.payload
        elif topic == 'hub/battery':
            self.battery = int(message.payload)
        self.statusReceived.emit()
