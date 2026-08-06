"""
Top Bar for VYOM.
"""

from __future__ import annotations

from datetime import datetime


def _resolve_market_state(now: datetime | None = None) -> str:
    now = now or datetime.now()
    if now.weekday() >= 5:
        return "CLOSED"

    if now.time() < datetime.strptime("09:15", "%H:%M").time():
        return "PRE OPEN"

    if now.time() < datetime.strptime("15:30", "%H:%M").time():
        return "OPEN"

    return "CLOSED"

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QWidget,
)


class TopBar(QWidget):

    def __init__(self):

        super().__init__()

        self._build_ui()

        self._start_clock()

    def _build_ui(self):

        self.title = QLabel("VYOM AI")
        font = self.title.font()
        font.setBold(True)
        font.setPointSize(14)
        self.title.setFont(font)

        self.market_state = "CLOSED"

        self.market = QLabel("Market : NSE")
        self.market_status = QLabel("Status : Market Open")
        self.market_status.setStyleSheet("color: #28a745; font-weight: bold;")
        self.scan_time = QLabel("Last Scan : --")
        self.clock = QLabel()

        layout = QHBoxLayout()
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(16)

        layout.addWidget(self.title)
        layout.addStretch()
        layout.addWidget(self.market)
        layout.addWidget(self.market_status)
        layout.addWidget(self.scan_time)
        layout.addWidget(self.clock)

        self.setLayout(layout)

    def _market_state(self, now: datetime | None = None) -> str:
        return _resolve_market_state(now)

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

        now = datetime.now()
        self.clock.setText(now.strftime("%d-%b-%Y  %I:%M:%S %p"))
        state = _resolve_market_state(now)
        state_map = {"OPEN": "Market Open", "PRE OPEN": "Pre Open", "CLOSED": "Market Closed"}
        status_text = state_map.get(state, state)
        color = "#28a745" if state == "OPEN" else "#fd7e14" if state == "PRE OPEN" else "#dc3545"
        self.market_status.setText(f"Status : {status_text}")
        self.market_status.setStyleSheet(f"color: {color}; font-weight: bold;")

    def update_market(self, market: str):
        self.market.setText(f"Market : {market.upper()}")

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

        # Emotion removed from UI - kept method for backward compatibility
        pass

    def update_status(self, status: str):
        # Status is now shown in market_status label via clock update
        pass