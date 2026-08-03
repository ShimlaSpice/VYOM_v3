"""
Stock Details Panel for VYOM.
Matches reference: Trade Details, VYOM Analysis, VYOM Summary
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QSizePolicy,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtGui import QColor, QFont


def _lbl(text="", bold=False, color=None) -> QLabel:
    l = QLabel(text)
    if bold:
        f = l.font()
        f.setBold(True)
        l.setFont(f)
    if color:
        l.setStyleSheet(f"color: {color};")
    l.setWordWrap(True)
    return l


class StockDetails(QWidget):

    def __init__(self):
        super().__init__()
        self._build_ui()

    def _build_ui(self):
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        content = QWidget()
        self._content_layout = QVBoxLayout(content)
        self._content_layout.setContentsMargins(6, 6, 6, 6)
        self._content_layout.setSpacing(8)

        scroll.setWidget(content)
        outer_layout.addWidget(scroll)

        # ===== TRADE DETAILS GROUP =====
        trade_group = QGroupBox("Trade Details")
        trade_layout = QGridLayout(trade_group)
        trade_layout.setSpacing(4)
        trade_layout.setContentsMargins(8, 8, 8, 8)

        self.lbl_symbol = _lbl("-")
        self.lbl_company = _lbl("-")
        self.lbl_sector = _lbl("-")
        self.lbl_industry = _lbl("-")
        self.lbl_cmp = _lbl("-")
        self.lbl_open = _lbl("-")
        self.lbl_high = _lbl("-")
        self.lbl_low = _lbl("-")
        self.lbl_prev_close = _lbl("-")
        self.lbl_volume = _lbl("-")
        self.lbl_vwap = _lbl("-")
        self.lbl_atr = _lbl("-")
        self.lbl_rsi = _lbl("-")
        self.lbl_macd = _lbl("-")
        self.lbl_ema20 = _lbl("-")
        self.lbl_ema50 = _lbl("-")
        self.lbl_sma20 = _lbl("-")
        self.lbl_sma50 = _lbl("-")
        self.lbl_52w_high = _lbl("-")
        self.lbl_52w_low = _lbl("-")
        self.lbl_entry = _lbl("-", color="#28a745")
        self.lbl_target = _lbl("-", color="#28a745")
        self.lbl_stop_loss = _lbl("-", color="#dc3545")
        self.lbl_risk_reward = _lbl("-")
        self.lbl_confidence = _lbl("-")
        self.lbl_probability = _lbl("-")
        self.lbl_recommendation = _lbl("-", bold=True)

        left_fields = [
            ("Symbol", self.lbl_symbol),
            ("Company", self.lbl_company),
            ("Sector", self.lbl_sector),
            ("Industry", self.lbl_industry),
            ("CMP", self.lbl_cmp),
            ("Open", self.lbl_open),
            ("High", self.lbl_high),
            ("Low", self.lbl_low),
            ("Prev Close", self.lbl_prev_close),
            ("Volume", self.lbl_volume),
            ("VWAP", self.lbl_vwap),
            ("ATR (14)", self.lbl_atr),
        ]

        right_fields = [
            ("52W High", self.lbl_52w_high),
            ("52W Low", self.lbl_52w_low),
            ("RSI (14)", self.lbl_rsi),
            ("MACD", self.lbl_macd),
            ("EMA 20", self.lbl_ema20),
            ("EMA 50", self.lbl_ema50),
            ("SMA 20", self.lbl_sma20),
            ("SMA 50", self.lbl_sma50),
            ("Entry", self.lbl_entry),
            ("Target", self.lbl_target),
            ("Stop Loss", self.lbl_stop_loss),
            ("Risk Reward", self.lbl_risk_reward),
        ]

        for r, (key, val) in enumerate(left_fields):
            k = _lbl(key, bold=False)
            k.setStyleSheet("color: #666;")
            trade_layout.addWidget(k, r, 0)
            trade_layout.addWidget(val, r, 1)

        for r, (key, val) in enumerate(right_fields):
            k = _lbl(key, bold=False)
            k.setStyleSheet("color: #666;")
            trade_layout.addWidget(k, r, 2)
            trade_layout.addWidget(val, r, 3)

        # Bottom rows spanning all columns
        row_base = max(len(left_fields), len(right_fields))
        for col_i, (key, val) in enumerate([
            ("Confidence", self.lbl_confidence),
            ("Probability", self.lbl_probability),
            ("Recommendation", self.lbl_recommendation),
        ]):
            k = _lbl(key)
            k.setStyleSheet("color: #666;")
            trade_layout.addWidget(k, row_base + col_i, 0)
            trade_layout.addWidget(val, row_base + col_i, 1, 1, 3)

        self._content_layout.addWidget(trade_group)

        # ===== VYOM ANALYSIS GROUP =====
        analysis_group = QGroupBox("VYOM Analysis")
        analysis_layout = QGridLayout(analysis_group)
        analysis_layout.setSpacing(4)
        analysis_layout.setContentsMargins(8, 8, 8, 8)

        self.lbl_trend = _lbl("-")
        self.lbl_momentum = _lbl("-")
        self.lbl_breakout = _lbl("-")
        self.lbl_vol_signal = _lbl("-")
        self.lbl_sector_strength = _lbl("-")
        self.lbl_market_strength = _lbl("-")
        self.lbl_news_sentiment = _lbl("-")
        self.lbl_ai_insight = _lbl("-")
        self.lbl_risk_bias = _lbl("-")
        self.lbl_bias = _lbl("-")
        self.lbl_verdict = _lbl("-")

        left_analysis = [
            ("Trend", self.lbl_trend),
            ("Momentum", self.lbl_momentum),
            ("Breakout", self.lbl_breakout),
            ("Volume", self.lbl_vol_signal),
            ("Sector Strength", self.lbl_sector_strength),
            ("Market Strength", self.lbl_market_strength),
            ("News Sentiment", self.lbl_news_sentiment),
        ]

        right_analysis = [
            ("AI Insight", self.lbl_ai_insight),
            ("Risk", self.lbl_risk_bias),
            ("Bias", self.lbl_bias),
            ("Overall", self.lbl_verdict),
        ]

        for r, (key, val) in enumerate(left_analysis):
            k = _lbl(key)
            k.setStyleSheet("color: #666;")
            analysis_layout.addWidget(k, r, 0)
            analysis_layout.addWidget(val, r, 1)

        for r, (key, val) in enumerate(right_analysis):
            k = _lbl(key)
            k.setStyleSheet("color: #666;")
            analysis_layout.addWidget(k, r, 2)
            analysis_layout.addWidget(val, r, 3)

        self._content_layout.addWidget(analysis_group)

        # ===== VYOM SUMMARY GROUP =====
        summary_group = QGroupBox("VYOM Summary")
        summary_layout = QVBoxLayout(summary_group)
        summary_layout.setContentsMargins(8, 8, 8, 8)
        summary_layout.setSpacing(6)

        # Action badge + AI summary
        top_row = QHBoxLayout()
        self.lbl_action_badge = _lbl("BUY", bold=True)
        self.lbl_action_badge.setFixedSize(60, 28)
        self.lbl_action_badge.setAlignment(Qt.AlignCenter)
        self.lbl_action_badge.setStyleSheet(
            "background: #d4edda; color: #155724; border-radius: 4px; font-weight: bold;"
        )
        top_row.addWidget(self.lbl_action_badge)

        self.lbl_ai_summary = QLabel("-")
        self.lbl_ai_summary.setWordWrap(True)
        self.lbl_ai_summary.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        top_row.addWidget(self.lbl_ai_summary, 1)
        summary_layout.addLayout(top_row)

        # Trade metrics row
        metrics_widget = QWidget()
        metrics_layout = QGridLayout(metrics_widget)
        metrics_layout.setSpacing(4)
        self.lbl_sum_entry = _lbl("-", color="#28a745")
        self.lbl_sum_target = _lbl("-", color="#28a745")
        self.lbl_sum_sl = _lbl("-", color="#dc3545")
        self.lbl_sum_risk = _lbl("-", color="#dc3545")
        self.lbl_sum_reward = _lbl("-", color="#28a745")
        self.lbl_sum_rr = _lbl("-")
        self.lbl_sum_hold = _lbl("-")

        for col, (key, val) in enumerate([
            ("Entry", self.lbl_sum_entry),
            ("Target", self.lbl_sum_target),
            ("Stop Loss", self.lbl_sum_sl),
            ("Risk", self.lbl_sum_risk),
            ("Reward", self.lbl_sum_reward),
            ("RR Ratio", self.lbl_sum_rr),
            ("Hold Period", self.lbl_sum_hold),
        ]):
            k = _lbl(key)
            k.setStyleSheet("color: #666; font-size: 10px;")
            metrics_layout.addWidget(k, 0, col)
            metrics_layout.addWidget(val, 1, col)

        summary_layout.addWidget(metrics_widget)

        self._content_layout.addWidget(summary_group)
        self._content_layout.addStretch()

    def update_details(self, stock: dict):
        if not stock:
            return

        def gf(key, default=0.0):
            v = stock.get(key, default)
            try:
                return float(v) if v not in (None, "", "-") else default
            except (ValueError, TypeError):
                return default

        def gs(key, default="-"):
            v = stock.get(key, default)
            return str(v) if v not in (None, "", 0) else default

        symbol = gs("symbol")
        company = symbol.replace(".NS", "").replace(".BO", "")
        rec = gs("recommendation", "HOLD")
        confidence = int(gf("confidence"))
        probability = int(gf("probability"))

        # Trade details
        self.lbl_symbol.setText(symbol)
        self.lbl_company.setText(company)
        self.lbl_sector.setText(gs("sector"))
        self.lbl_industry.setText(gs("industry"))
        self.lbl_cmp.setText(f"Rs{gf('close', gf('price')):,.2f}")
        self.lbl_open.setText(f"Rs{gf('open'):,.2f}")
        self.lbl_high.setText(f"Rs{gf('high'):,.2f}")
        self.lbl_low.setText(f"Rs{gf('low'):,.2f}")
        self.lbl_prev_close.setText(f"Rs{gf('previous_close'):,.2f}")
        vol = int(gf("volume"))
        if vol >= 10_000_000:
            vol_str = f"{vol / 10_000_000:.2f} Cr"
        elif vol >= 100_000:
            vol_str = f"{vol / 100_000:.2f} L"
        else:
            vol_str = f"{vol:,}"
        self.lbl_volume.setText(vol_str)
        self.lbl_vwap.setText(f"Rs{gf('vwap'):,.2f}" if stock.get("vwap") else "-")
        self.lbl_atr.setText(f"Rs{gf('atr'):,.2f}")

        scores = stock.get("scores", {}) or {}
        self.lbl_rsi.setText(f"{scores.get('rsi', gf('rsi', 0)):.1f}" if scores.get("rsi") or stock.get("rsi") else "-")
        self.lbl_macd.setText(f"{gf('macd'):.2f}" if stock.get("macd") else "-")
        self.lbl_ema20.setText(f"Rs{gf('ema_20'):,.2f}" if stock.get("ema_20") else "-")
        self.lbl_ema50.setText(f"Rs{gf('ema_50'):,.2f}" if stock.get("ema_50") else "-")
        self.lbl_sma20.setText(f"Rs{gf('sma_20'):,.2f}" if stock.get("sma_20") else "-")
        self.lbl_sma50.setText(f"Rs{gf('sma_50'):,.2f}" if stock.get("sma_50") else "-")
        self.lbl_52w_high.setText(f"Rs{gf('week_52_high'):,.2f}" if stock.get("week_52_high") else "-")
        self.lbl_52w_low.setText(f"Rs{gf('week_52_low'):,.2f}" if stock.get("week_52_low") else "-")
        self.lbl_entry.setText(f"Rs{gf('entry'):,.2f}")
        self.lbl_target.setText(f"Rs{gf('target1', gf('target')):,.2f}")
        self.lbl_stop_loss.setText(f"Rs{gf('stop_loss'):,.2f}")
        rr = gf("risk_reward")
        self.lbl_risk_reward.setText(f"1 : {rr:.2f}" if rr else "-")
        self.lbl_confidence.setText(f"{confidence}%")
        self.lbl_probability.setText(f"{probability}%")
        self.lbl_recommendation.setText(rec)

        # Recommendation color
        rec_colors = {
            "BUY": "#28a745", "STRONG BUY": "#155724",
            "SELL": "#dc3545", "HOLD": "#856404", "WATCH": "#fd7e14",
        }
        self.lbl_recommendation.setStyleSheet(
            f"color: {rec_colors.get(rec.upper(), '#333')}; font-weight: bold;"
        )

        # VYOM Analysis from scores
        def score_label(val, thresholds=("Weak", "Moderate", "Strong")):
            if val is None:
                return "-"
            try:
                v = float(val)
                if v >= 70:
                    return thresholds[2]
                elif v >= 40:
                    return thresholds[1]
                else:
                    return thresholds[0]
            except:
                return str(val)

        reasons = stock.get("reasons", []) or []
        trend_txt = next((r for r in reasons if "trend" in r.lower()), "")
        self.lbl_trend.setText(score_label(scores.get("trend_score"), ("Bearish", "Neutral", "Bullish")))
        self.lbl_momentum.setText(score_label(scores.get("momentum_score"), ("Weak", "Moderate", "Strong")))
        self.lbl_breakout.setText(score_label(scores.get("breakout_score"), ("Unconfirmed", "Emerging", "Confirmed")))
        self.lbl_vol_signal.setText(score_label(scores.get("volume_score"), ("Low", "Moderate", "High")))
        self.lbl_sector_strength.setText(score_label(scores.get("sector_score"), ("Weak", "Moderate", "Strong")))
        self.lbl_market_strength.setText(score_label(scores.get("market_score"), ("Weak", "Moderate", "Strong")))
        sentiment = stock.get("news_sentiment", stock.get("sentiment", ""))
        self.lbl_news_sentiment.setText(str(sentiment) if sentiment else "-")

        ai_summary = stock.get("ai_summary", "")
        insight_short = (ai_summary[:120] + "...") if len(ai_summary) > 120 else ai_summary
        self.lbl_ai_insight.setText(insight_short or "-")
        risk_level = stock.get("risk_level", "-")
        self.lbl_risk_bias.setText(str(risk_level))
        change_pct = gf("change_percent")
        self.lbl_bias.setText("Bullish" if change_pct >= 0 else "Bearish")
        self.lbl_verdict.setText("Positive Setup" if rec in ("BUY", "STRONG BUY") else "Neutral" if rec == "HOLD" else "Negative")

        # VYOM Summary
        rec_colors2 = {
            "BUY": ("#155724", "#d4edda"),
            "STRONG BUY": ("#0d3c14", "#c3e6cb"),
            "SELL": ("#721c24", "#f8d7da"),
            "HOLD": ("#856404", "#fff3cd"),
        }
        fg, bg = rec_colors2.get(rec.upper(), ("#333", "#eee"))
        self.lbl_action_badge.setText(rec)
        self.lbl_action_badge.setStyleSheet(
            f"background: {bg}; color: {fg}; border-radius: 4px; font-weight: bold;"
        )
        self.lbl_ai_summary.setText(ai_summary or "-")
        self.lbl_sum_entry.setText(f"Rs{gf('entry'):,.2f}")
        self.lbl_sum_target.setText(f"Rs{gf('target1', gf('target')):,.2f}")
        self.lbl_sum_sl.setText(f"Rs{gf('stop_loss'):,.2f}")
        entry_v = gf("entry")
        target_v = gf("target1", gf("target"))
        sl_v = gf("stop_loss")
        risk_val = entry_v - sl_v if entry_v and sl_v else 0
        reward_val = target_v - entry_v if target_v and entry_v else 0
        self.lbl_sum_risk.setText(f"Rs{risk_val:,.2f}")
        self.lbl_sum_reward.setText(f"Rs{reward_val:,.2f}")
        self.lbl_sum_rr.setText(f"1 : {rr:.2f}" if rr else "-")
        category = stock.get("category", "")
        hold_map = {"Intraday": "Intraday", "Swing": "2 - 5 Days", "Positional": "2 - 4 Weeks", "Long Term": "3+ Months"}
        self.lbl_sum_hold.setText(hold_map.get(category, "2 - 5 Days"))
