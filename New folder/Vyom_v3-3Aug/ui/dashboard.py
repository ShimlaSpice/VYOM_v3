"""
Dashboard widget for VYOM.
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QGroupBox,
    QProgressBar,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from ui.recommendation_table import RecommendationTable
from ui.stock_details import StockDetails


class Dashboard(QWidget):

    def __init__(self):

        super().__init__()

        self._build_ui()

    def _build_ui(self):

        self.recommendation_table = RecommendationTable()

        self.details = StockDetails()

        self.emotion_group = QGroupBox(

            "Market Emotion"

        )

        emotion_layout = QVBoxLayout()

        self.emotion_label = QLabel(

            "NEUTRAL"

        )

        self.emotion_score = QLabel(

            "50 / 100"

        )

        self.emotion_bar = QProgressBar()

        self.emotion_bar.setRange(

            0,

            100,

        )

        self.emotion_bar.setValue(

            50,

        )

        self.fear = QLabel(

            "Fear : 50"

        )

        self.greed = QLabel(

            "Greed : 50"

        )

        self.fomo = QLabel(

            "FOMO : 50"

        )

        self.panic = QLabel(

            "Panic : 50"

        )

        self.breadth = QLabel(

            "Breadth : --"

        )

        self.momentum = QLabel(

            "Momentum : --"

        )

        self.discipline = QLabel(

            "Discipline : --"

        )

        emotion_layout.addWidget(

            self.emotion_label,

        )

        emotion_layout.addWidget(

            self.emotion_score,

        )

        emotion_layout.addWidget(

            self.emotion_bar,

        )

        emotion_layout.addWidget(

            self.fear,

        )

        emotion_layout.addWidget(

            self.greed,

        )

        emotion_layout.addWidget(

            self.fomo,

        )

        emotion_layout.addWidget(

            self.panic,

        )

        emotion_layout.addWidget(

            self.breadth,

        )

        emotion_layout.addWidget(

            self.momentum,

        )

        emotion_layout.addWidget(

            self.discipline,

        )

        self.emotion_group.setLayout(

            emotion_layout,

        )

        right_panel = QWidget()

        right_layout = QVBoxLayout()

        right_layout.setContentsMargins(

            0,

            0,

            0,

            0,

        )

        right_layout.setSpacing(

            6,

        )

        right_layout.addWidget(

            self.emotion_group,

        )

        right_layout.addWidget(

            self.details,

            1,

        )

        right_panel.setLayout(

            right_layout,

        )

        self.splitter = QSplitter(

            Qt.Horizontal,

        )

        self.splitter.setChildrenCollapsible(

            False,

        )

        self.splitter.addWidget(

            self.recommendation_table,

        )

        self.splitter.addWidget(

            right_panel,

        )

        self.splitter.setStretchFactor(

            0,

            5,

        )

        self.splitter.setStretchFactor(

            1,

            3,

        )

        self.splitter.setSizes(

            [

                1080,

                520,

            ]

        )

        layout = QVBoxLayout()

        layout.setContentsMargins(

            2,

            2,

            2,

            2,

        )

        layout.setSpacing(

            2,

        )

        layout.addWidget(

            self.splitter,

        )

        self.setLayout(

            layout,

        )

        self.recommendation_table.stock_selected.connect(

            self.details.update_details,

        )

    def update_emotion(

        self,

        emotion: dict,

    ):

        self.emotion_label.setText(

            emotion["label"]

        )

        self.emotion_score.setText(

            f'{emotion["emotion"]} / 100'

        )

        self.emotion_bar.setValue(

            emotion["emotion"]

        )

        self.fear.setText(

            f'Fear : {emotion["fear"]}'

        )

        self.greed.setText(

            f'Greed : {emotion["greed"]}'

        )

        self.fomo.setText(

            f'FOMO : {emotion["fomo"]}'

        )

        self.panic.setText(

            f'Panic : {emotion["panic"]}'

        )

        self.breadth.setText(

            f'Breadth : {emotion["breadth"]}'

        )

        self.momentum.setText(

            f'Momentum : {emotion["momentum"]}'

        )

        self.discipline.setText(

            f'Discipline : {emotion["discipline"]}'

        )