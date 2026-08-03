"""
Global stylesheet for VYOM.
"""

from __future__ import annotations


DARK_THEME = """
QMainWindow {
    background-color: #121212;
    color: #E0E0E0;
}

QWidget {
    background-color: #121212;
    color: #E0E0E0;
    font-family: Segoe UI;
    font-size: 10pt;
}

QGroupBox {
    border: 1px solid #303030;
    border-radius: 8px;
    margin-top: 12px;
    padding-top: 10px;
    font-weight: bold;
}

QGroupBox::title {
    left: 12px;
    padding: 0 5px;
}

QLabel {
    color: #E0E0E0;
}

QLineEdit,
QComboBox,
QTextEdit {
    background: #1F1F1F;
    border: 1px solid #404040;
    border-radius: 6px;
    padding: 6px;
    color: white;
}

QLineEdit:focus,
QComboBox:focus,
QTextEdit:focus {
    border: 1px solid #00BFFF;
}

QPushButton {
    background: #007ACC;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 6px 14px;
    font-weight: bold;
}

QPushButton:hover {
    background: #0099FF;
}

QPushButton:pressed {
    background: #005C99;
}

QPushButton:checked {
    background: #0062A3;
    border: 2px solid #007ACC;
}

QPushButton:disabled {
    background: #404040;
    color: #888;
}

QTableWidget {
    background: #181818;
    alternate-background-color: #202020;
    gridline-color: transparent;
    border: 1px solid #303030;
    selection-background-color: #1a4a7a;
    selection-color: white;
}

QTableWidget::item {
    padding: 4px;
    border-bottom: 1px solid #2a2a2a;
}

QTableWidget::item:selected {
    background: #1a4a7a;
}

QHeaderView::section {
    background: #262626;
    color: #cccccc;
    padding: 6px 8px;
    border: none;
    border-right: 1px solid #333;
    border-bottom: 2px solid #007ACC;
    font-weight: bold;
    font-size: 9pt;
}

QScrollBar:vertical {
    width: 12px;
    background: #181818;
}

QScrollBar::handle:vertical {
    background: #505050;
    border-radius: 6px;
}

QScrollBar::handle:vertical:hover {
    background: #707070;
}

QStatusBar {
    background: #1A1A1A;
    border-top: 1px solid #303030;
}

QSplitter::handle {
    background: #303030;
}

QToolTip {
    background: #303030;
    color: white;
    border: 1px solid #505050;
}
"""