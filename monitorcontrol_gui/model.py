import monitorcontrol as mc
from dataclasses import dataclass


@dataclass
class Monitor:
    obj: mc.Monitor
    idx: int
    model: str
    luminance: int


class Model:
    def __init__(self) -> None:
        self.monitors: list[Monitor] = []

    def query_monitors(self) -> None:
        for idx, monitor_obj in enumerate(mc.get_monitors(), 1):
            with monitor_obj as monitor:
                capabilities = monitor.get_vcp_capabilities()
                luminance = monitor.get_luminance()

            self.monitors.append(
                Monitor(monitor_obj, idx, capabilities["model"], luminance)
            )


class Worker:
    pass
