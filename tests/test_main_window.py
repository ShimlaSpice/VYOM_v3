import os
from unittest.mock import patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow, ScanWorker
from ui.recommendation_table import RecommendationTable


def test_main_window_starts_scan_on_startup():
    app = QApplication.instance() or QApplication([])

    with patch("ui.main_window.QTimer.singleShot") as single_shot:
        window = MainWindow()
        window.show()

    assert single_shot.called
    args, kwargs = single_shot.call_args
    assert args[0] == 0
    assert args[1] == window._startup_scan

    app.quit()


def test_recommendation_table_loads_dict_payloads():
    app = QApplication.instance() or QApplication([])

    table = RecommendationTable()
    table.load_data(
        [
            {
                "symbol": "TEST",
                "recommendation": "BUY",
                "confidence": 85,
                "probability": 70,
                "entry": 10.0,
                "stop_loss": 9.0,
                "target1": 12.0,
                "target2": 13.0,
                "risk_level": "MEDIUM",
                "reasons": ["test"],
            }
        ],
        {},
    )

    assert table.rowCount() == 1
    assert table.item(0, 1).text() == "TEST"

    app.quit()


def test_scan_result_handler_routes_payload_to_ui():
    app = QApplication.instance() or QApplication([])

    window = MainWindow()

    with patch.object(window, "_scan_finished") as scan_finished:
        window._handle_scan_result(([{"symbol": "TEST"}], {"top": 1}))
        app.processEvents()

    scan_finished.assert_called_once_with([{"symbol": "TEST"}], {"top": 1})

    app.quit()
