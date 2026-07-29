"""
Left Sidebar for VYOM.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QButtonGroup,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class LeftSidebar(QWidget):
    """
    Left navigation panel.
    """

    category_changed = Signal(str)

    def __init__(self) -> None:

        super().__init__()

        self._buttons: dict[str, QPushButton] = {}

        self._build_ui()

    def _build_ui(self) -> None:

        layout = QVBoxLayout()

        layout.setContentsMargins(
            10,
            10,
            10,
            10,
        )

        layout.setSpacing(
            8,
        )

        self.button_group = QButtonGroup(
            self,
        )

        self.button_group.setExclusive(
            True,
        )

        categories = [

            "Today",

            "Intraday",

            "Swing",

            "Long Term",

            "F&O",

            "Penny",

        ]

        for name in categories:

            button = QPushButton(
                name,
            )

            button.setCheckable(
                True,
            )

            button.setMinimumHeight(
                42,
            )

            button.clicked.connect(

                lambda checked, n=name: self.category_changed.emit(
                    n,
                )

            )

            self.button_group.addButton(
                button,
            )

            self._buttons[name] = button

            layout.addWidget(
                button,
            )

        self._buttons["Today"].setChecked(
            True,
        )

        layout.addStretch()

        self.setFixedWidth(
            170,
        )

        self.setLayout(
            layout,
        )

    def set_category(

        self,

        category: str,

    ) -> None:

        button = self._buttons.get(
            category,
        )

        if button:

            button.setChecked(
                True,
            )

    def current_category(

        self,

    ) -> str:

        for name, button in self._buttons.items():

            if button.isChecked():

                return name

        return "Today"