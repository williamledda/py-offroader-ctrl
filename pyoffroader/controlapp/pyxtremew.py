from PySide2.QtWidgets import QWidget
from PySide2.QtCore import QFile, Slot
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QTimer
from pyoffroader.motorinterface import HubDataSender, HubDataReceiver


class PyXtremeW(QWidget):
    def __init__(self):
        super(PyXtremeW, self).__init__()
        self.widget = None
        self.motorSender = HubDataSender.HubDataSender()
        self.motorSender.connect_to_controller()

        self.hubReceiver = HubDataReceiver.HubDataReceiver()
        self.hubReceiver.connect_to_controller()
        self.hubReceiver.statusUpdate.connect(self.update_status)

        self.load_ui()

        if self.widget is not None:
            self.widget.motorSlider.sliderReleased.connect(self.on_motor_slider_released)
            self.widget.steeringSlider.sliderReleased.connect(self.on_steering_slider_released)

            self.timer = QTimer()
            self.timer.setInterval(200)
            self.timer.timeout.connect(self.on_timer)

            self.timer.start()
            self.hubReceiver.start()  # Run data receiver thread

    def load_ui(self):
        loader = QUiLoader()
        # path = os.path.join(os.path.dirname(__file__), "form.ui")
        ui_file = QFile('ui/pyxtremew.ui')
        ui_file.open(QFile.ReadOnly)
        self.widget = loader.load(ui_file, self)
        ui_file.close()

    def closeEvent(self, event):
        if self.motorSender is not None:
            self.motorSender.disconnect_from_controller()
            self.hubReceiver.disconnect_from_controller()

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

    @Slot()
    def update_status(self):
        self.widget.statusLabel.setText(self.hubReceiver.status)
        self.widget.fwVersionLabel.setText(self.hubReceiver.fw)
        self.widget.hwVersionLabel.setText(self.hubReceiver.hw)
        self.widget.batteryLvl.setValue(self.hubReceiver.batteryLevel)
