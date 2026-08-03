"""
Dashboard widget for VYOM.
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from ui.recommendation_table import RecommendationTable
from ui.stock_details import StockDetails


class Dashboard(QWidget):

    def __init__(self):

        super().__init__()

        self._build_ui()

    def _build_ui(self):

        self.recommendation_table = RecommendationTable()

        self.details = StockDetails()

        # Footer label under table
        self.table_footer = QLabel("Showing 0 results")
        self.table_footer.setStyleSheet("color: #888; font-size: 9pt; padding: 4px 8px;")

        # Left panel: table + footer
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)
        left_layout.addWidget(self.recommendation_table, 1)
        left_layout.addWidget(self.table_footer)

        # Right panel with just details (emotion removed)
        right_panel = QWidget()

        right_layout = QVBoxLayout()

        right_layout.setContentsMargins(0, 0, 0, 0)

        right_layout.setSpacing(6)

        right_layout.addWidget(self.details, 1)

        right_panel.setLayout(right_layout)

        # Splitter with table on left (~65%) and details on right (~35%)
        self.splitter = QSplitter(Qt.Horizontal)

        self.splitter.setChildrenCollapsible(False)

        self.splitter.addWidget(left_widget)

        self.splitter.addWidget(right_panel)

        self.splitter.setStretchFactor(0, 65)

        self.splitter.setStretchFactor(1, 35)

        layout = QVBoxLayout()

        layout.setContentsMargins(2, 2, 2, 2)

        layout.setSpacing(2)

        layout.addWidget(self.splitter)

        self.setLayout(layout)

        self.recommendation_table.stock_selected.connect(

            self.details.update_details,

        )

        # Update footer when table data loads
        self.recommendation_table.model().rowsInserted.connect(self._update_footer)
        self.recommendation_table.model().rowsRemoved.connect(self._update_footer)

    def _update_footer(self, *args):
        n = self.recommendation_table.rowCount()
        if n > 0:
            self.table_footer.setText(f"Showing 1 to {n} of {n} results")
        else:
            self.table_footer.setText("No results")

    def update_emotion(self, emotion: dict):
        # Emotion removed from UI - kept method for backward compatibility
        pass