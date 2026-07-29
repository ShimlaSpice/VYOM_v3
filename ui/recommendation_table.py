"""
Recommendation Table for VYOM.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QAbstractItemView,
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
)


class RecommendationTable(QTableWidget):
    """
    Displays Top Recommendations.
    """

    stock_selected = Signal(dict)

    HEADERS = [

        "Rank",

        "Symbol",

        "Market",

        "Price",

        "Score",

        "Confidence",

        "Action",

        "Entry",

        "Target",

        "SL",

    ]

    def __init__(self) -> None:

        super().__init__()

        self._build_ui()

        self.recommendations = []

    def _build_ui(self) -> None:

        self.setColumnCount(

            len(self.HEADERS),

        )

        self.setHorizontalHeaderLabels(

            self.HEADERS,

        )

        self.verticalHeader().setVisible(

            False,

        )

        self.setSelectionBehavior(

            QAbstractItemView.SelectRows,

        )

        self.setSelectionMode(

            QAbstractItemView.SingleSelection,

        )

        self.setEditTriggers(

            QAbstractItemView.NoEditTriggers,

        )

        self.setAlternatingRowColors(

            True,

        )

        self.setSortingEnabled(

            True,

        )

        self.horizontalHeader().setSectionResizeMode(

            QHeaderView.Stretch,

        )

        self.itemSelectionChanged.connect(

            self._emit_selected,

        )

    def load_data(

        self,

        recommendations,
            filters: dict | None = None,

    ) -> None:

        self.setSortingEnabled(False)

        self.recommendations = recommendations

        self.setRowCount(len(recommendations))

        for row, stock in enumerate(recommendations):

            values = [

                row + 1,

                stock.symbol,

                "NSE",

                f"₹{stock.close:.2f}",

                stock.scores.get(
                    "technical",
                    0,
                ),

                stock.confidence,

                stock.recommendation,

                f"₹{stock.entry:.2f}",

                f"₹{stock.target1:.2f}",

                f"₹{stock.stop_loss:.2f}",

            ]

            for column, value in enumerate(values):

                item = QTableWidgetItem(str(value))

                item.setTextAlignment(Qt.AlignCenter)

                self.setItem(

                    row,

                    column,

                    item,

                )

        self.setSortingEnabled(True)

    def clear_table(

        self,

    ) -> None:

        self.setRowCount(

            0,

        )

    def _emit_selected(

        self,

    ) -> None:

        row = self.currentRow()

        if row < 0:

            return

        stock = self.recommendations[row]

        self.stock_selected.emit(
            stock.__dict__
        )
