"""ENEX to Folder 변환기 진입점."""
import tkinter as tk

from enex_to_folder.gui.main_window import MainWindow

__version__ = "1.0.0"
APP_TITLE = "ENEX to Folder v1.0.0"


def main() -> None:
    root = tk.Tk()
    MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
