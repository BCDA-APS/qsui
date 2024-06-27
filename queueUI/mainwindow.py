"""
Defines MainWindow class.

.. autosummary::

    ~MainWindow
"""

from bluesky_queueserver_api.zmq import REManagerAPI
from PyQt5 import QtWidgets

from . import APP_TITLE, utils
from .user_settings import settings

UI_FILE = utils.getUiFileName(__file__)

# Connect to the QServer
# def queueserver_api():
#     try:
#         #Where is the TOML file located?
#         config = load_config()["queueserver"]
#     except KeyError:
#         raise InvalidConfiguration("Could not load queueserver info from iconfig.toml file.")
#     ctrl_addr = f"tcp://{config['control_host']}:{config['control_port']}"
#     info_addr = f"tcp://{config['info_host']}:{config['info_port']}"
#     api = REManagerAPI(zmq_control_addr=ctrl_addr, zmq_info_addr=info_addr)
#     return api


class MainWindow(QtWidgets.QMainWindow):
    """
    The main window of the app, built in Qt designer.

    """

    def __init__(self):
        super().__init__()
        utils.myLoadUi(UI_FILE, baseinstance=self)
        self.setWindowTitle(APP_TITLE)

        # self.actionOpen.triggered.connect(self.doOpen)
        self.actionAbout.triggered.connect(self.doAboutDialog)
        self.actionExit.triggered.connect(self.doClose)

        settings.restoreWindowGeometry(self, "mainwindow_geometry")
        print("Settings are saved in:", settings.fileName())

        self.RM = REManagerAPI()
        self.REOpenButton.clicked.connect(self.openRunEngine)
        self.RECloseButton.clicked.connect(self.closeRunEngine)

    # RE Function:
    def openRunEngine(self):
        """Checks the status of the RE. Then opens the RE."""
        if not self.RM.status().get("worker_environment_exists"):
            # BUG: Status bar in app window does not print the statement below
            self.setStatus("RE Environment is opening.", timeout=0)
            self.RM.environment_open()
            self.RM.wait_for_idle()
            self.REEnvironmentStatusLabel.setText("Open")
            self.REOpenButton.setEnabled(False)
            self.RECloseButton.setEnabled(True)
            self.setStatus("RE Environment is now open.", timeout=0)

            # print(f"status = {self.RM.status().get('worker_environment_exists')}")
        else:
            pass

    def closeRunEngine(self):
        """Checks the status of the RE. Then closes the RunEngine."""
        if self.RM.status().get("worker_environment_exists"):
            self.setStatus("RE Environment is closing.", timeout=0)
            self.RM.environment_close()
            self.RM.wait_for_idle()
            self.REEnvironmentStatusLabel.setText("Closed")
            self.RECloseButton.setEnabled(False)
            self.REOpenButton.setEnabled(True)
            self.setStatus("RE Environment is now closed.", timeout=0)

            # print(f"status = {self.RM.status().get('worker_environment_exists')}")
        else:
            pass

    def destroyRunEngine(self):
        """Destroys the RunEngine."""
        # TODO: Remove this function.
        self.RM.environment_destroy()

    @property
    def status(self):
        """Returns the current message in the mainwindow status bar.

        Returns:
            str: the current message in the mainwindow status bar.
        """
        return self.statusbar.currentMessage()

    def setStatus(self, text, timeout=0):
        """Write new status to the main window and terminal output."""
        print(text)
        self.statusbar.showMessage(str(text), msecs=timeout)

    def doAboutDialog(self, *args, **kw):
        """
        Show the "About ..." dialog
        """
        from .aboutdialog import AboutDialog

        about = AboutDialog(self)
        about.open()

    def closeEvent(self, event):
        """
        User clicked the big [X] to quit.
        """
        self.doClose()
        event.accept()  # let the window close

    def doClose(self, *args, **kw):
        """
        User chose exit (or quit), or closeEvent() was called.
        """
        self.setStatus("Application quitting ...")
        settings.saveWindowGeometry(self, "mainwindow_geometry")
        self.close()

    # def doOpen(self, *args, **kw):
    #     """
    #     User chose to open (connect with) a queue server.
    #     """
    #     from .opendialog import OpenDialog

    #     self.setStatus("Please select a server...")
    #     open_dialog = OpenDialog(self)

    # def doPopUp(self, message):
    #     """
    #     User chose to open (connect with) a tiled server.
    #     """
    #     from .popup import PopUp

    #     popup = PopUp(self, message)
    #     return popup.exec_() == QtWidgets.QDialog.Accepted

    # def proceed(self):
    #     """Handle the logic when the user clicks 'OK'."""
    #     return True

    # def cancel(self):
    #     """Handle the logic when the user clicks 'Cancel'."""
    #     return False
