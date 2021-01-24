import paho.mqtt.client as mqtt
from PySide2.QtCore import QThread, Signal


class HubDataReceiver(QThread):
    # Defining signal outside __init__ to to avoid exception:
    # AttributeError: 'PySide2.QtCore.Signal' object has no attribute 'connect'
    statusUpdate = Signal()

    def __init__(self):
        super(HubDataReceiver, self).__init__()
        self.client = mqtt.Client(client_id="HubReceiver")

        self.status = 'Unknown'
        self.fw = 'Unknown'
        self.hw = 'Unknown'
        self.batteryLevel = 0

    def connect_to_controller(self):
        print("Connecting to Host...")
        self.client.connect(host="192.168.0.41")
        self.client.subscribe("hub/status")
        self.client.subscribe("hub/fw")
        self.client.subscribe("hub/hw")
        self.client.subscribe("hub/battery")
        self.client.on_message = self.on_message

    def disconnect_from_controller(self):
        print("Disconnecting from Host...")
        self.client.disconnect()

    def run(self):
        print("Waiting to receive data...")
        self.client.loop_forever(retry_first_connection=True)

    def on_message(self, client, userdata, message):
        topic = message.topic
        payload = message.payload.decode("utf-8")

        print('Topic: ' + topic + ' payload: ' + payload)

        if topic == 'hub/status':
            self.status = payload
        elif topic == 'hub/fw':
            self.fw = payload
        elif topic == 'hub/hw':
            self.hw = payload
        elif topic == 'hub/battery':
            self.batteryLevel = int(payload)

        self.statusUpdate.emit()  # Emit a signal when status is updated
