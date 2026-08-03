"""
FII / DII Data Provider.

Fetches daily institutional activity.
"""

from __future__ import annotations

from typing import Any

import pandas as pd


class FIIDIIProvider:

    URL = (

        "https://archives.nseindia.com/"

        "content/fii_stats_1.xls"

    )

    def fetch(

        self,

    ) -> dict[str, Any]:

        try:

            table = pd.read_excel(

                self.URL,

            )

        except Exception:

            return {

                "fii_net": 0.0,

                "dii_net": 0.0,

            }

        fii_net = 0.0

        dii_net = 0.0

        try:

            for _, row in table.iterrows():

                text = str(

                    row.iloc[0]

                ).upper()

                if "FII" in text:

                    buy = float(

                        row.iloc[1]

                    )

                    sell = float(

                        row.iloc[2]

                    )

                    fii_net = round(

                        buy - sell,

                        2,

                    )

                elif "DII" in text:

                    buy = float(

                        row.iloc[1]

                    )

                    sell = float(

                        row.iloc[2]

                    )

                    dii_net = round(

                        buy - sell,

                        2,

                    )

        except Exception:

            pass

        return {

            "fii_net": fii_net,

            "dii_net": dii_net,

        }