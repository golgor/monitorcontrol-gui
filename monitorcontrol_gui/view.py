from PySide6.QtWidgets import QMainWindow
from monitorcontrol_gui.controller import Controller
from monitorcontrol_gui.model import Model
from monitorcontrol_gui.ui.main_window import Ui_MainWindow


class View(QMainWindow):
    def __init__(self, ctrl: Controller, model: Model) -> None:
        super().__init__()
        self.ctrl = ctrl
        self.model = model
        print("Setting up UI")
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.buttonSet.clicked.connect(self.click_button)

        self.model.query_monitors()
        self.ui.monitorComboBox.addItem("0: All")
        self.ui.monitorComboBox.addItems([
            f"{monitor.idx}: {monitor.model}"
            for monitor in self.model.monitors
        ])
        self.ui.monitorComboBox.setCurrentIndex(0)

    def click_button(self) -> None:
        value = int(self.ui.luminanceValueLabel.text())
        idx = int(self.ui.monitorComboBox.currentText().split(":")[0])
        self.ctrl.set_luminosity(value, idx)
