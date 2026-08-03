"""
Top Bar for VYOM.
"""

from __future__ import annotations

from datetime import datetime

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QWidget,
)


class TopBar(QWidget):

    def __init__(self):

        super().__init__()

        self._build_ui()

        self._start_clock()

    def _build_ui(self):

        self.title = QLabel(

            "VYOM AI"

        )

        self.market = QLabel(

            "Market : CLOSED"

        )

        self.emotion = QLabel(

            "Emotion : 50/100 😐"

        )

        self.status = QLabel(

            "Status : Idle"

        )

        self.search = QLineEdit()

        self.search.setPlaceholderText(

            "Universal Search (Ctrl+K)"

        )

        self.search.setFixedWidth(

            260,

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

        layout.setSpacing(

            12,

        )

        layout.addWidget(

            self.title,

        )

        layout.addSpacing(

            20,

        )

        layout.addWidget(

            self.search,

        )

        layout.addStretch()

        layout.addWidget(

            self.market,

        )

        layout.addWidget(

            self.emotion,

        )

        layout.addWidget(

            self.status,

        )

        layout.addWidget(

            self.scan_time,

        )

        layout.addWidget(

            self.clock,

        )

        self.setLayout(

            layout,

        )

    def _start_clock(

        self,

    ):

        self.timer = QTimer(

            self,

        )

        self.timer.timeout.connect(

            self._update_clock,

        )

        self.timer.start(

            1000,

        )

        self._update_clock()

    def _update_clock(

        self,

    ):

        self.clock.setText(

            datetime.now().strftime(

                "%d-%b-%Y  %I:%M:%S %p"

            )

        )

    def update_market(

        self,

        market: str,

    ):

        self.market.setText(

            f"Market : {market}"

        )

    def update_scan_time(

        self,

        seconds: float,

    ):

        self.scan_time.setText(

            f"Last Scan : {seconds:.2f} sec"

        )

    def update_emotion(

        self,

        score: int,

        label: str,

    ):

        self.emotion.setText(

            f"Emotion : {score}/100 ({label})"

        )

    def update_status(

        self,

        status: str,

    ):

        self.status.setText(

            f"Status : {status}"

        )