from PySide6.QtWidgets import QApplication

import db
from ui.main_window import MainWindow


def main() -> None:
    db.init_db()
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()