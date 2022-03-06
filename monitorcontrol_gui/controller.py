from monitorcontrol_gui.model import Model


class Controller:
    def __init__(self, model: Model) -> None:
        self.model = model
        self.model.get_monitors()

    def set_luminosity(self, value: int) -> None:
        for monitor in self.model.monitors:
            with monitor:
                monitor.set_luminance(value)
