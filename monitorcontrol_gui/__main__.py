import sys
from PySide6.QtWidgets import QApplication
from monitorcontrol_gui.controller import Controller
from monitorcontrol_gui.view import View
from monitorcontrol_gui.model import Model


class App(QApplication):
    def __init__(self, sys_argv: list) -> None:
        super().__init__(sys_argv)
        self.model = Model()
        self.ctrl = Controller(model=self.model)
        self.view = View(model=self.model, ctrl=self.ctrl)

    def run(self) -> None:
        self.view.show()
        sys.exit(self.exec())


def main():
    app = App([])
    app.run()


if __name__ == '__main__':
    main()
