"""
Filter Bar for VYOM Dashboard.
"""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QWidget,
)
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import QCheckBox

class FilterBar(QWidget):

    scan_requested = Signal(dict)

    def __init__(self):

        super().__init__()

        self._build_ui()

    def _build_ui(self):

        layout = QHBoxLayout()

        layout.setSpacing(10)

        layout.addWidget(QLabel("Market"))

        self.market = QComboBox()
        self.market.addItems(
            [
                "NSE",
                "BSE",
            ]
        )
        layout.addWidget(self.market)

        layout.addWidget(QLabel("Universe"))

        self.universe = QComboBox()
        self.universe.addItems(
            [
                "NIFTY50",
                "NIFTY100",
                "NIFTY200",
                "NIFTY500",
                "F&O",
                "MIDCAP",
                "SMALLCAP",
                "PENNY",
            ]
        )
        layout.addWidget(self.universe)

        layout.addWidget(QLabel("Category"))

        self.category = QComboBox()
        self.category.addItems(
            [
                "Today",
                "Intraday",
                "Swing",
                "Long Term",
            ]
        )
        layout.addWidget(self.category)

        layout.addWidget(QLabel("Price"))

        self.price_band = QComboBox()
        self.price_band.addItems(
            [
                "All",
                "Below ₹100",
                "₹100 - ₹500",
                "₹500 - ₹1,000",
                "₹1,000 - ₹5,000",
                "Above ₹5,000",
            ]
        )
        layout.addWidget(self.price_band)

        self.min_price = QLineEdit()
        self.min_price.setPlaceholderText("Min")
        self.min_price.setFixedWidth(70)
        layout.addWidget(self.min_price)

        self.max_price = QLineEdit()
        self.max_price.setPlaceholderText("Max")
        self.max_price.setFixedWidth(70)
        layout.addWidget(self.max_price)

        layout.addWidget(QLabel("Capital"))

        self.capital = QComboBox()
        self.capital.addItems(
            [
                "10000",
                "25000",
                "50000",
                "100000",
                "500000",
            ]
        )
        layout.addWidget(self.capital)

        layout.addWidget(QLabel("Sort"))

        self.sort_by = QComboBox()
        self.sort_by.addItems(
            [
                "Confidence",
                "Score",
                "Probability",
                "Price",
            ]
        )
        layout.addWidget(self.sort_by)

        layout.addWidget(QLabel("Top"))

        self.top = QComboBox()
        self.top.addItems(
            [
                "10",
                "20",
                "50",
            ]
        )
        layout.addWidget(self.top)

        layout.addWidget(
            QLabel("Refresh")
        )
        self.refresh_interval = QComboBox()
        self.refresh_interval.addItems(
            [
                "30 Sec",
                "1 Min",
                "2 Min",
                "5 Min",
                "10 Min",
            ]
        )

        layout.addWidget(
            self.refresh_interval,
        )

        layout.addStretch()

        self.scan_button = QPushButton("🔍 Scan (F5)")
        self.scan_button.clicked.connect(
            self._emit_scan_request,
        )

        self.refresh = QPushButton("↻ Refresh")

        self.refresh.clicked.connect(
            self._emit_scan_request,
        )

        layout.addWidget(
            self.refresh,
        )

        self.auto_refresh = QCheckBox(
            "Auto"
        )

        layout.addWidget(
            self.auto_refresh,
        )

        layout.addWidget(
            self.scan_button,
        )

        self.setLayout(
            layout,
        )

        QShortcut(

           QKeySequence("F5"),

            self,

            activated=self._emit_scan_request,

        )

        QShortcut(

            QKeySequence("Ctrl+R"),

            self,

            activated=self._emit_scan_request,

        )

    def _emit_scan_request(self):

        self.scan_requested.emit(

            {

                "market": self.market.currentText(),

                "universe": self.universe.currentText(),

                "category": self.category.currentText(),

                "price_band": self.price_band.currentText(),

                "min_price": self.min_price.text(),

                "max_price": self.max_price.text(),

                "capital": self.capital.currentText(),

                "sort_by": self.sort_by.currentText(),

                "top": int(
                    self.top.currentText()
                ),
                
                "auto_refresh": self.auto_refresh.isChecked(),

                "refresh_interval": self.refresh_interval.currentText(),

            }

        )