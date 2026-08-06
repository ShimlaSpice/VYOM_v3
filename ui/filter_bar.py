"""
Filter Bar for VYOM Dashboard.
Row 1: Market | Universe | Price | Min | Max | Capital | Sort | Top | Refresh
Row 2: Strategy buttons | Search | Scan | Refresh | Auto
"""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QButtonGroup,
    QCheckBox,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class FilterBar(QWidget):

    scan_requested = Signal(dict)
    category_changed = Signal(str)

    def __init__(self):
        super().__init__()
        self._build_ui()

    def _build_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(6, 4, 6, 4)
        main_layout.setSpacing(6)

        # ── ROW 1: market controls ──────────────────────────────────────────
        row1 = QHBoxLayout()
        row1.setSpacing(8)

        row1.addWidget(QLabel("Market"))
        self.market = QComboBox()
        self.market.addItems(["NSE", "BSE"])
        self.market.setFixedWidth(70)
        row1.addWidget(self.market)

        row1.addWidget(QLabel("Universe"))
        self.universe = QComboBox()
        self.universe.addItems([
            "NIFTY50", "NIFTY100", "NIFTY200", "NIFTY500", "NEXT50",
            "BANKNIFTY", "MIDCAP", "SMALLCAP", "MICROCAP", "F&O", "PENNY",
            "SME", "ETF", "REIT", "INVIT", "AUTO", "BANK", "IT", "PHARMA",
            "FMCG", "REALTY", "ENERGY", "METAL", "PSU", "DEFENCE", "CHEMICAL",
            "TEXTILE", "MEDIA", "TELECOM", "HEALTHCARE", "CAPITALGOODS",
            "FINANCIAL", "ALL",
        ])
        self.universe.setFixedWidth(100)
        row1.addWidget(self.universe)

        row1.addWidget(QLabel("Price"))
        self.price_band = QComboBox()
        self.price_band.addItems([
            "All", "Below ₹100", "₹100-₹500", "₹500-₹1k", "₹1k-₹5k", "Above ₹5k",
        ])
        self.price_band.setFixedWidth(110)
        row1.addWidget(self.price_band)

        self.min_price = QLineEdit()
        self.min_price.setPlaceholderText("Min")
        self.min_price.setFixedWidth(55)
        row1.addWidget(self.min_price)

        self.max_price = QLineEdit()
        self.max_price.setPlaceholderText("Max")
        self.max_price.setFixedWidth(55)
        row1.addWidget(self.max_price)

        row1.addWidget(QLabel("Capital"))
        self.capital = QComboBox()
        self.capital.addItems(["10000", "25000", "50000", "100000", "500000"])
        self.capital.setFixedWidth(90)
        row1.addWidget(self.capital)

        row1.addWidget(QLabel("Sort"))
        self.sort_by = QComboBox()
        self.sort_by.addItems(["Confidence", "Score", "Probability", "Price"])
        self.sort_by.setFixedWidth(110)
        row1.addWidget(self.sort_by)

        row1.addWidget(QLabel("Top"))
        self.top = QComboBox()
        self.top.addItems(["10", "20", "50"])
        self.top.setFixedWidth(60)
        row1.addWidget(self.top)

        row1.addWidget(QLabel("Refresh"))
        self.refresh_interval = QComboBox()
        self.refresh_interval.addItems(["30 Sec", "1 Min", "2 Min", "5 Min", "10 Min"])
        self.refresh_interval.setFixedWidth(90)
        row1.addWidget(self.refresh_interval)

        row1.addStretch()
        main_layout.addLayout(row1)

        # ── ROW 2: strategy buttons | search | scan ─────────────────────────
        row2 = QHBoxLayout()
        row2.setSpacing(8)

        # Strategy buttons (exclusive)
        self.strategy_button_group = QButtonGroup(self)
        self.strategy_button_group.setExclusive(True)
        self._active_strategy = "Intraday"

        for i, strategy in enumerate(["Intraday", "Swing", "Positional", "Long Term", "Scalping"]):
            btn = QPushButton(strategy)
            btn.setCheckable(True)
            btn.setChecked(i == 0)
            btn.setMinimumHeight(34)
            self.strategy_button_group.addButton(btn, i)
            btn.clicked.connect(lambda checked, s=strategy: self._on_strategy(s))
            row2.addWidget(btn)

        # Universal search (moved from TopBar, reduced width)
        self.search = QLineEdit()
        self.search.setPlaceholderText("🔍  Universal Search  (Ctrl+K)")
        self.search.setFixedWidth(220)
        self.search.setMinimumHeight(34)
        row2.addWidget(self.search)

        row2.addStretch()

        # Scan button — primary action
        self.scan_button = QPushButton("🔍  Scan (F5)")
        self.scan_button.setMinimumSize(140, 36)
        self.scan_button.setObjectName("scanButton")
        self.scan_button.clicked.connect(self._emit_scan_request)
        row2.addWidget(self.scan_button)

        # Refresh button
        self.refresh = QPushButton("↻  Refresh")
        self.refresh.setMinimumSize(100, 36)
        self.refresh.clicked.connect(self._emit_scan_request)
        row2.addWidget(self.refresh)

        # Auto refresh checkbox
        self.auto_refresh = QCheckBox("Auto")
        row2.addWidget(self.auto_refresh)

        main_layout.addLayout(row2)

        # Hidden compat labels used by main_window
        self.scan_timer  = QLabel("⏱ 0.00 sec")
        self.scan_status = QLabel("Ready")
        self.scan_timer.setVisible(False)
        self.scan_status.setVisible(False)

        # Hidden category combo kept for _collect_filters() compat
        self.category = QComboBox()
        self.category.addItems(["Intraday", "Swing", "Positional", "Long Term", "Scalping"])
        self.category.setVisible(False)

        self.setLayout(main_layout)

    def _on_strategy(self, strategy: str) -> None:
        self._active_strategy = strategy
        self.category.setCurrentText(strategy)
        self.category_changed.emit(strategy)

    def _emit_scan_request(self) -> None:
        self.scan_requested.emit({
            "market":           self.market.currentText(),
            "universe":         self.universe.currentText(),
            "category":         self._active_strategy,
            "price_band":       self.price_band.currentText(),
            "min_price":        self.min_price.text(),
            "max_price":        self.max_price.text(),
            "capital":          self.capital.currentText(),
            "sort_by":          self.sort_by.currentText(),
            "top":              int(self.top.currentText()),
            "auto_refresh":     self.auto_refresh.isChecked(),
            "refresh_interval": self.refresh_interval.currentText(),
        })


class FilterBar(QWidget):

    scan_requested = Signal(dict)
    category_changed = Signal(str)

    def __init__(self):

        super().__init__()

        self._build_ui()

    def _build_ui(self):

        # Main vertical layout for 2 rows
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(8)

        # ============ ROW 1 ============
        row1 = QHBoxLayout()
        row1.setSpacing(10)

        # Market
        row1.addWidget(QLabel("Market"))
        self.market = QComboBox()
        self.market.addItems(["NSE", "BSE"])
        row1.addWidget(self.market)

        # Universe
        row1.addWidget(QLabel("Universe"))
        self.universe = QComboBox()
        self.universe.addItems([
            "NIFTY50", "NIFTY100", "NIFTY200", "NIFTY500", "NEXT50",
            "BANKNIFTY", "MIDCAP", "SMALLCAP", "MICROCAP", "F&O", "PENNY",
            "SME", "ETF", "REIT", "INVIT", "AUTO", "BANK", "IT", "PHARMA",
            "FMCG", "REALTY", "ENERGY", "METAL", "PSU", "DEFENCE", "CHEMICAL",
            "TEXTILE", "MEDIA", "TELECOM", "HEALTHCARE", "CAPITALGOODS",
            "FINANCIAL", "ALL",
        ])
        row1.addWidget(self.universe)

        # Price
        row1.addWidget(QLabel("Price"))
        self.price_band = QComboBox()
        self.price_band.addItems([
            "All", "Below ₹100", "₹100 - ₹500", "₹500 - ₹1,000",
            "₹1,000 - ₹5,000", "Above ₹5,000",
        ])
        row1.addWidget(self.price_band)

        # Min Price
        self.min_price = QLineEdit()
        self.min_price.setPlaceholderText("Min")
        self.min_price.setFixedWidth(60)
        row1.addWidget(self.min_price)

        # Max Price
        self.max_price = QLineEdit()
        self.max_price.setPlaceholderText("Max")
        self.max_price.setFixedWidth(60)
        row1.addWidget(self.max_price)

        # Capital
        row1.addWidget(QLabel("Capital"))
        self.capital = QComboBox()
        self.capital.addItems(["10000", "25000", "50000", "100000", "500000"])
        row1.addWidget(self.capital)

        # Sort
        row1.addWidget(QLabel("Sort"))
        self.sort_by = QComboBox()
        self.sort_by.addItems(["Confidence", "Score", "Probability", "Price"])
        row1.addWidget(self.sort_by)

        # Top
        row1.addWidget(QLabel("Top"))
        self.top = QComboBox()
        self.top.addItems(["10", "20", "50"])
        row1.addWidget(self.top)

        # Refresh Interval
        row1.addWidget(QLabel("Refresh"))
        self.refresh_interval = QComboBox()
        self.refresh_interval.addItems(["30 Sec", "1 Min", "2 Min", "5 Min", "10 Min"])
        row1.addWidget(self.refresh_interval)

        row1.addStretch()

        # Scan Button
        self.scan_button = QPushButton("🔍 Scan (F5)")
        self.scan_button.setMinimumSize(120, 32)
        self.scan_button.clicked.connect(self._emit_scan_request)
        row1.addWidget(self.scan_button)

        # Refresh Button
        self.refresh = QPushButton("↻ Refresh")
        self.refresh.setMinimumSize(100, 32)
        self.refresh.clicked.connect(self._emit_scan_request)
        row1.addWidget(self.refresh)

        # Auto Refresh
        self.auto_refresh = QCheckBox("Auto")
        row1.addWidget(self.auto_refresh)

        main_layout.addLayout(row1)

        # ============ ROW 2 ============
        row2 = QHBoxLayout()
        row2.setSpacing(10)

        # Category Dropdown
        row2.addWidget(QLabel("Category"))
        self.category = QComboBox()
        self.category.addItems(["Intraday", "Swing", "Positional", "Long Term", "Scalping"])
        self.category.setMaximumWidth(150)
        row2.addWidget(self.category)

        # Strategy Buttons (moved from LeftSidebar)
        self.strategy_button_group = QButtonGroup(self)
        self.strategy_button_group.setExclusive(True)

        strategies = ["Intraday", "Swing", "Positional", "Long Term", "Scalping"]
        for i, strategy in enumerate(strategies):
            btn = QPushButton(strategy)
            btn.setMinimumHeight(32)
            btn.setMaximumWidth(120)
            btn.setCheckable(True)
            if i == 0:  # Intraday is default
                btn.setChecked(True)
            self.strategy_button_group.addButton(btn, i)
            btn.clicked.connect(lambda checked, s=strategy: self.category_changed.emit(s))
            row2.addWidget(btn)

        row2.addStretch()

        main_layout.addLayout(row2)

        # Hidden elements for backward compatibility with main_window
        self.scan_timer = QLabel("⏱ 0.00 sec")
        self.scan_status = QLabel("Ready")
        self.scan_timer.setVisible(False)
        self.scan_status.setVisible(False)

        self.setLayout(main_layout)

    def _emit_scan_request(self) -> None:
        self.scan_requested.emit({
            "market": self.market.currentText(),
            "universe": self.universe.currentText(),
            "category": self.category.currentText(),
            "price_band": self.price_band.currentText(),
            "min_price": self.min_price.text(),
            "max_price": self.max_price.text(),
            "capital": self.capital.currentText(),
            "sort_by": self.sort_by.currentText(),
            "top": int(self.top.currentText()),
            "auto_refresh": self.auto_refresh.isChecked(),
            "refresh_interval": self.refresh_interval.currentText(),
        })