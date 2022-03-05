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

    def click_button(self) -> None:
        value = int(self.ui.luminanceValueLabel.text())
        self.ctrl.set_luminosity(value)
