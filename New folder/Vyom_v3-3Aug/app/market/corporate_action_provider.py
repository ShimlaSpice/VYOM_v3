"""
Corporate Action Provider.

Fetches corporate actions from Yahoo Finance.
"""

from __future__ import annotations

from typing import Any

import yfinance as yf


class CorporateActionProvider:

    def fetch(

        self,

        symbol: str,

    ) -> dict[str, Any]:

        try:

            ticker = yf.Ticker(

                symbol,

            )

            actions = ticker.actions

        except Exception:

            actions = None

        result = {

            "bonus": False,

            "split": False,

            "dividend": False,

            "buyback": False,

            "rights_issue": False,

            "merger": False,

        }

        if actions is None:

            return result

        try:

            if len(actions) == 0:

                return result

            latest = actions.tail(10)

            if "Stock Splits" in latest.columns:

                result["split"] = (

                    latest["Stock Splits"] > 0

                ).any()

            if "Dividends" in latest.columns:

                result["dividend"] = (

                    latest["Dividends"] > 0

                ).any()

        except Exception:

            pass

        return result