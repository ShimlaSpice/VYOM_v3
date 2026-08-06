"""
Recommendation Table for VYOM.
Columns: Rank, Symbol, Company, Change%, Confidence, Action, Entry, Target, SL, Volume
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
from PySide6.QtGui import QColor, QFont

from ui.company_names import get_company_name


class RecommendationTable(QTableWidget):

    stock_selected = Signal(dict)

    HEADERS = [
        "Rank", "Symbol", "Company", "Change %",
        "Confidence", "Action",
        "Entry (Rs)", "Target (Rs)", "SL (Rs)", "Volume",
    ]

    _COL_CONF   = 4
    _COL_ACTION = 5

    def __init__(self):
        super().__init__()
        self.recommendations = []
        self._build_ui()

    def _build_ui(self):
        self.setColumnCount(len(self.HEADERS))
        self.setHorizontalHeaderLabels(self.HEADERS)
        self.verticalHeader().setVisible(False)
        self.verticalHeader().setDefaultSectionSize(38)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)
        self.setShowGrid(False)
        self.setWordWrap(False)
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        hf = self.horizontalHeader().font()
        hf.setBold(True)
        self.horizontalHeader().setFont(hf)
        col_widths = [48, 130, 195, 90, 120, 90, 95, 95, 88, 100]
        for i, w in enumerate(col_widths):
            self.setColumnWidth(i, w)
        self.itemSelectionChanged.connect(self._emit_selected)

    def _make_action_widget(self, action: str) -> QLabel:
        label = QLabel(action)
        label.setAlignment(Qt.AlignCenter)
        label.setFixedHeight(26)
        colors = {
            "BUY":        ("#fff", "#198754"),
            "STRONG BUY": ("#fff", "#0d6efd"),
            "HOLD":       ("#212529", "#ffc107"),
            "SELL":       ("#fff", "#dc3545"),
            "WATCH":      ("#fff", "#6c757d"),
        }
        fg, bg = colors.get(action.upper(), ("#fff", "#6c757d"))
        label.setStyleSheet(
            f"background:{bg}; color:{fg}; border-radius:4px; font-weight:bold; font-size:10pt; padding:2px 8px;"
        )
        return label

    def _make_confidence_widget(self, confidence: int) -> QWidget:
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(6, 3, 6, 3)
        layout.setSpacing(6)
        label = QLabel(f"{confidence}%")
        label.setFixedWidth(38)
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        f = label.font(); f.setBold(True); label.setFont(f)
        bar = QProgressBar()
        bar.setRange(0, 100)
        bar.setValue(int(confidence))
        bar.setTextVisible(False)
        bar.setFixedHeight(8)
        chunk = "#28a745" if confidence >= 75 else "#2196F3" if confidence >= 55 else "#ffc107"
        bar.setStyleSheet(
            f"QProgressBar{{background:#3a3a3a;border-radius:4px;}}"
            f"QProgressBar::chunk{{background:{chunk};border-radius:4px;}}"
        )
        layout.addWidget(label)
        layout.addWidget(bar)
        return container

    def load_data(self, recommendations, filters=None):
        self.setSortingEnabled(False)
        self.clearContents()
        rows = list(recommendations or [])
        self.recommendations = rows
        self.setRowCount(len(rows))

        for row, stock in enumerate(rows):
            if isinstance(stock, dict):
                symbol     = stock.get("symbol", "")
                confidence = int(stock.get("confidence", 0) or 0)
                action     = stock.get("recommendation", stock.get("action", "HOLD"))
                entry      = float(stock.get("entry", 0) or 0)
                target     = float(stock.get("target1", stock.get("target", 0)) or 0)
                stop_loss  = float(stock.get("stop_loss", 0) or 0)
                change_pct = float(stock.get("change_percent", 0) or 0)
                volume     = int(stock.get("volume", 0) or 0)
            else:
                symbol     = getattr(stock, "symbol", "")
                confidence = int(getattr(stock, "confidence", 0) or 0)
                action     = getattr(stock, "recommendation", "HOLD")
                entry      = float(getattr(stock, "entry", 0) or 0)
                target     = float(getattr(stock, "target1", getattr(stock, "target", 0)) or 0)
                stop_loss  = float(getattr(stock, "stop_loss", 0) or 0)
                change_pct = float(getattr(stock, "change_percent", 0) or 0)
                volume     = int(getattr(stock, "volume", 0) or 0)

            company = get_company_name(symbol)
            change_color = QColor("#4caf50") if change_pct >= 0 else QColor("#f44336")
            change_str   = (f"+{change_pct:.2f}%" if change_pct >= 0 else f"{change_pct:.2f}%")
            if volume >= 10_000_000:
                vol_str = f"{volume/10_000_000:.2f} Cr"
            elif volume >= 100_000:
                vol_str = f"{volume/100_000:.2f} L"
            else:
                vol_str = f"{volume:,}"

            col_data = [
                (str(row+1),           Qt.AlignCenter,                  None),
                (symbol,               Qt.AlignLeft|Qt.AlignVCenter,    QColor("#82b1ff")),
                (company,              Qt.AlignLeft|Qt.AlignVCenter,    None),
                (change_str,           Qt.AlignCenter,                  change_color),
                ("", Qt.AlignCenter, None),   # confidence widget
                ("", Qt.AlignCenter, None),   # action widget
                (f"Rs{entry:,.2f}",    Qt.AlignRight|Qt.AlignVCenter,   None),
                (f"Rs{target:,.2f}",   Qt.AlignRight|Qt.AlignVCenter,   QColor("#4caf50")),
                (f"Rs{stop_loss:,.2f}",Qt.AlignRight|Qt.AlignVCenter,   QColor("#f44336")),
                (vol_str,              Qt.AlignRight|Qt.AlignVCenter,   None),
            ]
            for col, (text, align, color) in enumerate(col_data):
                item = QTableWidgetItem(text)
                item.setTextAlignment(align)
                if color:
                    item.setForeground(color)
                self.setItem(row, col, item)
            self.setCellWidget(row, self._COL_CONF,   self._make_confidence_widget(confidence))
            self.setCellWidget(row, self._COL_ACTION, self._make_action_widget(action or "HOLD"))

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
        payload: dict = {}
        if hasattr(stock, "__slots__"):
            for slot in stock.__slots__:
                payload[slot] = getattr(stock, slot, None)
        elif hasattr(stock, "__dict__"):
            payload = dict(stock.__dict__)
        else:
            payload = {"symbol": getattr(stock, "symbol", ""),
                       "recommendation": getattr(stock, "recommendation", "HOLD")}
        self.stock_selected.emit(payload)
