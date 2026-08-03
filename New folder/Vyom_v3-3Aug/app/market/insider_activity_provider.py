"""
Insider Activity Provider.

Fetches promoter and insider activity from
Yahoo Finance.
"""

from __future__ import annotations

from typing import Any

import yfinance as yf


class InsiderActivityProvider:

    def fetch(

        self,

        symbol: str,

    ) -> dict[str, Any]:

        result = {

            "promoter_buy": 0.0,

            "promoter_sell": 0.0,

            "insider_buy": 0.0,

            "insider_sell": 0.0,

        }

        try:

            ticker = yf.Ticker(

                symbol,

            )

            purchases = getattr(

                ticker,

                "insider_purchases",

                None,

            )

            transactions = getattr(

                ticker,

                "insider_transactions",

                None,

            )

        except Exception:

            return result

        try:

            if purchases is not None and not purchases.empty:

                for _, row in purchases.iterrows():

                    shares = float(

                        row.get(

                            "Shares",

                            0,

                        )

                    )

                    if shares > 0:

                        result["insider_buy"] += shares

                    elif shares < 0:

                        result["insider_sell"] += abs(

                            shares,

                        )

        except Exception:

            pass

        try:

            if transactions is not None and not transactions.empty:

                for _, row in transactions.iterrows():

                    shares = float(

                        row.get(

                            "Shares",

                            0,

                        )

                    )

                    relation = str(

                        row.get(

                            "Insider",

                            "",

                        )

                    ).lower()

                    if "promoter" in relation:

                        if shares > 0:

                            result["promoter_buy"] += shares

                        elif shares < 0:

                            result["promoter_sell"] += abs(

                                shares,

                            )

        except Exception:

            pass

        return result