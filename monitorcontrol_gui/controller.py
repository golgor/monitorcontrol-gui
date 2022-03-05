from monitorcontrol_gui.model import Model


class Controller:
    def __init__(self, model: Model) -> None:
        self.model = model
