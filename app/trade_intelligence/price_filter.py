"""
Price Filter Engine for VYOM.
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

        stocks: list,

        filter_name: str = "ALL",

    ) -> list:

        filter_name = filter_name.upper()

        maximum_price = self.FILTERS.get(

            filter_name,

            float("inf"),

        )

        filtered = []

        for stock in stocks:

            if isinstance(

                stock,

                dict,

            ):

                price = stock.get(

                    "price",

                    stock.get(

                        "last_price",

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

            if price <= maximum_price:

                filtered.append(

                    stock,

                )

        return filtered

    def available_filters(

        self,

    ) -> list[str]:

        return list(

            self.FILTERS.keys()

        )

    def statistics(

        self,

        original: list,

        filtered: list,

        filter_name: str,

    ) -> dict:

        return {

            "filter": filter_name,

            "total_scanned": len(original),

            "qualified": len(filtered),

            "removed": len(original) - len(filtered),

        }