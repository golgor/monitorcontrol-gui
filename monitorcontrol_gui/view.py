from PySide6.QtWidgets import QMainWindow
from monitorcontrol_gui.controller import Controller
from monitorcontrol_gui.model import Model, Monitor
from monitorcontrol_gui.ui.main_window import Ui_MainWindow


class View(QMainWindow):
    """Class handling the main window of the app."""
    def __init__(self, ctrl: Controller, model: Model) -> None:
        """Initializer of the graphical interface.

        Setting up the controller and model as well as initializing the actual
        graphical qt interface. It also queries for monitors using QThread to
        not block the main thread.

        Args:
            ctrl (Controller): _description_
            model (Model): _description_
        """
        super().__init__()
        self.ctrl = ctrl
        self.model = model
        print("Setting up UI")
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.buttonSet.clicked.connect(self.set_button_handler)
        self.ctrl.query_monitors(self.init_monitor_combobox)

    def init_monitor_combobox(self, monitors: list[Monitor]) -> None:
        """Initialize the monitor combobox.

        Insert all monitors into the combobox. Also adds 'All' with index 0 as
        the first entry, and also the default. Sets the items from the model
        using the ID and Model.

        Sets the current index to 'All'.
        """
        self.ui.monitorComboBox.addItem("0: All")
        self.ui.monitorComboBox.addItems([
            f"{monitor.idx}: {monitor.model}"
            for monitor in monitors
        ])
        self.ui.monitorComboBox.setCurrentIndex(0)

    def set_button_handler(self) -> None:
        """Handler for clicking the setButton.

        Setting the luminosity of the monitor with the given index of the
        combo box. Extracts the index from the text value in the combobox.
        """
        value = int(self.ui.luminanceValueLabel.text())
        idx = int(self.ui.monitorComboBox.currentText().split(":")[0])
        self.ctrl.set_luminosity(value, idx)
