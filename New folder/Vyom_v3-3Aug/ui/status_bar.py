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

        self.market = QLabel("Market : --")

        self.scanned = QLabel("Scanned : 0")

        self.filtered = QLabel("Filtered : 0")

        self.displayed = QLabel("Displayed : 0")

        self.scan_time = QLabel("Scan : 0.00 sec")

        self.data_source = QLabel("Source : Yahoo")

        self.last_update = QLabel("Updated : --")

        self.jarvis = QLabel("Jarvis : READY")

        self.message = QLabel("Ready")

        layout = QHBoxLayout()

        layout.setContentsMargins(

            10,

            5,

            10,

            5,

        )

        layout.addWidget(

            self.market,

        )

        layout.addStretch()

        layout.addWidget(

            self.message,

        )

        layout.addStretch()

        layout.addWidget(

            self.scanned,

        )

        layout.addWidget(

            self.filtered,

        )

        layout.addWidget(

            self.displayed,

        )

        layout.addWidget(

            self.scan_time,

        )

        layout.addWidget(

            self.data_source,

        )

        layout.addWidget(

            self.last_update,

        )

        layout.addWidget(

            self.jarvis,

        )

        self.setLayout(

            layout,

        )

    def show_message(

        self,

        message: str,

    ) -> None:
        print("[STATUS]",message)

#        self.message.setText(
#
#           message,
#
#        )
#
#        self.last_update.setText(
#
#            f"Updated : {datetime.now().strftime('%H:%M:%S')}",
#
#        )

    def update_status(
        self,
        market,
        scanned,
        filtered,
        displayed,
        scan_time,
        source,
        jarvis,
    ):
        print("[STATUS UPDATE]")



#    def update_status(
#
 #       self,
#
 #       market: str,
#
 #       scanned: int,
#
 #       filtered: int,
#
 #       displayed: int,
#
 #       scan_time: float,
#
 #       source: str,
#
 #       jarvis: str,
#
 #     self.market.setText(
#
 #           f"Market : {market}"
#
 #       )
#
 #       self.scanned.setText(
#
 #           f"Scanned : {scanned}"
#
 #       )
#
 #       self.filtered.setText(
#
 #           f"Filtered : {filtered}"
#
 #       )
#
 #       self.displayed.setText(
#
 #           f"Displayed : {displayed}"
#
 #       )
#
 #       self.scan_time.setText(
#
 #           f"Scan : {scan_time:.2f} sec"
#
 #       )
#
 #       self.data_source.setText(
#
 #           f"Source : {source}"
#
 #       )
#
 #       self.jarvis.setText(
#
 #           f"Jarvis : {jarvis}"
#
 #       )
#
 #       self.last_update.setText(
#
 #           f"Updated : {datetime.now().strftime('%H:%M:%S')}"
#
 #       )