"""
Main Window for VYOM Desktop.
"""

from __future__ import annotations

from time import perf_counter

from PySide6.QtCore import (
    QTimer,
)

from PySide6.QtGui import (
    QKeySequence,
    QShortcut,
)

from PySide6.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QProgressBar,
    QVBoxLayout,
    QWidget,
)

from app.pipeline.market_pipeline import MarketPipeline

from ui.dashboard import Dashboard
from ui.filter_bar import FilterBar
from ui.left_sidebar import LeftSidebar
from ui.status_bar import StatusBar
from ui.top_bar import TopBar


class MainWindow(QMainWindow):
    """
    Main application window.
    """

    def __init__(self):

        super().__init__()

        self.setWindowTitle(

            "VYOM AI",

        )

        self.resize(

            1600,

            900,

        )

        self.pipeline = None

        self.refresh_timer = QTimer()

        self._build_ui()

        self._connect_signals()

        self._create_shortcuts()

        self.refresh_timer.timeout.connect(

            self._auto_refresh,

        )

    def _build_ui(

        self,

    ):

        self.top_bar = TopBar()

        self.filter_bar = FilterBar()

        self.sidebar = LeftSidebar()

        self.dashboard = Dashboard()

        self.status = StatusBar()

        self.progress = QProgressBar()

        self.progress.setRange(

            0,

            100,

        )

        self.progress.hide()

        central = QWidget()

        self.setCentralWidget(

            central,

        )

        root_layout = QVBoxLayout()

        root_layout.setContentsMargins(

            5,

            5,

            5,

            5,

        )

        root_layout.setSpacing(

            5,

        )

        root_layout.addWidget(

            self.top_bar,

        )

        root_layout.addWidget(

            self.filter_bar,

        )

        root_layout.addWidget(

            self.progress,

        )

        body = QHBoxLayout()

        body.setSpacing(

            5,

        )

        body.addWidget(

            self.sidebar,

        )

        body.addWidget(

            self.dashboard,

            1,

        )

        root_layout.addLayout(

            body,

            1,

        )

        root_layout.addWidget(

            self.status,

        )

        central.setLayout(

            root_layout,

        )

    def _connect_signals(

        self,

    ):

        self.sidebar.category_changed.connect(

            self._category_changed,

        )

        self.filter_bar.scan_requested.connect(

            self._scan_requested,

        )

    def _create_shortcuts(

        self,

    ):

        QShortcut(

            QKeySequence(

                "F5",

            ),

            self,

            activated=self._auto_refresh,

        )

        QShortcut(

            QKeySequence(

                "Ctrl+R",

            ),

            self,

            activated=self._auto_refresh,

        )

    def _collect_filters(

        self,

    ) -> dict:

        return {

            "market": self.filter_bar.market.currentText(),

            "universe": self.filter_bar.universe.currentText(),

            "category": self.filter_bar.category.currentText(),

            "price_band": self.filter_bar.price_band.currentText(),

            "min_price": self.filter_bar.min_price.text(),

            "max_price": self.filter_bar.max_price.text(),

            "capital": self.filter_bar.capital.currentText(),

            "sort_by": self.filter_bar.sort_by.currentText(),

            "top": int(

                self.filter_bar.top.currentText(),

            ),

            "auto_refresh": self.filter_bar.auto_refresh.isChecked(),

            "refresh_interval": self.filter_bar.refresh_interval.currentText(),

        }

    def _auto_refresh(

        self,

    ):

        self._scan_requested(

            self._collect_filters(),

        )
    def _category_changed(

        self,

        category: str,

    ) -> None:

        self.filter_bar.category.setCurrentText(

            category,

        )

    def _scan_requested(

        self,

        filters: dict,

    ) -> None:

        scan_start = perf_counter()

        self.filter_bar.scan_button.setText(

            "🔄 Scanning...",

        )

        self.filter_bar.scan_status.setText(

            "Downloading Market Data...",

        )

        self.filter_bar.scan_timer.setText(

            "⏱ 0.00 sec",

        )

        self.progress.show()

        self.progress.setValue(

            10,

        )

        if hasattr(

            self.status,

            "show_message",

        ):

            self.status.show_message(

                "Scanning market...",

            )

        if self.pipeline is None:

            self.pipeline = MarketPipeline()

        self.progress.setValue(

            25,

        )

        self.filter_bar.scan_status.setText(

            "Analyzing Market...",

        )

        recommendations = self.pipeline.run(

            filters,

        )

        elapsed = perf_counter() - scan_start

        self.filter_bar.scan_timer.setText(

            f"⏱ {elapsed:.2f} sec",

        )

        self.progress.setValue(

            80,

        )

        self.filter_bar.scan_status.setText(

            "Preparing Dashboard...",

        )

        self.dashboard.recommendation_table.load_data(

            recommendations,

            filters,

        )

        self.progress.setValue(

            100,

        )

        QTimer.singleShot(

            700,

            self.progress.hide,

        )

        message = (

            f"Scan Complete | "

            f"{len(recommendations)} Recommendations | "

            f"Universe: {filters['universe']}"

        )

        if hasattr(

            self.status,

            "show_message",

        ):

            self.status.show_message(

                message,

            )

        print(

            message,

        )

        self.filter_bar.scan_button.setText(

            "🔍 Scan (F5)",

        )

        self.filter_bar.scan_status.setText(

            "Ready",

        )

        if filters.get(

            "auto_refresh",

            False,

        ):

            interval = {

                "30 Sec": 30000,

                "1 Min": 60000,

                "2 Min": 120000,

                "5 Min": 300000,

                "10 Min": 600000,

            }.get(

                filters.get(

                    "refresh_interval",

                    "2 Min",

                ),

                120000,

            )

            self.refresh_timer.start(

                interval,

            )

        else:

            self.refresh_timer.stop()