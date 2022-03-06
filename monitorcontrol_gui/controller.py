from monitorcontrol_gui.model import Model


class Controller:
    def __init__(self, model: Model) -> None:
        self.model = model

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
