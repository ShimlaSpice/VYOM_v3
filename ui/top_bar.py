"""
Top Bar for VYOM.
"""

from __future__ import annotations

from datetime import datetime

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QWidget,
)


class TopBar(QWidget):
    """
    Top application bar.
    """

    def __init__(self) -> None:

        super().__init__()

        self._build_ui()

        self._start_clock()

    def _build_ui(self) -> None:

        self.title = QLabel(
            "VYOM AI"
        )

        self.market = QLabel(
            "Market : --"
        )

        self.clock = QLabel()

        self.scan_time = QLabel(
            "Last Scan : --"
        )

        layout = QHBoxLayout()

        layout.setContentsMargins(
            10,
            5,
            10,
            5,
        )

        layout.addWidget(
            self.title,
        )

        layout.addStretch()

        layout.addWidget(
            self.market,
        )

        layout.addSpacing(
            20,
        )

        layout.addWidget(
            self.scan_time,
        )

        layout.addSpacing(
            20,
        )

        layout.addWidget(
            self.clock,
        )

        self.setLayout(
            layout,
        )

    def _start_clock(

        self,

    ) -> None:

        self.timer = QTimer(self)

        self.timer.timeout.connect(
            self._update_clock,
        )

        self.timer.start(
            1000,
        )

        self._update_clock()

    def _update_clock(

        self,

    ) -> None:

        self.clock.setText(

            datetime.now().strftime(

                "%d-%b-%Y   %I:%M:%S %p"

            )

        )

    def update_market(

        self,

        market: str,

    ) -> None:

        self.market.setText(

            f"Market : {market}"

        )

    def update_scan_time(

        self,

        seconds: float,

    ) -> None:

        self.scan_time.setText(

            f"Last Scan : {seconds:.2f} sec"

        )