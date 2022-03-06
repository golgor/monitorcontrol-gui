from PySide6.QtCore import QObject, QThread, Signal
from PySide6.QtCore import QBasicMutex
import monitorcontrol as mc
from monitorcontrol_gui.model import Model, Monitor


class Controller:
    def __init__(self, model: Model) -> None:
        self.model = model
        self.dcc_interface = DccInterface()

    def set_luminosity(self, value: int, idx: int = 0) -> None:
        """Set the luminosity of the monitor with the given index.

        If the index is not specified or 0, the luminosity of all detected
        monitors will be set. The combobox have '0: All' appended, but the
        monitor list does not, thus subtracting with 1.

        Args:
            value (int): The luminance value as %.
            idx (int, optional): Id of a monitor. Defaults to None.
        """
        print(f"{idx=}: {value=}")
        if idx:
            monitor = self.model._monitors[idx - 1]
            with monitor.obj as mon:
                mon.set_luminance(value)
            return

        for monitor in self.model._monitors:
            with monitor.obj as mon:
                mon.set_luminance(value)
        return

    def query_monitors(self, callback=None) -> None:
        self.ddc_thread = QThread()

        self.dcc_interface.moveToThread(self.ddc_thread)
        self.ddc_thread.started.connect(self.dcc_interface.query_monitors)
        self.dcc_interface.q_monitors_finished.connect(self.ddc_thread.quit)
        self.dcc_interface.q_monitors_finished.connect(self.model.set_monitors)
        # TODO: Remove this when Update Callbacks are implemented in the model.
        if callback:
            self.dcc_interface.q_monitors_finished.connect(callback)
        self.ddc_thread.start()


class DccInterface(QObject):
    """Class handling threaded work for quering for monitors."""
    q_monitors_finished = Signal(list)

    def __init__(self):
        super().__init__()
        self.lock = QBasicMutex()

    def query_monitors(self) -> None:
        """Executing the query for monitors."""
        self.lock.lock()
        monitors = []
        for idx, monitor_obj in enumerate(mc.get_monitors(), 1):
            with monitor_obj as monitor:
                capabilities = monitor.get_vcp_capabilities()
                luminance = monitor.get_luminance()

            monitors.append(
                Monitor(monitor_obj, idx, capabilities["model"], luminance)
            )
        self.lock.unlock()
        self.q_monitors_finished.emit(monitors)
