from PySide2.QtWidgets import QWidget
from PySide2.QtCore import QFile, Slot
from PySide2.QtUiTools import QUiLoader

class PyXtremeW(QWidget):
    def __init__(self):
        super(PyXtremeW, self).__init__()
        self.widget = None
        self.load_ui()

        self.widget.motorSlider.sliderReleased.connect(self.on_motor_slider_released)
        self.widget.motorSlider.valueChanged.connect(self.on_motor_slider_value_changed)

    def load_ui(self):
        loader = QUiLoader()
        # path = os.path.join(os.path.dirname(__file__), "form.ui")
        ui_file = QFile('ui/pyxtremew.ui')
        ui_file.open(QFile.ReadOnly)
        self.widget = loader.load(ui_file, self)
        ui_file.close()

    @Slot()
    def on_motor_slider_released(self):
        self.widget.motorSlider.setValue(0)

    @Slot()
    def on_motor_slider_value_changed(self, value):
        print('Value set to ' + str(value))

