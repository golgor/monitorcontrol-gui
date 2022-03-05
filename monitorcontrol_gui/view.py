from PySide6.QtWidgets import QMainWindow
from monitorcontrol_gui.controller import Controller
from monitorcontrol_gui.model import Model


class View(QMainWindow):
    def __init__(self, ctrl: Controller, model: Model) -> None:
        super().__init__()
        self.ctrl = ctrl
        self.model = model
