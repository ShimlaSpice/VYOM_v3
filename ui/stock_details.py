"""
Stock Details Panel for VYOM.
Full-width horizontal layout: Trade Details | VYOM Analysis | VYOM Summary
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
    QSplitter,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtGui import QFont

from ui.company_names import get_company_name


def _key(text: str) -> QLabel:
    lbl = QLabel(text)
    lbl.setStyleSheet("color: #9e9e9e; font-size: 9pt;")
    lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
    return lbl


def _val(text: str = "-", color: str | None = None, bold: bool = False) -> QLabel:
    lbl = QLabel(text)
    lbl.setWordWrap(True)
    style = "font-size: 10pt;"
    if color:
        style += f" color: {color};"
    if bold:
        style += " font-weight: bold;"
    lbl.setStyleSheet(style)
    return lbl


def _group(title: str) -> tuple[QGroupBox, QGridLayout]:
    g = QGroupBox(title)
    lay = QGridLayout(g)
    lay.setSpacing(5)
    lay.setContentsMargins(10, 12, 10, 10)
    return g, lay


class StockDetails(QWidget):

    def __init__(self):
        super().__init__()
        self._build_ui()

    # ------------------------------------------------------------------
    def _build_ui(self):
        outer = QHBoxLayout(self)
        outer.setContentsMargins(4, 4, 4, 4)
        outer.setSpacing(6)

        # ── PANEL 1: Trade Details ──────────────────────────────────────
        trade_group, tg = _group("Trade Details")

        self.v_symbol    = _val(bold=True)
        self.v_company   = _val()
        self.v_sector    = _val()
        self.v_industry  = _val()
        self.v_cmp       = _val(bold=True)
        self.v_open      = _val()
        self.v_high      = _val()
        self.v_low       = _val()
        self.v_prev      = _val()
        self.v_vol       = _val()
        self.v_vwap      = _val()
        self.v_atr       = _val()
        self.v_52h       = _val()
        self.v_52l       = _val()
        self.v_rsi       = _val()
        self.v_macd      = _val()
        self.v_ema20     = _val()
        self.v_ema50     = _val()
        self.v_sma20     = _val()
        self.v_sma50     = _val()
        self.v_entry     = _val(color="#4caf50", bold=True)
        self.v_target    = _val(color="#4caf50", bold=True)
        self.v_sl        = _val(color="#f44336", bold=True)
        self.v_rr        = _val()
        self.v_conf      = _val()
        self.v_prob      = _val()
        self.v_rec       = _val(bold=True)

        # 3 key-value pairs per row
        rows = [
            [("Symbol",    self.v_symbol),   ("Company",  self.v_company),   ("Sector",    self.v_sector)],
            [("Industry",  self.v_industry), ("CMP",      self.v_cmp),       ("52W High",  self.v_52h)],
            [("52W Low",   self.v_52l),      ("Open",     self.v_open),      ("High",      self.v_high)],
            [("Low",       self.v_low),      ("Prev Close",self.v_prev),     ("Volume",    self.v_vol)],
            [("VWAP",      self.v_vwap),     ("ATR (14)", self.v_atr),       ("RSI (14)",  self.v_rsi)],
            [("MACD",      self.v_macd),     ("EMA 20",   self.v_ema20),     ("EMA 50",    self.v_ema50)],
            [("SMA 20",    self.v_sma20),    ("SMA 50",   self.v_sma50),     ("Entry",     self.v_entry)],
            [("Target",    self.v_target),   ("Stop Loss",self.v_sl),        ("Risk Reward",self.v_rr)],
            [("Confidence",self.v_conf),     ("Probability",self.v_prob),    ("Recommendation",self.v_rec)],
        ]
        for r, triplet in enumerate(rows):
            for c, (key, val) in enumerate(triplet):
                tg.addWidget(_key(key), r, c * 2)
                tg.addWidget(val,       r, c * 2 + 1)
        for col in range(6):
            tg.setColumnStretch(col, 1 if col % 2 == 1 else 0)

        # ── PANEL 2: VYOM Analysis ──────────────────────────────────────
        analysis_group, ag = _group("VYOM Analysis")

        self.v_trend     = _val()
        self.v_momentum  = _val()
        self.v_breakout  = _val()
        self.v_vol_sig   = _val()
        self.v_sector_s  = _val()
        self.v_market_s  = _val()
        self.v_news      = _val()
        self.v_risk_bias = _val()
        self.v_bias      = _val()
        self.v_verdict   = _val(bold=True)
        self.v_insight   = _val()
        self.v_insight.setWordWrap(True)
        self.v_insight.setStyleSheet("font-size: 9pt; color: #b0b0b0;")

        technical_fields = [
            ("Trend",           self.v_trend),
            ("Momentum",        self.v_momentum),
            ("Breakout",        self.v_breakout),
            ("Volume Signal",   self.v_vol_sig),
        ]
        market_fields = [
            ("Sector Strength", self.v_sector_s),
            ("Market Strength", self.v_market_s),
            ("News Sentiment",  self.v_news),
        ]
        risk_fields = [
            ("Risk Level",      self.v_risk_bias),
            ("Bias",            self.v_bias),
            ("Overall Verdict", self.v_verdict),
        ]

        # Section headers + field rows
        def _section_hdr(text: str) -> QLabel:
            lbl = QLabel(text.upper())
            lbl.setStyleSheet("color: #607d8b; font-size: 8pt; font-weight: bold; padding-top: 6px;")
            return lbl

        ag_row = 0
        for section_title, fields in [
            ("Technical", technical_fields),
            ("Market",    market_fields),
            ("Risk",      risk_fields),
        ]:
            ag.addWidget(_section_hdr(section_title), ag_row, 0, 1, 4)
            ag_row += 1
            for key, val in fields:
                ag.addWidget(_key(key), ag_row, 0)
                ag.addWidget(val,       ag_row, 1)
                ag_row += 1

        # AI Insight spans full width at bottom
        ag.addWidget(_section_hdr("AI Insight"), ag_row, 0, 1, 4)
        ag_row += 1
        ag.addWidget(self.v_insight, ag_row, 0, 1, 4)
        ag.setColumnStretch(1, 1)
        ag.setColumnStretch(3, 1)
        ag.setRowStretch(ag_row + 1, 1)

        # ── PANEL 3: VYOM Summary ───────────────────────────────────────
        summary_group, sg = _group("VYOM Summary")

        # Top: badge + recommendation + confidence
        self.v_badge  = QLabel("BUY")
        self.v_badge.setAlignment(Qt.AlignCenter)
        self.v_badge.setFixedSize(80, 36)
        self.v_badge.setStyleSheet(
            "background: #198754; color: #fff; border-radius: 6px; font-weight: bold; font-size: 14pt;"
        )

        self.v_rec_lbl = _val("BUY", bold=True)
        self.v_rec_lbl.setStyleSheet("font-size: 16pt; font-weight: bold; color: #4caf50;")
        self.v_conf_lbl = _val()
        self.v_conf_lbl.setStyleSheet("font-size: 11pt; color: #b0b0b0;")

        badge_row = QHBoxLayout()
        badge_row.addWidget(self.v_badge)
        badge_col = QVBoxLayout()
        badge_col.setSpacing(2)
        badge_col.addWidget(self.v_rec_lbl)
        badge_col.addWidget(self.v_conf_lbl)
        badge_row.addLayout(badge_col)
        badge_row.addStretch()
        sg.addLayout(badge_row, 0, 0, 1, 4)

        # Divider
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("color: #333;")
        sg.addWidget(line, 1, 0, 1, 4)

        # Trade metrics: two columns of key-value
        self.v_sum_entry  = _val(color="#4caf50", bold=True)
        self.v_sum_target = _val(color="#4caf50", bold=True)
        self.v_sum_sl     = _val(color="#f44336", bold=True)
        self.v_sum_risk   = _val(color="#f44336")
        self.v_sum_reward = _val(color="#4caf50")
        self.v_sum_rr     = _val(bold=True)
        self.v_sum_hold   = _val()

        metric_pairs = [
            ("Entry",       self.v_sum_entry,  "Target",      self.v_sum_target),
            ("Stop Loss",   self.v_sum_sl,     "Risk Reward", self.v_sum_rr),
            ("Risk",        self.v_sum_risk,   "Reward",      self.v_sum_reward),
            ("Hold Period", self.v_sum_hold,   "",            None),
        ]
        for i, (k1, v1, k2, v2) in enumerate(metric_pairs):
            sg.addWidget(_key(k1), i + 2, 0)
            sg.addWidget(v1,       i + 2, 1)
            if k2 and v2 is not None:
                sg.addWidget(_key(k2), i + 2, 2)
                sg.addWidget(v2,       i + 2, 3)

        # Divider
        line2 = QFrame()
        line2.setFrameShape(QFrame.HLine)
        line2.setStyleSheet("color: #333;")
        sg.addWidget(line2, 6, 0, 1, 4)

        # AI Summary text
        sg.addWidget(_key("AI Summary"), 7, 0, Qt.AlignTop)
        self.v_ai_summary = QLabel("-")
        self.v_ai_summary.setWordWrap(True)
        self.v_ai_summary.setStyleSheet("font-size: 9pt; color: #ccc; line-height: 1.4;")
        self.v_ai_summary.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sg.addWidget(self.v_ai_summary, 7, 1, 1, 3)
        sg.setColumnStretch(1, 1)
        sg.setColumnStretch(3, 1)
        sg.setRowStretch(8, 1)

        # ── Assemble panels in horizontal splitter ──────────────────────
        self.h_splitter = QSplitter(Qt.Horizontal)
        self.h_splitter.setChildrenCollapsible(False)
        for widget in [trade_group, analysis_group, summary_group]:
            wrapper = QScrollArea()
            wrapper.setWidgetResizable(True)
            wrapper.setFrameShape(QFrame.NoFrame)
            wrapper.setWidget(widget)
            self.h_splitter.addWidget(wrapper)
        self.h_splitter.setStretchFactor(0, 35)
        self.h_splitter.setStretchFactor(1, 35)
        self.h_splitter.setStretchFactor(2, 30)

        outer.addWidget(self.h_splitter)

    # ------------------------------------------------------------------
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

        symbol  = gs("symbol")
        company = get_company_name(symbol)
        rec     = gs("recommendation", "HOLD")
        conf    = int(gf("confidence"))
        prob    = int(gf("probability"))

        # ── Trade Details ───────────────────────────────────────────────
        self.v_symbol.setText(symbol)
        self.v_company.setText(company)
        self.v_sector.setText(gs("sector"))
        self.v_industry.setText(gs("industry"))
        self.v_cmp.setText(f"Rs {gf('close', gf('price')):,.2f}")
        self.v_open.setText(f"Rs {gf('open'):,.2f}")
        self.v_high.setText(f"Rs {gf('high'):,.2f}")
        self.v_low.setText(f"Rs {gf('low'):,.2f}")
        self.v_prev.setText(f"Rs {gf('previous_close'):,.2f}")

        vol = int(gf("volume"))
        if vol >= 10_000_000:
            vs = f"{vol/10_000_000:.2f} Cr"
        elif vol >= 100_000:
            vs = f"{vol/100_000:.2f} L"
        else:
            vs = f"{vol:,}"
        self.v_vol.setText(vs)

        self.v_vwap.setText(f"Rs {gf('vwap'):,.2f}" if stock.get("vwap") else "-")
        self.v_atr.setText(f"Rs {gf('atr'):,.2f}")

        sc = stock.get("scores", {}) or {}
        self.v_rsi.setText(f"{sc.get('rsi', gf('rsi', 0)):.1f}" if sc.get("rsi") or stock.get("rsi") else "-")
        self.v_macd.setText(f"{gf('macd'):.2f}" if stock.get("macd") else "-")
        self.v_ema20.setText(f"Rs {gf('ema_20'):,.2f}" if stock.get("ema_20") else "-")
        self.v_ema50.setText(f"Rs {gf('ema_50'):,.2f}" if stock.get("ema_50") else "-")
        self.v_sma20.setText(f"Rs {gf('sma_20'):,.2f}" if stock.get("sma_20") else "-")
        self.v_sma50.setText(f"Rs {gf('sma_50'):,.2f}" if stock.get("sma_50") else "-")
        self.v_52h.setText(f"Rs {gf('week_52_high'):,.2f}" if stock.get("week_52_high") else "-")
        self.v_52l.setText(f"Rs {gf('week_52_low'):,.2f}" if stock.get("week_52_low") else "-")

        entry_v  = gf("entry")
        target_v = gf("target1", gf("target"))
        sl_v     = gf("stop_loss")
        rr       = gf("risk_reward")

        self.v_entry.setText(f"Rs {entry_v:,.2f}")
        self.v_target.setText(f"Rs {target_v:,.2f}")
        self.v_sl.setText(f"Rs {sl_v:,.2f}")
        self.v_rr.setText(f"1 : {rr:.2f}" if rr else "-")
        self.v_conf.setText(f"{conf}%")
        self.v_prob.setText(f"{prob}%")
        self.v_rec.setText(rec)
        rec_color = {"BUY": "#4caf50", "STRONG BUY": "#66bb6a", "SELL": "#f44336", "HOLD": "#ffc107"}.get(rec.upper(), "#e0e0e0")
        self.v_rec.setStyleSheet(f"font-weight: bold; color: {rec_color}; font-size: 10pt;")

        # ── VYOM Analysis ───────────────────────────────────────────────
        def slbl(val, lo="Weak", med="Moderate", hi="Strong"):
            try:
                v = float(val)
                return hi if v >= 70 else med if v >= 40 else lo
            except (TypeError, ValueError):
                return str(val) if val else "-"

        self.v_trend.setText(slbl(sc.get("trend_score"),    "Bearish", "Neutral", "Bullish"))
        self.v_momentum.setText(slbl(sc.get("momentum_score")))
        self.v_breakout.setText(slbl(sc.get("breakout_score"), "Unconfirmed", "Emerging", "Confirmed"))
        self.v_vol_sig.setText(slbl(sc.get("volume_score"),  "Low",    "Moderate", "High"))
        self.v_sector_s.setText(slbl(sc.get("sector_score")))
        self.v_market_s.setText(slbl(sc.get("market_score"), "Weak", "Moderate", "Strong"))
        self.v_news.setText(gs("news_sentiment", gs("sentiment")))

        risk_level = gs("risk_level")
        self.v_risk_bias.setText(risk_level)
        change_pct = gf("change_percent")
        self.v_bias.setText("Bullish" if change_pct >= 0 else "Bearish")
        verdict = "Positive Setup" if rec in ("BUY", "STRONG BUY") else "Neutral" if rec == "HOLD" else "Negative"
        self.v_verdict.setText(verdict)
        verdict_color = "#4caf50" if "Positive" in verdict else "#f44336" if "Negative" in verdict else "#ffc107"
        self.v_verdict.setStyleSheet(f"font-weight: bold; color: {verdict_color}; font-size: 10pt;")

        ai_txt = gs("ai_summary", "")
        self.v_insight.setText((ai_txt[:180] + "...") if len(ai_txt) > 180 else ai_txt or "-")

        # ── VYOM Summary ────────────────────────────────────────────────
        badge_colors = {
            "BUY":        ("#fff", "#198754"),
            "STRONG BUY": ("#fff", "#0d6efd"),
            "HOLD":       ("#212529", "#ffc107"),
            "SELL":       ("#fff", "#dc3545"),
        }
        fg, bg = badge_colors.get(rec.upper(), ("#fff", "#6c757d"))
        self.v_badge.setText(rec)
        self.v_badge.setStyleSheet(
            f"background: {bg}; color: {fg}; border-radius: 6px; font-weight: bold; font-size: 13pt;"
        )
        self.v_rec_lbl.setText(rec)
        self.v_rec_lbl.setStyleSheet(f"font-size: 15pt; font-weight: bold; color: {bg};")
        self.v_conf_lbl.setText(f"Confidence: {conf}%   |   Probability: {prob}%")

        self.v_sum_entry.setText(f"Rs {entry_v:,.2f}")
        self.v_sum_target.setText(f"Rs {target_v:,.2f}")
        self.v_sum_sl.setText(f"Rs {sl_v:,.2f}")
        risk_val   = entry_v - sl_v  if entry_v and sl_v    else 0
        reward_val = target_v - entry_v if target_v and entry_v else 0
        self.v_sum_risk.setText(f"Rs {risk_val:,.2f}")
        self.v_sum_reward.setText(f"Rs {reward_val:,.2f}")
        self.v_sum_rr.setText(f"1 : {rr:.2f}" if rr else "-")
        category = stock.get("category", "")
        hold_map = {"Intraday": "Intraday", "Swing": "2-5 Days", "Positional": "2-4 Weeks", "Long Term": "3+ Months"}
        self.v_sum_hold.setText(hold_map.get(category, "2-5 Days"))
        self.v_ai_summary.setText(ai_txt or "-")
