import paho.mqtt.client as mqtt


class HubDataSender:

    def __init__(self):
        self.client = mqtt.Client(client_id="Motor_data_Sender")

    def connect_to_controller(self):
        print("Connecting to Host...")
        self.client.connect(host="192.168.0.41")

    def disconnect_from_controller(self):
        print("Disconnecting from Host...")
        self.client.disconnect()

    def send_motor_commands(self, steering, motors):
        # print("Sending steering and motor values: " + str(steering) + " " + str(motors))
        self.client.publish("control/motor/power", motors)
        self.client.publish("control/steering/power", steering)
