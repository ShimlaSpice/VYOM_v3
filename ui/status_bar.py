"""
Status Bar for VYOM.
"""

from __future__ import annotations

from datetime import datetime

from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QWidget,
)


class StatusBar(QWidget):
    """
    Bottom Status Bar for VYOM.
    """

    def __init__(self):

        super().__init__()

        self._build_ui()

    def _build_ui(self):

        self.lbl_market = QLabel("Market : NSE")
        self.lbl_universe = QLabel("Universe : NIFTY50")
        self.lbl_category = QLabel("Category : All")
        self.lbl_strategy = QLabel("Strategy : Intraday")
        self.lbl_scanned = QLabel("Scanned : 0")
        self.lbl_filtered = QLabel("Filtered : 0")
        self.lbl_displayed = QLabel("Displayed : 0")
        self.lbl_scan_time = QLabel("Scan Time : --")
        self.lbl_source = QLabel("Source : Yahoo")
        self.lbl_cache = QLabel("Cache : Fresh")
        self.lbl_jarvis = QLabel("Jarvis : READY ●")
        self.lbl_jarvis.setStyleSheet("color: #28a745;")

        self.message = QLabel("Ready")

        layout = QHBoxLayout()
        layout.setContentsMargins(10, 3, 10, 3)
        layout.setSpacing(15)

        sep = "  |  "
        for w in [
            self.lbl_market, self.lbl_universe, self.lbl_category,
            self.lbl_strategy, self.lbl_scanned, self.lbl_filtered,
            self.lbl_displayed, self.lbl_scan_time,
        ]:
            layout.addWidget(w)

        layout.addStretch()
        layout.addWidget(self.lbl_source)
        layout.addWidget(self.lbl_cache)
        layout.addWidget(self.lbl_jarvis)

        self.setLayout(layout)

        # Backward compat aliases
        self.market = self.lbl_market
        self.scanned = self.lbl_scanned
        self.filtered = self.lbl_filtered
        self.displayed = self.lbl_displayed
        self.scan_time = self.lbl_scan_time
        self.data_source = self.lbl_source
        self.last_update = self.lbl_cache
        self.jarvis = self.lbl_jarvis

    def show_message(

        self,

        message: str,

    ) -> None:
        print("[STATUS]", message)
        self.message.setText(message)
        self.last_update.setText(
            f"Updated : {datetime.now().strftime('%H:%M:%S')}",
        )

    def update_status(
        self,
        market,
        scanned,
        filtered,
        displayed,
        scan_time,
        source,
        jarvis,
        universe=None,
        category=None,
        strategy=None,
        cache=None,
    ):
        self.lbl_market.setText(f"Market : {market}")
        self.lbl_scanned.setText(f"Scanned : {scanned}")
        self.lbl_filtered.setText(f"Filtered : {filtered}")
        self.lbl_displayed.setText(f"Displayed : {displayed}")
        self.lbl_scan_time.setText(f"Scan Time : {scan_time:.2f} sec")
        self.lbl_source.setText(f"Source : {source}")
        self.lbl_jarvis.setText(f"Jarvis : {jarvis} ●")
        if universe:
            self.lbl_universe.setText(f"Universe : {universe}")
        if category:
            self.lbl_category.setText(f"Category : {category}")
        if strategy:
            self.lbl_strategy.setText(f"Strategy : {strategy}")
        if cache:
            self.lbl_cache.setText(f"Cache : {cache}")
        print(f"[STATUS UPDATE] scanned={scanned} filtered={filtered} displayed={displayed}")