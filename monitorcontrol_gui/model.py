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
        # TODO: Add update callbacks for the model.
        self._monitors: list[Monitor] = []

    def set_monitors(self, monitors: list[Monitor]) -> None:
        self._monitors = monitors
