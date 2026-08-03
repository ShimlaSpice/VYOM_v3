"""
Left Sidebar for VYOM.
"""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QButtonGroup,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class LeftSidebar(QWidget):

    category_changed = Signal(str)

    def __init__(self):

        super().__init__()

        self._buttons = {}

        self._build_ui()

    def _build_ui(self):

        layout = QVBoxLayout()

        layout.setContentsMargins(

            6,

            6,

            6,

            6,

        )

        layout.setSpacing(

            6,

        )

        self.button_group = QButtonGroup(

            self,

        )

        self.button_group.setExclusive(

            True,

        )

        categories = [

            "Intraday",

            "Swing",

            "Positional",

            "Long Term",

            "Scalping",

        ]

        for category in categories:

            button = QPushButton(

                category,

            )

            button.setCheckable(

                True,

            )

            button.setFixedHeight(

                34,

            )

            button.clicked.connect(

                lambda checked, c=category:

                self.category_changed.emit(

                    c,

                )

            )

            self.button_group.addButton(

                button,

            )

            self._buttons[category] = button

            layout.addWidget(

                button,

            )

        self._buttons["Intraday"].setChecked(

            True,

        )

        layout.addStretch()

        self.setFixedWidth(

            125,

        )

        self.setLayout(

            layout,

        )

    def set_category(

        self,

        category: str,

    ):

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

        for category, button in self._buttons.items():

            if button.isChecked():

                return category

        return "Intraday"