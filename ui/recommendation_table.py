"""
Recommendation Table for VYOM.
Columns: Rank, Symbol, Company, Market, CMP(Rs), Change%, Score, Confidence, Action, Entry(Rs), Target(Rs), SL(Rs), Volume
"""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QAbstractItemView,
    QHeaderView,
    QLabel,
    QProgressBar,
    QTableWidget,
    QTableWidgetItem,
    QWidget,
    QHBoxLayout,
)
from PySide6.QtGui import QColor


class RecommendationTable(QTableWidget):

    stock_selected = Signal(dict)

    HEADERS = [
        "Rank",
        "Symbol",
        "Company",
        "Market",
        "CMP (Rs)",
        "Change %",
        "Score",
        "Confidence",
        "Action",
        "Entry (Rs)",
        "Target (Rs)",
        "SL (Rs)",
        "Volume",
    ]

    def __init__(self):
        super().__init__()
        self.recommendations = []
        self._build_ui()

    def _build_ui(self):
        self.setColumnCount(len(self.HEADERS))
        self.setHorizontalHeaderLabels(self.HEADERS)
        self.verticalHeader().setVisible(False)
        self.verticalHeader().setDefaultSectionSize(32)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)
        self.setShowGrid(False)
        self.setWordWrap(False)
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        col_widths = [45, 130, 160, 60, 90, 80, 65, 100, 80, 90, 90, 85, 90]
        for i, w in enumerate(col_widths):
            self.setColumnWidth(i, w)
        self.itemSelectionChanged.connect(self._emit_selected)

    def _make_action_widget(self, action: str) -> QLabel:
        label = QLabel(action)
        label.setAlignment(Qt.AlignCenter)
        label.setFixedHeight(24)
        colors = {
            "BUY": ("#155724", "#d4edda"),
            "STRONG BUY": ("#0d3c14", "#c3e6cb"),
            "HOLD": ("#856404", "#fff3cd"),
            "SELL": ("#721c24", "#f8d7da"),
            "WATCH": ("#533f03", "#ffeeba"),
        }
        fg, bg = colors.get(action.upper(), ("#333", "#eee"))
        label.setStyleSheet(
            f"background-color: {bg}; color: {fg}; "
            f"border-radius: 4px; font-weight: bold; padding: 2px 6px;"
        )
        return label

    def _make_confidence_widget(self, confidence: int) -> QWidget:
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(4, 2, 4, 2)
        layout.setSpacing(4)
        bar = QProgressBar()
        bar.setRange(0, 100)
        bar.setValue(int(confidence))
        bar.setTextVisible(False)
        bar.setFixedHeight(8)
        bar.setStyleSheet(
            "QProgressBar { background: #e0e0e0; border-radius: 4px; }"
            "QProgressBar::chunk { background: #2196F3; border-radius: 4px; }"
        )
        label = QLabel(f"{confidence}%")
        label.setFixedWidth(36)
        label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        layout.addWidget(label)
        layout.addWidget(bar)
        return container

    def load_data(self, recommendations, filters=None):
        self.setSortingEnabled(False)
        self.clearContents()
        rows = list(recommendations or [])
        self.recommendations = rows
        self.setRowCount(len(rows))
        print(f"[TABLE] Loading {len(rows)} rows")
        for row, stock in enumerate(rows):
            if isinstance(stock, dict):
                symbol = stock.get("symbol", "")
                market = stock.get("market", "NSE")
                price = float(stock.get("price", stock.get("close", 0)) or 0)
                score = float(stock.get("score", 0) or 0)
                confidence = int(stock.get("confidence", 0) or 0)
                action = stock.get("recommendation", stock.get("action", "HOLD"))
                entry = float(stock.get("entry", 0) or 0)
                target = float(stock.get("target1", stock.get("target", 0)) or 0)
                stop_loss = float(stock.get("stop_loss", 0) or 0)
                change_pct = float(stock.get("change_percent", 0) or 0)
                volume = int(stock.get("volume", 0) or 0)
            else:
                symbol = getattr(stock, "symbol", "")
                market = getattr(stock, "market", "NSE")
                price = float(getattr(stock, "price", getattr(stock, "close", 0)) or 0)
                score = float(getattr(stock, "score", 0) or 0)
                confidence = int(getattr(stock, "confidence", 0) or 0)
                action = getattr(stock, "recommendation", "HOLD")
                entry = float(getattr(stock, "entry", 0) or 0)
                target = float(getattr(stock, "target1", getattr(stock, "target", 0)) or 0)
                stop_loss = float(getattr(stock, "stop_loss", 0) or 0)
                change_pct = float(getattr(stock, "change_percent", 0) or 0)
                volume = int(getattr(stock, "volume", 0) or 0)
            company = symbol.replace(".NS", "").replace(".BO", "")
            print(f"[TABLE] Row {row} extracted: symbol={symbol}, price={price}, conf={confidence}")
            if volume >= 10000000:
                vol_str = f"{volume / 10000000:.2f} Cr"
            elif volume >= 100000:
                vol_str = f"{volume / 100000:.2f} L"
            else:
                vol_str = f"{volume:,}"
            change_color = QColor("#28a745") if change_pct >= 0 else QColor("#dc3545")
            col_values = [
                (str(row + 1), Qt.AlignCenter, None),
                (symbol, Qt.AlignLeft | Qt.AlignVCenter, QColor("#1a73e8")),
                (company, Qt.AlignLeft | Qt.AlignVCenter, None),
                (market, Qt.AlignCenter, None),
                (f"{price:,.2f}", Qt.AlignRight | Qt.AlignVCenter, None),
                (f"+{change_pct:.2f}%" if change_pct >= 0 else f"{change_pct:.2f}%", Qt.AlignCenter, change_color),
                (f"{score:.1f}", Qt.AlignCenter, None),
                ("", Qt.AlignCenter, None),
                ("", Qt.AlignCenter, None),
                (f"{entry:,.2f}", Qt.AlignRight | Qt.AlignVCenter, None),
                (f"{target:,.2f}", Qt.AlignRight | Qt.AlignVCenter, QColor("#28a745")),
                (f"{stop_loss:,.2f}", Qt.AlignRight | Qt.AlignVCenter, QColor("#dc3545")),
                (vol_str, Qt.AlignRight | Qt.AlignVCenter, None),
            ]
            for col, (text, align, color) in enumerate(col_values):
                item = QTableWidgetItem(text)
                item.setTextAlignment(align)
                if color:
                    item.setForeground(color)
                self.setItem(row, col, item)
            self.setCellWidget(row, 7, self._make_confidence_widget(confidence))
            self.setCellWidget(row, 8, self._make_action_widget(action or "HOLD"))
        print(f"[TABLE] Rows inserted = {self.rowCount()}")
        self.setSortingEnabled(True)
        if self.rowCount() > 0:
            self.selectRow(0)
            self._emit_selected()

    def clear_table(self):
        self.recommendations = []
        self.clearContents()
        self.setRowCount(0)

    def _emit_selected(self):
        row = self.currentRow()
        if row < 0 or row >= len(self.recommendations):
            return
        stock = self.recommendations[row]
        if isinstance(stock, dict):
            self.stock_selected.emit(stock)
            return
        payload = {}
        if hasattr(stock, "__slots__"):
            for slot in stock.__slots__:
                payload[slot] = getattr(stock, slot, None)
        elif hasattr(stock, "__dict__"):
            payload = dict(stock.__dict__)
        else:
            payload = {"symbol": getattr(stock, "symbol", ""), "recommendation": getattr(stock, "recommendation", "HOLD")}
        self.stock_selected.emit(payload)
