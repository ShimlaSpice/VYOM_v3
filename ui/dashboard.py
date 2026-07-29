"""
Dashboard widget for VYOM.

Main dashboard responsible for displaying:

- Recommendation Table
- Stock Details
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from ui.recommendation_table import RecommendationTable
from ui.stock_details import StockDetails


class Dashboard(QWidget):
    """
    Main dashboard widget.
    """

    def __init__(self) -> None:

        super().__init__()

        self._build_ui()

    def _build_ui(self) -> None:

        self.recommendation_table = RecommendationTable()

        self.details = StockDetails()

        self.splitter = QSplitter(
            Qt.Horizontal,
        )

        self.splitter.addWidget(
            self.recommendation_table,
        )

        self.splitter.addWidget(
            self.details,
        )

        self.splitter.setStretchFactor(
            0,
            3,
        )

        self.splitter.setStretchFactor(
            1,
            2,
        )

        layout = QVBoxLayout()

        layout.setContentsMargins(
            5,
            5,
            5,
            5,
        )

        layout.addWidget(
            self.splitter,
        )

        self.setLayout(
            layout,
        )

        self.recommendation_table.stock_selected.connect(
            self.details.update_details,
        )