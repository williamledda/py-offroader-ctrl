from PySide2.QtWidgets import QWidget
from PySide2.QtCore import QFile, Slot
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QTimer
from pyoffroader.motorinterface import HubDataSender, HubDataReceiver
import paho.mqtt.client as mqtt


class PyXtremeW(QWidget):
    def __init__(self):
        super(PyXtremeW, self).__init__()
        self.widget = None
        self.motorSender = HubDataSender.HubDataSender()
        self.motorSender.connectToHub()

        self.hubReceiver = mqtt.Client(client_id="HubReceiver")
        self.hubReceiver.connect(host="192.168.0.41")
        self.hubReceiver.subscribe("hub/status")
        self.hubReceiver.subscribe("hub/fw")
        self.hubReceiver.subscribe("hub/hw")
        self.hubReceiver.subscribe("hub/battery")
        self.hubReceiver.on_message = self.on_message

        self.load_ui()

        if self.widget is not None:
            self.widget.motorSlider.sliderReleased.connect(self.on_motor_slider_released)
            self.widget.steeringSlider.sliderReleased.connect(self.on_steering_slider_released)

            self.timer = QTimer()
            self.timer.setInterval(200)
            self.timer.timeout.connect(self.on_timer)

            self.timer.start()
            self.hubReceiver.loop_start()

    def load_ui(self):
        loader = QUiLoader()
        # path = os.path.join(os.path.dirname(__file__), "form.ui")
        ui_file = QFile('ui/pyxtremew.ui')
        ui_file.open(QFile.ReadOnly)
        self.widget = loader.load(ui_file, self)
        ui_file.close()

    def closeEvent(self, event):
        if self.motorSender is not None:
            self.motorSender.disconnectFromHub()

    @Slot()
    def on_motor_slider_released(self):
        self.widget.motorSlider.setValue(0)

    @Slot()
    def on_steering_slider_released(self):
        self.widget.steeringSlider.setValue(0)

    @Slot()
    def on_timer(self):
        if self.motorSender is not None:
            self.motorSender.send_motor_commands(self.widget.steeringSlider.value(), self.widget.motorSlider.value())

    def on_message(self, client, userdata, message):
        topic = message.topic
        payload = message.payload.decode("utf-8")

        print('Topic: ' + topic + ' payload: ' + payload)

        if topic == 'hub/status':
            self.widget.statusLabel.setText(payload)
        elif topic == 'hub/fw':
            self.widget.fwVersionLabel.setText(payload)
        elif topic == 'hub/hw':
            self.widget.hwVersionLabel.setText(payload)
        elif topic == 'hub/battery':
            self.widget.batteryLvl.setValue(int(payload))
