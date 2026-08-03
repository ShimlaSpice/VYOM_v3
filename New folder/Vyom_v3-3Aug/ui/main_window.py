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

from PySide6.QtCore import (
    QObject,
    QThread,
    QTimer,
    Signal,
)

from app.pipeline.market_pipeline import MarketPipeline

from ui.dashboard import Dashboard
from ui.filter_bar import FilterBar
from ui.left_sidebar import LeftSidebar
from ui.status_bar import StatusBar
from ui.top_bar import TopBar
from app.ai.emotion_engine import EmotionEngine

class ScanWorker(QObject):

    finished = Signal(list)

    failed = Signal(str)

    def __init__(

        self,

        pipeline,

        filters,

    ):

        super().__init__()

        self.pipeline = pipeline

        self.filters = filters

    def run(self):
        import traceback

        try:

            recommendations = self.pipeline.run(

                self.filters,

            )

            self.finished.emit(

                recommendations,

            )

        except Exception:
            traceback.print_exc()

            self.failed.emit(
                traceback.format_exc(),
            )

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
        self.emotion_engine = EmotionEngine()

        self.scan_thread = None

        self.scan_worker = None

        self.scan_start = 0

        self.refresh_timer = QTimer()

        self._build_ui()

        self._connect_signals()

        self._create_shortcuts()

        self.refresh_timer.timeout.connect(

            self._auto_refresh,

        )
#        QTimer.singleShot(
#
#            100,
#
#            self._startup_scan,
#        ),
    def _startup_scan(

        self,

    ):

        self.status.show_message(

            "Initializing market data...",

        )

        self._scan_requested(

            self._collect_filters(),

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

        if self.pipeline is None:

            self.pipeline = MarketPipeline()

        # --------------------------------------------------
        # Thread already running?
        # --------------------------------------------------

        try:

            if (

                self.scan_thread is not None

                and self.scan_thread.isRunning()

            ):

                return

        except RuntimeError:

            self.scan_thread = None

            self.scan_worker = None

        self.scan_start = perf_counter()

        self.filter_bar.scan_button.setEnabled(False)

        self.filter_bar.scan_button.setText(

            "🔄 Scanning..."

        )

        self.filter_bar.scan_status.setText(

            "Scanning..."

        )

        self.filter_bar.scan_timer.setText(

            "⏱ 0.00 sec"

        )

        self.progress.show()

        self.progress.setValue(5)

        self.status.show_message(

            "Loading market universe...",

        )

        self.scan_thread = QThread()

        self.scan_worker = ScanWorker(

            self.pipeline,

            filters,

        )

        self.scan_worker.moveToThread(

            self.scan_thread,

        )

        self.scan_thread.started.connect(

            self.scan_worker.run,

        )

        self.scan_worker.finished.connect(

            lambda recommendations:

            self._scan_finished(

                recommendations,

                filters,

            )

        )

        self.scan_worker.failed.connect(

            self._scan_failed,

        )

        self.scan_worker.finished.connect(

            self.scan_thread.quit,

        )

        self.scan_worker.finished.connect(

            self.scan_worker.deleteLater,

        )

        self.scan_thread.finished.connect(

            self.scan_thread.deleteLater,

        )

        self.scan_thread.finished.connect(

            lambda: setattr(

                self,

                "scan_thread",

                None,

            )

        )

        self.scan_thread.finished.connect(

            lambda: setattr(

                self,

                "scan_worker",

                None,

            )

        )

        self.progress.setValue(15)

        self.status.show_message(

            "Downloading market data...",

        )

        self.scan_thread.start()


    def _scan_finished(

        self,

        recommendations,

        filters,

    ):
        self.progress.setValue(
            85,
        )

        self.status.show_message(
            "Preparing recommendations...",
        )

        elapsed = perf_counter() - self.scan_start
        market_change = 0.0

        if recommendations:

            market_change = sum(

                getattr(

                    item,

                    "change_percent",

                    0.0,

                )

                for item in recommendations

            ) / len(

                recommendations,

            )

        emotion = self.emotion_engine.evaluate(

            market_change=market_change,

            vix=15,

            breadth=0.62,

            momentum=6.5,

            news_sentiment=0.60,

        )

        self.top_bar.update_emotion(

            emotion["emotion"],

            emotion["label"],

        )
        self.dashboard.update_emotion(

            emotion,

        )

        self.top_bar.update_status(

            "Market Scanned",

        )

        self.top_bar.update_market(

            filters.get(

                "market",

                "NSE",

            ),

        )

        self.top_bar.update_scan_time(

            elapsed,

        )        
        self.dashboard.recommendation_table.load_data(

            recommendations,

            filters,

        )

        self.progress.setValue(
            100,
        )

        self.filter_bar.scan_timer.setText(

            f"⏱ {elapsed:.2f} sec"

        )

        self.filter_bar.scan_status.setText(

            emotion["label"]

        )

        self.filter_bar.scan_button.setEnabled(True)

        self.filter_bar.scan_button.setText(

            "🔍 Scan (F5)"

        )
        self.status.show_message(

            f"Scan completed in {elapsed:.2f} sec",
        )

        QTimer.singleShot(

            500,

            self.progress.hide

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

            QTimer.singleShot(

                0,

                lambda: self.refresh_timer.start(

                    interval,

                ),

            )

        else:

            QTimer.singleShot(

                0,

                self.refresh_timer.stop,

            )


    def closeEvent(self, event):

        if self.scan_thread is not None:

            try:

                if self.scan_thread.isRunning():

                    self.scan_thread.quit()

                    self.scan_thread.wait()

            except RuntimeError:

                pass

        event.accept()

    def _scan_failed(

        self,

        error,

    ):

        self.progress.hide()

        self.filter_bar.scan_button.setEnabled(

            True,

        )

        self.filter_bar.scan_button.setText(

            "🔍 Scan (F5)",

        )

        self.filter_bar.scan_status.setText(

            "Failed",

        )

        self.status.show_message(

            "Scan failed",

        )

        print(

            error,
        )
