from monitorcontrol_gui.model import Model
import monitorcontrol as mc


class Controller:
    def __init__(self, model: Model) -> None:
        self.model = model

    def set_luminosity(self, value: int) -> None:
        for monitor_obj in mc.get_monitors():
            with monitor_obj:
                monitor_obj.set_luminance(value)
