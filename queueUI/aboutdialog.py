"""
About dialog window

.. autosummary::

    ~AboutDialog
"""

from PyQt5 import QtCore, QtGui, QtWidgets

from . import (
    APP_DESC,
    APP_TITLE,
    AUTHOR_LIST,
    COPYRIGHT_TEXT,
    DOCS_URL,
    ISSUES_URL,
    __version__,
    utils,
)


class AboutDialog(QtWidgets.QDialog):
    """
    Load a generic About... Dialog as a .ui file.

    """

    # UI file name matches this module, different extension
    ui_file = utils.getUiFileName(__file__)

    def __init__(self, parent):
        self.parent = parent
        self.license_box = None
        self.settings = None

        super().__init__(parent)
        utils.myLoadUi(self.ui_file, baseinstance=self)
        self.setup()

    def setup(self):
        """_summary_"""
        import os

        pid = os.getpid()

        self.setWindowTitle(f"About ... {APP_TITLE}")
        self.title.setText(APP_TITLE)
        self.version.setText(f"version {__version__}")
        self.description.setText(APP_DESC)
        self.authors.setText(", ".join(AUTHOR_LIST))
        self.copyright.setText(COPYRIGHT_TEXT)

        self.setStatus(f"About {APP_TITLE}, {pid=}")

        # handle the push buttons
        self.docs_pb.setToolTip(DOCS_URL)
        self.issues_pb.setToolTip(ISSUES_URL)
        self.docs_pb.clicked.connect(self.doDocsUrl)
        self.issues_pb.clicked.connect(self.doIssuesUrl)
        self.license_pb.clicked.connect(self.doLicense)

        self.setModal(False)

    def closeEvent(self, event):
        """
        called when user clicks the big [X] to quit
        """
        if self.license_box is not None:
            self.license_box.close()
        event.accept()  # let the window close

    def doUrl(self, url):
        """opening URL in default browser"""
        url = QtCore.QUrl(url)
        service = QtGui.QDesktopServices()
        service.openUrl(url)

    def doDocsUrl(self):
        """opening documentation URL in default browser"""
        self.setStatus("opening documentation URL in default browser")
        self.doUrl(DOCS_URL)

    def doIssuesUrl(self):
        """opening issues URL in default browser"""
        self.setStatus("opening issues URL in default browser")
        self.doUrl(ISSUES_URL)

    def doLicense(self):
        """show the license"""
        from .licensedialog import LicenseDialog

        self.setStatus("opening License in new window")

        license = LicenseDialog(self)
        license.finished.connect(self.clearStatus)
        license.open()  # modal: must close licensedialog BEFORE aboutdialog

    def clearStatus(self):
        """_summary_"""
        self.setStatus("")

    def setStatus(self, text):
        """_summary_

        Args:
            text (_type_): _description_
        """
        self.parent.setStatus(text)
