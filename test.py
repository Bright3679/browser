import sys
import json
from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction, QLineEdit, QVBoxLayout, QWidget,
                             QTabWidget, QStatusBar, QPushButton, QToolBar)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon

class SimpleBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setWindowTitle("Simple Browser")
        self.setGeometry(100, 100, 1200, 800)

        # Set up tabs
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)
        self.add_new_tab(QUrl("https://www.google.com"))

        # Create a toolbar for address and search bars
        self.toolbar = QToolBar("Main Toolbar")
        self.addToolBar(self.toolbar)

        # Address bar
        self.address_bar = QLineEdit()
        self.address_bar.setPlaceholderText("Enter URL and press Enter")
        self.address_bar.returnPressed.connect(self.navigate_to_url)
        self.toolbar.addWidget(self.address_bar)

        # Search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search...")
        self.search_bar.returnPressed.connect(self.search)
        self.toolbar.addWidget(self.search_bar)

        # Search button
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search)
        self.toolbar.addWidget(self.search_button)

        # Create a status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Create a menu bar with navigation actions
        self.menu_bar = self.menuBar()
        self.navigation_menu = self.menu_bar.addMenu("Navigation")

        self.back_action = QAction(QIcon("icons/back.png"), "Back", self)
        self.back_action.triggered.connect(self.current_web_view().back)
        self.navigation_menu.addAction(self.back_action)

        self.forward_action = QAction(QIcon("icons/forward.png"), "Forward", self)
        self.forward_action.triggered.connect(self.current_web_view().forward)
        self.navigation_menu.addAction(self.forward_action)

        self.refresh_action = QAction(QIcon("icons/refresh.png"), "Refresh", self)
        self.refresh_action.triggered.connect(self.current_web_view().reload)
        self.navigation_menu.addAction(self.refresh_action)

        self.home_action = QAction(QIcon("icons/home.png"), "Home", self)
        self.home_action.triggered.connect(self.navigate_home)
        self.navigation_menu.addAction(self.home_action)

        # Create a menu bar with bookmarks actions
        self.bookmarks_menu = self.menu_bar.addMenu("Bookmarks")

        self.add_bookmark_action = QAction(QIcon("icons/bookmark.png"), "Add Bookmark", self)
        self.add_bookmark_action.triggered.connect(self.add_bookmark)
        self.bookmarks_menu.addAction(self.add_bookmark_action)

        self.view_bookmarks_action = QAction(QIcon("icons/view_bookmarks.png"), "View Bookmarks", self)
        self.view_bookmarks_action.triggered.connect(self.view_bookmarks)
        self.bookmarks_menu.addAction(self.view_bookmarks_action)

        # Create a menu bar with history actions
        self.history_menu = self.menu_bar.addMenu("History")

        self.view_history_action = QAction(QIcon("icons/view_history.png"), "View History", self)
        self.view_history_action.triggered.connect(self.view_history)
        self.history_menu.addAction(self.view_history_action)

        # Create a menu bar with tabs actions
        self.tabs_menu = self.menu_bar.addMenu("Tabs")

        self.new_tab_action = QAction(QIcon("icons/new_tab.png"), "New Tab", self)
        self.new_tab_action.triggered.connect(self.add_new_tab)
        self.tabs_menu.addAction(self.new_tab_action)

        self.close_tab_action = QAction(QIcon("icons/close_tab.png"), "Close Tab", self)
        self.close_tab_action.triggered.connect(self.close_current_tab)
        self.tabs_menu.addAction(self.close_tab_action)

        # Initialize bookmarks and history
        self.bookmarks = []
        self.history = []
        self.load_bookmarks()

    def add_new_tab(self, url=None, title="New Tab"):
        if url is None:
            url = QUrl("http://www.example.com")
        web_view = QWebEngineView()
        web_view.setUrl(url)
        self.tab_widget.addTab(web_view, title)
        self.tab_widget.setCurrentWidget(web_view)
        web_view.loadStarted.connect(self.on_load_started)
        web_view.loadFinished.connect(self.on_load_finished)
        self.update_tab_title()

    def close_current_tab(self):
        index = self.tab_widget.currentIndex()
        self.tab_widget.removeTab(index)

    def current_web_view(self):
        return self.tab_widget.currentWidget()

    def navigate_to_url(self):
        url_text = self.address_bar.text().strip()
        if url_text:
            url = QUrl(url_text)
            if url.scheme() == "":
                url.setScheme("http")
            self.load_url(url)
        else:
            self.status_bar.showMessage("Address bar is empty.")

    def navigate_home(self):
        self.load_url(QUrl("http://www.example.com"))

    def load_url(self, url):
        self.current_web_view().setUrl(url)
        self.address_bar.setText(url.toString())
        self.update_tab_title()

    def search(self):
        query = self.search_bar.text().strip()
        if query:
            url = QUrl(f"https://www.google.com/search?q={query}")
            self.load_url(url)
        else:
            self.status_bar.showMessage("Search query is empty.")

    def add_bookmark(self):
        url = self.current_web_view().url().toString()
        if url not in self.bookmarks:
            self.bookmarks.append(url)
            self.save_bookmarks()
            print(f"Added bookmark: {url}")

    def save_bookmarks(self):
        with open("bookmarks.json", "w") as file:
            json.dump(self.bookmarks, file)

    def load_bookmarks(self):
        try:
            with open("bookmarks.json", "r") as file:
                self.bookmarks = json.load(file)
        except FileNotFoundError:
            self.bookmarks = []

    def view_bookmarks(self):
        print("Bookmarks:")
        for bookmark in self.bookmarks:
            print(bookmark)

    def view_history(self):
        print("History:")
        for entry in self.history:
            print(entry)

    def on_load_started(self):
        self.status_bar.showMessage("Loading...")

    def on_load_finished(self, success):
        if success:
            self.status_bar.showMessage("Load finished")
        else:
            self.status_bar.showMessage("Load failed")
        self.history.append(self.current_web_view().url().toString())

    def update_tab_title(self):
        current_index = self.tab_widget.currentIndex()
        title = self.current_web_view().url().toString()
        self.tab_widget.setTabText(current_index, title)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = SimpleBrowser()
    browser.show()
    sys.exit(app.exec_())
