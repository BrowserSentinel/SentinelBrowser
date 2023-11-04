import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QPropertyAnimation, QUrl, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QShortcut, QLineEdit, QVBoxLayout, QWidget, QTabWidget, QMessageBox, QDialog, QGridLayout, QLabel
from PyQt5.QtWebEngineWidgets import QWebEngineView
import webbrowser
import os
import keyboard
import subprocess

class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sentinel Browser")
        self.resize(1200, 800)
        
        icon = QIcon("home/assets/icon.ico")
        self.setWindowIcon(icon)  

        self.app = QApplication(sys.argv)
        self.app.setStyle("Cleanlooks")

        self.keyPressEvent = self.keyPressEvent
        # Fade in 
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(500)
        self.animation.setStartValue(0)  
        self.animation.setEndValue(1)
        self.animation.start()

        self.central_widget = QWidget(self)
        self.layout = QVBoxLayout(self.central_widget)

        self.search_bar = QLineEdit(self)
        self.search_bar.returnPressed.connect(self.load_url)
        self.search_bar.setPlaceholderText("Search...") 
        self.layout.addWidget(self.search_bar)

        self.search_bar.setStyleSheet("""
        padding: 6px; 
        border: 2px solid black;
        border-radius: 15px;
        """)

        self.tab_widget = QTabWidget(self)
        self.layout.addWidget(self.tab_widget)

        self.tab_widget.setStyleSheet("QTabBar::tab { height: 30px; color: white; }"
                                      "QTabBar::tab:selected { background: black; }"
                                      "QTabBar::tab:!selected { color: black; }"
                                      "QTabBar::tab:!selected { background: white; }")

        self.setCentralWidget(self.central_widget)

        new_tab_shortcut = QShortcut(Qt.CTRL + Qt.Key_N, self)
        new_tab_shortcut.activated.connect(self.open_new_tab)

        close_tab_shortcut = QShortcut(Qt.CTRL + Qt.Key_M, self)
        close_tab_shortcut.activated.connect(self.close_current_tab)

        self.open_new_tab()




    def open_new_tab(self):
        web_view = QWebEngineView(self)
        script_dir = os.path.dirname(os.path.realpath(__file__))
        folder_name = "home"  # Name of the folder where your HTML file is located
        local_file_url = QUrl.fromLocalFile(os.path.join(script_dir, folder_name, "home.html"))
        web_view.load(local_file_url)
        self.tab_widget.addTab(web_view, "New Tab")



    def close_current_tab(self):
        current_index = self.tab_widget.currentIndex()
        if current_index != -1:
            self.tab_widget.removeTab(current_index)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F1:
            self.close_all_tabs()
            self.open_new_tab()
            

    def close_all_tabs(self):

        for i in range(self.tab_widget.count()):
            self.tab_widget.removeTab(0)

    def load_url(self):
        current_web_view = self.tab_widget.currentWidget()
        url = self.search_bar.text()
        if url.startswith("?"):
          
            # Search query
            url = "https://duckduckgo.com/?q=" + url[1:]
        
        else:
          
            if not url.startswith("http"):
                url = "https://" + url

        current_web_view.load(QUrl(url))
    
help_process = None 

def open_or_terminate_help():
  global help_process
  
  if help_process is None or help_process.poll() is not None:

    # Specify full path to help.py
    components_dir = os.path.join(os.getcwd(), 'components')
    help_path = os.path.join(components_dir, 'help.py')

    help_process = subprocess.Popen(["python", help_path])
  
  else:
    help_process.terminate()

keyboard.add_hotkey("ctrl+h", open_or_terminate_help) 

COMPONENTS_DIR = 'Components'

PW_SCRIPT = os.path.join(COMPONENTS_DIR, 'pw.py')
ENC_SCRIPT = os.path.join(COMPONENTS_DIR, 'enc.py')  
ADBLOCKER_SCRIPT = os.path.join(COMPONENTS_DIR, 'adblocker.py')

def start_script(script_path):
    # Open a new command prompt window and run the script
    subprocess.Popen(["start", "cmd", "/k", "python", script_path], shell=True)

def toggle_pw():
    start_script(PW_SCRIPT)

keyboard.add_hotkey("ctrl+p", toggle_pw)

def toggle_enc():
    start_script(ENC_SCRIPT)  

keyboard.add_hotkey("ctrl+e", toggle_enc)

def toggle_adblocker():
    start_script(ADBLOCKER_SCRIPT)

keyboard.add_hotkey("ctrl+b", toggle_adblocker)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = BrowserWindow()
    browser.show()
    sys.exit(app.exec_())
    