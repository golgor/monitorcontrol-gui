import monitorcontrol as mc


class Model:
    def __init__(self) -> None:
        self.monitors: list[mc.Monitor] = []

    def get_monitors(self) -> None:
        self.monitors = mc.get_monitors()
