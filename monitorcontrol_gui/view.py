from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import QObject, QThread, Signal
from monitorcontrol_gui.controller import Controller
from monitorcontrol_gui.model import Model
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

        self.init_monitor_query_thread()

    def init_monitor_query_thread(self) -> None:
        """Setting up the QThread to query for monitors.

        Creating a worker object from a Worker class and setting the model.
        This is done as the worker will communicate with the model itself.
        Not particularly thread-safe, but considered OK as it is only
        performed during application start.

        Putting the same functionality in
        controller/model would make it a bit more complex.
        """
        self.worker = Worker()
        self.worker.set_model(self.model)
        self.query_thread = QThread()

        self.worker.moveToThread(self.query_thread)
        self.query_thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.query_thread.quit)
        self.worker.finished.connect(self.init_monitor_combobox)
        self.query_thread.start()

    def init_monitor_combobox(self) -> None:
        """Initialize the monitor combobox.

        Insert all monitors into the combobox. Also adds 'All' with index 0 as
        the first entry, and also the default. Sets the items from the model
        using the ID and Model.

        Sets the current index to 'All'.
        """
        self.ui.monitorComboBox.addItem("0: All")
        self.ui.monitorComboBox.addItems([
            f"{monitor.idx}: {monitor.model}"
            for monitor in self.model._monitors
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


class Worker(QObject):
    """Class handling threaded work for quering for monitors."""
    finished = Signal()

    def set_model(self, model: Model) -> None:
        """Create a link to the Model.

        This is used to be able to communicate with the model.

        Args:
            model (Model): The system Model.
        """
        self.model = model

    def run(self) -> None:
        """Executing the query for monitors."""
        self.model.query_monitors()
        self.finished.emit()
