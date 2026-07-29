"""
Stock Details Panel for VYOM.
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QFormLayout,
    QGroupBox,
    QLabel,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class StockDetails(QWidget):

    def __init__(self):

        super().__init__()

        self._build_ui()

    def _build_ui(self):

        self.symbol = QLabel("-")
        self.action = QLabel("-")
        self.category = QLabel("-")
        self.confidence = QLabel("-")

        self.open = QLabel("-")
        self.high = QLabel("-")
        self.low = QLabel("-")
        self.close = QLabel("-")

        self.previous_close = QLabel("-")
        self.change = QLabel("-")

        self.entry = QLabel("-")
        self.target = QLabel("-")
        self.stop_loss = QLabel("-")

        self.risk = QLabel("-")
        self.risk_reward = QLabel("-")
        self.atr = QLabel("-")

        self.sector = QLabel("-")
        self.industry = QLabel("-")

        self.volume = QLabel("-")

        self.form = QFormLayout()

        self.form.addRow("Symbol", self.symbol)
        self.form.addRow("Recommendation", self.action)
        self.form.addRow("Category", self.category)
        self.form.addRow("Confidence", self.confidence)

        self.form.addRow("Open", self.open)
        self.form.addRow("High", self.high)
        self.form.addRow("Low", self.low)
        self.form.addRow("Close", self.close)

        self.form.addRow("Previous Close", self.previous_close)
        self.form.addRow("Day Change", self.change)

        self.form.addRow("Entry", self.entry)
        self.form.addRow("Target", self.target)
        self.form.addRow("Stop Loss", self.stop_loss)

        self.form.addRow("Risk", self.risk)
        self.form.addRow("Risk Reward", self.risk_reward)
        self.form.addRow("ATR", self.atr)

        self.form.addRow("Sector", self.sector)
        self.form.addRow("Industry", self.industry)
        self.form.addRow("Volume", self.volume)

        group = QGroupBox("Trade Details")

        group.setLayout(self.form)

        self.reasons = QTextEdit()

        self.reasons.setReadOnly(True)

        self.summary = QTextEdit()

        self.summary.setReadOnly(True)

        layout = QVBoxLayout()

        layout.addWidget(group)

        layout.addWidget(QLabel("Jarvis Reasons"))

        layout.addWidget(self.reasons)

        layout.addWidget(QLabel("Jarvis Summary"))

        layout.addWidget(self.summary)

        self.setLayout(layout)

    def update_details(

        self,

        stock,

    ):

        self.symbol.setText(str(stock.get("symbol", "-")))
        self.action.setText(str(stock.get("recommendation", stock.get("action", "-"))))
        self.category.setText(str(stock.get("category", "-")))
        self.confidence.setText(f"{stock.get('confidence', 0)} %")

        self.open.setText(str(stock.get("open", "-")))
        self.high.setText(str(stock.get("high", "-")))
        self.low.setText(str(stock.get("low", "-")))
        self.close.setText(str(stock.get("close", "-")))

        self.previous_close.setText(str(stock.get("previous_close", "-")))

        self.change.setText(
            f"{stock.get('change', 0)} ({stock.get('change_percent',0):.2f}%)"
        )

        self.entry.setText(str(stock.get("entry", "-")))
        self.target.setText(str(stock.get("target1", stock.get("target", "-"))))
        self.stop_loss.setText(str(stock.get("stop_loss", "-")))

        self.risk.setText(str(stock.get("risk_level", stock.get("risk", "-"))))
        self.risk_reward.setText(str(stock.get("risk_reward", "-")))
        self.atr.setText(str(stock.get("atr", "-")))

        self.sector.setText(str(stock.get("sector", "-")))
        self.industry.setText(str(stock.get("industry", "-")))

        self.volume.setText(f"{stock.get('volume',0):,}")

        reasons = stock.get("reasons", [])

        if isinstance(reasons, list):

            self.reasons.setPlainText(

                "\n".join(

                    f"✓ {r}"

                    for r in reasons

                )

            )

        else:

            self.reasons.setPlainText(str(reasons))

        self.summary.setPlainText(

            stock.get(

                "ai_summary",

                "",

            )

        )