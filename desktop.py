import sys
import os

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QToolBar, QAction, QFileDialog, QMessageBox
)
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineDownloadItem, QWebEngineProfile, QWebEnginePage

class ArkIDEBrowser(QMainWindow):
    """
    An enhanced web browser application designed to display the ArkIDE editor.
    This version loads the editor from local files, enabling offline use.
    It includes back/forward navigation, file download capability, and persistent
    user data for the loaded website.
    """
    def __init__(self):
        """
        Initializes the ArkIDEBrowser window with navigation controls,
        web view, and download handling, configured for offline content.
        """
        super().__init__()
        self.setWindowTitle("ArkIDE Desktop")
        self.setGeometry(100, 100, 1200, 800)

        # --- Setup Web Engine Profile for Persistent Data ---
        self.web_profile = QWebEngineProfile.defaultProfile()

        # --- Create QWebEngineView instance ---
        self.browser = QWebEngineView()
        page = QWebEnginePage(self.web_profile, self.browser)
        self.browser.setPage(page)

        # --- Set the URL to load from local files ---
        # Determine the base path of the bundled application or script
        if getattr(sys, 'frozen', False):
            # Running in a PyInstaller bundle
            base_path = sys._MEIPASS
            print(f"Running in frozen mode. sys._MEIPASS: {base_path}")
        else:
            # Running as a regular Python script
            base_path = os.path.dirname(os.path.abspath(__file__))
            print(f"Running as script. Script directory: {base_path}")

        # Construct the path to the local editor.html file
        local_html_path = os.path.join(base_path, "ArkIDE", "editor.html")
        print(f"Attempting to load local HTML from: {local_html_path}")

        # Add a check to see if the file actually exists at this path
        if not os.path.exists(local_html_path):
            print(f"ERROR: Local HTML file NOT FOUND at: {local_html_path}")
            # You could show a message box here to the user in a real app
            QMessageBox.critical(self, "File Not Found",
                                 f"The ArkIDE editor file was not found at:\n{local_html_path}\n"
                                 "Please ensure the 'ArkIDE' folder is correctly bundled with the application.")
            # Optionally, set a fallback URL or exit
            # self.browser.setUrl(QUrl("about:blank"))
        else:
            print(f"Local HTML file found at: {local_html_path}")

        self.browser.setUrl(QUrl.fromLocalFile(local_html_path))

        # --- Connect downloadRequested signal ---
        self.web_profile.downloadRequested.connect(self.handle_download_requested)

        # --- Setup Navigation Toolbar ---
        self.navigation_toolbar = QToolBar("Navigation")
        self.addToolBar(self.navigation_toolbar)

        # Back Button
        back_button = QAction(QIcon.fromTheme("go-previous", QIcon(":/qt-project.org/styles/commonstyle/images/left-32.png")), "Back", self)
        back_button.setStatusTip("Go back to the previous page")
        back_button.triggered.connect(self.browser.back)
        self.navigation_toolbar.addAction(back_button)

        # Forward Button
        forward_button = QAction(QIcon.fromTheme("go-next", QIcon(":/qt-project.org/styles/commonstyle/images/right-32.png")), "Forward", self)
        forward_button.setStatusTip("Go forward to the next page")
        forward_button.triggered.connect(self.browser.forward)
        self.navigation_toolbar.addAction(forward_button)

        # Reload Button
        reload_button = QAction(QIcon.fromTheme("view-refresh", QIcon(":/qt-project.org/styles/commonstyle/images/refresh-32.png")), "Reload", self)
        reload_button.setStatusTip("Reload current page")
        reload_button.triggered.connect(self.browser.reload)
        self.navigation_toolbar.addAction(reload_button)

        # --- Layout Setup ---
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.browser)

    def handle_download_requested(self, download_item: QWebEngineDownloadItem):
        """
        Handles file download requests from the web engine.
        Prompts the user for a save location and starts the download.
        """
        if download_item.state() == QWebEngineDownloadItem.DownloadRequested:
            suggested_filename = os.path.basename(download_item.path())
            if not suggested_filename:
                suggested_filename = "downloaded_file"

            file_path, _ = QFileDialog.getSaveFileName(
                self, "Save File", suggested_filename, "All Files (*)"
            )

            if file_path:
                download_item.setPath(file_path)
                download_item.accept()
                QMessageBox.information(self, "Download Started", f"Download of '{os.path.basename(file_path)}' started.")
            else:
                download_item.cancel()
                QMessageBox.warning(self, "Download Cancelled", "File download was cancelled by the user.")
        elif download_item.state() == QWebEngineDownloadItem.DownloadInterrupted:
            QMessageBox.critical(self, "Download Failed", f"Download of '{os.path.basename(download_item.path())}' failed: {download_item.interruptReasonString()}")
        elif download_item.state() == QWebEngineDownloadItem.DownloadFinished:
            QMessageBox.information(self, "Download Complete", f"Download of '{os.path.basename(download_item.path())}' finished successfully.")


def main():
    """
    Main function to run the ArkIDE Browser application.
    """
    app = QApplication(sys.argv)
    window = ArkIDEBrowser()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
