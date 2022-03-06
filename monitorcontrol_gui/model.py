from dataclasses import dataclass
import monitorcontrol as mc


@dataclass
class Monitor:
    obj: mc.Monitor
    idx: int
    model: str
    luminance: int


class Model:
    def __init__(self) -> None:
        self._monitors: list[Monitor] = []

    def set_monitors(self, monitors: list[Monitor]) -> None:
        self._monitors = monitors

    def query_monitors(self) -> None:
        for idx, monitor_obj in enumerate(mc.get_monitors(), 1):
            with monitor_obj as monitor:
                capabilities = monitor.get_vcp_capabilities()
                luminance = monitor.get_luminance()

            self._monitors.append(
                Monitor(monitor_obj, idx, capabilities["model"], luminance)
            )
