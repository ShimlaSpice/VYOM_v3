# VYOM Desktop UI v1.0

## Vision

The UI exists for one purpose:

**Help a trader make a confident decision within 30 seconds.**

The user should never have to search through hundreds of stocks.

Jarvis does the research.

The trader makes the decision.

---

# Design Principles

- Minimal clicks
- Maximum clarity
- No unnecessary charts
- No information overload
- Explain every recommendation
- Desktop first
- Dark theme by default

---

# Home Screen

The dashboard will display only the **Top 10 recommendations**.

No long watchlists.

No hundreds of rows.

Jarvis filters the market.

The trader reviews only the best opportunities.

---

# Dashboard Layout

Header

- Market Status
- Scan Time
- Current Time
- Jarvis Status

Filter Bar

- Market (NSE / BSE)
- Category
    - Today
    - Swing
    - Long Term
    - F&O
    - Penny
- Price Filter
- Capital Filter
- Sort By
- Top Results
- Scan Button

Recommendation Table

Columns

- Rank
- Symbol
- Price
- Score
- Confidence
- Action
- Entry
- Target
- Stop Loss

Status Bar

- Stocks Scanned
- Stocks Filtered
- Results Displayed
- Data Source
- Jarvis Status

---

# Price Filters

Quick Filters

- All
- Below ₹100
- ₹100–₹500
- ₹500–₹1,000
- ₹1,000–₹5,000
- Above ₹5,000
- Custom

Custom

Minimum Price

Maximum Price

---

# Capital Filter

Quick Options

- ₹10,000
- ₹25,000
- ₹50,000
- ₹1,00,000
- ₹5,00,000
- Custom

Jarvis should calculate

- Quantity
- Capital Required
- Expected Profit
- Maximum Risk

---

# Advanced Filters

- Breakout
- High Volume
- High Confidence
- Low Risk
- Strong Fundamentals
- Intraday
- Swing
- Long Term
- Penny Stocks
- F&O
- Dividend

---

# Stock Details

When a user clicks a stock, show:

Recommendation

Confidence

Probability

Entry

Target 1

Target 2

Stop Loss

Risk

Holding Period

Risk Reward Ratio

Reasons

Risks

Jarvis Summary

Nothing else.

---

# Charts

Charts are NOT shown on the Home Screen.

Charts appear only after selecting a stock.

---

# Performance Goal

Dashboard Load

< 2 seconds

Market Scan

< 5 seconds

Recommendation Generation

< 5 seconds

Total Wait Time

< 10 seconds

---

# UI Rules

Never show more than 10 recommendations by default.

Every recommendation must contain

- Entry
- Stop Loss
- Target
- Confidence
- Explanation

No scrolling through hundreds of stocks.

No technical jargon without explanation.

Every click should reveal more information, never more confusion.

---

# Future Versions

Version 1

- Dashboard
- Scanner
- Recommendations
- Stock Details

Version 2

- Portfolio
- Trade Journal
- Alerts
- Broker Integration

Version 3

- Backtesting
- Strategy Builder
- AI Chat
- Voice Assistant
- Mobile Companion

---

# Definition of Success

A trader should be able to

1. Open VYOM

2. Click Scan

3. See the Top 10 opportunities

4. Open one stock

5. Understand WHY Jarvis recommends it

6. Place the trade

All within 30 seconds.

┌────────────────────────────────────────────────────────────────────────────┐
│                               TOP BAR                                     │
├────────────────────────────────────────────────────────────────────────────┤
│                            FILTER BAR                                     │
├──────────────┬───────────────────────────────────────────────┬────────────┤
│              │                                               │            │
│              │                                               │            │
│              │                                               │            │
│              │                                               │            │
│  SIDEBAR     │        TOP 10 RECOMMENDATIONS                 │  DETAILS   │
│              │                                               │            │
│              │                                               │            │
│              │                                               │            │
│              │                                               │            │
├──────────────┴───────────────────────────────────────────────┴────────────┤
│                            STATUS BAR                                     │
└────────────────────────────────────────────────────────────────────────────┘



Left Sidebar

Today
Intraday
Swing
Long Term
F&O
Penny
Settings
Exit



Filter Bar
Market = [NSE ▼]
Category = [Today ▼]
Price Band = [₹100-₹500 ▼]
Min Price = [____]
Max Price = [____]
Capital = [₹50,000 ▼]
Sort = [Score ▼]
Top = [10 ▼]
[SCAN]

Recommendation Table
Rank	Symbol	Price	Score	Confidence	Action	Entry	Target	SL

Only 10 rows.
Double-click → Stock Details.


Stock Details Panel
RELIANCE
BUY
Confidence
92%
Entry
₹2850
Target
₹2945
SL
₹2815
Qty
17
Capital
₹48,450
Potential Profit
₹1,615
Maximum Loss
₹595
Reason
✓ Breakout
✓ Strong Trend
✓ High Volume
✓ Good Fundamentals
✓ Positive News
Jarvis Summary
4–5 lines.

Status Bar
Market = Bullish
Stocks = 500
Filtered = 67
Displayed = 10
Scan = 3.4 sec
Jarvis READY

Theme
Dark Theme
Green = BUY
Red = SELL
Orange = WATCH
Yellow = CAUTION
Blue = Information

🚫 Not in V1
Portfolio
Login
Charts on dashboard
Broker integration
Paper trading
Strategy Builder
AI Chat

Those come later.