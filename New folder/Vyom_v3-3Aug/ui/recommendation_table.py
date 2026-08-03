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

    def __init__(self):

        super().__init__()

        self.recommendations = []

        self._build_ui()

    def _build_ui(self):

        self.setColumnCount(

            len(self.HEADERS)

        )

        self.setHorizontalHeaderLabels(

            self.HEADERS

        )

        self.verticalHeader().setVisible(

            False

        )

        self.verticalHeader().setDefaultSectionSize(

            28

        )

        self.setSelectionBehavior(

            QAbstractItemView.SelectRows

        )

        self.setSelectionMode(

            QAbstractItemView.SingleSelection

        )

        self.setEditTriggers(

            QAbstractItemView.NoEditTriggers

        )

        self.setAlternatingRowColors(

            True

        )

        self.setSortingEnabled(

            True

        )

        self.setShowGrid(

            False

        )

        self.setWordWrap(

            False

        )

        self.horizontalHeader().setStretchLastSection(

            True

        )

        self.horizontalHeader().setSectionResizeMode(

            QHeaderView.Interactive

        )

        self.setColumnWidth(

            0,

            55,

        )

        self.setColumnWidth(

            1,

            135,

        )

        self.setColumnWidth(

            2,

            70,

        )

        self.setColumnWidth(

            3,

            90,

        )

        self.setColumnWidth(

            4,

            75,

        )

        self.setColumnWidth(

            5,

            90,

        )

        self.setColumnWidth(

            6,

            120,

        )

        self.setColumnWidth(

            7,

            95,

        )

        self.setColumnWidth(

            8,

            95,

        )

        self.setColumnWidth(

            9,

            95,

        )

        self.itemSelectionChanged.connect(

            self._emit_selected

        )

    def load_data(

        self,

        recommendations,

        filters: dict | None = None,

    ):

        self.setSortingEnabled(False)

        self.clearContents()

        self.recommendations = recommendations

        self.setRowCount(len(recommendations))

        for row, stock in enumerate(recommendations):

            symbol = getattr(stock, "symbol", "")

            price = getattr(

                stock,

                "close",

                getattr(

                    stock,

                    "ltp",

                    getattr(

                        stock,

                        "price",

                        0,

                    ),

                ),

            )

            score = getattr(

                stock,

                "score",

                getattr(

                    stock,

                    "confidence",

                    0,

                ),

            )

            confidence = getattr(

                stock,

                "confidence",

                0,

            )

            action = getattr(

                stock,

                "recommendation",

                getattr(

                    stock,

                    "action",

                    "HOLD",

                ),

            )

            entry = getattr(

                stock,

                "entry",

                getattr(

                    stock,

                    "entry_price",

                    0,

                ),

            )

            target = getattr(

                stock,

                "target1",

                getattr(

                    stock,

                    "target",

                    0,

                ),

            )

            stop_loss = getattr(

                stock,

                "stop_loss",

                getattr(

                    stock,

                    "sl",

                    0,

                ),

            )

            values = [

                row + 1,

                symbol,

                "NSE",

                f"₹{float(price):.2f}",

                score,

                confidence,

                action,

                f"₹{float(entry):.2f}",

                f"₹{float(target):.2f}",

                f"₹{float(stop_loss):.2f}",

            ]

            for column, value in enumerate(values):

                item = QTableWidgetItem(str(value))

                item.setTextAlignment(

                    Qt.AlignCenter

                )

                self.setItem(

                    row,

                    column,

                    item,

                )

        self.setSortingEnabled(True)

    def clear_table(self):

        self.recommendations = []

        self.clearContents()

        self.setRowCount(0)

    def _emit_selected(self):

        row = self.currentRow()

        if row < 0:

            return

        if row >= len(self.recommendations):

            return

        stock = self.recommendations[row]

        if isinstance(stock, dict):

            self.stock_selected.emit(stock)

            return

        if hasattr(stock, "__dict__"):

            self.stock_selected.emit(stock.__dict__)

            return

        data = {}

        for name in dir(stock):

            if name.startswith("_"):

                continue

            try:

                value = getattr(stock, name)

            except Exception:

                continue

            if callable(value):

                continue

            data[name] = value

        self.stock_selected.emit(data)