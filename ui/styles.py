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
    border: 1px solid #2c2c2c;
    border-radius: 6px;
    margin-top: 10px;
    padding-top: 8px;
    font-weight: bold;
    color: #b0bec5;
}

QGroupBox::title {
    left: 10px;
    padding: 0 4px;
    color: #90caf9;
}

QLabel {
    color: #E0E0E0;
    background: transparent;
}

QLineEdit,
QComboBox {
    background: #1e1e1e;
    border: 1px solid #3a3a3a;
    border-radius: 4px;
    padding: 4px 8px;
    color: #e0e0e0;
    min-height: 24px;
}

QLineEdit:focus,
QComboBox:focus {
    border: 1px solid #42a5f5;
}

QComboBox::drop-down {
    border: none;
    width: 20px;
}

QComboBox QAbstractItemView {
    background: #1e1e1e;
    selection-background-color: #1a4a7a;
    color: #e0e0e0;
    border: 1px solid #444;
}

QPushButton {
    background: #263238;
    color: #90caf9;
    border: 1px solid #37474f;
    border-radius: 5px;
    padding: 5px 14px;
    font-weight: bold;
}

QPushButton:hover {
    background: #2e3f4f;
    border-color: #42a5f5;
    color: #fff;
}

QPushButton:pressed {
    background: #1a3a5c;
}

QPushButton:checked {
    background: #1565c0;
    border: 1px solid #42a5f5;
    color: #ffffff;
}

QPushButton:disabled {
    background: #1e1e1e;
    color: #555;
    border-color: #333;
}

QPushButton#scanButton {
    background: #1565c0;
    color: #ffffff;
    border: 1px solid #42a5f5;
    font-size: 11pt;
    padding: 6px 20px;
}

QPushButton#scanButton:hover {
    background: #1976d2;
}

QPushButton#scanButton:pressed {
    background: #0d47a1;
}

QPushButton#scanButton:disabled {
    background: #263238;
    color: #607d8b;
}

QTableWidget {
    background: #181818;
    alternate-background-color: #1e1e1e;
    gridline-color: transparent;
    border: 1px solid #2c2c2c;
    selection-background-color: #1565c0;
    selection-color: #ffffff;
    font-size: 10pt;
}

QTableWidget::item {
    padding: 5px 6px;
    border-bottom: 1px solid #252525;
}

QTableWidget::item:selected {
    background-color: #1565c0;
    color: #ffffff;
}

QHeaderView::section {
    background: #1e2a35;
    color: #90caf9;
    padding: 6px 8px;
    border: none;
    border-right: 1px solid #2c2c2c;
    border-bottom: 2px solid #1565c0;
    font-weight: bold;
    font-size: 9pt;
}

QScrollBar:vertical {
    width: 10px;
    background: #1a1a1a;
}

QScrollBar::handle:vertical {
    background: #3a3a3a;
    border-radius: 5px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background: #505050;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    height: 10px;
    background: #1a1a1a;
}

QScrollBar::handle:horizontal {
    background: #3a3a3a;
    border-radius: 5px;
}

QStatusBar {
    background: #141414;
    border-top: 1px solid #2c2c2c;
    color: #9e9e9e;
    font-size: 9pt;
}

QSplitter::handle:vertical {
    background: #1e2a35;
    height: 6px;
    border-top: 1px solid #2c2c2c;
    border-bottom: 1px solid #2c2c2c;
}

QSplitter::handle:horizontal {
    background: #1e2a35;
    width: 6px;
    border-left: 1px solid #2c2c2c;
    border-right: 1px solid #2c2c2c;
}

QScrollArea {
    border: none;
    background: transparent;
}

QCheckBox {
    color: #b0bec5;
    spacing: 5px;
}

QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border-radius: 3px;
    border: 1px solid #555;
    background: #1e1e1e;
}

QCheckBox::indicator:checked {
    background: #1565c0;
    border-color: #42a5f5;
}

QToolTip {
    background: #263238;
    color: #e0e0e0;
    border: 1px solid #455a64;
    padding: 4px 8px;
    border-radius: 4px;
}

QProgressBar {
    background: #1e1e1e;
    border: none;
    border-radius: 3px;
}

QProgressBar::chunk {
    background: #1565c0;
    border-radius: 3px;
}
"""
