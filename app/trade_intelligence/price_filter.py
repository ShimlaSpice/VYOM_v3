"""
Price Filter Engine for VYOM.
"""

from __future__ import annotations


class PriceFilter:

    def apply(

        self,

        stocks: list,

        filters: dict | None = None,

    ) -> list:

        if filters is None:

            return stocks

        min_price = self._minimum(filters)

        max_price = self._maximum(filters)

        qualified = []

        for stock in stocks:

            if isinstance(stock, dict):

                price = stock.get(

                    "price",

                    stock.get(

                        "entry",

                        0,

                    ),

                )

            else:

                price = getattr(

                    stock,

                    "entry",

                    0,

                )

            if price is None:

                continue

            if price < min_price:

                continue

            if max_price > 0 and price > max_price:

                continue

            qualified.append(

                stock,

            )

        return qualified

    def _minimum(

        self,

        filters: dict,

    ) -> float:

        try:

            value = filters.get(

                "min_price",

                "",

            )

            if value:

                return float(value)

        except Exception:

            pass

        band = filters.get(

            "price_band",

            "All",

        )

        mapping = {

            "Below ₹100": 0,

            "₹100 - ₹500": 100,

            "₹500 - ₹1,000": 500,

            "₹1,000 - ₹5,000": 1000,

            "Above ₹5,000": 5000,

            "All": 0,

        }

        return mapping.get(

            band,

            0,

        )

    def _maximum(

        self,

        filters: dict,

    ) -> float:

        try:

            value = filters.get(

                "max_price",

                "",

            )

            if value:

                return float(value)

        except Exception:

            pass

        band = filters.get(

            "price_band",

            "All",

        )

        mapping = {

            "Below ₹100": 100,

            "₹100 - ₹500": 500,

            "₹500 - ₹1,000": 1000,

            "₹1,000 - ₹5,000": 5000,

            "Above ₹5,000": 0,

            "All": 0,

        }

        return mapping.get(

            band,

            0,

        )

    def statistics(

        self,

        original: list,

        filtered: list,

        filters: dict,

    ) -> dict:

        return {

            "total_scanned": len(

                original,

            ),

            "qualified": len(

                filtered,

            ),

            "removed": len(

                original,

            ) - len(

                filtered,

            ),

            "filters": filters,

        }