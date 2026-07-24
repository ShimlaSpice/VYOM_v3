"""
Price Filter Engine for VYOM.

Filters stocks based on current market price.
"""

from __future__ import annotations


class PriceFilter:

    FILTERS = {
        "UNDER_100": 100,
        "UNDER_500": 500,
        "UNDER_1000": 1000,
        "UNDER_5000": 5000,
        "ALL": float("inf"),
    }

    def apply(
        self,
        stocks: list[dict],
        filter_name: str = "ALL",
    ) -> list[dict]:
        """
        Filter stocks by price.

        Each stock dictionary must contain:

        {
            "symbol": "...",
            "price": 123.45
        }
        """

        filter_name = filter_name.upper()

        if filter_name not in self.FILTERS:
            filter_name = "ALL"

        maximum_price = self.FILTERS[filter_name]

        filtered = []

        for stock in stocks:

            price = stock.get("price", 0)

            if price <= maximum_price:
                filtered.append(stock)

        return filtered

    def available_filters(self) -> list[str]:
        """
        Returns supported filters.
        """

        return list(self.FILTERS.keys())

    def statistics(
        self,
        original: list[dict],
        filtered: list[dict],
        filter_name: str,
    ) -> dict:

        return {

            "filter": filter_name,

            "total_scanned": len(original),

            "qualified": len(filtered),

            "removed": len(original) - len(filtered),
        }